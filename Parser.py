
import string

from automaton.Functions import direct_afd_algorithm, afd_simulation
from automaton.configuration import replace_reserved_words


class Parser:
    def __init__(self):
        self.results = {}
    
    
    [('name', 'Expr'), ('attribute', ''), '=', '{', ('ident', 'Stat'), ('token', '6'), '}', ('token', '7')]
    
    [('name', 'Stat'), ('attribute', ''), '=', ('semAction', 'value = 0'), ('ident', 'Expression'), ('attribute', 'value'), ('semAction', 'print(value)')]
    
    [('name', 'Expression'), ('attribute', 'result: int'), '=', ('semAction', 'result1, result2 = 0'), ('ident', 'Term'), ('attribute', 'result1'), '{', ('token', '8'), ('ident', 'Term'), ('attribute', 'result2'), ('semAction', 'result1 += result2'), '|', ('token', '9'), ('ident', 'Term'), ('attribute', 'result2'), ('semAction', 'result1 -= result2'), '}', ('semAction', 'result = result1')]
    
    [('name', 'Term'), ('attribute', 'result: int'), '=', ('semAction', 'result1, result2 = 0'), ('ident', 'Factor'), ('attribute', 'result1'), '{', ('token', '10'), ('ident', 'Factor'), ('attribute', 'result2'), ('semAction', 'result1 *= result2'), '|', ('token', '11'), ('ident', 'Factor'), ('attribute', 'result2'), ('semAction', 'result1 /= result2'), '}', ('semAction', 'result = result1')]
    
    [('name', 'Factor'), ('attribute', 'result: int'), '=', ('semAction', 'signo = 1'), '[', ('token', '12'), ('semAction', 'signo = -1'), ']', '(', ('ident', 'Number'), ('attribute', 'result'), '|', ('token', '13'), ('ident', 'Expression'), ('attribute', 'result'), ('token', '14'), ')', ('semAction', 'result *= signo')]
    
    [('name', 'Number'), ('attribute', 'result: int'), '=', ('token', 'number'), ('semAction', 'result = int(lastToken.value)')]
    
    
    def Expr():
		while True:
			
		

	def Stat():
		(value)

	def Expression(result: int):
		(result1)while True:
			(result2)(result2)
		

	def Term(result: int):
		(result1)while True:
			(result2)(result2)
		

	def Factor(result: int):
		(result)(result)

	def Number(result: int):
		

	

    def move(self):
        # Se avanzan los caracteres ignore
        while (self.ignore_afd and
               self.index < len(self.file_information) and
               afd_simulation(self.ignore_afd, replace_reserved_words(
                   self.file_information[self.index]))[0]):
            self.index += 1

        finish = True
        final_index = self.index
        result = None

        # Se simula mientras:
        # - no se encuentre un simbolo que no esta en las transiciones
        # - no se exceda al tamaño del archivo
        while finish and final_index <= len(self.file_information):
            final_index += 1
            (new_result, finish) = afd_simulation(
                self.afd,
                replace_reserved_words(
                    self.file_information[self.index:final_index])
            )
            if new_result:
                result = (new_result, final_index)

        if (final_index > self.index and result):
            initial_index = self.index
            final_index = result[1]
            self.index = result[1]
            if(self.afd.finals_ids[result[0]] < len(self.tokens)):
                self.results[(initial_index, final_index)] = (
                    self.tokens[self.afd.finals_ids[result[0]]],
                    self.file_information[initial_index:final_index]
                )
        else:
            if self.index < len(self.file_information):
                print('Error léxico el caracter {} en la posición: {}'.format(
                    repr(self.file_information[self.index]), self.index))
                self.index += 1

parser = Parser()
parser.parse("inputs/archivo.txt")