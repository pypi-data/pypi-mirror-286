
import math
import copy
import re


from itertools import permutations, chain
from math import factorial 
from collections import Counter
from itertools import product

def nStirling2(n, k):
    if n < 0:
        raise ValueError("n < 0")
    if k < 0:
        raise ValueError("k < 0")
    if k > n:
        raise ValueError("k > n")
    
    m = 0
    for j in range(k + 1):
        m += (-1) ** (k - j) * factorial(k) // (factorial(j) * factorial(k - j)) * (j ** n)
    
    return m // factorial(k)

def ff(n, k):
    if k is None:
        raise ValueError("Argument 'k' must be provided")
    if k > n:
        raise ValueError("k > n")
    if n < 0:
        raise ValueError("n < 0")
    
    nff = 1
    for i in range(k):
        nff *= (n - i)
    
    return nff

def m2Set(v=[0]):
    if v is None:
        v = [[]]
    
    nv = []
    for item in v:
        for sublist in item[0]:
            if sublist not in nv:
                nv.append(sublist)
    
    return nv


def mCoeff(v=None, L=None):
    if v is None:
        raise ValueError("Le premier paramètre est manquant")
    if L is None:
        raise ValueError("Le deuxième paramètre est manquant")

    def is_equal(v1, v2):
        """Check if two values or lists are equal, handling nested lists."""
        if isinstance(v1, list) and isinstance(v2, list):
            if all(isinstance(item, int) for item in v1) and all(isinstance(item, int) for item in v2):
                # Both v1 and v2 are lists of integers, no need to check permutations
                return v1 == v2
            else:
                if len(v1) != len(v2):
                    return False
                
                # Check all permutations of v1 against v2
                for perm in permutations(v1):
                    if all(is_equal(perm[i], v2[i]) for i in range(len(v1))):
                        return True
                return False
        
        return v1 == v2

    for u in L:
        if is_equal(v, u[0]):
            return u[1]

    return 0
def nPerm(L=[]):
    def insc(pv, c):
        U = []
        for v in pv:
            for i in range(len(v) + 1):
                new_perm = v[:i] + [c] + v[i:]
                if new_perm not in U:
                    U.append(new_perm)
        return U

    if not L:
        raise ValueError("The vector/list is empty")
    
    if len(L) == 1:
        return [L]
    
    if L[0] == L[1]:
        u = [[L[0], L[1]]]
    else:
        u = [[L[0], L[1]], [L[1], L[0]]]
    
    if len(L) == 2:
        return u
    
    for i in range(2, len(L)):
        u = insc(u, L[i])
    
    return u

def powS(vn=None, lvd=None):
    if vn is None:
        raise ValueError("Le premier paramètre est manquant")
    if lvd is None:
        raise ValueError("Le deuxième paramètre est manquant")
    
    # Si vn est un entier, le transformer en une liste contenant cet entier
    if isinstance(vn, int):
        vn = [vn]
    
    # Si lvd est une liste de valeurs, le transformer en une liste de listes
    if not isinstance(lvd[0], list):
        lvd = [[val] for val in lvd]
    
    for i in range(len(vn)):
        if vn[i] < 0:
            raise ValueError("Les valeurs du premier paramètre ne peuvent pas être négatives")
    for i in range(len(lvd)):
        if len(vn) != len(lvd[i]):
            raise ValueError("Tous les vecteurs de la liste doivent avoir la même taille que le premier paramètre")
    
    n = 0
    for i in range(len(lvd)):
        p = 1
        for j in range(len(vn)):
            p *= lvd[i][j] ** vn[j]
        n += p
    
    return n

def pPoly(L=None):
    if L is None:
        raise ValueError("The parameter is missing")
    
    nL = len(L)
    if nL == 1:
        return L[0]
    
    vdim = sum(len(poly) for poly in L)
    uv = [0] * vdim
    u = L[0]
    
    for k in range(1, nL):
        v = L[k]
        for i in range(len(u)):
            for j in range(len(v)):
                uv[i + j] += u[i] * v[j]
        u = [coef for coef in uv if coef != 0]
        uv = [0] * vdim
    
    return [0] * (vdim - len(u)) + u

def Set2expr(v=None):
    if v is None:
        raise ValueError("The parameter is missing")

    u = []
    U = []
    nv = len(v)
    
    def python_format(v):
        formatted_list = []
        
        for sublist in v:
            formatted_sublist = []
            for item in sublist:
                # Convert '^' to '**' in string elements
                formatted_item = [s.replace('^', '**') if isinstance(s, str) else s for s in item]
                formatted_sublist.append(formatted_item)
            formatted_list.append(formatted_sublist)
        
        return formatted_list
    
    def remove_brackets(s):
        
        if not 'g' in s:
            return s
        
        res = []
        skip = False
        i = 0
        
        while i < len(s):
            if s[i] != ')' and not skip:
                res.append(s[i])
            
            elif s[i] == ')':
                res.append(s[i])
                j = i + 1
                while j < len(s) and s[j] != 'g' and s[j] != '+' and s[j] != '(':
                    j += 1
                i = j - 1  # Move i to the last character inside the skip range
            
            i += 1
        
        return ''.join(res)
    
    # Grouping terms based on the first element
    for i in range(1, nv):
        u.append(v[i - 1])
        if v[i][0] != v[i - 1][0]:
            U.append(u)
            u = []
    u.append(v[nv - 1])
    U.append(u)
    U = python_format(U)
    S = []
    for m in U:
        lm = len(m)
        # Sorting terms within each group
        for i in range(lm - 1):
            for j in range(i + 1, lm):
                if m[i][2] == m[j][2] and m[i][3] > m[j][3]:
                    app_m = m[i]
                    m[i] = m[j]
                    m[j] = app_m
        # Constructing the coefficient part of the expression
        c = "1"
        for i in range(lm):
            c = f"{c}*{m[i][1]}"
            m[i][1] = 1
        c = str(eval(c))
        # Constructing the variable part of the expression
        s = ""
        for i in range(lm - 1):
            k = int(m[i][4])
            for j in range(i + 1, lm):
                if m[i][2] == m[j][2] and m[i][3] == m[j][3] and m[j][2] != "":
                    k += int(m[j][4])
                    m[j][2] = ""
            s = f"{s}{m[i][2]}{'[' + m[i][3] + ']' if m[i][3] != '' else ''}{'^' + str(k) if k > 1 else ''}"
        if m[lm - 1][2] != "":
            k = int(m[lm - 1][4])
            s = f"{s}{m[lm - 1][2]}{'[' + m[lm - 1][3] + ']' if m[lm - 1][3] != '' else ''}{'^' + str(k) if k > 1 else ''}"
        S.append([c, s])

    V = ""
    if len(S) > 1:
        for i in range(len(S)-1):
            if S[i][1] != "":
                c = S[i][0]
                for j in range(i + 1, len(S)):
                    if S[i][1] == S[j][1] and S[j][1] != "":
                        c = f"{c}+{S[j][0]}"
                        S[j][1] = ""
                c = str(eval(c))
                signc = " + " if float(c) > 0 else " - "
                c = str(int(float(c)))
                c = "" if abs(int(c)) == 1 else abs(int(c))
                if c != "":
                    if int(c) != 0:
                        V = f"{V}{signc}{c}{S[i][1]}"
                else:
                    V = f"{V}{signc}{c}{S[i][1]}"
    i = len(S) - 1
    c = S[i][0]
    c = str(eval(c))
    signc = " + " if float(c) > 0 else " - "
    c = "" if abs(float(c)) == 1 else abs(float(c))
    if c != "":
        if float(c) != 0 and S[i][1] != "":
            V = f"{V}{signc}{c}{S[i][1]}"
    else:
        V = f"{V}{signc}{c}{S[i][1]}"

    if V.startswith(" + "):
        V = V[3:]
    
    V = remove_brackets(V)
    
    return V

