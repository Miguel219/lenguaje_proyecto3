import string

import pydot

from automaton.AFN import AFN
from automaton.configuration import epsilon, hash, symbols
from automaton.ExpressionTree import ExpressionTree


class AFD:
    def __init__(self):
        # Componentes del AFD
        self.states = list()
        self.symbols = list()
        self.transitions = {}
        self.initial = None
        self.finals = list()
        self.finals_ids = {}

        # Guarda los estados y transiciones con los estados de un AFN
        self.d_states = list()
        self.d_tran = {}

        # Diccionario donde se hace el match de los estados de un AFN con un AFD
        self.matchStates = {}

        # AFN
        self.afn = None

        # Árbol de la expresión regular
        self.expression_tree = None

        # Si esta minimanizado
        self.minimized = False

    def __str__(self):
        return (('-' * 100) +
                '\nAFD {}({}):\n'.format('minimizado ' if self.minimized else '', 'a partir de un AFN' if self.afn else 'a partir de una expresión regular') +
                ('-' * 100) +
                '\nstates: {}\nsymbols: {}\ntransitions: {}\ninitial: {}\nfinals: {}\n' +
                ('-' * 100)
                ).format(self.states, self.symbols, self.transitions, self.initial, self.finals)

    # Función cerradura epsilon
    def epsilon_closure(self, states: list, result=list()):
        for state in states:
            if (state, epsilon) in self.afn.transitions:
                transitions = self.afn.transitions[(state, epsilon)]
                new_trans = [
                    tran for tran in transitions if tran not in result]
                result = list(dict.fromkeys([*result, *transitions]))
                result = self.epsilon_closure(new_trans, result)
        result = list(dict.fromkeys([*result, *states]))
        result.sort()
        return result

    # Función move dado un símbolo
    def move(self, states: list, symbol):
        result = list()
        for state in states:
            if (state, symbol) in self.afn.transitions:
                transitions = self.afn.transitions[(state, symbol)]
                for newState in transitions:
                    result.append(newState)
        result = list(dict.fromkeys(result))
        result.sort()
        return result

    # Función que procesa pi para la minimización
    def process_pi(self, pi):
        for group in pi:
            for symbol in self.symbols:
                subsets = {}
                for state in group:
                    if (state, symbol) in self.transitions:
                        new_state = self.transitions[(state, symbol)]
                        for i in range(len(pi)):
                            if new_state in pi[i]:
                                if i in subsets.keys():
                                    subsets[i] = [*subsets[i], state]
                                else:
                                    subsets[i] = [state]
                if len(subsets.values()) > 1:
                    return [*[pi[index] for index in range(len(pi)) if pi[index] != group], *subsets.values()]
        return pi

    # Limpia el AFD para generar todas las partes de un automata finito determinista
    def clean_AFD(self):
        for i in range(len(self.d_states)):
            state = str(i)
            d_state = (','.join(str(state) for state in self.d_states[i]))
            self.matchStates[d_state] = state

            if self.afn:
                if self.afn.initial in self.d_states[i]:
                    self.initial = state
                if self.afn.final in self.d_states[i]:
                    self.finals.append(state)
            if self.expression_tree:
                firstpos = self.expression_tree.firstpos[self.expression_tree.tree.id]
                lastpos = self.expression_tree.lastpos[self.expression_tree.tree.id]
                state_lastpos = set(self.d_states[i]) & set(lastpos)
                if d_state == ','.join(str(state) for state in firstpos):
                    self.initial = state
                if state_lastpos:
                    self.finals.append(state)
                    self.finals_ids[state] = min(
                        [lastpos.index(s) for s in state_lastpos])

        for d_state in self.matchStates.keys():
            state = self.matchStates[d_state]
            self.states.append(state)
            for symbol in self.symbols:
                if (d_state, symbol) in self.d_tran:
                    self.transitions[(state, symbol)] = self.matchStates[','.join(
                        str(state) for state in self.d_tran[(d_state, symbol)])]

    def generate_AFD_from_AFN(self, afn: AFN):
        '''Genera la AFD a partir de una AFN'''

        self.afn = afn
        self.d_states.append(self.epsilon_closure([self.afn.initial]))
        self.epsilon_closure([5, 10])
        self.symbols = [
            symbol for symbol in self.afn.symbols if symbol != epsilon]
        for states in self.d_states:
            for symbol in self.symbols:
                u = self.epsilon_closure(self.move(states, symbol))
                if len(u) > 0:
                    u.sort()
                    if u not in self.d_states:
                        self.d_states.append(u)
                    self.d_tran[(','.join(str(state)
                                for state in states), symbol)] = u
        self.clean_AFD()

    def generate_AFD_from_re(self, expression_tree: ExpressionTree):
        '''Genera la AFD a partir de una expresión regular'''

        self.expression_tree = expression_tree
        self.d_states.append(
            self.expression_tree.firstpos[self.expression_tree.tree.id])

        for c in self.expression_tree.r:
            if c in symbols and c != hash:
                self.symbols.append(c)
        self.symbols = list(dict.fromkeys(self.symbols))

        for states in self.d_states:
            d_state = ','.join(str(state) for state in states)
            for symbol in self.symbols:
                for id in states:
                    node = self.expression_tree.search_by_id(id)
                    if(node == symbol):
                        if (d_state, symbol) in self.d_tran.keys():
                            self.d_tran[(d_state, symbol)] = list(dict.fromkeys([
                                *self.d_tran[(d_state, symbol)], *self.expression_tree.nextpos[id]]))
                        else:
                            self.d_tran[(d_state, symbol)
                                        ] = self.expression_tree.nextpos[id]
                if (d_state, symbol) in self.d_tran.keys() and self.d_tran[(d_state, symbol)] not in self.d_states:
                    self.d_states.append(self.d_tran[(d_state, symbol)])

        self.clean_AFD()

    def simulate_AFN(self, afn: AFN, w: str):
        '''Simula un AFN dada una cadena w. Retorna True en caso la cadena w es aceptada por el AFN y False en el caso contrario'''

        self.afn = afn
        S = self.epsilon_closure([self.afn.initial])
        for c in w:
            S = self.epsilon_closure(self.move(S, c))
        if self.afn.final in S:
            return True
        return False

    def simulate_AFD(self, w: str):
        '''Simula un AFD dada una cadena w. Retorna True en caso la cadena w es aceptada por el AFD y False en el caso contrario'''

        s = self.initial
        for c in w:
            if (s, c) in self.transitions.keys():
                s = self.transitions[(s, c)]
            else:
                return (False, False)
        if s in self.finals:
            return (s, True)
        return (False, True)

    def minimize_AFD(self):
        '''Minimiza un AFD para generar un AFD que acepta el mismo lenguaje y tiene el menor número de estados posible.'''
        pi = [[state for state in self.states if state not in self.finals], self.finals]
        final_pi = []
        while len(pi) != len(final_pi):
            pi = final_pi if len(final_pi) > 0 else pi
            final_pi = self.process_pi(pi)

        final_pi.sort()

        new_states = list()
        new_finals = list()
        for states in final_pi:
            if len(states) > 0:
                state = states[0]
                new_states.append(state)
                if set(self.finals) & set(states):
                    new_finals = [*new_finals, state]

        self.transitions = {
            (new_states.index(key[0]), key[1]): new_states.index([states[0] for states in final_pi if self.transitions[key] in states][0]) for key in self.transitions if key[0] in new_states}
        self.states = [i for i in range(len(new_states))]
        self.initial = new_states.index(self.initial)
        self.finals = [new_states.index(state) for state in new_finals]
        self.minimized = True

    def graph_AFD(self):
        '''Genera el archivo AFD.png a partir de un archivo AFD.dot generado con la informacion del automata finito determinista'''

        with open('results/AFD.dot', 'w', encoding='utf-8') as file:
            keys = list(self.transitions)
            file.write('digraph{\n')
            file.write('rankdir=LR\n')
            for state in self.states:
                if state == self.initial:
                    file.write('{} [root=true]\n'.format(state))
                    file.write('fake [style=invisible]\n')
                    file.write('fake -> {} [style=bold]\n'.format(state))
                elif state in self.finals:
                    file.write('{} [shape=doublecircle]\n'.format(state))
                else:
                    file.write('{}\n'.format(state))
            for key in keys:
                file.write(
                    '{} -> {} [ label="{}" ]\n'.format(key[0], self.transitions[key], key[1]))
            file.write('}\n')

        (graph,) = pydot.graph_from_dot_file('results/AFD.dot')
        graph.write_png(('results/{}AFD.png' if self.afn else 'results/{}direct_AFD.png').format(
            'min_' if self.minimized else ''))
