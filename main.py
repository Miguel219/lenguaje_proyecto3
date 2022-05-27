from scanner.Scanner import Scanner

scanner = Scanner()
r, tokens, ignore = scanner.scan("inputs/1.atg")
scanner.generateFile(r, tokens, ignore)