def mpCart(m1=None, m2=None):
    if m1 is None:
        raise ValueError("The first parameter is missing")
    if m2 is None:
        raise ValueError("The second parameter is missing")
        
    M12 = []
    M1 = copy.deepcopy(m1)
    M2 = copy.deepcopy(m2)
    verif1 = False
    verif2 = False
    
    if len(m1) == 1:
        M1 = copy.deepcopy(m1[0])
    if len(m2) == 1:
        M2 = copy.deepcopy(m2[0])
        
    if isinstance(M1[1], int):
        verif1 = True
    if isinstance(M2[1], int):
        verif2 = True

    if verif1 and verif2:
        if len(M1) == len(M2):
            combined_list = copy.deepcopy(M1[0])
            combined_list.extend(M2[0])
            M12 = [[combined_list, M1[1] * M2[1]]]
    
    elif verif1 or verif2:
        if verif2:
            M12 = []
            for i in range(len(M1)):
                combined_list = copy.deepcopy(M1[i][0])
                combined_list.extend(M2[0])
                M12.append([combined_list, M1[i][1] * M2[1]])
                
        if verif1:
            M12 = []
            for i in range(len(M2)):
                combined_list = copy.deepcopy(M2[i][0])
                combined_list.extend(M1[0])
                M12.append([combined_list, M2[i][1] * M1[1]])
                
    else:
        for i in range(len(M1)):
            for j in range(len(M2)):
                combined_list = copy.deepcopy(M1[i][0]) + copy.deepcopy(M2[j][0])
                combined_product = M1[i][1] * M2[j][1]
                M12.append([combined_list, combined_product])
    
    return M12

def pCart(L):
    
    def pCartAB(v1, v2):
        v12 = []
        p12 = 0
        for i in range(len(v1)):
            for j in range(len(v2)):
                p12 += 1
                if isinstance(v1[i], list):
                    if isinstance(v1[i][0], list):
                        new_list = []
                        for k in range(len(v1[i])):
                            new_list.append(v1[i][k])
                        if isinstance(v2[j], int):
                            new_list.append([v2[j]])
                        else:
                            new_list.append(v2[j])
                        v12.append(new_list)
                    else:
                        v12.append([v1[i], v2[j]])
                else :
                    v12.append([v1[i], v2[j]])
        return v12
    
    if len(L) == 1:
        return L
    
    vL = pCartAB(L[0], L[1])
    if len(L) < 3:
        return vL
    
    for i in range(2, len(L)):
        vL = pCartAB(vL, L[i])    
    return vL

def list2Set(v=[0]):
    nv = [v[0]]
    
    if len(v) > 1:
        for i in range(1, len(v)):
            if v[i] not in nv:
                nv.append(v[i])
                
    return nv

def list2m(v=[0]):
    v_set = []
    nv = []
    
    for value in v:
        if isinstance(value, list):
            if value not in v_set:
                v_set.append(value)
        else:
            if [value] not in v_set:
                v_set.append([value])
    
    for i in range(len(v_set)):
        k = 0
        if isinstance(value, list):
            for j in range(len(v)):
                if v_set[i] == v[j]:
                    k += 1
        else:
            for j in range(len(v)):
                if v_set[i] == [v[j]]:
                    k += 1
        
        nv.append([v_set[i], k])
    
    return nv

def countP(v):
    
    if isinstance(v, int):
        v = [v]
    if not all(isinstance(i, (int, list)) for i in v):
        raise ValueError("All elements of the input list must be either integers or lists")

    for i in v:
        if isinstance(i, int) and i < 0:
            raise ValueError("The values cannot be negative")
        if isinstance(i, list):
            for j in i:
                if j < 0:
                    raise ValueError("The values cannot be negative")
    np = 1
    
    if isinstance(v[0], list):
        n = 1
        u = []
        for j in range(len(v[0])):
            s = 0
            p = 1
            for i in range(len(v)):
                m = v[i][j]
                u.append(m)
                p *= math.factorial(m)
                s += m
            n *= math.factorial(s) / p
    else:
        p = 1
        for x in v:
            p *= math.factorial(x)
        n = math.factorial(sum(v)) / p
    
    u = list2m(v)
    
    for i in range(len(u)):
        np *= math.factorial(u[i][1])
    
    return int(n / np)


def intPart(n=0, vOutput = False):
    if n < 1:
        raise ValueError("n must be > 0")
    
    def f_intPart(n1, n2):
        if n1 == 0:
            return []
        if n2 == 1:
            return [[1] * n1]
        
        vP = []
        for i in range(1, n2 + 1):
            v = f_intPart(n1 - i, min(n1 - i, i))
            
            if not v:
                v = [[n1]]
            else:
                v = [item + [i] for item in v]
            
            vP.extend(v)
        
        return vP
    
    u = f_intPart(n, n)
    
    if not vOutput:
        return u
    
    for m in u:
        print(m)

