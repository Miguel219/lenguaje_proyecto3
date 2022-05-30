from automaton.configuration import (alternative, closingGroup,
                                     closingIteration, closingOption, dot,
                                     epsilon, openingGroup, openingIteration,
                                     openingOption, question, star)
from automaton.Node import Node


class ProductionTree:
    def __init__(self, r):
        # Expresión Regular
        self.r = r

        # Árbol de la expresión regular
        self.tree = None

        # Guarda el valor de cada nodo según su id
        self.nodes = {}

        # Expresión regular en postfix
        self.postfix = []

        # Último caracter
        self.last_c = None

        # Precedencia de los operadores
        self.precedence = {
            alternative: 1,
            dot: 2,
            question: 3,
            star: 3
        }

        # Funciones calculadas a partir del árbol sintáctico
        self.nullable = {}
        self.firstpos = {}
        self.lastpos = {}
        self.nextpos = {}

        # Stack útil para generar el AFN
        self.stack = []

    # Funciones para manejar el stack de la clase
    def is_empty(self):
        return len(self.stack) == 0

    def last(self):
        return self.stack[-1]

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            BaseException("Error")

    def push(self, op):
        self.stack.append(op)

    # Revisa la precedencia entre dos operadores
    def not_greater(self, i):
        try:
            return self.precedence[i] <= self.precedence[self.last()]
        except:
            BaseException("Error")

    # Procesa la concatenacion (dot) de dos caracteres
    def process_dot(self, c):
        # Si el siguiente caracter es algun simbolo o un ( o { o [
        # y el anterior simbolo fue algun simbolo o un ) o } o ] o ? o *
        if ((c in [openingGroup, openingIteration, openingOption] or type(c) is tuple) and
                (self.last_c in [closingGroup, closingIteration, closingOption, question, star] or type(self.last_c) is tuple)):
            self.process(dot)

    # Procesa un operador
    def process_operator(self, c):
        # Se agrega a postfix hasta que haya un operador con menor jerarquía en el stack
        while(not self.is_empty() and self.not_greater(c)):
            self.postfix.append(self.pop())
        self.push(c)

    # Procesa un caracter
    def process(self, c):
        # Si es algun simbolo o un ( o { o [ se extraen todos los operadores de un solo simbolo ? o *
        if c in [openingGroup, openingIteration, openingOption] or type(c) is tuple:
            while(not self.is_empty() and self.last() in [question, star]):
                self.postfix.append(self.pop())

        # Si es algun simbolo
        if type(c) is tuple:
            self.postfix.append(c)

        # Si es un ( o { o [
        elif c in [openingGroup, openingIteration, openingOption]:
            self.push(c)

        # Si es un )
        elif c == closingGroup:
            while not self.is_empty() and self.last() != openingGroup:
                a = self.pop()
                self.postfix.append(a)
            if self.is_empty() or self.last() != openingGroup:
                BaseException("Error")
            else:
                self.pop()

        # Si es un }
        elif c == closingIteration:
            while not self.is_empty() and self.last() != openingIteration:
                a = self.pop()
                self.postfix.append(a)
            if self.is_empty() and self.last() != openingIteration:
                BaseException("Error")
            else:
                self.pop()
                self.process_operator(star)

        # Si es un ]
        elif c == closingOption:
            while not self.is_empty() and self.last() != openingOption:
                a = self.pop()
                self.postfix.append(a)
            if self.is_empty() and self.last() != openingOption:
                BaseException("Error")
            else:
                self.pop()
                self.process_operator(question)

        # Si es un operador
        else:
            self.process_operator(c)

        # Se guarda el ultimo caracter procesado
        self.last_c = c

    # Genera el postfix a partir de la expresion regular
    def generate_postfix(self):
        self.last_c = None

        for c in self.r:
            self.process_dot(c)
            self.process(c)

        while not self.is_empty():
            self.postfix.append(self.pop())

    # Genera el arbol de la expresion a partir del postfix
    def generate_functions(self, node: Node, i=0):
        if node:
            i = self.generate_functions(node.left, i)
            i = self.generate_functions(node.right, i)
            # Se guarda el id del nodo
            node.id = i
            self.nodes[i] = node.value

            # Se calcula el valor de nullable(n) y firstpos(n)
            if type(node.value) is tuple:
                if node.value[0] == 'semAction':
                    self.nullable[node.id] = True
                    self.firstpos[node.id] = []
                else:
                    self.nullable[node.id] = False
                    self.firstpos[node.id] = [node.value]
            elif node.value == alternative:
                self.nullable[node.id] = self.nullable[node.left.id] or self.nullable[node.right.id]
                self.firstpos[node.id] = [
                    *self.firstpos[node.left.id], *self.firstpos[node.right.id]]
            elif node.value == dot:
                self.nullable[node.id] = self.nullable[node.left.id] and self.nullable[node.right.id]
                self.firstpos[node.id] = [*self.firstpos[node.left.id], *self.firstpos[node.right.id]
                                          ] if self.nullable[node.left.id] else self.firstpos[node.left.id]
            elif node.value in [star, question]:
                self.nullable[node.id] = True
                self.firstpos[node.id] = self.firstpos[node.left.id]

            return i + 1
        return i

    def generate_tree(self):
        '''Genera el arbol de la expresion a partir de una expresión regular'''
        # Primero se genera la expresion en postfix
        self.generate_postfix()

        for c in self.postfix:
            # Si es algun simbolo
            if type(c) is tuple:
                self.push(Node(c))
            # Si es un operador
            else:
                op = Node(c)
                # Si es algun operador de un solo simbolo ? o *
                if c in [question, star]:
                    x = self.pop()
                # De lo contrario
                else:
                    y = self.pop()
                    x = self.pop()
                    op.right = y
                op.left = x
                self.push(op)
        self.tree = self.pop()
        self.generate_functions(self.tree)

    # Busca dentro del arbol según su id
    def search_by_id(self, id):
        if id in self.nodes.keys():
            return self.nodes[id]
        return None
