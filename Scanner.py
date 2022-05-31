
import string

from automaton.Functions import direct_afd_algorithm, afd_simulation
from automaton.configuration import replace_reserved_words


class Scanner:
    def __init__(self):
        self.file_information = ''
        self.index = 0

        self.lexical_analyzer_name = 'Double'

        self.r = '((0|1|2|3|4|5|6|7|8|9){(0|1|2|3|4|5|6|7|8|9)})#|((0|1|2|3|4|5|6|7|8|9){(0|1|2|3|4|5|6|7|8|9)}.(0|1|2|3|4|5|6|7|8|9){(0|1|2|3|4|5|6|7|8|9)})#|((\n|\r|\t){(\n|\r|\t)})#|(;)#|(.)#|(+)#|(-)#|(*)#|(/)#|(-)#|(β)#|(δ)#'

        self.tokens = [('number', '(0|1|2|3|4|5|6|7|8|9){(0|1|2|3|4|5|6|7|8|9)}'), ('decnumber', '(0|1|2|3|4|5|6|7|8|9){(0|1|2|3|4|5|6|7|8|9)}.(0|1|2|3|4|5|6|7|8|9){(0|1|2|3|4|5|6|7|8|9)}'), ('white', '(\n|\r|\t){(\n|\r|\t)}'), ('7', ';'), ('8', '.'), ('9', '+'), ('10', '-'), ('11', '*'), ('12', '/'), ('13', '-'), ('14', 'β'), ('15', 'δ')]

        self.ignore = None
        
        self.afd = direct_afd_algorithm(self.r, False)

        self.ignore_afd = direct_afd_algorithm(
            self.ignore, False) if self.ignore else None

        self.results = {}

    def scan(self, file_name: string):
        with open(file_name, "r") as file:
            for line in file:
                self.file_information += line

        while self.index < len(self.file_information):
            self.move()

        return [(token[0], value, key) for (key, (token, value)) in self.results.items()]

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
                print('Error léxico: el caracter {} en la posición: {}'.format(
                    repr(self.file_information[self.index]), self.index))
                self.index += 1