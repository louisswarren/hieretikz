#!/usr/bin/env python3

from hierarchy import *

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
    connection = is_superior(frozenset({*tails}), head, frozenset(proofs))
    if connection:
        print('{} => {}'.format(', '.join(tails), head))
        print('Proof:')
        print_proof_tree(connection[0], proofs)
        return
    separation = is_separated(frozenset({*tails}), head, models)
    if separation:
        print('{} =/=> {}'.format(', '.join(tails), head))
        sepname, presep, postsep = separation
        print('Since {} holds in {}'.format(', '.join(tails), sepname))
        for tree in presep:
            if tree:
                print_proof_tree(tree, proofs)
        print('but {} fails'.format(head))
        if postsep:
            print_proof_tree(postsep, proofs)
        return
    print("Currently unknown.")
    possible_models = {name for name, low, high in models
                       if head in high
                       if not any(t in high for t in tails)}
    possible_counter_models = {name for name, low, high in models
                               if all(t in low for t in tails)
                               if head not in low}
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
            print()
            break
        except KeyboardInterrupt:
            print()
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
    from drinker import formulae, proofs, models
    repl(proofs, completed_separations(models, formulae, frozenset(proofs.keys())))
