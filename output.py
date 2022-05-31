from Scanner import Scanner
from Parser import Parser

scanner = Scanner()
tokens = scanner.scan("inputs/3.atg")

parser = Parser(tokens=tokens)
parser.parse()
