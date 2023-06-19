import random

def generate_chains(alphabet: set, min_size:int, max_size: int, number:int) -> list:
    chain_list = []
    rd = random.Random()
    
    for x in range(number):
        chain = ''
        size = rd.randint(min_size, max_size)
        while(len(chain) < size):
            chain += alphabet[rd.randint(0, len(alphabet) - 1)]
        chain_list.append(chain)

    return chain_list

def generate_chains_sequence(alphabet: set, max_size: int, number:int) -> list:
    chain_list = []
    rd = random.Random()
    
    for x in range(number):
        chain = ''
        size = rd.randint(len(alphabet), max_size)
        sizes = [1] * len(alphabet)
        max_i = size
        for i in range(len(alphabet)):
            size_i = rd.randint(1, (max_i - (len(alphabet) - i - 1)))
            sizes[i] = size_i
            max_i = size - size_i
        for i in range(len(alphabet)):
            chain_i = ''
            while(len(chain_i) < sizes[i]):
                chain_i += alphabet[i]
            chain += chain_i
        chain_list.append(chain)

    return chain_list