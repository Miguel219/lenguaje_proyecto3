import string

from jinja2 import Environment, FileSystemLoader
from numpy import array
from automaton.AFD import AFD

from automaton.Functions import direct_afd_algorithm, afd_simulation
from automaton.ProductionTree import ProductionTree
from automaton.configuration import hash, replace_reserved_words

from scanner.configuration import (
    Char, char, ident, str, ignored_characters, any)


class Scanner:
    def __init__(self):
        self.file_information = ''
        self.lexical_analyzer_name = ''
        self.index = 0

        self.variables = {}

        self.characters = []
        self.keywords = []
        self.tokensExceptKeywords = []
        self.tokens = []
        self.whiteSpace = []
        self.productions = []

        self.str_afd = direct_afd_algorithm(str)
        self.char_afd = direct_afd_algorithm(char)
        self.ident_afd = direct_afd_algorithm(ident)
        self.Char_afd = direct_afd_algorithm(Char)
        self.ignored_characters_afd = direct_afd_algorithm(ignored_characters)
        self.reserved_words_afd = direct_afd_algorithm(
            'CHARACTERS|KEYWORDS|TOKENS|IGNORE|PRODUCTIONS|END')

    def scan(self, file_name: string):
        with open(file_name, "r") as file:
            for line in file:
                self.file_information += line

        self.move(direct_afd_algorithm('COMPILER'))
        self.lexical_analyzer_name = self.move(self.ident_afd)
        self.moveComments()
        reserved_word = self.move(self.reserved_words_afd)

        while reserved_word and reserved_word != 'END':
            # Se procesan los characters
            if reserved_word == 'CHARACTERS':
                self.processSetDecl()

            # Se procesan los keywords
            if reserved_word == 'KEYWORDS':
                self.processKeywordDecl()

            # Se procesan los tokens
            if reserved_word == 'TOKENS':
                self.processTokenDecl()

            # Se procesan los ignore
            if reserved_word == 'IGNORE':
                self.whiteSpace.append(self.processSet())

            # Se procesan las productions
            if reserved_word == 'PRODUCTIONS':
                self.productions.append(self.processProduction())

            # Se procesan los comentarios
            self.moveComments()

            # Se revisa si ya se cambio de sección
            reserved_word = self.move(self.reserved_words_afd) or reserved_word

        r_array = []

        if len(self.tokens) > 0:
            r_array.append('|'.join(['({}){}'.format(self.variables[token], hash)
                                     for token in self.tokens]))
        if len(self.keywords) > 0:
            r_array.append('|'.join(['({}){}'.format(self.variables[token], hash)
                                     for token in self.keywords]))
        if len(self.tokensExceptKeywords) > 0:
            r_array.append('|'.join(['({}){}'.format(self.variables[token], hash)
                                     for token in self.tokensExceptKeywords]))

        self.generateScanner(
            '|'.join(r_array),
            [
                (token, self.variables[token])
                for token in [*self.tokens, *self.keywords, *self.tokensExceptKeywords]
            ],
            '({}){}'.format('|'.join(self.whiteSpace), hash) if len(
                self.whiteSpace) > 0 else None
        )

        # self.generateParser()

    def move(self, afd: AFD, include_reserved_words=False, ignored_characters=False):
        # Se avanzan todos los caracteres ignorados
        if not ignored_characters:
            self.move(self.ignored_characters_afd, ignored_characters=True)

        finish = True
        final_index = self.index

        # Se simula mientras:
        # - no se encuentre un simbolo que no esta en las transiciones
        # - no se exceda al tamaño del archivo
        while finish and final_index <= len(self.file_information):
            final_index += 1
            finish = afd_simulation(
                afd,
                (
                    replace_reserved_words(
                        self.file_information[self.index:final_index])
                    if include_reserved_words else
                    self.file_information[self.index:final_index]
                )
            )[1]

        # Se regresa al caracter anterior
        final_index -= 1
        # Si es una cadena de largo 1 o más y pertenece al afd, entonces avanzar el indice hasta ese caracter
        if (final_index > self.index):
            final_string = (
                replace_reserved_words(
                    self.file_information[self.index:final_index])
                if include_reserved_words else
                self.file_information[self.index:final_index]
            )
            if(afd_simulation(afd, final_string)[0]):
                self.index = final_index
                # Se devuelve la cadena que cumplio con el afd
                return final_string

    def moveComments(self):
        while self.move(direct_afd_algorithm(replace_reserved_words('(.')), include_reserved_words=True):
            while not self.move(direct_afd_algorithm(replace_reserved_words('.)')), include_reserved_words=True):
                self.index += 1

    def processSetDecl(self):
        i = self.move(self.ident_afd)
        self.characters.append(i)
        self.move(direct_afd_algorithm('='))
        self.variables[i] = self.processSet()
        self.move(direct_afd_algorithm('.'))

    def processSet(self):
        s = self.processBasicSet()
        sign = self.move(direct_afd_algorithm('+|-'))
        while sign:
            list_s = list(s)
            for c in list(self.processBasicSet()):
                if sign == '+':
                    if c not in list_s:
                        list_s.append(c)
                else:
                    if c in list_s:
                        list_s.remove(c)
            s = ''.join(list_s)
            sign = self.move(direct_afd_algorithm('+|-'))
        return '|'.join(s)

    def processBasicSet(self):
        s = self.move(self.str_afd, include_reserved_words=True)
        if s:
            return s[1:-1]
        else:
            s = self.move(self.Char_afd, include_reserved_words=True)
            if s:
                if s.startswith('CHR'):
                    initial_s = chr(int(s[4:-1]))
                else:
                    initial_s = s[1:-1]
                if(self.move(direct_afd_algorithm('..'))):
                    s = self.move(self.Char_afd, include_reserved_words=True)
                    if s.startswith('CHR'):
                        final_s = chr(int(s[4:-1]))
                    else:
                        final_s = s[1:-1]
                    return ''.join([chr(i) for i in range(
                        ord(initial_s),
                        ord(final_s)
                    )])
                else:
                    return initial_s
            else:
                s = self.move(self.ident_afd)
                if s == 'ANY':
                    return any[1:-1].replace('|', '')
                return self.variables[s].replace('|', '')

    def processKeywordDecl(self):
        i = self.move(self.ident_afd)
        self.keywords.append(i)
        self.move(direct_afd_algorithm('='))
        self.variables[i] = self.move(
            self.str_afd, include_reserved_words=True)[1:-1]
        self.move(direct_afd_algorithm('.'))

    def processTokenDecl(self):
        i = self.move(self.ident_afd)
        self.move(direct_afd_algorithm('='))
        s, isExceptKeyword = self.processTokenExpr()
        self.variables[i] = s
        if isExceptKeyword and len(self.keywords) > 0:
            self.tokensExceptKeywords.append(i)
        else:
            self.tokens.append(i)

    def processTokenExpr(self):
        s = ''
        final = self.move(direct_afd_algorithm('EXCEPT KEYWORDS.|.'))
        while not final:
            if self.file_information[self.index] in ['|', '(', ')', '[', ']', '{', '}']:
                s += self.file_information[self.index]
                self.index += 1
            else:
                s += self.processTokenTerm()
            final = self.move(direct_afd_algorithm('EXCEPT KEYWORDS.|.'))
        if final == 'EXCEPT KEYWORDS.':
            return s, True
        else:
            return s, False

    def processTokenTerm(self):
        s = self.move(self.str_afd, include_reserved_words=True)
        if s:
            return s[1:-1]
        else:
            s = self.move(self.ident_afd)
            if s == 'ANY':
                return any
            if s:
                return '({})'.format(self.variables[s])
            else:
                s = self.move(self.char_afd, include_reserved_words=True)
                return s[1:-1]

    def processProduction(self):
        expression = list()
        expression.append(('name', self.move(self.ident_afd)))
        attributes = self.processAttributes()
        expression.append(('attribute', attributes or ''))
        semAction = self.processSemAction()
        if semAction:
            expression.append(('semAction', semAction))
        expression.append(self.move(direct_afd_algorithm('=')))
        expression = self.processExpression(expression=list())
        print(expression)
        pt = ProductionTree(r=expression)
        pt.generate_tree()
        return expression

    def processAttributes(self):
        if self.move(direct_afd_algorithm('<')):
            attributes = ''
            while not self.move(direct_afd_algorithm('>'), ignored_characters=True):
                attributes += self.file_information[self.index]
                self.index += 1
            return attributes

    def processSemAction(self):
        if self.move(direct_afd_algorithm(replace_reserved_words('(.')), include_reserved_words=True):
            semAction = ''
            while not self.move(direct_afd_algorithm(replace_reserved_words('.)')), include_reserved_words=True, ignored_characters=True):
                semAction += self.file_information[self.index]
                self.index += 1
            return semAction

    def processExpression(self, afd_finisher=direct_afd_algorithm('.'), include_reserved_words=False, expression: list = list()):
        while not self.move(afd_finisher, include_reserved_words=include_reserved_words):
            # attribute
            s = self.processAttributes()
            if s:
                expression.append(('attribute', s))
            # semAction
            s = self.processSemAction()
            if s:
                expression.append(('semAction', s))
            # ()
            s = self.move(direct_afd_algorithm(
                replace_reserved_words('(')), include_reserved_words=True)
            if s:
                expression.append('(')
                self.processExpression(direct_afd_algorithm(
                    replace_reserved_words(')')), True, expression=expression)
                expression.append(')')
            # []
            s = self.move(direct_afd_algorithm(
                replace_reserved_words('[')), include_reserved_words=True)
            if s:
                expression.append('[')
                self.processExpression(direct_afd_algorithm(
                    replace_reserved_words(']')), True, expression=expression)
                expression.append(']')
            # {}
            s = self.move(direct_afd_algorithm(
                replace_reserved_words('{')), include_reserved_words=True)
            if s:
                expression.append('{')
                self.processExpression(direct_afd_algorithm(
                    replace_reserved_words('}')), True, expression=expression)
                expression.append('}')
            # |
            s = self.move(direct_afd_algorithm(
                replace_reserved_words('|')), include_reserved_words=True)
            if s:
                expression.append('|')
            # symbol
            s = self.move(self.str_afd, include_reserved_words=True)
            if s:
                i = "{}".format(len(self.variables))
                self.variables[i] = s[1:-1]
                self.tokens.append(i)
                expression.append(('token', i))
            # ident
            s = self.move(self.ident_afd)
            if s:
                if s in [*self.tokens, *self.keywords, *self.tokensExceptKeywords]:
                    expression.append(('token', s))
                else:
                    expression.append(('ident', s))
        return expression

    def generateScanner(self, r: string, tokens: list, ignore: string):

        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('Scanner.txt')
        output_from_parsed_template = template.render(
            lexical_analyzer_name=repr(self.lexical_analyzer_name), r=repr(r), tokens=tokens, ignore=repr(ignore)
        )

        with open('Scanner.py', 'w', encoding='utf-8') as file:
            file.write(output_from_parsed_template)
            file.close()

    def generateParser(self):

        code = []
        for production in self.productions:
            tab = 1
            for term in production:
                if term[0] == 'name':
                    code.append('def {}'.format(term[1]))
                elif term[0] == 'attribute':
                    code.append('({})'.format(term[1]))
                elif term[0] == '=':
                    tab += 1
                    code.append(':\n{}'.format('\t'*tab))
                elif term[0] == '{':
                    tab += 1
                    code.append('while True:\n{}'.format('\t'*tab))
                elif term[0] == '}':
                    tab -= 1
                    code.append('\n{}'.format('\t'*tab))
            code.append('\n\n\t')

        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('Parser.txt')
        output_from_parsed_template = template.render(
            lexical_analyzer_name=repr(self.lexical_analyzer_name), productions=self.productions, code=code
        )

        with open('Parser.py', 'w', encoding='utf-8') as file:
            file.write(output_from_parsed_template)
            file.close()
