
import string

from automaton.Functions import direct_afd_algorithm, afd_simulation
from automaton.configuration import replace_reserved_words


class Scanner:
    def __init__(self):
        self.file_information = ''
        self.index = 0

        self.lexical_analyzer_name = 'MyCOCOR'

        self.r = '((A|B|C|D|E|F|G|H|I|J|K|L|M|N|Ñ|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|ñ|o|p|q|r|s|t|u|v|w|x|y|z){(A|B|C|D|E|F|G|H|I|J|K|L|M|N|Ñ|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|ñ|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9)})#|((")(\x01|\x02|\x03|\x04|\x05|\x06|\x07|\x08|\x0b|\x0c|\x0e|\x0f|\x10|\x11|\x12|\x13|\x14|\x15|\x16|\x17|\x18|\x19|\x1a|\x1b|\x1c|\x1d|\x1e|\x1f| |!|#|$|%|&|\'|β|δ|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|θ|\\|ω|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|ζ|φ|η|~|\x7f|\x80|\x81|\x82|\x83|\x84|\x85|\x86|\x87|\x88|\x89|\x8a|\x8b|\x8c|\x8d|\x8e|\x8f|\x90|\x91|\x92|\x93|\x94|\x95|\x96|\x97|\x98|\x99|\x9a|\x9b|\x9c|\x9d|\x9e|\x9f|\xa0|¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|\xad|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ){(\x01|\x02|\x03|\x04|\x05|\x06|\x07|\x08|\x0b|\x0c|\x0e|\x0f|\x10|\x11|\x12|\x13|\x14|\x15|\x16|\x17|\x18|\x19|\x1a|\x1b|\x1c|\x1d|\x1e|\x1f| |!|#|$|%|&|\'|β|δ|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|θ|\\|ω|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|ζ|φ|η|~|\x7f|\x80|\x81|\x82|\x83|\x84|\x85|\x86|\x87|\x88|\x89|\x8a|\x8b|\x8c|\x8d|\x8e|\x8f|\x90|\x91|\x92|\x93|\x94|\x95|\x96|\x97|\x98|\x99|\x9a|\x9b|\x9c|\x9d|\x9e|\x9f|\xa0|¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|\xad|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ)}("))#|(\'[/](A|B|C|D|E|F|G|H|I|J|K|L|M|N|Ñ|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|ñ|o|p|q|r|s|t|u|v|w|x|y|z)\')#|(CHRβ(0|1|2|3|4|5|6|7|8|9){(0|1|2|3|4|5|6|7|8|9)}δ)#|(CHRβ(0|1|2|3|4|5|6|7|8|9){(0|1|2|3|4|5|6|7|8|9)}δ..CHRβ(0|1|2|3|4|5|6|7|8|9){(0|1|2|3|4|5|6|7|8|9)}δ)#|((\x01|\x02|\x03|\x04|\x05|\x06|\x07|\x08|\t|\n|\x0b|\x0c|\r|\x0e|\x0f|\x10|\x11|\x12|\x13|\x14|\x15|\x16|\x17|\x18|\x19|\x1a|\x1b|\x1c|\x1d|\x1e|\x1f| |!|"|#|$|%|&|\'|*|,|/|0|1|2|3|4|5|6|7|8|9|:|;|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|\\|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~|\x7f|\x80|\x81|\x82|\x83|\x84|\x85|\x86|\x87|\x88|\x89|\x8a|\x8b|\x8c|\x8d|\x8e|\x8f|\x90|\x91|\x92|\x93|\x94|\x95|\x96|\x97|\x98|\x99|\x9a|\x9b|\x9c|\x9d|\x9e|\x9f|\xa0|¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|\xad|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ))#|(β.)#|(.δ)#'

        self.tokens = [('ident', '(A|B|C|D|E|F|G|H|I|J|K|L|M|N|Ñ|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|ñ|o|p|q|r|s|t|u|v|w|x|y|z){(A|B|C|D|E|F|G|H|I|J|K|L|M|N|Ñ|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|ñ|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9)}'), ('string', '(")(\x01|\x02|\x03|\x04|\x05|\x06|\x07|\x08|\x0b|\x0c|\x0e|\x0f|\x10|\x11|\x12|\x13|\x14|\x15|\x16|\x17|\x18|\x19|\x1a|\x1b|\x1c|\x1d|\x1e|\x1f| |!|#|$|%|&|\'|β|δ|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|θ|\\|ω|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|ζ|φ|η|~|\x7f|\x80|\x81|\x82|\x83|\x84|\x85|\x86|\x87|\x88|\x89|\x8a|\x8b|\x8c|\x8d|\x8e|\x8f|\x90|\x91|\x92|\x93|\x94|\x95|\x96|\x97|\x98|\x99|\x9a|\x9b|\x9c|\x9d|\x9e|\x9f|\xa0|¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|\xad|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ){(\x01|\x02|\x03|\x04|\x05|\x06|\x07|\x08|\x0b|\x0c|\x0e|\x0f|\x10|\x11|\x12|\x13|\x14|\x15|\x16|\x17|\x18|\x19|\x1a|\x1b|\x1c|\x1d|\x1e|\x1f| |!|#|$|%|&|\'|β|δ|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|θ|\\|ω|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|ζ|φ|η|~|\x7f|\x80|\x81|\x82|\x83|\x84|\x85|\x86|\x87|\x88|\x89|\x8a|\x8b|\x8c|\x8d|\x8e|\x8f|\x90|\x91|\x92|\x93|\x94|\x95|\x96|\x97|\x98|\x99|\x9a|\x9b|\x9c|\x9d|\x9e|\x9f|\xa0|¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|\xad|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ)}(")'), ('char', "'[/](A|B|C|D|E|F|G|H|I|J|K|L|M|N|Ñ|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|ñ|o|p|q|r|s|t|u|v|w|x|y|z)'"), ('charnumber', 'CHRβ(0|1|2|3|4|5|6|7|8|9){(0|1|2|3|4|5|6|7|8|9)}δ'), ('charinterval', 'CHRβ(0|1|2|3|4|5|6|7|8|9){(0|1|2|3|4|5|6|7|8|9)}δ..CHRβ(0|1|2|3|4|5|6|7|8|9){(0|1|2|3|4|5|6|7|8|9)}δ'), ('nontoken', '(\x01|\x02|\x03|\x04|\x05|\x06|\x07|\x08|\t|\n|\x0b|\x0c|\r|\x0e|\x0f|\x10|\x11|\x12|\x13|\x14|\x15|\x16|\x17|\x18|\x19|\x1a|\x1b|\x1c|\x1d|\x1e|\x1f| |!|"|#|$|%|&|\'|*|,|/|0|1|2|3|4|5|6|7|8|9|:|;|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|\\|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~|\x7f|\x80|\x81|\x82|\x83|\x84|\x85|\x86|\x87|\x88|\x89|\x8a|\x8b|\x8c|\x8d|\x8e|\x8f|\x90|\x91|\x92|\x93|\x94|\x95|\x96|\x97|\x98|\x99|\x9a|\x9b|\x9c|\x9d|\x9e|\x9f|\xa0|¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|\xad|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ)'), ('startcode', 'β.'), ('endcode', '.δ')]

        self.ignore = '(\r|\n|\t)#'
        
        self.afd = direct_afd_algorithm(self.r, False)

        self.ignore_afd = direct_afd_algorithm(
            self.ignore, False) if self.ignore else None

        self.results = {}

    def scan(self, file_name: string):
        with open(file_name, "r") as file:
            for line in file:
                self.file_information += line

        print('Resultados del analizador léxico "{}":'.format(
            self.lexical_analyzer_name))

        while self.index < len(self.file_information):
            self.move()

        print('{')
        for (token, value) in self.results.values():
            print('\t{}: {}'.format(token[0], repr(value)))
        print('}')

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

scanner = Scanner()
scanner.scan("inputs/archivo.txt")