def mkmSet(vPar=None, vOutput=False):
    
    if vPar is None:
        raise ValueError("The first parameter is missing")
    for v in vPar:
        if v < 0:
            raise ValueError("Values cannot be negative")   
    
    def URv(Mp, n): 
        Mr = []
        

        if isinstance(Mp[0], list):
            L = len(Mp[0])
        else:
            L = len(Mp)
        

        for i in range(len(Mp) - 1, -1, -1):
            if n <= (Mp[i][L - 1] if isinstance(Mp[i], list) else Mp[i]):
                break
        ptr = i
        
        ou = [-1]
        
        for i in range(ptr, len(Mp)):
            condition_ou = Mp[i][:L - 1] if isinstance(Mp[i], list) else []
            if ou != condition_ou and n > (Mp[i][L - 1] if isinstance(Mp[i], list) else Mp[i]) and (Mp[i][L - 1] if isinstance(Mp[i], list) else Mp[i]) == 0:
                Ms = copy.deepcopy(Mp)
                if isinstance(Mp[i], list):
                    Ms[i][L - 1] = n
                else:
                    Ms[i] = n
                ou = Ms[i][:L - 1] if isinstance(Ms[i], list) else []
                Mr.append(Ms)
        
        if n == 0:
            Mr.append(copy.deepcopy(Mp))
        else:
            if isinstance(Mp[0], list):
                new_element = [0] * (L - 1) + [n]
            else:
                new_element = n
            new_Mp = copy.deepcopy(Mp)
            if isinstance(Mp[0], list):
                new_Mp.append(new_element)
            else:
                new_Mp = new_Mp + [new_element]
            Mr.append(new_Mp)
        
        return Mr


    def URV(M1, M2):
        Mr = []
        M = [copy.deepcopy(M1)]
        for i in range(len(M2)):
            for j in range(len(M)):
                Mr.extend(URv(M[j], M2[i]))
            M = Mr
            Mr = []
        return M

    def aDim(M):
        Mr = []
        for i in range(len(M)):
            if isinstance(M[i], list):
                if len(M[i]) == 0:
                    Mr.append([[], 0])
                else:
                    Mr.append(M[i] + [0])
            else:
                Mr.append([M[i], 0])
        return Mr
            
    v = vPar
    U = []
    
    if sum(v) == 0:
        return [0]
    if len(v) == 1:
        s = sum(v)
        u = intPart(s)
        for i in range(len(u)):
            U.append([u[i], countP(u[i])])
        u = U       
    else:
        vHead = []
        for i in range(len(v)):
            if v[i] == 0:
                vHead.append(0)
            else:
                v = v[i:]
                break

        if len(v) == 1:
            s = sum(v)
            u = intPart(s)
            U = []
            for i in range(len(u)):
                u1 = []
                for j in range(len(u[i])):
                    u1.append(vHead+[u[i][j]])
                U.append([u1, countP(u[i])])
            return U
        
        s1 = v[0]
        u1 = intPart(s1)

        for ik in range(1, len(v)):
            s2 = v[ik]
            if s2 == 0:
                u2 = [0]
            else:
                u2 = intPart(s2)
            u = []
            
            for i in range(len(u1)):
                u.append(aDim(u1[i]))
                
            U = []
            
            for i in range(len(u)):
                for j in range(len(u2)):
                    
                    if isinstance(u2[j], list):
                        
                        for ui in URV(u[i], u2[j]):
                            U.append(ui)
                            
                    else :
                        
                        for  ui in URV(u[i],[u2[j]]):
                            U.append(ui)
                            
            u1 = U

        u = []
        for i in range(len(U)):
            u.append([U[i], countP(U[i])])
            #u += [U[i] + [countP(U[i])]]

        if len(vHead) > 0:
            for i in range(len(u)):
                for j in range(len(u[i][0])):
                    u[i][0][j] = vHead + u[i][0][j]
        for i in range(len(u)):
            if len(u[i][0]) > 1:
                for j1 in range(len(u[i][0])-1):
                    for j2 in range(j1+1, len(u[i][0])):
                        if u[i][0][j1] > u[i][0][j2]:
                            cTMP = u[i][0][j2]
                            u[i][0][j2] = u[i][0][j1]
                            u[i][0][j1] = cTMP
                            
        if len(u) > 1:
            for i in range(len(u)-1):
                for j in range(i+1, len(u)):
                    if u[i] > u[j]:
                        cTMP = u[i]
                        u[i] = u[j]
                        u[j] = cTMP
                        

    if not vOutput:
        return u

    for mm in u:
        print("[", end="")
        for i, m in enumerate(mm[0]):
            if i != 0:
                print(" ", end="")
            print("(", end="")
            if isinstance(m, list):
                for j, val in enumerate(m):
                    if j != 0:
                        print(" ", end="")
                    print(val, end="")
            else:
                print(m, end="")
            print(")", end="")
        print(f", {mm[1]} ]")
    print("\r\n")   

def nKM(v=None, V=None):
    if v is None:
        raise ValueError("The first parameter is missing")
    if V is None:
        raise ValueError("The second parameter is missing")
    if sum(v) > len(V):
        raise ValueError("The database must contain more data")
    if any(i < 0 for i in v):
        raise ValueError("The values cannot be negative")
    if any(len(V[i]) != len(V[0]) for i in range(1, len(V))):
        raise ValueError("The arrays in the data set must have the same length")
    if len(v) != len(V[0]):
        raise ValueError("The first parameter and the arrays in the data set must have the same length")

    N = len(V)
    n = sum(v)
    vTabS = mkmSet(v)
    vTabK = []
    k = 0
    for u1 in vTabS:
        k += 1
        app = [sum(u2) for u2 in u1[0]]
        vTabK.append([app, u1[1]])

    vx = [(-1)**(i - 1) * factorial(i - 1) / ff(N, i) for i in range(1, n + 1)]
    vk = []
    for i in range(1, n + 1):
        u = [nStirling2(i, j) * (-1)**(j - 1) * factorial(j - 1) for j in range(1, i + 1)]
        vk.append(u)

    vS = []
    k = 0
    for u in m2Set(vTabS):
        k += 1
        vS.append([u, powS(u, V)])

    s = 0
    for j in range(len(vTabK)):
        u = vTabK[j]
        pk = []
        for i in range(len(u[0])):
            pk.append(vk[u[0][i]-1])
        vm = pPoly(pk)
        evm = 0
        for i in range(len(vm)):
            evm += vx[i] * vm[i] * u[1]
        
        pS = 1
        for s1 in vTabS[j][0]:
            pS *= mCoeff(s1, vS)
        
        s = s + pS * evm


    return s
