import functools
import timeit

from automaton.AFD import AFD
from automaton.AFN import AFN
from automaton.configuration import hash
from automaton.ExpressionTree import ExpressionTree


def timemeasure(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed_time = timeit.default_timer() - start_time
        # print('Función [{}] ejecutada en {} ms'.format(
        #     func.__name__, elapsed_time * 1000))
        return result
    return new_func


@timemeasure
def thompson_algorithm(r: str, printResult: bool = False):
    """Crea un AFN a parir del arbol de una expresion regular"""

    # Se genera el arbol
    expression_tree = ExpressionTree(r)
    expression_tree.generate_tree()

    afn = AFN()
    afn.generate_AFN_from_re(expression_tree)

    if printResult:
        print(afn)
        afn.graph_AFN()

    return afn


@timemeasure
def subset_algorithm(afn: AFN, printResult: bool = False):
    """Crea un AFD a parir de un AFN"""

    afd = AFD()
    afd.generate_AFD_from_AFN(afn)

    if printResult:
        print(afd)
        afd.graph_AFD()

    return afd


@timemeasure
def direct_afd_algorithm(r: str, appendHash: bool = True, printResult: bool = False):
    """Crea un AFD a parir del arbol de una expresion regular"""

    # Se genera el arbol
    if appendHash:
        r = '({}){}'.format(r, hash)
    expression_tree = ExpressionTree(r)
    expression_tree.generate_tree()

    afd = AFD()
    afd.generate_AFD_from_re(expression_tree)

    if printResult:
        print(afd)
        afd.graph_AFD()

    return afd


@timemeasure
def minimization_algorithm(afd: AFD, printResult: bool = False):
    """Minimización de un AFD"""

    afd.minimize_AFD()

    if printResult:
        print(afd)
        afd.graph_AFD()

    return afd


@timemeasure
def afn_simulation(afn: AFN, w: str, printResult: bool = False):
    """Simulación de un AFN dada una cadena w"""

    # Se genera el AFD que se formará en la simulación del AFN
    afd = AFD()

    result = afd.simulate_AFN(afn, w)

    if printResult:
        print('Simulación del AFN y w={}:\n\tResultado: {}'.format(
            w, 'SÍ' if result else 'NO'))

    return result


@timemeasure
def afd_simulation(afd: AFD, w: str, printResult: bool = False):
    """Simulación de un AFD dada una cadena w"""

    (result, finish) = afd.simulate_AFD(w)

    if printResult:
        print('Simulación del AFN y w={}:\n\tResultado: {}'.format(
            w, 'SÍ' if result else 'NO'))

    return (result, finish)
