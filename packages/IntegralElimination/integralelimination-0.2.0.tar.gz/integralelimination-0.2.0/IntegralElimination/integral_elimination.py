from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .IntegralAlgebra import IntegralAlgebra

from ordered_set import OrderedSet

from .IntegralPolynomial import IntegralPolynomial 



def integral_elimination(IA: IntegralAlgebra,
                        F: OrderedSet[IntegralPolynomial],
                        disable_exp: bool = False,
                        disable_critical_pairs: bool = False,
                        nb_iter = None) -> tuple:

    T = OrderedSet([elem for elem in F])
    E = OrderedSet()
    X_prime = IA.order
    finished = False
    
    # print("""
    #     WARNING: topological sort not implemented  in extend_X_with_exp. 
    #     Elements are added at the end of E : 
    #     is it enough to ensure that each Qi does not
    #     involve any uj or vj with j > i ?
    #     """)
    
    i = 1
    while not finished:   
        T_prime = IA.auto_reduce(T)    
        if not disable_exp:
            T_E, E_prime = IA.update_exp(T_prime, E)
            X_prime = IA.extend_X_with_exp(E_prime)
            IA.update_IMO(X_prime)
            T_prime = T_prime | T_E # T_prime union T_E
 
        if not disable_critical_pairs:
            C = IA.critical_pairs(T_prime) 
            for Q in C:
                # _ is a boolean = has_been_reduced
                Q_red, _ = IA.reduce(Q,T_prime) 
                if not Q_red.is_zero():
                    T_prime.add(Q_red)
 
        if not disable_exp:
            E_prime_red = OrderedSet([])
            for ui, vi, Qi in E_prime:
                # _ is a boolean = has_been_reduced
                Qi_red, _ = IA.reduce(Qi, T_prime) 
                E_prime_red.add((ui, vi ,Qi_red))
            
            X_prime = IA.extend_X_with_exp(E_prime_red)
            IA.update_IMO(X_prime)
            E = E_prime_red 
 
        T_equal_T_prime = check_T_equal_T_prime(T, T_prime)
 
        if (i == nb_iter) or T_equal_T_prime:
            finished = True
        else:
            T = T_prime
        i += 1
    return (E, T, X_prime)


def check_T_equal_T_prime(T: OrderedSet[IntegralPolynomial],
                          T_prime: OrderedSet[IntegralPolynomial]) -> bool:
    T_sp = OrderedSet([eq.get_sympy_repr() for eq in T])
    T_prime_sp = OrderedSet([eq.get_sympy_repr() for eq in T_prime]) 
    return T_sp == T_prime_sp