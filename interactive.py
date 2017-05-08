from constructive_hierarchy import *
from hieretikz import all_separations

def print_proof_path(path, proofs):
    for x, y in path:
        if x != y:
            print('\t{} => {}{:>20}'.format(x, y, proofs[(x, y)]))

def examine(a, b, proofs, separations):
    connection = is_connected(a, b, proofs)
    if connection:
        print('{} => {}'.format(a, b))
        print('Proof:')
        print_proof_path(connection, proofs)
        return
    separation = is_separated(a, b, set(proofs), set(separations))
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
    print("A separation requires a model satisfying one of")
    print(set(upward_closure(a, set(proofs))))
    print("but which is a counter-model for one of")
    print(set(downward_closure(b, set(proofs))))



def repl(proofs, separations):
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
            examine(*cmdlist, proofs, separations)
        print()

from drinkertest import proofs, models
separations = all_separations(models)
repl(proofs, separations)