def nKS(v=None, V=None):
    
    if v is None:
        raise ValueError("The first parameter is missing")
    if V is None:
        raise ValueError("The second parameter is missing")
    if isinstance(v, int):
        v = [v]
    if sum(v) > len(V):
        raise ValueError("The database must contain more data")
    if any(i < 0 for i in v):
        raise ValueError("The values cannot be negative")
    if not all(isinstance(item, list) for item in V):
        V = [[item] for item in V]
    if any(len(V[i]) != len(V[0]) for i in range(1, len(V))):
        raise ValueError("The arrays in the data set must have the same length")
    if len(v) > 1:
        raise ValueError("The first parameter must be an integer or a single-element array")
        
    N = len(V)
    n = sum(v)
    vTab = mkmSet(v)
    vx = []
    for i in range(1, n + 1):
        vx.append((-1) ** (i - 1) * factorial(i - 1) / ff(N, i))
    vk = []
    for i in range(1, n + 1):
        u = []
        for j in range(1, i + 1):
            u.append(nStirling2(i, j) * (-1) ** (j - 1) * factorial(j - 1))
        vk.append(u)
    vS = []
    for i in range(1, n + 1):
        vS.append(powS(i, V))
    s = 0
    for u in vTab:
        pk = []
        for i in range(1, len(u[0]) + 1):
            pk.append(vk[u[0][i - 1]-1])
        vm = pPoly(pk)
        evm = 0
        for i in range(1, len(vm)+1):
            evm += vx[i - 1] * vm[i - 1] * u[1]
        pS = 1
        for s1 in u[0]:
            pS *= vS[s1 - 1]
        s += pS * evm
    
    return s

def nPM(v=None, V=None):
    if v is None:
        raise ValueError("The first parameter is missing")
    if V is None:
        raise ValueError("The second parameter is missing")
    if not isinstance(v, list):
        raise ValueError("The first parameter must be a list")
    if not isinstance(V, list):
        raise ValueError("The second parameter must be a list")
    if len(v[0]) != len(V[0]):
        raise ValueError("The dimension of the polykay indexes and the number of the columns of the data must be equal")
    if sum(sum(i) for i in v) > len(V):
        raise ValueError("The database must contain more data")
    for i in v:
        if any(x < 0 for x in i):
            raise ValueError("The values cannot be negative")
    if any(len(V[i]) != len(V[0]) for i in range(1, len(V))):
        raise ValueError("The arrays in the data set must have the same length")
    if any(len(v[i]) != len(v[0]) for i in range(1, len(v))):
        raise ValueError("The arrays in the first parameter must have the same length")
    
    def ricalcMF(M):
        appM = M[:]
        for i in range(len(appM)):
            appM[i][1] = appM[i][1] * (-1) ** (len(appM[i][0]) - 1) * factorial(len(appM[i][0]) - 1)
        return appM

    def umSet(pM=None):
        if pM is None:
            raise ValueError("The parameter is missing")

        M = pM.copy()

        for i in range(len(M) - 1):
            for j in range(i + 1, len(M)):
                if M[i][0] == M[j][0] and len(M[i][0]) == len(M[j][0]):
                    M[i][1] += M[j][1]
                    M[j][1] = 0

        oM = []
        for item in M:
            if item[0][1] != 0:
                oM.append(item)

        return oM
        
    #npk = 0
    NN = len(V)
    u = [len([x for x in v_elem if x > 0]) for v_elem in v]
    #M = max(u)
    u = [sum(v_elem[i] for v_elem in v) for i in range(len(v[0]))]
    vTab = mkmSet(u)
    #N = sum(sum(v_elem) for v_elem in v)
    vS = [[x, powS(x, V)] for x in m2Set(vTab)]
    vTabS = copy.deepcopy(vTab)

    for i in range(len(vTab)):
        pS = 1
        for m in vTabS[i][0]:
            pS *= mCoeff(m, vS)

        vTabS[i][1] *= pS
        
    vk_ptr = [vS[i][0] for i in range(len(vS))]
    
    
    U = [[m, ricalcMF(mkmSet(m))] for m in vk_ptr]

    u = ricalcMF(mkmSet(v[0]))
    for i in range(1, len(v)):
        u = mpCart(u, ricalcMF(mkmSet(v[i])))
    
    u = umSet(u)
    
    for i in range(len(u)):
        #wrap_u = [[x] for x in u[i][0]]
        u[i][1] /= mCoeff(u[i][0], vTab) 
        u[i][1] /= ff(NN, len(u[i][0]))
    s = 0
    Ue = []
    for m in vTabS:
        p = m[1]

        if len(m[0]) == 1:
            Ue = mCoeff(m[0][0], U)
        else:
            m1 = mCoeff(m[0][0], U)
            m2 = mCoeff(m[0][1], U)
            if m1 and m2:
                Ue = mpCart(m1, m2)
                for i in range(2, len(m[0])):
                    Ue = mpCart(Ue, mCoeff(m[0][i], U))
                              
        for i in range(len(Ue)):
            Ue[i][1] *= p
        sUe = 0
        for m1 in Ue:
            #wrapped_m1 = [[x] for x in m1[0]]
            sUe += mCoeff(m1[0], u) * m1[1]
        s += sUe
    
    return s

def mkT(v=[], n=0, vOutput=False):
    if len(v) == 0:
        raise ValueError("The first parameter is empty")
    if n == 0:
        raise ValueError("The second parameter must be a positive integer")
    
    u = []
    m = mkmSet(v)
    
    for i in range(len(m)):
        lm = len(m[i][0])
        
        if lm == 1 and isinstance(m[i][0][0], int):  # Handle the case where m[i][0] is a single integer
            m_elem = m[i][0][0]
            if n == 1:
                u.append([[m_elem]])
            else:
                u.append([[m_elem]] + [[0] * len(v)] * (n - 1))
        
        elif (lm - n) == 0:
            u.append(m[i][0])
        
        elif lm < n:
            u.append(m[i][0] + [[0] * len(v)] * (n - lm))
    
    U = []
    for m_elem in u:
        if m_elem is not None:
            U.extend(nPerm(m_elem))
    U = list2Set(U)
    
    if not vOutput:
        return list2Set(U)
    
    for mm in U:
        print("[", end="")
        for m in mm:
            print("( ", end="")
            for elem in m:
                print(f"{elem} ", end="")
            print(")", end="")
        print("]")
        
