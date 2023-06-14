import re

class TuringMachine:
    def __init__(self) -> None:
        self.__rules = {}
        self.__tape = []
        self.__tape_length = 0
        self.__current_state = 'q1'
        self.__current_position = 0

    def read_rules_from_file(self, file_name: str) -> None:
        file = open(file_name)
        self.__rules.clear()
        pattern = re.compile('^(q([0-9]+|f)([A-Za-z]|\s)q([0-9]+|f)[A-Za-z](R|L))$')
        for line in file:
            line = line.replace('\n', '')
            if(pattern.match(line)):
                rules = list(filter(None, line.split('q')))
                next_state = rules[1]
                step = ['q'+next_state[:-2], next_state[-2], next_state[-1]] 
                self.__rules['q'+rules[0]] = step
            else:
                print('Regra', line, 'não reconhecida', sep=' ')
                self.__rules.clear()
                break

        file.close()

    def load_tape(self, chain: str):
        self.__tape = list(chain)
        self.__tape_length = len(chain)

    def __go_to_next_state(self) -> bool:
        current = self.__current_state + self.__tape[self.__current_position]
        if not current in self.__rules:
            return False
        next = self.__rules[current]
        self.__current_state = next[0]
        self.__tape[self.__current_position] = next[1]
        if(next[2] == 'R'):
            self.__current_position += 1
        elif(next[2] == 'L'):
            self.__current_position -= 1
        if(self.__current_position == self.__tape_length):
            self.__tape.append(' ')
            self.__tape_length += 1
        return True

    def __print(self):
        space = 0
        for pos in range(self.__tape_length):
            letter = self.__tape[pos]
            if letter == ' ':
                letter = '◊'
            if(pos < self.__current_position):
                space += 2
            print(letter, end=' ')
        print('...')
        print(' ' * space, '↑', sep='')
        print(' ' * space, self.__current_state, sep='', end='\n\n')

    def run_machine(self) -> bool:
        if(len(self.__rules) == 0):
            print("Aviso: nenhuma regra encontrada")
        self.__print()
        while(self.__go_to_next_state()):
            # if(self.__current_position >= 99):
            #     print("Limite prático da fita alcançado (100 caratécres)")
            #     return False
            self.__print()
        if(self.__current_state == 'qf'):
            return True
        else:
            return False

    def print_rules(self):
        for key in self.__rules.keys():
            rule = self.__rules[key]
            print(key, rule[0], rule[1], rule[2], sep='')




tm = TuringMachine()
tm.read_rules_from_file("turing.txt")
tm.load_tape('aaabbb')
result = tm.run_machine()
if(result):
    print("Cadeia Reconhecida")
else:
    print("Cadeia Não Reconhecida")
