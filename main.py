from scanner.Scanner import Scanner

scanner = Scanner()
r, tokens, ignore = scanner.scan("inputs/Archivo3.ATG")
scanner.generateFile(r, tokens, ignore)