def MFB(v=[], n=0):
    if len(v) < 1:
        raise ValueError("The first parameter must be a non-zero vector of integers")
    if n < 1:
        raise ValueError("The second parameter must be a positive integer")
    if any(m < 0 for m in v):
        raise ValueError("The first parameter cannot contain negative values")
        
    
    def um_MFB(v):
        s = 0
        for m in v:
            s += sum(m) if isinstance(m, list) else m

        if s == 0:
            return "1"

        s = ""
        mkm_set = mkmSet(v)  # Assuming mkmSet returns a similar structure as in R
        
        for m in mkm_set:
            if m[1] > 1:
                s += f"({m[1]})"
            
            s += f"f[{len(m[0])}]"
            
            for r in list2m(m[0]):
                if isinstance(r[0][0], list):
                    s += f"g{','.join(map(str, r[0]))}"
                
                if not isinstance(r[0][0], list):
                    s += f"g[{','.join(map(str, r[0]))}]"
                if r[1] > 1:
                    s += f"^{r[1]}"
            
            s += " + "

        return s[:-3]

    def gval(s, n0):
        v = list(s)
        ls = len(v)
        c_rest = ""
        n = 1
        i = 0
        nv = [0] * n0
        
        while i < ls:
            if v[i] == '(':
                i += 1
                c_word = ''
                while True:
                    c_word += v[i]
                    i += 1
                    if i >= ls or v[i] == ')':
                        break
                if c_word.isdigit():
                    n *= int(c_word)
                i += 1
            
            elif v[i] == 'f':
                i += 1
                c_word = ''
                while True:
                    c_word += v[i]
                    i += 1
                    if i >= ls or v[i] == '[':
                        break
                p = int(c_word) - 1 if c_word.isdigit() else 0  
                c_word = ""
                i += 1
                
                while True:
                    c_word += v[i]
                    i += 1
                    if i >= ls or v[i] == ']':
                        break
                if c_word:
                    try:
                        nv[p] = int(c_word)
                    except ValueError:
                        nv[p] = 0  
                i += 1
            
            else:
                c_rest += v[i]
                i += 1
        
        f_out = ""

        if f_out == "":
            f_out += 'f['
        for i in range(len(nv)-1):    
            m = str(nv[i])
            f_out += m
            f_out += ','
        f_out += str(nv[len(nv)-1])
        f_out += ']'
        
        return [str(n), f_out, c_rest]

    def gf(ps, n):
        s = gval(ps, n)
        if int(s[0]) > 1:
            return f"({s[0]}){s[1]}{s[2]}"
        else:
            return f"{s[1]}{s[2]}"
    
    def joint(v):
        if isinstance(v[0], int):
            v = [[elem] for elem in v]
        n = len(v)
        u = []
        p = 1

        for i in range(len(v[0])):
            a = 0
            for m in v:
                a += m[i]
            p *= factorial(a)

        for m in sum(v, []):
            p /= factorial(m)

        for i in range(len(v)):
            df = um_MFB(v[i])
            if df == '1':
                u.append([""])
            else:
                u.append([re.sub(r'f', f'f{i+1}', re.sub(r'g', f'g{i+1}', s)).replace(" ", "") for s in df.split("+")])
                
        u1 = []
        for i in range(len(u)):
            u2 = []
            for j in range(len(u[i])):
                u2.append([u[i][j].replace(" ", "")])
            u1.append(u2)
            
        u2 = pCart(u1)
        results = []
        
        for sublist1 in u2:
            concatenated_str = ''.join(''.join(sublist2) for sublist2 in sublist1)
            result = gf(f"{'(' + str(int(p)) + ')' if p > 1 else ''}{concatenated_str}", n)
            results.append(result)
        
        results = ' + '.join(results)
        
        return [results]
    
    if n == 1:
        u = um_MFB(v)
    else:
        u = []
        M = mkT(v, n)

        for i in range(len(M)):
            u.append([joint(M[i])])

        u = " + ".join(["".join(inner_list) for sublist in u for inner_list in sublist])
        
    u = u.strip()
    u = u.replace(")", "").replace("(", "")
    
    return u

def MFB2Set(sExpr=""):
    if len(sExpr) == 0:
        raise ValueError("The first parameter cannot be empty")
        
    def extract_number_from_brackets(s):
        """ Extracts a number from between brackets [ and ] """
        match = re.search(r'\[(.*?)\]', s)
        if match:
            return match.group(1)
        else:
            return None
    
    l_MFB = sExpr
    l_MFB = l_MFB.replace(" ", "")
    v_MFB = l_MFB.split('+')
    
    k = 0
    v = []
    
    for i in range(len(v_MFB)):
        u = v_MFB[i].split('g')
        u_f = u[0].split('f')
        k += 1

        elem = [str(i + 1)]

        num = extract_number_from_brackets(u_f[1])
               
        if u_f[0] != '':
            elem.append(str(u_f[0]))
        else:
            elem.append('1')  
            
        elem.extend(['f', num, '1'])
        
        elem = [re.sub(r'\[|\]', '', str(x)) for x in elem]

        
        v.append(elem)
        
        for j in range(1, len(u)):
            k += 1
            u_g = u[j].split('[')
            elem_g = [str(i + 1), '1', f'g{u_g[0]}']
            
            if '^' in u_g[1]:
                u_g_pow = u_g[1].split('^')
                elem_g.extend([re.sub(r'\]|\^', '', u_g_pow[0]), u_g_pow[1]])
            else:
                elem_g.extend([re.sub(r'\]', '', u_g[1]), '1'])
            
            elem_g = [re.sub(r'\[|\]', '', str(x)) for x in elem_g]
            v.append(elem_g)
    
    return v


def cum2mom(n=1):
    
    tmp = n
    if isinstance(n, int):
        tmp = [n]
    v = MFB(tmp, 1)  # Appel à la fonction MFB avec les paramètres n et 1
    v = MFB2Set(v)  # Conversion de v à l'aide de MFB2Set
    
    for j in range(len(v)):
        c = v[j][1]
        x = v[j][2]
        i = v[j][3]
        k = int(v[j][4])
        
        if x == "f":
            i = int(i)
            c = f"{c}*(-1)**({i - 1})*factorial({i - 1})"
            x = ""
            i = ""
        elif x == "g":
            x = "m"
        
        v[j][1] = c
        v[j][2] = x
        v[j][3] = i
        v[j][4] = k
        
    return Set2expr(v)

def mom2cum(n=1):
    
    tmp = n
    if isinstance(n, int):
        tmp = [n]
        
    v = MFB(tmp, 1)  # Appel à la fonction MFB pour obtenir v
    v = MFB2Set(v)  # Transformation de v en un format approprié

    
    for j in range(len(v)):
        if len(v[j]) >= 5:
            c = str(v[j][1])
            x = v[j][2]
            i = v[j][3]
            k = v[j][4]  # Conserver k en tant que chaîne, l'évaluation se fera dans Set2expr
            
            if x == "f":
                x = ""
                i = ""
            elif x == "g":
                x = "k"
            
            v[j][1] = c
            v[j][2] = x
            v[j][3] = i
            v[j][4] = k  # Ne convertir k qu'au moment de l'évaluation
    
    return Set2expr(v)

