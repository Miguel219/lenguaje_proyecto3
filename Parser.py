
class Parser:
    def __init__(self, tokens):
        self.i = 0
        self.tokens = tokens
        self.lookAheadToken = None
        self.lastToken = None
        self.errors = list()
    
    def MyCOCOR(self):
        CompilerName, EndName = '', ''
        self.move('18')
        CompilerName = self.Ident(CompilerName)
        print("Nombre Inicial del Compilador:{}".format(CompilerName))
        if self.lookAheadToken[0] == 'startcode':
            self.Codigo()
        self.Body()
        self.move('19')
        EndName = self.Ident(EndName)
        print("Nombre Final del Compilador:{}".format(EndName))

    def Body(self):
        self.Characters()
        if self.lookAheadToken[0] == '25':
            self.Keywords()
        self.Tokens()
        if self.lookAheadToken[0] == '27':
            self.Ignore()
        self.Productions()

    def Characters(self):
        CharName, Counter = '', 0
        self.move('20')
        print("LEYENDO CHARACTERS")
        while self.lookAheadToken[0] == 'ident':
            CharName = self.Ident(CharName)
            Counter += 1
            print("Char Set {}: {}".format(Counter, CharName))
            self.move('21')
            self.CharSet()
            while self.lookAheadToken[0] == '22' or self.lookAheadToken[0] == '23':
                if self.lookAheadToken[0] == '22':
                    self.move('22')
                    self.CharSet()
                elif self.lookAheadToken[0] == '23':
                    self.move('23')
                    self.CharSet()
                else:
                    self.printError()
            self.move('24')

    def Keywords(self):
        KeyName, StringValue, Counter = '', '', 0
        self.move('25')
        print("LEYENDO KEYWORDS")
        while self.lookAheadToken[0] == 'ident':
            KeyName = self.Ident(KeyName)
            Counter += 1
            print("KeyWord {}: {}".format(Counter, KeyName))
            self.move('21')
            StringValue = self.String(StringValue)
            self.move('24')

    def Tokens(self):
        TokenName, Counter = '', 0
        self.move('26')
        print("LEYENDO TOKENS")
        while self.lookAheadToken[0] == 'ident':
            TokenName = self.Ident(TokenName)
            Counter += 1
            print("Token {}: {}".format(Counter, TokenName))
            self.move('21')
            self.TokenExpr()
            if self.lookAheadToken[0] == '29':
                self.ExceptKeyword()
            self.move('24')

    def Ignore(self):
        self.move('27')
        print("LEYENDO IGNORE")
        self.CharSet()
        while self.lookAheadToken[0] == '22' or self.lookAheadToken[0] == '23':
            if self.lookAheadToken[0] == '22':
                self.move('22')
                self.CharSet()
            elif self.lookAheadToken[0] == '23':
                self.move('23')
                self.CharSet()
            else:
                self.printError()

    def Productions(self):
        Counter = 0
        self.move('28')
        ProdName = ''
        print("LEYENDO PRODUCTIONS")
        while self.lookAheadToken[0] == 'ident':
            ProdName = self.Ident(ProdName)
            Counter += 1
            print("Production {}: {}".format(Counter, ProdName))
            if self.lookAheadToken[0] == '37':
                self.Atributos()
            self.move('21')
            while self.lookAheadToken[0] == 'startcode':
                self.Codigo()
            self.ProductionExpr()
            self.move('24')

    def ExceptKeyword(self):
        self.move('29')
        self.move('25')

    def ProductionExpr(self):
        self.ProdTerm()
        while self.lookAheadToken[0] == '30':
            self.move('30')
            self.ProdTerm()

    def ProdTerm(self):
        self.ProdFactor()
        while self.lookAheadToken[0] == 'ident' or self.lookAheadToken[0] == 'char' or self.lookAheadToken[0] == '35' or self.lookAheadToken[0] == '33' or self.lookAheadToken[0] == '31' or self.lookAheadToken[0] == 'string':
            self.ProdFactor()

    def ProdFactor(self):
        if self.lookAheadToken[0] == 'ident' or self.lookAheadToken[0] == 'char' or self.lookAheadToken[0] == '33' or self.lookAheadToken[0] == '31' or self.lookAheadToken[0] == 'string':
            if self.lookAheadToken[0] == 'char' or self.lookAheadToken[0] == 'string' or self.lookAheadToken[0] == 'ident' or self.lookAheadToken[0] == '31':
                if self.lookAheadToken[0] == 'char' or self.lookAheadToken[0] == 'string' or self.lookAheadToken[0] == 'ident':
                    self.SymbolProd()
                elif self.lookAheadToken[0] == '31':
                    self.move('31')
                    self.ProductionExpr()
                    self.move('32')
                else:
                    self.printError()
            elif self.lookAheadToken[0] == '33':
                self.move('33')
                self.ProductionExpr()
                self.move('34')
            else:
                self.printError()
        elif self.lookAheadToken[0] == '35':
            self.move('35')
            self.ProductionExpr()
            self.move('36')
        else:
            self.printError()
        while self.lookAheadToken[0] == 'startcode':
            self.Codigo()

    def SymbolProd(self):
        SV, IN = '', ''
        if self.lookAheadToken[0] == 'char' or self.lookAheadToken[0] == 'string':
            if self.lookAheadToken[0] == 'string':
                SV = self.String(SV)
                print("String en Production: {}".format(SV))
            elif self.lookAheadToken[0] == 'char':
                self.move('char')
            else:
                self.printError()
        elif self.lookAheadToken[0] == 'ident':
            IN = self.Ident(IN)
            print("Identificador en Production: {}".format(IN))
            if self.lookAheadToken[0] == '37':
                self.Atributos()
        else:
            self.printError()

    def Codigo(self):
        self.move('startcode')
        while self.lookAheadToken[0] != 'endcode':
            self.ANY()
        self.move('endcode')

    def Atributos(self):
        self.move('37')
        while self.lookAheadToken[0] != '38':
            self.ANY()
        self.move('38')

    def TokenExpr(self):
        self.TokenTerm()
        while self.lookAheadToken[0] == '30':
            self.move('30')
            self.TokenTerm()

    def TokenTerm(self):
        self.TokenFactor()
        while self.lookAheadToken[0] == 'ident' or self.lookAheadToken[0] == 'char' or self.lookAheadToken[0] == '35' or self.lookAheadToken[0] == '33' or self.lookAheadToken[0] == '31' or self.lookAheadToken[0] == 'string':
            self.TokenFactor()

    def TokenFactor(self):
        if self.lookAheadToken[0] == 'ident' or self.lookAheadToken[0] == 'char' or self.lookAheadToken[0] == '33' or self.lookAheadToken[0] == '31' or self.lookAheadToken[0] == 'string':
            if self.lookAheadToken[0] == 'char' or self.lookAheadToken[0] == 'string' or self.lookAheadToken[0] == 'ident' or self.lookAheadToken[0] == '31':
                if self.lookAheadToken[0] == 'char' or self.lookAheadToken[0] == 'string' or self.lookAheadToken[0] == 'ident':
                    self.SimbolToken()
                elif self.lookAheadToken[0] == '31':
                    self.move('31')
                    self.TokenExpr()
                    self.move('32')
                else:
                    self.printError()
            elif self.lookAheadToken[0] == '33':
                self.move('33')
                self.TokenExpr()
                self.move('34')
            else:
                self.printError()
        elif self.lookAheadToken[0] == '35':
            self.move('35')
            self.TokenExpr()
            self.move('36')
        else:
            self.printError()

    def SimbolToken(self):
        IdentName, StringValue = '', ''
        if self.lookAheadToken[0] == 'char' or self.lookAheadToken[0] == 'string':
            if self.lookAheadToken[0] == 'string':
                StringValue = self.String(StringValue)
            elif self.lookAheadToken[0] == 'char':
                self.move('char')
            else:
                self.printError()
        elif self.lookAheadToken[0] == 'ident':
            IdentName = self.Ident(IdentName)
            print("Identificador en Token: {}".format(IdentName))
        else:
            self.printError()

    def CharSet(self):
        IdentName, StringValue = '', ''
        if self.lookAheadToken[0] == 'char' or self.lookAheadToken[0] == 'string' or self.lookAheadToken[0] == 'charinterval' or self.lookAheadToken[0] == 'charnumber':
            if self.lookAheadToken[0] == 'string':
                StringValue = self.String(StringValue)
            elif self.lookAheadToken[0] == 'char' or self.lookAheadToken[0] == 'charinterval' or self.lookAheadToken[0] == 'charnumber':
                self.Char()
            else:
                self.printError()
        elif self.lookAheadToken[0] == 'ident':
            IdentName = self.Ident(IdentName)
            print("Identificador en CharSet: {}".format(IdentName))
        else:
            self.printError()

    def Char(self):
        if self.lookAheadToken[0] == 'char' or self.lookAheadToken[0] == 'charnumber':
            if self.lookAheadToken[0] == 'char':
                self.move('char')
            elif self.lookAheadToken[0] == 'charnumber':
                self.move('charnumber')
            else:
                self.printError()
        elif self.lookAheadToken[0] == 'charinterval':
            self.move('charinterval')
        else:
            self.printError()

    def String(self, S):
        self.move('string')
        S = self.lastToken[1]
        return S

    def Ident(self, S):
        self.move('ident')
        S = self.lastToken[1]
        return S

    def ANY(self):
        self.lastToken = self.lookAheadToken
        self.i += 1
        if self.i < len(self.tokens):
            self.lookAheadToken = self.tokens[self.i]
   
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
        self.MyCOCOR()
    
    def printError(self):
        if(self.lookAheadToken[2] not in self.errors):
            print('Error sintáctico: los caracteres {} en la posición: {}'.format(
                repr(self.lookAheadToken[1]), self.lookAheadToken[2]))
            self.errors.append(self.lookAheadToken[2])