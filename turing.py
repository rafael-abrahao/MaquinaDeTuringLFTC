import re

class EndState:
    def __init__(self, result: bool, final_state: str) -> None:
        self.__result = result
        self.state = final_state.replace(' ', '◊')

    def __bool__(self) -> bool:
        return self.__result

class TuringMachine:
    def __init__(self) -> None:
        self.__rules = {}
        self.__tape = []
        self.__tape_length = 0
        self.__current_state = 'q1'
        self.__current_position = 0

    def read_rules_from_file(self, file_name: str) -> None:
        with open(file_name, 'r') as file:
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

    def load_tape(self, chain: str):
        self.__chain = chain + ' '
        self.__tape = list(chain + ' ')
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
            if(pos < self.__current_position):
                space += 2
            print(letter.replace(' ', '◊'), end=' ')
        if(self.__tape_length == 0):
            print('◊', end =' ')
        print('...')
        print(' ' * space, '↑', sep='')
        print(' ' * space, self.__current_state, sep='', end='\n\n')

    def run_machine(self, verbose = True) -> EndState:
        if(len(self.__rules) == 0):
            print("Aviso: nenhuma regra encontrada")
        if(verbose):
            self.__print()
        while(self.__go_to_next_state()):
            # if(self.__current_position >= 99):
            #     print("Limite prático da fita alcançado (100 caratécres)")
            #     return False
            if(verbose):
                self.__print()
            if(self.__current_state == 'qf'):
                return EndState(True, self.__current_state + self.__tape[self.__current_position])

        return EndState(False, self.__current_state + self.__tape[self.__current_position])

        
    def reset(self):
        self.__current_state = 'q1'
        self.__current_position = 0
        self.__tape.clear()
        self.load_tape(self.__chain)

    def print_rules(self):
        if len(self.__rules) == 0:
            print('<vazio>')
        else:
            for key in self.__rules.keys():
                rule = self.__rules[key]
                print(key.replace(' ', '◊'), rule[0], rule[1], rule[2], sep='')

def __get_command(tm: TuringMachine) -> bool:
    cmd = input(">> ").strip()
    if(re.match('read ', cmd)):
        tm.read_rules_from_file(cmd[5:])
    elif(re.match('test\s?', cmd)):
        print()
        tm.load_tape(cmd[5:])
        result = tm.run_machine()
        tm.reset()
        if(result):
            print("Cadeia \"", cmd[5:], "\" reconhecida.", sep='', end='\n\n')
        else:
            print("Cadeia \"", cmd[5:], "\" não reconhecida.", sep='')
            print("Não existe regra para \"", result.state, "\".", sep='', end='\n\n')
    elif(re.match('^(print)$', cmd)):
        print()
        tm.print_rules()
        print()
    elif(re.match('^(quit)$', cmd)):
        return False
    else:
        print("Comando não reconhecido")
    
    return True

def main():
    tm = TuringMachine()
    while __get_command(tm):
        pass

if __name__ == '__main__':
    main()