def pPart(n=0):
    
    if not isinstance(n, int) or n <= 0:
        raise ValueError("The first parameter must be a positive integer")
    tmp = n    
    if isinstance(n, int):
        tmp = [n]
        
    v = MFB(tmp, 1)  # Appel à la fonction MFB pour obtenir v
    v = MFB2Set(v)  # Transformation de v en un format approprié
    
    for j in range(len(v)):
        c = str(v[j][1])
        x = v[j][2]
        i = v[j][3]
        k = v[j][4]
        
        if x == "f":
            c = c + "/factorial(" + str(n) + ")"
            x = ""
            i = ""
        elif x == "g":
            c = c + "*(factorial(" + str(i) + ")^" + str(k) + "*factorial(" + str(k) + "))"
            x = "y"
            i = ""
        
        v[j][1] = c
        v[j][2] = x
        v[j][3] = i
        v[j][4] = k
    
    return Set2expr(v)

def gpPart(n=0):
    if not isinstance(n, int) or n <= 0:
        raise ValueError("The first parameter must be a positive integer")
    
    tmp = n
    
    if isinstance(n, int):
        tmp = [n]
    
    v = MFB(tmp, 1)  # Appel à la fonction MFB pour obtenir v
    v = MFB2Set(v)  # Transformation de v en un format approprié
    
    for j in range(len(v)):
        c = str(v[j][1])
        x = v[j][2]
        i = v[j][3]
        k = v[j][4]
        
        if x == "f":
            x = "a" + i
            i = ""
        elif x == "g":
            x = "(y" + i + ("^" + str(k) if int(k) > 1 else "") + ")"
            i = ""
            k = 1
        
        v[j][1] = c
        v[j][2] = x
        v[j][3] = i
        v[j][4] = k
        
    return Set2expr(v)

def GCBellPol(nv=[], m=1, b=False):
    v = MFB(nv, m)
    v = MFB2Set(v)
    
    for j in range(len(v)):
        c = str(v[j][1])
        x = v[j][2]
        i = v[j][3]
        k = int(v[j][4])
        
        if x == "f":
            vi = i.split(",")
            if len(vi) == 1:
                x = f"(y{'' if i == '1' else f'^{i}'}" + ")"  # Add closing parenthesis here
            else:
                x = ""
                for lvi in range(len(vi)):
                    if vi[lvi] != "0":
                        x += f"(y{lvi + 1}{'' if vi[lvi] == '1' else f'^{vi[lvi]}'}" + ")"
        
        elif m > 1 and b:
            x = "g"
        
        v[j][1] = c
        v[j][2] = x
        v[j][3] = i
        v[j][4] = k

    return Set2expr(v)

def eBellPol(n=1, m=0):
    
    tmp = n
    if isinstance(n, int):       
        tmp = [n]
    v = MFB(tmp, 1)
    v = MFB2Set(v)
    
    for j in range(len(v)):
        c = str(v[j][1])
        x = v[j][2]
        i = v[j][3]
        k = int(v[j][4])
        
        if x == "f":
            if m > 0 and str(i) != str(m):
                c = "0"
            x = ""
            i = ""
        elif x == "g":
            x = f"(y{i}{f'^{k}' if k > 1 else ''})"
            i = ""
            k = 1

        v[j][1] = c
        v[j][2] = x
        v[j][3] = i
        v[j][4] = k

    return Set2expr(v)

def e_eBellPol(n=1, m=0, v=None):

    if v is None:
        v = [1] * n
    if len(v) < n:
        raise ValueError(f"The length of the data vector is less than {n}")
    
    s = eBellPol(n, m)
    s = s.replace(" ", "")
    if s.startswith("("):
        s = "1" + s
    s = re.sub(r"\(", r"*", s) 
    s = re.sub(r"\)", r"", s) 
    for i in range(n, 0, -1):
        s = re.sub(f"y{i}", f"({v[i-1]})", s)
    
    s = re.sub(r" ", "", s)
    s = re.sub(r"\+\*", r"+", s)
    s = s.replace("^", "**")
    
    # Évaluer l'expression résultante
    try:
        result = eval(s)
    except Exception as e:
        raise ValueError(f"Error evaluating the expression: {s}\n{e}")
    
    return result

