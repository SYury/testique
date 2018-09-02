import argparse
import sys
import os
from subprocess import call, TimeoutExpired

ending = {}
ending['cpp'] = 'cpp'
ending['c'] = 'c'
ending['py3'] = 'py'


def compile_sol(tp):
    if tp == 'cpp':
        os.system('g++ -O2 -std=c++11 tmp.cpp -o tmp')
    if tp == 'c':
        os.system('gcc -O2 -std=c11 tmp.c -o tmp')


def run_sol(tp, checker, test, tl, chf):
    if chf == sys.stdout:
        chf.write('\033[0mon test ' + test + '\n')
    else:
        chf.write('on test ' + test + '\n')
    if chf == sys.stdout:
        check_line = './' + checker + ' ' + test + ' output.txt ' + test[:-3] + '.out'
    else:
        check_line = './' + checker + ' ' + test + ' output.txt ' + test[:-3] + '.out' + ' tmp_checker_out'
    if tp == 'cpp' or tp == 'c':
        excode = 0
        try:
            os.system('ulimit -s unlimited')
            excode = call(['./tmp'], stdin=open(test, 'r'), stdout=open('output.txt', 'w'), timeout=tl)
        except TimeoutExpired:
            if chf == sys.stdout:
                chf.write('\033[0;31mTL\033[0m\n')
            else:
                chf.write('TL\n')
        else:
            if excode != 0:
                chf.write('Runtime Error\n')
            else:
                os.system(check_line)
                if chf != sys.stdout:
                    with open('tmp_checker_out', 'r') as co:
                        for line in co:
                            chf.write(line+'\n')
    if tp == 'py3':
        try:
            call(['python3 tmp.py'], shell=True, stdin=open(test, 'r'), stdout=open('output.txt', 'w'), timeout=tl)
        except TimeoutExpired:
            if chf == sys.stdout:
                chf.write('\033[0;31mTL\033[0m\n')
            else:
                chf.write('TL\n')
        else:
            os.system(check_line)
            if chf != sys.stdout:
                with open('tmp_checker_out', 'r') as co:
                    for line in co:
                        chf.write(line+'\n')


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--show', type=str, nargs=1,
                        help="show statement")
    parser.add_argument('--submit', type=str, nargs=2,
                        help="submit solution")
    parser.add_argument('--file', type=str, nargs=1,
                        help="file")
    parser.add_argument('--list', action='store_true',
                        help="list all problems")
    parser.add_argument('--out', type=str, nargs=1,
                        help="specify output file")
    args = parser.parse_args()
    return args


args = get_arguments()

if args.submit and args.show:
    print('ERROR: submit and show must not be selected at once')
    exit(0)

if args.show:
    title = 'pr/' + args.show[0] + '/statement'
    with open(title, 'r') as st:
        for line in st:
            print(line)
    exit(0)

if args.list:
    for name in os.listdir('pr'):
        if os.path.isdir(os.path.join('pr', name)):
            print(name)
    exit(0)

chf = sys.stdout
if args.out:
    chf = open(args.out[0], 'w')

if args.submit:
    title = 'pr/' + args.submit[1]
    tmp = open('tmp.' + ending[args.submit[0]], 'w')
    infl = sys.stdin
    if args.file:
        infl = open(args.file[0], 'r')
    for line in infl:
        tmp.write(line)
    tmp.close()
    compile_sol(args.submit[0])
    tl = 0.0
    with open(title + '/time', 'r') as fl:
        tl = float(fl.read())
    for file in os.listdir(title + '/tests'):
        filename = os.fsdecode(file)
        if filename.endswith('.in'):
            run_sol(args.submit[0], os.path.join(title, 'check'), os.path.join(title + '/tests', filename), tl, chf)
