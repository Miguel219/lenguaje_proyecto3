
import string

from automaton.Functions import direct_afd_algorithm, afd_simulation
from automaton.configuration import replace_reserved_words


class Parser:
    def __init__(self, tokens):
        self.i = 0
        self.tokens = tokens
        self.lookAheadToken = None
        self.lastToken = None
    
    def Expr(self):
        while self.lookAheadToken[0] == '13' or self.lookAheadToken[0] == '12' or self.lookAheadToken[0] == 'number':
            self.Stat()
            self.move('6')
        self.move('7')

    def Stat(self):
        value = 0
        value = self.Expression(value)
        print(value)

    def Expression(self, result):
        result1, result2 = 0, 0
        result1 = self.Term(result1)
        while self.lookAheadToken[0] == '9' or self.lookAheadToken[0] == '8':
            if self.lookAheadToken[0] == '8':
                self.move('8')
                result2 = self.Term(result2)
                result1 += result2
            if self.lookAheadToken[0] == '9':
                self.move('9')
                result2 = self.Term(result2)
                result1 -= result2
        result = result1
        return result

    def Term(self, result):
        result1, result2 = 0, 0
        result1 = self.Factor(result1)
        while self.lookAheadToken[0] == '11' or self.lookAheadToken[0] == '10':
            if self.lookAheadToken[0] == '10':
                self.move('10')
                result2 = self.Factor(result2)
                result1 *= result2
            if self.lookAheadToken[0] == '11':
                self.move('11')
                result2 = self.Factor(result2)
                result1 /= result2
        result = result1
        return result

    def Factor(self, result):
        signo = 1
        if self.lookAheadToken[0] == '12':
            self.move('12')
            signo = -1
        if self.lookAheadToken[0] == 'number':
            result = self.Number(result)
        if self.lookAheadToken[0] == '13':
            self.move('13')
            result = self.Expression(result)
            self.move('14')
        result *= signo
        return result

    def Number(self, result):
        self.move('number')
        result = int(self.lastToken[1])
        return result

    def move(self, token):
        if self.lookAheadToken[0] == token:
            self.lastToken = self.lookAheadToken
            self.i += 1
            if self.i < len(self.tokens):
                self.lookAheadToken = self.tokens[self.i]

    def parse(self):
        self.i = 0
        self.lookAheadToken = self.tokens[self.i]
        self.Expr()