def e_GCBellPol(pv=[], pn=0, pyc=[], pc=[], b=False):

    l = len(pyc)

    if not pyc:
        pyc = None

    if len(pv) < 1:
        raise ValueError("The first parameter must be a non-zero vector of integers")
    if pn < 1:
        raise ValueError("The second parameter must be a positive integer")
    for m in pv:
        if m < 0:
            raise ValueError("The first parameter cannot contain negative values")

    if isinstance(pyc, str):
        if len(pc) != 0 or b:
            raise ValueError(pyc)

    vyc = []
    vc = []
    l_MFB = GCBellPol(pv, pn)
    l_MFB = l_MFB.replace("(", "").replace(")", "")
    l_MFB = l_MFB.replace("**", "^")
    v = list(l_MFB)
    ls = len(v)
    c_word = ""
    i = 0

    while i < ls:
        if v[i] == "g":
            i += 1
            c_word = "g"
            while True:
                c_word += v[i]
                if v[i] == "]":
                    break
                i += 1
            vc.append(c_word)
        i += 1

    vyc = ["y" + str(i + 1) for i in range(pn)] if pn > 1 else ["y"]
    vc = sorted(set(vc))

    s = ""

    if not isinstance(pyc, str):
        if l != pn and l > 0:
            raise ValueError("The length of the vector in the third parameter must be equal to the value of the second parameter")

    if l == 0 and len(pc) == 0:
        if pn == 1:
            s = "The third parameter must contain the value of"
        else:
            s = f"The third parameter must contain the {len(vyc)} values of y:"
        for m in vyc:
            s += f" {m}"

    if len(pc) == 0:
        if isinstance(pyc, str):
            s = pyc.replace(" ", "").replace(",g", "~g").replace(",y", "~y")
            s = s.split("~")
            vyc = []
            vc = []
            for m in s:
                v = m.split("=")
                #v[0] = re.escape(v[0])
                vyc.extend([v[0], v[1]])
            s = ""

        else:
            s += f".\n The fourth parameter must contain the {len(vc)} values of g:"
            for m in vc:
                s += f" {m}"

    if s:
        raise ValueError(s)

    if b and len(vc) == len(pc):
        s = ", ".join([f"{vyc[i]}={pyc[i] if pyc is not None else ''}" for i in range(len(vyc))] + [f"{vc[i]}={pc[i]}" for i in range(len(vc))])

    else:
        s = l_MFB.replace("y", "*y").replace("+*", "+")
        tmp = s.split("+")
        aux = []
        for el in tmp:
            if el.startswith("*"):
                el = el[1:]
                aux.append(el)
            elif el.startswith(" *"):
                el = el[2:]
                aux.append(el)
            else:
                aux.append(el)        

        s = "+ ".join(aux)
        s = s.replace("g", "*g")

        if len(vyc) > 0 and len(vc) == 0:
            for i in range(0, len(vyc) - 1, 2):
                s = s.replace(vyc[i], vyc[i + 1])
        else:
            if len(vc) != len(pc):
                raise ValueError(f"The vector of the \"g\" values must have {len(vc)} elements.")
            #vc = [re.escape(g) for g in vc]
            for i in range(len(vc)):
                s = s.replace(vc[i], str(pc[i]))
            if not isinstance(pyc, str) and l > 0:
                for i in range(len(vyc)):
                    s = s.replace(vyc[i], str(pyc[i])) 
        if "g" in s:
            raise ValueError(f"Some \"g\" values have not been assigned: {s}")

        if "y" not in s:
            s = s.replace("^", "**")
            s = eval(s)

        else:
            v = s.split("+")
            vs = []
            for m1 in v:
                m2 = m1.split("*")
                m2 = ' '.join(m2)
                m2 = m2.replace("^", "**")
                m2 = m2.split()
                s1 = ""
                s2 = ""
                for m3 in m2:
                    if "y" not in m3:
                        s2 += f"*{m3}"
                    else:
                        s1 += f"({m3})"
                s2 = s2[1:]
                vs.extend([eval(s2), s1.strip()])

            for i in range(0, len(vs) - 2, 2):
                if vs[i + 1]:
                    for j in range(i + 2, len(vs), 2):
                        if vs[i + 1] == vs[j + 1]:
                            vs[i] = str(float(vs[i]) + float(vs[j]))
                            vs[j + 1] = ""
            s = " + ".join([f"{vs[i]}{vs[i + 1]}" for i in range(0, len(vs) - 1, 2) if vs[i + 1]])

    if isinstance(s, int) or isinstance(s, float):
        return s

    s = s.replace(" + -", " - ")
    s = s.replace("**", "^")

    
    return s

def e_MFB(pv=[], pn=0, pf=[], pg=[], b=False):
    
    if len(pv) < 1:
        raise ValueError("The first parameter must be a non-zero vector of integers")
    if pn < 1:
        raise ValueError("The second parameter must be a positive integer")
    for m in pv:
        if m < 0:
            raise ValueError("The first parameter cannot contain negative values")

    vf = []
    vg = []
    l_MFB = MFB(pv, pn)  # Assuming MFB is a predefined function
    v = list(l_MFB)
    ls = len(v)
    c_word = ""
    i = 0

    while i < ls:
        if v[i] == "f":
            i += 1
            c_word = "f"
            while True:
                c_word += v[i]
                if v[i] == "]":
                    break
                i += 1
            vf.append(c_word)
        if v[i] == "g":
            i += 1
            c_word = "g"
            while True:
                c_word += v[i]
                if v[i] == "]":
                    break
                i += 1
            vg.append(c_word)
        i += 1

    vf = list(reversed(list2Set(vf)))
    vg = list2Set(vg)
    s = ""

    if len(pf) == 0:
        s = f"The third parameter must contain the {len(vf)} values of f:"
        for m in vf:
            s += f" {m}"
    if len(pg) == 0:
        if isinstance(pf, str):
            s = pf.replace(" ", "").replace(",g", "~g").replace(",f", "~f")
            s = s.split("~")
            vf = []
            vg = []
            for m in s:
                v = m.split("=")
                #v[0] = re.escape(v[0])
                vf.extend([v[0],v[1]])
            s = ""
        else:
            s += f". The fourth parameter must contain the {len(vg)} values of g:"
            for m in vg:
                s += f" {m}"           
    if s:
        raise ValueError(s)

    if b:
        s = ", ".join([f"{vf[i]}={pf[i]}" for i in range(len(vf))] + [f"{vg[i]}={pg[i]}" for i in range(len(vg))])

    else:
        s = l_MFB.replace("f", "*f").replace("+ *", "+ ")
        if s.startswith("*"):
            s = s[1:]
        s = s.replace("g", "*g")
        
        if len(vf) > 0 and len(vg) == 0:
            for i in range(0, len(vf) - 1, 2):
                s = s.replace(" ", "")
                s = s.replace("+", " + ")
                s = s.replace(vf[i], vf[i + 1])
            if "g" in s:
                raise ValueError(f"Some 'g' parameters were not evaluated: {s}")
            if "f" in s:
                raise ValueError(f"Some 'f' parameters were not evaluated: {s}")
        else:
            for i in range(len(vf)):
                s = s.replace(vf[i], str(pf[i]))
            for i in range(len(vg)):
                s = s.replace(vg[i], str(pg[i]))
                
        s = eval(s)
    return s

