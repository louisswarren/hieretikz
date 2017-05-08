from constructive_hierarchy import *

def print_proof_path(path, proofs):
    for x, y in path:
        if x != y:
            print('\t{} => {}{:>20}'.format(x, y, proofs[(x, y)]))

def examine(a, b, proofs, counter_models):
    connection = is_connected(a, b, proofs)
    if connection:
        print('{} => {}'.format(a, b))
        print('Proof:')
        print_proof_path(connection, proofs)
        return
    separation = is_separated(a, b, set(proofs), set(counter_models))
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
            start, end, counter_models[(start, end)]))
        return
    print("Currently unknown.")
    print("A separation requires a model satisfying one of")
    print(set(upward_closure(a, set(proofs))))
    print("but which is a counter-model for one of")
    print(set(downward_closure(b, set(proofs))))



def repl(proofs, counter_models):
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
        if len(cmdlist) != 2:
            print('Invalid input.')
        else:
            examine(*cmdlist, proofs, counter_models)
        print()

from drinkertest import proofs, counter_models
repl(proofs, counter_models)
