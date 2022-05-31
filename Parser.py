
class Parser:
    def __init__(self, tokens):
        self.i = 0
        self.tokens = tokens
        self.lookAheadToken = None
        self.lastToken = None
    
    def Expr(self):
        while self.lookAheadToken[0] == 'number' or self.lookAheadToken[0] == '14' or self.lookAheadToken[0] == 'decnumber' or self.lookAheadToken[0] == '13':
            self.Stat()
            self.move('7')
            while self.lookAheadToken[0] == 'white':
                self.move('white')
        while self.lookAheadToken[0] == 'white':
            self.move('white')
        self.move('8')

    def Stat(self):
        value = 0
        value = self.Expression(value)
        print("Resultado: {}".format(value))

    def Expression(self, result):
        result1, result2 = 0, 0
        result1 = self.Term(result1)
        while self.lookAheadToken[0] == '10' or self.lookAheadToken[0] == '9':
            if self.lookAheadToken[0] == '9':
                self.move('9')
                result2 = self.Term(result2)
                result1 += result2
            elif self.lookAheadToken[0] == '10':
                self.move('10')
                result2 = self.Term(result2)
                result1 -= result2
            else:
                self.printError()
        result = result1
        return result

    def Term(self, result):
        result1, result2 = 0, 0
        result1 = self.Factor(result1)
        while self.lookAheadToken[0] == '12' or self.lookAheadToken[0] == '11':
            if self.lookAheadToken[0] == '11':
                self.move('11')
                result2 = self.Factor(result2)
                result1 *= result2
            elif self.lookAheadToken[0] == '12':
                self.move('12')
                result2 = self.Factor(result2)
                result1 /= result2
            else:
                self.printError()
        result = result1
        return result

    def Factor(self, result):
        sign = 1
        if self.lookAheadToken[0] == '13':
            self.move('13')
            sign = -1
        if self.lookAheadToken[0] == 'number' or self.lookAheadToken[0] == 'decnumber':
            result = self.Number(result)
        elif self.lookAheadToken[0] == '14':
            self.move('14')
            result = self.Expression(result)
            self.move('15')
        else:
            self.printError()
        result *= sign
        return result

    def Number(self, result):
        if self.lookAheadToken[0] == 'number':
            self.move('number')
        elif self.lookAheadToken[0] == 'decnumber':
            self.move('decnumber')
        else:
            self.printError()
        result = float(self.lastToken[1])
        return result

    def move(self, token):
        if self.lookAheadToken[0] == token:
            self.lastToken = self.lookAheadToken
            self.i += 1
            if self.i < len(self.tokens):
                self.lookAheadToken = self.tokens[self.i]
        else:
            self.printError()

    def parse(self):
        self.i = 0
        self.lookAheadToken = self.tokens[self.i]
        self.Expr()
    
    def printError(self):
        print('Error sintáctico: los caracteres {} en la posición: {}'.format(
            repr(self.lookAheadToken[1]), self.lookAheadToken[2]))