def nPS(v=None, V=None):
    
    if v is None:
        raise ValueError("The first parameter is missing")
    if V is None:
        raise ValueError("The second parameter is missing")
    if sum(v) > len(V):
        raise ValueError("The database must contain more data")
    if any(i < 0 for i in v):
        raise ValueError("The values cannot be negative")
    if isinstance(V[0], (list, tuple)):
        if any(len(V[i]) != len(V[0]) for i in range(1, len(V))):
            raise ValueError("The data arrays must have the same length")
    
    def kProd(u, v):
        uv = []

        if all(isinstance(i, list) for i in u):
            
            if all(isinstance(j, list) for j in v):
                for l in range(len(u)):
                    for k in range(len(v)):
                        uv.append(sorted(u[l]+v[k]))
            
            else:
                for l in range(len(u)):
                    for k in range(len(v)):
                        uv.append(sorted(u[l]+[v[k]]))
        
        else:
            
            if all(isinstance(j, list) for j in v):
                for l in range(len(u)):
                    for k in range(len(v)):
                        uv.append(u[l]*v[k])
            
            else:
                for l in range(len(u)):
                    for k in range(len(v)):
                        uv.append([u[l]*v[k]])
                        
        return uv

    N = len(V)
    n = sum(v)
    vTab = mkmSet([sum(v)])
    vP = [intPart(val) for val in v]
    vP = pCart(vP)
    vMu = []
    sC = 0

    for p in vP:
        product = 1
        sdim = 0
        for part in p:
            product *= (-1) ** (len(part) - 1) * factorial(len(part) - 1) * countP(part)
            sdim += len(part)
        sorted_v = sorted([item for sublist in p for item in sublist])
        product /= (ff(N, sdim) * countP(sorted_v))
        vMu.append([sorted_v, product])

    vApp = copy.deepcopy(vTab)
    for app in vApp:
        app[1] = 0
        for mu in vMu:
            if app[0] == mu[0]:
                app[1] += mu[1]

    vMu = vApp
    vk = [intPart(i) for i in range(1, n + 1)]
    evk = copy.deepcopy(vk)
    
    for i in range(len(vk)):
        for j in range(len(vk[i])):
            if len(vk[i])>1:
                evk[i][j] = [(-1) ** (len(vk[i][j]) - 1) * factorial(len(vk[i][j]) - 1) * countP(vk[i][j]) * countP([sum(vk[i][j])])]
            else:
                evk[i][j] = [(-1) ** (len(vk[i][j]) - 1) * factorial(len(vk[i][j]) - 1) * countP(vk[i][j]) * countP([sum(vk[i][j])])]
    
    vS = [powS(i, V) for i in range(1, n + 1)]
    
    s = 0

    for u in vTab:
        app_vk = []
        app_evk = []
        if len(u[0]) == 1:
            app_vk = copy.deepcopy(vk[u[0][0] - 1])
            app_evk = list(chain(*evk[u[0][0]-1]))*u[1]
        else:
            app_vk = kProd(vk[u[0][0] - 1], vk[u[0][1] - 1])
            flat_u = list(chain(*evk[u[0][0]-1]))
            flat_v = list(chain(*evk[u[0][1]-1]))
            app_evk = kProd(flat_u, flat_v)
            app_evk = list(chain(*app_evk))  # Aplatir la liste
            app_evk = [x * u[1] for x in app_evk]
            
            if len(u[0]) > 2:
                for i in range(2, len(u[0])):
                    app_vk = kProd(app_vk, vk[u[0][i] - 1])
                    if any(isinstance(i, int) for i in app_evk):
                        app_evk = kProd(app_evk, list(chain(*evk[u[0][i]-1])))
                    else :
                        app_evk = kProd(list(chain(*app_evk)), list(chain(*evk[u[0][i]-1])))

                
        pS = 1
        for i in u[0]:
            pS *= vS[i-1]
            
        sC = 0
        for i in range(len(app_vk)):
            
            if isinstance(app_evk[i], int):                
                sC += mCoeff(app_vk[i], vMu) * app_evk[i]
                    
            else :
                for j in range(len(app_evk[i])):
                    sC += mCoeff(app_vk[i], vMu) * app_evk[i][j]
        s += sC * pS

    return s

def nPolyk(L=None, data=None, bhelp=None):
    if L is None:
        raise ValueError("The first parameter is missing")
    if data is None:
        raise ValueError("The second parameter is missing")

    bHelp = False if bhelp is None or bhelp != True else True

    if all(isinstance(el, list) for el in L):
        if len(L) == 1:
            if isinstance(L[0], int):
                if bHelp:
                    print("KS:")
                return nKS(L[0], data)
            else:
                if bHelp:
                    print("KM:")
                return nKM(L[0], data)
        else:
            isPS = True
            
            for v in L:
                if len(v) > 1:
                    isPS = False
            
            if isPS:
                if bHelp:
                    print("PS:")
                return nPS([item for sublist in L for item in sublist], data)
            else:
                if bHelp:
                    print("PM:")
                return nPM(L, data)
        print("Error: type of sub-function not determined")
    else:
        if len(L) == 1:
            if bHelp:
                print("KS:")
            return nKS(L, data)
        else:
            if bHelp:
                print("KM:")
            return nKM(L, data)
        
def oBellPol(n=1, m=0):
    
    tmp = n
    if isinstance(n, int):
        tmp = [n]
    v = MFB(tmp, 1)  # Assuming MFB and MFB2Set are defined elsewhere
    v = MFB2Set(v)
    
    for j in range(len(v)):
        c = str(v[j][1])
        x = v[j][2]
        i = v[j][3]
        k = int(v[j][4])
        
        if x == "f":
            if m > 0 and i != str(m):
                c = "0"
            else:
                c = c + "*(factorial(" + str(i) + "))"
            x = ""
            i = ""
        
        elif x == "g":
            c = c + "*(factorial(" + str(i) + "))^" + str(k)
            x = "(y" + str(i) + (("^" + str(k)) if k > 1 else "") + ")"
            i = ""
            k = 1
        
        v[j][1] = c
        v[j][2] = x
        v[j][3] = i
        v[j][4] = k
    
    if n == 1:
        return Set2expr(v)  # Assuming Set2expr is defined elsewhere
    else:
        return "1/" + str(math.factorial(n)) + "*( " + Set2expr(v) + " )"
    
    
def evaluate(s=None, S=None):
    
    if s is None or S is None:
        raise ValueError('One of the parameters is missing')
    
    if 'k' in s and 'm' in S:
        raise ValueError('Trying to evaluate cum2mom with values of cumulants')
    
    if 'm' in s and 'k' in S:
        raise ValueError('Trying to evaluate mom2cum with values of moments')
            
    # Parse the values of the variables from s
    var_dict = {}
    assignments = s.split(',')
    
    # Handle the powers and the products within the same terms
    S = S.replace('^', '**')
    S = S.replace('m', '*m')
    S = S.replace('k', '*k')
    S = S.split()
    
    for i in range(len(S)):
        if S[i].startswith('*'):
            S[i] = S[i][1:]
    
    S = ''.join(S)
        
    for assign in assignments:
        var, value = assign.split('=')
        var = var.strip()
        value = float(value.strip())
        var_dict[var] = value
    
    pattern = re.compile(r'[km]\[\d+\]')
    variables_in_S = pattern.findall(S)
    undefined_vars = [var for var in variables_in_S if var not in var_dict]
    undefined_vars = list(set(undefined_vars))
    
    if undefined_vars:
        raise ValueError(f'Undefined variables in expression: {undefined_vars}')
        
    # Replace the variables in S
    def replace_var(match):
        var_name = match.group(0)
        return str(var_dict.get(var_name, var_name))
    
    pattern = re.compile(r'[km]\[\d+\]')
    expression = pattern.sub(replace_var, S)
    # Evaluate the mathematical expression
    try:
        result = eval(expression)
    except Exception as e:
        return str(e)
    
    return result