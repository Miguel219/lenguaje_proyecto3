import string

from numpy import number
from automaton.configuration import replace_reserved_words, symbols

any = '({})'.format('|'.join(symbols))

anyButQuote = '({})'.format('|'.join([c for c in symbols if c != '"']))

anyButApostrophe = '({})'.format('|'.join([c for c in symbols if c != '\'']))

letter = '({})'.format('|'.join(string.ascii_letters))

digit = '({})'.format(
    '|'.join(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']))

ident = '({}{{{}|{}}})'.format(letter, letter, digit)

num = '({}{{{}}})'.format(digit, digit)

str = '("{{{}}}")'.format(anyButQuote)

char = '(\'{}\')'.format(anyButApostrophe)

Char = '({}|(CHR{}{}{}))'.format(
    char, replace_reserved_words('('), num, replace_reserved_words(')'))

ignored_characters = '({}){{{}}}'.format(
    '|'.join(['\n', ' ', '\t']), '|'.join(['\n', ' ', '\t']))
