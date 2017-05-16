#!/usr/bin/env python3

from constructive_hierarchy import *
from hieretikz import all_separations

def print_proof_path(path, proofs):
    for x, y in path:
        if x != y:
            print('\t{} => {}{:>20}'.format(x, y, proofs[(x, y)]))

def examine(a, b, proofs, models):
    separations = all_separations(models)
    connection = is_connected(a, b, frozenset(proofs))
    if connection:
        print('{} => {}'.format(a, b))
        print('Proof:')
        print_proof_path(connection, proofs)
        return
    separation = is_separated(a, b, frozenset(proofs), frozenset(separations))
    if separation:
        presep, postsep = separation
        start = presep[0][0]
        end = postsep[-1][1]
        print('{} =/=> {}'.format(a, b))
        print('Since {} => {}'.format(start, a))
        print_proof_path(presep, proofs)
        print('and {} => {}'.format(b, end))
        print_proof_path(postsep, proofs)
        print('and there is a counter-model showing')
        print('\t{} =/=> {}{:>20}'.format(
            start, end, separations[(start, end)]))
        return
    print("Currently unknown.")
    possible_models = {k for k in models
                       if b in models[k][1] and a not in models[k][1]}
    possible_counter_models = {k for k in models
                               if a in models[k][0] and b not in models[k][0]}
    if possible_models or possible_counter_models:
        print("A separation would exist if it were shown that")
        if possible_models:
            print("{} holds in {}".format(a, ', or '.join(possible_models)))
        if possible_models and possible_counter_models:
            print("or")
        if possible_counter_models:
            print("{} fails in {}".format(b, ', or '.join(
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
        if len(cmdlist) != 2:
            print('Invalid input.')
        else:
            examine(*cmdlist, proofs, models)
        print()

from drinker import proofs, models
repl(proofs, models)
