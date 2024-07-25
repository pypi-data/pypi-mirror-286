import sympy as sp
from ordered_set import OrderedSet
from IPython.display import display, Math

from .ordering import IMO
from .IntegralMonomial import IM
from .utils import (
    is_int,
    ShuffleList,
    diff_lists
)
from .IntegralPolynomial import IntegralPolynomial
from .reduction import (
    reduction_M_by_P_simple_case,
    reduction_M_by_P_reduced_power, 
    reduction_M_by_P, 
    reduce,auto_reduce
)
from .critical_pairs import (
    critical_pairs_PI_QI,
    critical_pairs_PI_QN,
    critical_pairs_PN_QN,
    critical_pairs
)
from .exponentials import (
    find_A_A0_G_F, 
    update_exp, 
    extend_X_with_exp
)
from .integral_elimination import integral_elimination

class IntegralAlgebra():
    """
    integral polynomials will be represented as follows :
    eq = {IM(x(t):3, IM(y(t),1,y(t)):theta+lambda}
    using eq.as_coefficients_dict(IM)
    It means that eq is the sum of the two tuples 
    """
    def __init__(self, order, parameters):
        self.order = order
        self.t = sp.Symbol("t")
        self.used_order = order
        self.IMO_le = lambda m1, m2 : IMO(m1, m2, self.used_order) 
        self.parameters = parameters
    
    
    def update_IMO(self, order):
        self.used_order = order
        self.IMO = lambda m1, m2 : IMO(m1, m2, self.used_order)
 

    def LM_LC(self, P:IntegralPolynomial) -> tuple[IM, sp.Expr]:
        """
        get leading monomials and coeff
        """
        L = P.get_content()
        LC, LM = L[0][1], L[0][0]
        for M,coeff in L:   
            #if True then M <= LM, else M > LM
            if self.IMO_le(M, LM) == False: 
                LM = M # im > LM
                LC = coeff
        return LM, LC
    
        
    def display_rules(self, sys):
        display(Math(r"\{")) 
        for eq in sys:
            LM, LC = self.LM_LC(eq)
            key = IntegralPolynomial(LC*LM)
            value = self.polynomials_subtraction(eq, key)
            value = self.product_P_Coeff(value,-1)
            arrow = r"{\Huge \color{red} \mathbf{\rightarrow}}"  
            key_repr = key.repr_display_math()
            value_repr = value.repr_display_math()
            export = Math(f"{key_repr} {arrow} {value_repr}") 
            display(export)
        display(Math(r"\}"))
         

    def normalize_LC_of_P(self, 
                        P: IntegralPolynomial) -> IntegralPolynomial:
        _, LC = self.LM_LC(P)
        normalized_P = {}
        for M, coeff in P.get_content():
            normalized_P[M] = coeff/LC
        # Since we only have division 
        # coeffs can't be zero  after 
        # a simplification process
        # then, using copy=True, we disable de simplification
        # to optimize the reduction process
        return IntegralPolynomial(normalized_P,copy=True), LC
    
    def monomials_product(self, M: IM, N: IM )-> IntegralPolynomial:
        e = M.get_nb_int()
        f = N.get_nb_int()
        m0n0 = M.get_content()[0]*N.get_content()[0]
        if e == f == 0:
            MN = IM(m0n0)
        elif e == 0 and f != 0:
            N1p = N.cut("1+").get_content() #N1plus
            MN = IM(m0n0,*N1p) 
        elif e != 0 and f== 0 :
            M1p = M.cut("1+").get_content() #N1plus
            MN = IM(m0n0,*M1p) 
        else:
            N1p = N.cut("1+").get_content() #N1plus
            M1p = M.cut("1+").get_content() #N1plus
            sh = ShuffleList(M1p,N1p)
            MN = sp.Add(*[IM(m0n0,*elem) for elem in sh]) 
        return IntegralPolynomial(MN)

    def fusion(self, M,N):
        """
        M = IM(x(t))
        N = IM(1,y(t),z(t)) 
        order = [x(t),y(t),z]
        return IM(x(t),y(t),z(t)) 
        """
        L1 = M.get_content()
        L2 = N.get_content()
        res = [L1[0]*L2[0]]
        i, j = 1, 1
        while i!=len(L1) and j!=len(L2): 
            #L1_i <= L2_j
            if self.IMO_le(IM(L1[i]), IM(L2[j])): 
                res += [L1[i]]
                i += 1
            else:
                res += [L2[j]]
                j += 1
        if i<len(L1):
            res += [*L1[i:]]
        else:
            res += [*L2[j:]]
        return IM(*res) 

    def anti_fusion(self,M,N):
        """
        find an integral monomial M2 such that lm(N \cdot N2) = M
        """
        if N.get_nb_int() > M.get_nb_int():
            return None
        if not self.IMO_le(N,M):
            return None
        M_c = M.get_content()
        N_c = N.get_content()
        if M_c[0] == N_c[0] == 1:
            N2_0 = 1
        else:
            q, r = sp.div(M_c[0],N_c[0])
            if r != 0: return None
            N2_0 = q 
        diff = diff_lists(M_c[1:],N_c[1:])
        N2 = IM(*[N2_0, *diff])
        #now that we have a candidate for N2, we need to 
        #check that lm(N \cdot N2) = M
        N_dot_N2 = self.monomials_product(N,N2)
        LM_N_dot_N2, _ = self.LM_LC(N_dot_N2)
        if LM_N_dot_N2 == M:
            return N2
        else:
            return None 
    
    def product_P_Coeff(self, 
                        P: IntegralPolynomial, 
                        alpha: sp.Expr) -> IntegralPolynomial:
        """
        alpha is cst 
        """
        alpha_P = {} 
        for M, c in P.get_content():
            alpha_P[M] = c*alpha
        return IntegralPolynomial(alpha_P)
        
    def polynomials_add(self, 
                        P: IntegralPolynomial, 
                        Q: IntegralPolynomial) -> IntegralPolynomial: 
        PplusQ = dict(P.get_content())
        for N,c_N in Q.get_content(): 
            if N not in PplusQ:
                PplusQ[N] = c_N
            else:
                PplusQ[N] += c_N
        PplusQ = {M:coeff for M, coeff in PplusQ.items() if coeff != 0}
        return IntegralPolynomial(PplusQ)
    
    def polynomials_subtraction(self, 
                                P: IntegralPolynomial, 
                                Q: IntegralPolynomial) -> IntegralPolynomial: 
        PminusQ = dict(P.get_content())
        for N,c_N in Q.get_content(): 
            if N not in PminusQ:
                PminusQ[N] = -c_N
            else:
                PminusQ[N] -= c_N
        PminusQ = {M:coeff for M, coeff in PminusQ.items() if coeff != 0}
        return IntegralPolynomial(PminusQ)
    
    def polynomials_product(self,
                            P: IntegralPolynomial,
                            Q: IntegralPolynomial) -> IntegralPolynomial: 
        PQ = IntegralPolynomial(0)
        for M_P, c_P in P.get_content():
            for M_Q, c_Q in Q.get_content(): 
                M_PdotM_Q = self.monomials_product(M_P,M_Q)
                c_P_c_Q_M_PdotM_Q = self.product_P_Coeff(M_PdotM_Q, c_P*c_Q)
                PQ = self.polynomials_add(PQ, c_P_c_Q_M_PdotM_Q)
        return PQ 
    
    def integrate_monomial(self, M: IM):
        return IM(1,*M.get_content())

    def integrate_polynomial(self, 
                             P: IntegralPolynomial) -> IntegralPolynomial:
        Int_P = {}
        for M, coeff in P.get_content():
            Int_M = self.integrate_monomial(M)
            Int_P[Int_M] = coeff
        return IntegralPolynomial(Int_P)
 
    def add_prefix_to_polynomial(self, 
                                prefix: IM, 
                                P: IntegralPolynomial) -> IntegralPolynomial:
        new_P = {} 
        for M, coeff in P.get_content():
            pref_M = M.add_prefix(prefix)
            new_P[pref_M] = coeff
        return IntegralPolynomial(new_P)

    def reduced_product(self, 
                        P:IntegralPolynomial, 
                        M:IM) -> IntegralPolynomial:
        """
        see section 3.1  
        if |M| = 0 or LM(P)=LM(P_N)
        reduced_product = P \cdot M
        else:
        reduced_product = (P \cdot M) - \int (M]1+] \cdot P)
        """ 
        LM_P,_ = self.LM_LC(P)
        P_N = P.get_P_N()
        if P_N.is_zero():
            LM_P_N = 0
        else:
            LM_P_N,_ = self.LM_LC(P_N)

        if (M.get_nb_int() == 0) or (LM_P == LM_P_N):
            M = IntegralPolynomial(M)
            reduced_product = self.polynomials_product(P,M) 
        else:
            M1p = IntegralPolynomial(M.cut("1+"))
            M = IntegralPolynomial(M)
            #(P \cdot M)
            PdotM = self.polynomials_product(P,M) 
            
            #\int (M]1+] \cdot P)
            IntMdotP = self.integrate_polynomial(
                            self.polynomials_product(M1p,P)
                        ) 

            reduced_product = self.polynomials_add(
                                PdotM ,self.product_P_Coeff(IntMdotP, -1)
                            )
        return reduced_product
        
    def polynomial_power(self, 
                        P:IntegralPolynomial,
                        n:int) -> IntegralPolynomial:
        assert is_int(n) 
        assert isinstance(P,IntegralPolynomial)
        if n == 0: return IntegralPolynomial(IM(1))
        P_pow_n = P
        for _ in range(n-1):
            P_pow_n = self.polynomials_product(P_pow_n,P)
        return P_pow_n
    
    def reduced_power(self, 
                      P:IntegralPolynomial, 
                      n:int) -> IntegralPolynomial:
        """
        see section 3.2  

        P^{\circled{n}} = n (\int (P_I[cut{1+}] cdot P_N^{n-1})) + P_N^n
        """
        assert is_int(n) and n >= 1 
        P_I = P.get_P_I()
        P_N = P.get_P_N() 
        P_I_1plus = P_I.cut_P("1+") 
        P_N_pow_n_minus_one = self.polynomial_power(P_N, n-1)
        P_N_pow_n = self.polynomials_product(P_N_pow_n_minus_one, P_N)
        
        #lets compute n (\int (P_I[cut{1+}] cdot P_N^{n-1})) in temp
        temp = self.integrate_polynomial(
                    self.polynomials_product(P_I_1plus, P_N_pow_n_minus_one)
                )
        temp = self.product_P_Coeff(temp, n)

        reduced_power = self.polynomials_add(temp, P_N_pow_n)
        return reduced_power
    
    def reduction_M_by_P_simple_case(self,
                                    M: IM, 
                                    P: IntegralPolynomial
                                    ) -> IntegralPolynomial:
        return reduction_M_by_P_simple_case(self, M, P)
    
    def reduction_M_by_P_reduced_power(self,
                                       M: IM, 
                                       P: IntegralPolynomial
                                       ) -> IntegralPolynomial:
        return reduction_M_by_P_reduced_power(self, M, P)
    
    def reduction_M_by_P(self,
                         M: IM, 
                         P: IntegralPolynomial
                        ) -> IntegralPolynomial:
        return reduction_M_by_P(self,M,P)
    
    def reduce(self, 
                Q: IntegralPolynomial, 
                T: OrderedSet[IntegralPolynomial]
            ) -> IntegralPolynomial:
        return reduce(self,Q,T)
    
    def auto_reduce(self,  
                    T:OrderedSet[IntegralPolynomial]
                ) -> OrderedSet[IntegralPolynomial]:
        return auto_reduce(self,T)
    
    def critical_pairs_PI_QI(self,
                            P: IntegralPolynomial,
                            Q: IntegralPolynomial) -> IntegralPolynomial:
        return critical_pairs_PI_QI(self,P,Q)
    
    def critical_pairs_PI_QN(self,
                            P: IntegralPolynomial,
                            Q: IntegralPolynomial) -> IntegralPolynomial:
        return critical_pairs_PI_QN(self,P,Q)
    
    def critical_pairs_PN_QN(self,
                            P: IntegralPolynomial,
                            Q: IntegralPolynomial) -> IntegralPolynomial:
        return critical_pairs_PN_QN(self,P,Q)
    
    def critical_pairs(self,
                       R: OrderedSet[IntegralPolynomial]
                    ) -> OrderedSet [IntegralPolynomial]:
        return critical_pairs(self,R)
    
    def find_A_A0_G_F(self, 
                      P:IntegralPolynomial
                      ) -> tuple[IntegralPolynomial]:
        return find_A_A0_G_F(self,P)
    
    def update_exp(self, 
                T_prime: OrderedSet[IntegralPolynomial],
                E: OrderedSet[sp.Function, sp.Function, IntegralPolynomial]
                ) -> tuple:
        return update_exp(self,T_prime,E)
    
    def extend_X_with_exp(self,
                      E: set[sp.Function, sp.Function, IntegralPolynomial]
                      ) -> list:
        return extend_X_with_exp(self, E)
    
    def integral_elimination(self,
                            F: OrderedSet[IntegralPolynomial],
                            disable_exp: bool = False,
                            disable_critical_pairs: bool = False,
                            nb_iter: int = 0) -> tuple:
        return integral_elimination(self, 
                                F, 
                                disable_exp=disable_exp,
                                disable_critical_pairs=disable_critical_pairs,
                                nb_iter=nb_iter)