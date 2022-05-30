from Scanner import Scanner
from Parser import Parser

scanner = Scanner()
tokens = scanner.scan("inputs/archivo.txt")

parser = Parser(tokens=tokens)
parser.parse()
