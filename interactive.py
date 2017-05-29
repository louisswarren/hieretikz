#!/usr/bin/env python3

from hierarchy import *
from hieretikz import all_separations

def print_proof_path(path, proofs):
    for x, y in path:
        if x != y:
            print('\t{} => {}{:>20}'.format(x, y, proofs[(x, y)]))

def print_proof_tree(path, proofs, level=0):
    edge, *successors = path
    *tails, head = edge
    print(('    '*level + '{} => {}{:>40}').format(
                       ', '.join(tails), head, 'by ' + str(proofs[edge])))
    for s in successors:
        print_proof_tree(s, proofs, level + 1)

def examine(tails, head, proofs, models):
    print("Examining")
    connection = is_superior({*tails}, {head}, frozenset(proofs))
    if connection:
        print('{} => {}'.format(', '.join(tails), head))
        print('Proof:')
        print_proof_tree(connection[0], proofs)
        return
    separation = is_separated({*tails}, {head}, frozenset(proofs), models)
    if separation:
        print('{} =/=> {}'.format(', '.join(tails), head))
        sepname, presep, postsep = separation
        print('Since {} holds in {}'.format(', '.join(tails), sepname))
        for tree in presep:
            if tree:
                print_proof_tree(tree, proofs)
        print('but {} fails'.format(head))
        for tree in postsep:
            if tree:
                print_proof_tree(tree, proofs)
        return
    print("Currently unknown.")
    possible_models = {v for k, v in models.items()
                       if head in k[1]
                       if not any(t in k[1] for t in tails)}
    possible_counter_models = {v for k, v in models.items()
                               if all(t in k[0] for t in tails)
                               if head not in k[0]}
    if possible_models or possible_counter_models:
        print("A separation would exist if it were shown that")
        if possible_models:
            print("{} holds in {}".format(', '.join(tails), ', or '.join(possible_models)))
        if possible_models and possible_counter_models:
            print("or")
        if possible_counter_models:
            print("{} fails in {}".format(head, ', or '.join(
                possible_counter_models)))


def repl(proofs, models):
    while True:
        try:
            cmd = input('? ')
        except EOFError:
            break
        if not cmd:
            break
        if ',' in cmd:
            cmdlist = list(map(str.strip, cmd.split(',')))
        elif ' ' in cmd:
            cmdlist = cmd.split()
        *tails, head = cmdlist
        examine(tails, head, proofs, models)
        print()

if __name__ == '__main__':
    from drinker import proofs, models
    repl(proofs, models)
