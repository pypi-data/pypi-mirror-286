import sympy as sp
import numpy as np

def is_float(expr):
    try:
        float(expr)
        return True
    except:
        return False

def is_int(expr):
    try:
        f = float(expr) 
        return f.is_integer()
    except:
        return False

def has_add_in_list(l):  
    for e in l:
        if not is_float(e) or not is_int(e):
            if e.has(sp.Add):
                return True
    return False
 

def expr_has_symbol(expr, symbol): 
    try: 
        return expr.has(symbol)
    except:
        return False


def expr_has_symbols(expr, symbols): 
    has_symbols = False
    for symbol in symbols:
        has_symbols = has_symbols or expr_has_symbol(expr,symbol)
    return has_symbols
 


def ShuffleList(l1, l2):
    """
    shuffle two lists
    u1.u >< v1.v = u1.(u >< v1.v) + v1.(u1.u >< v)
    with >< the shuffle operation
     
    return [u1, u2, ..., un] such that l1 >< l2 = u1 + u2 + ... + un,
    """
    res = []
    if len(l1) == 0:
        res = [l2]
    elif len(l2) == 0 :
        res = [l1]
    else:
        sh1 = ShuffleList(l1[1:], l2) # (u >< v1.v)
        sh2 = ShuffleList(l1, l2[1:]) # (u1.u >< v)
        for l in sh1:
            res = [*res, [l1[0], *l]] # u1.(u >< v1.v)
                
        for l in sh2:
            res = [*res, [l2[0], *l]] # v1.(u1.u >< v)
    return res


def diff_lists(L1,L2):
    """
    example:
    L1 = [x(t),y(t),z(t),a(t),b(t),c(t),x(t),z(t),b(t),y(t)]
    L2 = [a(t),x(t),y(t)]
    return [x(t), y(t), z(t), b(t), c(t), z(t), b(t)]

    """
    i=0
    j=0
    diff = []
    while i < len(L1) and j < len(L2): 
        m=L1[i] 
        if m == L2[j]:
            j+=1
        else:
            diff+=[m]
        i+=1 
    if j < len(L2):
        return []
    if i <  len(L1):
        diff += [*L1[i:]]
    return diff