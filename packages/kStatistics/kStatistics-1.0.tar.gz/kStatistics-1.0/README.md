# kStatistics
### July 24, 2024

### Unbiased Estimators for Cumulant Products and Faa Di Bruno's Formula

### Introduction
This package is a Python implementation of the original R package [kStatistics](https://cran.r-project.org/web/packages/kStatistics/index.html), written by [E. Di Nardo](https://elviradinardo.it) and G. Guarino. This file aims at presenting the kStatistics functions and how to use them through examples. Further explanations on the algorithms are available [here](https://cran.r-project.org/web/packages/kStatistics/kStatistics.pdf).


#### Contacts
hugo.mai@ensta-paris.fr (Maintainer)
elvira.dinardo@unito.it

### Description

kStatistics is a package producing estimates of (joint) cumulants and (joint) cumulant products of a given dataset, using (multivariate) k-statistics and (multivariate) polykays, which are symmetric unbiased estimators. The procedures rely on a symbolic method arising from the classical umbral calculus and described in the following papers.

- (2008) Di Nardo E., Guarino G., Senato D. A unifying framework for k-statistics, polykays and their multivariate generalizations. Bernoulli 14, 440--468. [here](http:http://arxiv.org/pdf/math/0607623)

- (2009) Di Nardo E., Guarino G., Senato D. A new method for fast computing unbiased estimators of cumulants. Statistics and Computing 19, 155--165. [here](https://arxiv.org/abs/0807.5008)

- (2011) Di Nardo E., Guarino G., Senato D. A new algorithm for computing the multivariate Faa di Bruno's formula. Appl. Math. Comp. 217, 6286--6295 [here](https://arxiv.org/abs/1012.6008)

In the package, a set of combinatorial tools are given useful in the construction of these estimations such as integer partitions, set partitions, multiset subdivisions or multi-index partitions, pairing and merging of multisets. In the package, there are also functions to recover univariate and multivariate cumulants from a sequence of univariate and multivariate moments (and vice-versa), using Faa di Bruno’s formula. Their evaluation is also provided when users specify in input numerical values for moments and/or cumulants. The function producing Faa di Bruno’s formula returns coefficients of exponential power series compositions such as $f[g(z)]$ with $f$ and $g$ both univariate, or $f[g(z_1,...,z_m)]$ with $f$ univariate and $g$ multivariate, or $f[g_1(z_1,...,z_m),...,g_n(z_1,...,z_m)]$ with $f$ and $g$ both multivariate. Let us recall that Faa di Bruno’s formula might also be employed to recover iterated (partial) derivatives of all these compositions. Lastly, using Faa di Bruno’s formula, some special families of polynomials are also generated, such as Bell polynomials, generalized complete Bell polynomials, partition polynomials and generalized partition polynomials.

For further applications of these functions, refer to the following paper:

- (2022) Di Nardo E., Guarino G.  kStatistics: Unbiased Estimates of Joint Cumulant Products from the Multivariate Faà Di Bruno’s Formula. [The R Journal](https://journal.r-project.org/articles/RJ-2022-033/RJ-2022-033.pdf) 14(2) 208-228.

### Presentation of the functions and their use

### countP

#### Description

The function computes the multiplicity of a multi-index partition. Note that a multi-index partition
corresponds to a subdivision of a multiset having the input multi-index as multiplicities.

#### Usage
```
countP( v=[1] )
```
#### Argument
v : list 
#### Value
int, the multiplicity of the given item

#### Examples
```
countP([2,1])
```
Returns 3 which is the multiplicity of [1,2], partition of the integer 3, or of [[a],[a,a]], subdivision of the multiset [a,a,a].
```
3
```
```
countP([4,2])
```
Return 15 which is the multiplicity of [4,2], partition of the integer 6, or of [[a,a,a,a],[a,a]], subdivision of the multiset [a,a,a,a,a,a].
```
15
```
```
countP( [[2,0], [1,0], [1,0], [0,1], [0,2]] )
```
Return 18 which is the multiplicity of [[2,0], [1,0], [1,0], [0,1], [0,2]], partition of the multi-index (4,3), or of [[b],[b,b],[a],[a],[a,a]], subdivision of the multiset [a,a,a,a,b,b,b].

### cum2mom

#### Description
The function computes a simple or a multivariate cumulant in terms of simple or multivariate moments.
#### Usage
```
cum2mom(n = 1)
```
#### Argument
n : integer or vector of integers.
#### Value
str, the expression of the cumulant in terms of moments
#### Examples
```
cum2mom(5)
```
Returns the simple cumulant k[5] in terms of the simple moments m[1],..., m[5].
```
24m[1]^5 - 60m[1]^3m[2] + 30m[1]m[2]^2 + 20m[1]^2m[3] - 10m[2]m[3] - 5m[1]m[4] + m[5]
```
```
cum2mom([3,1])
```
Returns the multivariate cumulant k[3,1] in terms of the multivariate moments m[i,j] for i=0,1,2,3 and j=0,1.
```
- 6m[0,1]m[1,0]^3 + 6m[0,1]m[1,0]m[2,0] - m[0,1]m[3,0] + 6m[1,0]^2m[1,1] - 3m[1,0]m[2,1] - 3m[1,1]m[2,0] + m[3,1]
```
### eBellPol
#### Description
The function generates a complete or a partial exponential Bell polynomial.
#### Usage
```
eBellPol(n = 1, m = 0)
```
#### Argument
n : integer, the degree of the polynomial

m : integer, the fixed degree of each monomial in the polynomial
#### Value
str, the expression of the exponential Bell polynomial
#### Examples
```
eBellPol(5)
```
Returns the complete exponential Bell Polynomial for n=5, that is
```
(y1**5) + 10(y1**3)(y2) + 15(y1)(y2**2) + 10(y1**2)(y3) + 10(y2)(y3) + 5(y1)(y4) + (y5)
```
```
eBellPol(5,3)
```
Returns the partial exponential Bell Polynomial for n=5 and m=3, that is
```
15(y1)(y2**2) + 10(y1**2)(y3)
```
### e_eBellPol
#### Description
The function evaluates a complete or a partial exponential Bell polynomial (output of the eBellPol
function) when its variables are substituted with numerical values
#### Usage
```
e_eBellPol(n=1, m=0, v=None)
```
#### Argument
n : integer, the degree of the polynomial

m : integer, the fixed degree of each monomial in the polynomial

v : vector, the numerical values in place of the variables of the polynomial

#### Value
int, the value assumed by the polynomial.
#### Warnings
By default, the function returns the Stirling numbers of second kind.
#### Examples
```
e_eBellPol(5,3)
```
Returns S(5,3) = 25 (where S=Stirling number of second kind).
```
25
```
Or (same output)
```
e_eBellPol(5, 3, [1, 1, 1, 1, 1])
```
```
25
```
```
e_eBellPol(5)
```
Returns B5=52 (where B5 is the 5-th Bell number).
```
52
```
Or (same output)
```
e_eBellPol(5,0)
52
```
Or (same output)
```
e_eBellPol(5, 0, [1, 1, 1, 1, 1])
52
```
```
e_eBellPol(5,3,[1,-1,2,-6,24])
```
Return s(5,3) = 35 (where s=Stirling number of first kind).
```
35
```
### e_GCBellPol
#### Description
The function evaluates a generalized complete Bell polynomial (output of the GCBellPol function)
when its variables and/or its coefficients are substituted with numerical values.
#### Usage
```
e_GCBellPol(pv=[], pn=0, pyc=[], pc=[], b=False)
```
#### Argument
pv : vector of integers, the subscript of the polynomial

pn : integer, the number of variables

pyc : vector, the numerical values into the variables [optional], or the string with the

direct assignment into the variables and/or the coefficients

pc : vector, the numerical values into the coefficients, [optional if pyc is a string]

b : boolean, if TRUE the function prints the list of all the assignments
#### Value
string or numerical, the evaluation of the polynomial
#### Warnings
The value of the first parameter is the same as the mkmSet function.
#### Examples
#####  Evaluation of the generalized complete Bell polynomial with subscript 2
The polynomial (y^2)g[1]^2 + (y^1)g[2], output of
```
GCBellPol( [2],1 )
```
when
g[1]=3 and g[2]=4
```
e_GCBellPol( [2], 1, [], [3,4] )
```
```
9(y^2) + 4(y)
```
OR (same output)
```
e_GCBellPol( [2], 1, "g[1]=3,g[2]=4" )
```
```
9(y^2) + 4(y)
```
Check the assignments setting the boolean parameter equals to True, that is g[1]=3
and g[2]=4
```
e_GCBellPol( [2], 1, [], [3,4], True )
```
```
y=, g[1]=3, g[2]=4
```
The numerical value of (y^2)g[1]^2 + (y^1)g[2], output of 
```
GCBellPol( c(2),1 )
```
when g[1]=3 and g[2]=4 and y=7, that is 469
```
e_GCBellPol( [2], 1, [7], [3,4] )
```
```
469
```
OR (same output)
```
e_GCBellPol( [2], 1, "y=7, g[1]=3,g[2]=4" )
```
Check the assignments setting the boolean parameter equals to True, that is g[1]=3
and g[2]=4 and y=7
```
e_GCBellPol( [2], 1, [7], [3,4], True )
```
```
y=7, g[1]=3, g[2]=4
```
##### Evaluation of the generalized complete Bell polynomial with subscript (2,1)
The polynomial 2(y^2)g[1,1]g[1,0] + (y^3)g[1,0]^2g[0,1] + (y)g[2,1] + (y^2)
g[2,0]g[0,1], output of
```
GCBellPol( [2,1], 1 )
```
 when g[0,1]=1, g[1,0]=2, g[1,1]=3,
g[2,0]=4, g[2,1]=5, that is 16(y^2) + 4(y^3) + 5(y)
```
import numpy as np

e_GCBellPol([2,1], 1, [], np.arange(1,6))
```
```
4(y^3) + 16.0(y^2) + 5(y)
```
Or (same output)
```
e_GCBellPol([2,1], 1, [], [1,2,3,4,5])
```
OR (same output)
```
e_GCBellPol( [2,1], 1, "g[0,1]=1, g[1,0]=2, g[1,1]=3, g[2,0]=4, g[2,1]=5" )
```
Check the assignments setting the boolean parameter equals to True, that is
g[0,1]=1, g[1,0]=2, g[1,1]=3, g[2,0]=4, g[2,1]=5
```
import numpy as np

e_GCBellPol( [2,1], 1, [], np.arange(1,6), True )
```
```
y=, g[0,1]=1, g[1,0]=2, g[1,1]=3, g[2,0]=4, g[2,1]=5
```
The numerical value of 2(y^2)g[1,1]g[1,0] + (y^3)g[1,0]^2g[0,1] + (y)g[2,1] + (y^2)
g[2,0]g[0,1], output of 
```
GCBellPol( [2,1], 1 )
```
when g[0,1]=1, g[1,0]=2,
g[1,1]=3, g[2,0]=4, g[2,1]=5 and y=7, that is 2191
```
import numpy as np

e_GCBellPol( [2,1], 1, [7], np.arange(1,6) )
```
```
2191
```
Or (same output)
```
e_GCBellPol( [2,1], 1, "y=7, g[0,1]=1, g[1,0]=2, g[1,1]=3, g[2,0]=4, g[2,1]=5" )
```
```
2191
```
Check the assignments setting the boolean parameter equals to True, that is
g[0,1]=1, g[1,0]=2, g[1,1]=3, g[2,0]=4, g[2,1]=5, y=7
```
import numpy as np

e_GCBellPol( [2,1], 1, [7], np.arange(1,6) )
```
```
y=7, g[0,1]=1, g[1,0]=2, g[1,1]=3, g[2,0]=4, g[2,1]=5
```
##### Evaluation of the generalized complete Bell Polynomial with subscript (1,1)
The polynomial (y1)g1[1,1] + (y1^2)g1[1,0]g1[0,1] + (y2)g2[1,1] + (y2^2)g2[1,0]
g2[0,1] + (y1)(y2)g1[1,0]g2[0,1] + (y1)(y2)g1[0,1]g2[1,0], output of 
```
GCBellPol([1,1], 2)
```
when g1[0,1]=1, g1[1,0]=2, g1[1,1]=3, g2[0,1]=4, g2[1,0]=5, g2[1,1]=6, that is
3(y1) + 2(y1^2) + 6(y2) + 20(y2^2) + 13(y1)(y2)
```
import numpy as np

e_GCBellPol( [1,1], 2, [], np.arange(1,7))
```
```
13.0(y1)(y2) + 2(y1^2) + 3(y1) + 20(y2^2) + 6(y2)
```
O (same output)
```
e_GCBellPol([1,1], 2, [], [1,2,3,4,5,6])
```
```
13.0(y1)(y2) + 2(y1^2) + 3(y1) + 20(y2^2) + 6(y2)
```
Or (same output)
```
e_GCBellPol( [1,1], 2, "g1[0,1]=1, g1[1,0]=2, g1[1,1]=3, g2[0,1]=4, g2[1,0]=5, g2[1,1]=6" )
```
```
13.0(y1)(y2) + 2(y1^2) + 3(y1) + 20(y2^2) + 6(y2)
```
Check the assignments setting the boolean parameter equals to True, that is
g1[0,1]=1, g1[1,0]=2, g1[1,1]=3, g2[0,1]=4, g2[1,0]=5, g2[1,1]=6
```
import numpy as np

e_GCBellPol( [1,1], 2, [], np.arange(1,7), True )
```
```
y1=, y2=, g1[0,1]=1, g1[1,0]=2, g1[1,1]=3, g2[0,1]=4, g2[1,0]=5, g2[1,1]=6
```
The numerical value of (y1)g1[1,1] + (y1^2)g1[1,0]g1[0,1] + (y2)g2[1,1] + (y2^2)g2[1,0]
g2[0,1] + (y1)(y2)g1[1,0]g2[0,1] + (y1)(y2)g1[0,1]g2[1,0], output of
```
GCBellPol([1,1], 2)
```
when g1[0,1]=1, g1[1,0]=2, g1[1,1]=3, g2[0,1]=4, g2[1,0]=5, y1=7 and y2=8, that is 2175
```
import numpy as np

e_GCBellPol( [1,1], 2, [7,8], np.arange(1,7))
```
```
2175
```
Or (same output)
```
cVal="y1=7, y2=8, g1[0,1]=1, g1[1,0]=2, g1[1,1]=3, g2[0,1]=4, g2[1,0]=5,g2[1,1]=6"
e_GCBellPol([1,1], 2, cVal)
```
```
2175
```
To recover which coefficients and variables are involved in the generalized complete
Bell polynomial, run the 
```
e_GCBellPol
```
function without any assignment.
```
e_GCBellPol([1, 1], 2)
```
The error message prints which coefficients and variables are involved, that is
```
ValueError: The third parameter must contain the 2 values of y: y1 y2.
 The fourth parameter must contain the 6 values of g: g1[0,1] g1[1,0] g1[1,1] g2[0,1] g2[1,0] g2[1,1]
```
To assign correctly the values to the coefficients and the variables:
1) run
```
e_GCBellPol(c(1, 1), 2)
```
and get the errors with the indication of the involved
coefficients and variables, that is
```
ValueError: The third parameter must contain the 2 values of y: y1 y2.
 The fourth parameter must contain the 6 values of g: g1[0,1] g1[1,0] g1[1,1] g2[0,1] g2[1,0] g2[1,1]
```
2) initialize g1[0,1] g1[1,0] g1[1,1] g2[0,1] g2[1,0] g2[1,1] with - for example - the
first 6 integer numbers and do the same for y1 and y2, that is
```
e_GCBellPol([1,1], 2, [1,2], [1,2,3,4,5,6], True)
```
3) trough the boolean value True, recover the string y1=1, y2=1, g1[0,1]=1, g1[1,0]=2,
g1[1,1]=3, g2[0,1]=4, g2[1,0]=5, g2[1,1]=6
4) copy and past the string in place of "..." when run
```
e_GCBellPol(c(1,1),2,"...")
```
5) change the assignments if necessar
```
cVal="y1=10,y2=11,g1[0,1]=1.1,g1[1,0]=-2,g1[1,1]=3.2,g2[0,1]=-4,g2[1,0]=10,g2[1,1]=6"
e_GCBellPol([1,1], 2, cVal)
```
```
-2872.0
```
### e_MFB
#### Description
The function evaluates the Faa di Bruno’s formula, output of the MFB function, when the coefficients
of the exponential formal power series f and g1,...,gn in the composition f[g1(),...,gn()] are
substituted with numerical values.
#### Usage
```
e_MFB(pv=[], pn=0, pf=[], pg=[], b=False)
```
#### Argument
pv : vector of integers, the subscript of Faa di Bruno’s formula

pn : integer, the number of the inner formal power series "g"

pf : vector, the numerical values in place of the coefficients of the outer formal power
series "f" or the string with the direct assignments in place of the coefficients
of both "f" and "g"

pg : vector, the numerical values in place of the coefficients of the inner formal power
series "g" [Optional if pf is a string]

b : boolean

#### Value
numerical, the evaluation of Faa di Bruno’s formula
#### Warnings
The value of the first parameter is the same as the mkmSet function.
#### Examples
The numerical value of f[1]g[1,1] + f[2]g[1,0]g[0,1], that is the coefficient of z1z2 in
$f(g1(z1,z2),g2(z1,z2)))$, output of 
```
MFB(c(1,1),1)
```
when
f[1] = 5 and f[2] = 10,
g[0,1]=3, g[1,0]=6, g[1,1]=9
```
e_MFB([1,1], 1, [5,10], [3,6,9])
```
```
225
```
Same as the previous example, with a string of assignments as third input parameter
```
e_MFB([1,1], 1, "f[1]=5, f[2]=10, g[0,1]=3, g[1,0]=6, g[1,1]=9")
```
```
225
```
Use the boolean parameter to verify the assignments to the coefficients of "f" and "g",
that is f[1]=5, f[2]=10, g[0,1]=3, g[1,0]=6, g[1,1]=9
```
e_MFB([1,1], 1, [5,10], [3,6,9], True)
```
```
f[1]=5, f[2]=10, g[0,1]=3, g[1,0]=6, g[1,1]=9
```
To recover which coefficients are involved, run the function without any assignment.
The error message recalls which coefficients are necessary, that is
```
e_MFB([1,1], 1)
```
```
ValueError: The third parameter must contain the 2 values of f: f[1] f[2]. The fourth parameter must contain the 3 values of g: g[0,1] g[1,0] g[1,1]
```
To assign correctly the values to the coefficients of "f" and "g" when the functions
become more complex:
1) run
```
e_MFB([1,1], 2)
```
and get the errors with the indication of the involved coefficients
of "f" and "g", that is
```
ValueError: The third parameter must contain the 5 values of f: f[0,1] f[0,2] f[1,0] f[2,0] f[1,1]. The fourth parameter must contain the 6 values of g: g1[0,1] g2[1,0] g1[1,0] g2[0,1] g1[1,1] g2[1,1]
```
2) initialize f[0,1] f[0,2] f[1,0] f[1,1] f[2,0] with - for example - the first 5 integer
numbers and do the same for g1[0,1] g1[1,0] g1[1,1] g2[0,1] g2[1,0] g2[1,1], that is
```
import numpy as np

e_MFB([1,1], 2, np.arange(1,6), np.arange(1,7), True)
```
```
f[0,1]=1, f[0,2]=2, f[1,0]=3, f[2,0]=4, f[1,1]=5, g1[0,1]=1, g2[1,0]=2, g1[1,0]=3, g2[0,1]=4, g1[1,1]=5, g2[1,1]=6
```
3) trough the boolean value True, recover the string f[0,1]=1, f[0,2]=2, f[1,0]=3, f[1,1]=4,
f[2,0]=5, g1[0,1]=1, g1[1,0]=2, g1[1,1]=3, g2[0,1]=4, g2[1,0]=5, g2[1,1]=6
4) copy and past the string in place of " ... " when run
```
e_MFB([1,1], 1, " ... ")
```
5) change the assignments if necessary
```
cfVal = "f[0,1]=2, f[0,2]=5, f[1,0]=13, f[1,1]=-4, f[2,0]=0"


cgVal = "g1[0,1]=-2.1, g1[1,0]=2, g1[1,1]=3.1, g2[0,1]=5, g2[1,0]=0, g2[1,1]=6.1"


cVal = cfVal + "," + cgVal


result = e_MFB((1, 1), 2, cVal)
print(result)
```
```
12.500000000000004
```
### ff
#### Description
The function computes the descending (falling) factorial of a positive integer n with respect to a
positive integer k less or equal to n.
#### Usage
```
ff( n=1, k )
```
#### Argument
n : integer

k : integer
#### Value
int, the descending factorial
#### Examples
```
ff(6,3)
```
```
120
```
### GCBellPol
#### Description
The function generates a generalized complete Bell polynomial, that is a coefficient of the composition 

exp(y[1] g1(z1,...,zm) + ... + y[n] gn(z1,...,zm)),

where y[1],...,y[n] are variables. The input vector of integers identifies the subscript of the polynomial.

#### Usage
```
GCBellPol(nv=[], m=1, b=False)
```
#### Argument
nv : vector of integers, the subscript of the polynomial, corresponding to the powers
of the product among z1, z2, ..., zm

m : integer, the number of z’s variables

b : boolean, TRUE if the inner formal power series "g" are all equal
#### Value
str, the expression of the polynomial
#### Warnings
The value of the first parameter is the same as the mkmSet function
#### Examples
Returns the generalized complete Bell Polynomial for n=1, m=1 and g1=g,
that is (y^2)g[1]^2 + (y)g[2]
```
GCBellPol( [2], 1 )
```
```
(y**2)g[1]^2 + (y)g[2]
```
Returns the generalized complete Bell Polynomial for n=1, m=2 and g1=g,
2(y^2)g[1,0]g[1,1] + (y^3)g[0,1]g[1,0]^2 + (y)g[2,1] + (y^2)g[0,1]g[2,0]
```
GCBellPol( [2,1], 1 )
```
```
(y**3)g[0,1]g[1,0]^2 + (y**2)g[0,1]g[2,0] + 2(y**2)g[1,0]g[1,1] + (y)g[2,1]
```
Returns the generalized complete Bell Polynomial for n=2, m=2 and g1=g2=g,
(y1)g[1,1] + (y1^2)g[0,1]g[1,0] + (y2)g[1,1] + (y2^2)g[0,1]g[1,0] + 2(y1)(y2)g[0,1]g[1,0]
```
GCBellPol( [1,1], 2, True )
```
```
2(y1)(y2)g[0,1]g[1,0] + (y1**2)g[0,1]g[1,0] + (y1)g[1,1] + (y2**2)g[0,1]g[1,0] + (y2)g[1,1]
```
Returns the generalized complete Bell Polynomial for n=2, m=2 and g1 different from g2,
that is (y1)g1[1,1] + (y1^2)g1[1,0]g1[0,1] + (y2)g2[1,1] + (y2^2)g2[1,0]g2[0,1] +
(y1)(y2)g1[1,0]g2[0,1] + (y1)(y2)g1[0,1]g2[1,0]
```
GCBellPol( [1,1], 2 )
```
```
(y1)(y2)g1[0,1]g2[1,0] + (y1)(y2)g1[1,0]g2[0,1] + (y1**2)g1[0,1]g1[1,0] + (y1)g1[1,1] + (y2**2)g2[0,1]g2[1,0] + (y2)g2[1,1]
```
### gpPart 
#### Description
The function returns a general partition polynomial.
#### Usage
```
gpPart(n = 0)
```
#### Argument
n : integer
#### Value
str, the expression of the polynomial 
#### Warnings
The value of the first parameter is the same as the MFB function in the univariate with univariate
composition.
#### Examples
Return the general partition polynomial G[a1,a2; y1,y2], that is a2(y1^2) + a1(y2)
```
gpPart(2)
```
```
a2(y1**2) + a1(y2)
```
Return the general partition polynomial G[a1,a2,a3,a4,a5; y1,y2,y3,y4,y5], that is
a5(y1^5) + 10a4(y1^3)(y2) + 15a3(y1)(y2^2) + 10a3(y1^2)(y3) + 10a2(y2)(y3) + 5a2(y1)(y4)
+ a1(y5)
```
gpPart(5)
```
```
a5(y1**5) + 10a4(y1**3)(y2) + 15a3(y1)(y2**2) + 10a3(y1**2)(y3) + 10a2(y2)(y3) + 5a2(y1)(y4) + a1(y5)
```
### intPart 
#### Description
The function generates all possible (unique) decomposition of a positive integer n in the sum of
positive integers less or equal to n.
#### Usage
```
intPart(n=0 ,vOutput = FALSE)
```
#### Argument
n : integer

vOutput : optional boolean parameter, if equal to TRUE the function produces a compact
output that is easy to read.
#### Value
list, all the partitions of n
#### Examples
Return the partition of the integer 3, that is
[1,1,1],[1,2],[3]
```
intPart(3)
```
```
[[1, 1, 1], [1, 2], [3]]
```
Return the partition of the integer 4, that is
[1,1,1,1],[1,1,2],[1,3],[2,2],[4]
```
intPart(4)
```
```
[[1, 1, 1, 1], [1, 1, 2], [2, 2], [1, 3], [4]]
```
Or (same output)
```
intPart(4, False)
```
```
[[1, 1, 1, 1], [1, 1, 2], [2, 2], [1, 3], [4]]
```
Return the same output as the previous example but in a compact expression
```
intPart(4, TRUE)
```
```
[1, 1, 1, 1]
[1, 1, 2]
[2, 2]
[1, 3]
[4]
None
```
### list2m 

#### Description
The function returns the multiset representation of a vector or a list, in increasing order
#### Usage
```
list2m(v=[0])
```
#### Argument
v : single vector or list of vectors
#### Value
multiset, the list of multisets
#### Examples
Returns the list of multisets [[1],3], [[2],1] from the input vector (1,2,1,1)
```
list2m([1,2,1,1])
```
```
[[[1], 3], [[2], 1]]
```
Returns the list of multisets [[1,2],2], [[2,3],1] from the input [[1,2], [2,3], [1,2]]
```
list2m([[1,2], [2,3], [1,2]])
```
```
[[[1, 2], 2], [[2, 3], 1]]
```
### list2Set
#### Description
Given a list, the function deletes the instances of an element in the list, leaving the order inalterated.
#### Usage
```
list2Set(v=[0])
```
#### Argument
v : single vector or list of vectors
#### Value
set, the sequence of distinct elements
#### Examples
Returns the vector [1,2,3,5,6]
```
list2Set([1,2,3,1,2,5,6])
```
```
[1, 2, 3, 5, 6]
```
Returns the list [[1,2], [10,11], [7,8]]
```
list2Set([[1,2], [1,2], [10,11], [1,2], [7,8]])
```
```
[[1, 2], [10, 11], [7, 8]]
```
### m2Set
#### Description
The function returns the vectors (only counted once) of all the multi-index partitions output of the
mkmSet function. These vectors correspond also to the blocks of the subdivisions of the multiset
having the given multi-index as multeplicites.
#### Usage
```
m2Set(v=[0])
```
#### Argument
v : sequence of type [[e1,e2,...], m1], [[f1,f2,...], m2],... with m1, m2,...
multiplicities
#### Value
set, the sequence with distinct elements
#### Examples
M1 = mkmSet([2,1])
M1 is
[
    [ [[0, 1], [1, 0], [1, 0]], 1 ],
    [ [[0, 1], [2, 0]], 1 ],
    [ [[1, 0], [1, 1]], 2 ],
    [ [[2, 1]], 1 ]
]
To print all the partitions of the multi-index (2,1) run 
```
mkmSet([2,1], True)
```
```
[( 0 1 )( 1 0 )( 1 0 ), 1 ]
[( 0 1 )( 2 0 ), 1 ]
[( 1 0 )( 1 1 ), 2 ]
[( 2 1 ), 1 ]
```
Then m2Set(M1) returns the following set: [[0,1],[1,0],[2,0],[1,1],[2,1]]
```
m2Set( M1 )
```
```
[[0, 1], [1, 0], [2, 0], [1, 1], [2, 1]]
```
### mCoeff
#### Description
Given a list containing vectors paired with numbers, the function returns the number paired with
the vector matching the one passed in input.
#### Usage
```
mCoeff(v=None, L=None)
```
#### Argument
v : vector to be searched in the list

L : two-dimensional list: in the first there is a vector and in the second a number
#### Value
float, the number paired with the input vector
#### Examples
Run
```
mkmSet([3])
```
to get the list
```
L1 = [[[1,1,1],1], [[1,2],3], [[3],1]]
```
```
L1 = mkmSet([3])
```
Returns the number 3, which is the number paired with [1,2] in L1
```
mCoeff( [1,2], L1)
```
```
3
```
### MFB
#### Description
The function returns the coefficient indexed by the integers i1,i2,... of an exponential formal
power series composition through the univariate or multivariate Faa di Bruno’s formula.
#### Usage
```
MFB(v=[], n=0)
```
#### Argument
v : vector of integers, the subscript of the coefficient

n : integer, the number of inner functions g’s
#### Value
str,  the expression of Faa di Bruno’s formula
#### Warnings
The value of the first parameter is the same as the mkmSet function
#### Examples
##### Univariate f with Univariate g
The coefficient of z^2 in f[g(z)], that is f[2]g[1]^2 + f[1]g[2], where

f[1] is the coefficient of x in f(x) with x=g(z)

f[2] is the coefficient of x^2 in f(x) with x=g(z)

g[1] is the coefficient of z in g(z)

g[2] is the coefficient of z^2 in g(z)
```
MFB( [2], 1 )
```
```
f[2]g[1]^2 + f[1]g[2]
```
The coefficient of z^3 in f[g(z)], that is f[3]g[1]^3 + 3f[2]g[1]g[2] + f[1]g[3]
```
MFB( [3], 1 )
```
```
f[3]g[1]^3 + 3f[2]g[1]g[2] + f[1]g[3]
```
##### Univariate f with Multivariate g
The coefficient of z1 z2 in f[g(z1,z2)], that is f[1]g[1,1] + f[2]g[1,0]g[0,1]
where

f[1] is the coefficient of x in f(x) with x=g(z1,z2)

f[2] is the coefficient of x^2 in f(x) with x=g(z1,z2)

g[1,0] is the coefficient of z1 in g(z1,z2)

g[0,1] is the coefficient of z2 in g(z1,z2)

g[1,1] is the coefficient of z1 z2 in g(z1,z2)
```
MFB( [1,1], 1 )
```
```
f[2]g[0,1]g[1,0] + f[1]g[1,1]
```
The coefficient of z1^2 z2 in f[g(z1,z2)]
```
MFB( [2,1], 1 )
```
```
f[3]g[0,1]g[1,0]^2 + f[2]g[0,1]g[2,0] + 2f[2]g[1,0]g[1,1] + f[1]g[2,1]
```
The coefficient of z1 z2 z3 in f[g(z1,z2,z3)]
```
MFB( [1,1,1], 1 )
```
```
f[3]g[0,0,1]g[0,1,0]g[1,0,0] + f[2]g[0,0,1]g[1,1,0] + f[2]g[0,1,0]g[1,0,1] + f[2]g[0,1,1]g[1,0,0] + f[1]g[1,1,1]
```
#####  Multivariate f with Univariate/Multivariate g1, g2, ..., gn
The coefficient of z in f[g1(z),g2(z)], that is f[1,0]g1[1] + f[0,1]g2[1] where

f[1,0] is the coefficient of x1 in f(x1,x2) with x1=g1(z) and x2=g2(z)

f[0,1] is the coefficient of x2 in f(x1,x2) with x1=g1(z) and x2=g2(z)

g1[1] is the coefficient of z of g1(z)

g2[1] is the coefficient of z of g2(z)
```
MFB( [1], 2 )
```
```
f[1,0]g1[1] + f[0,1]g2[1]
```
The coefficient of z1 z2 in f[g1(z1,z2),g2(z1,z2)], that is

f[1,0]g1[1,1] + f[2,0]g1[1,0]g1[0,1] + f[0,1]g2[1,1] + f[0,2]g2[1,0]g2[0,1] +
f[1,1]g1[1,0]g2[0,1] + f[1,1]g1[0,1]g2[1,0]

where

f[1,0] is the coefficient of x1 in f(x1,x2) with x1=g1(z1,z2) and x2=g2(z1,z2)

f[0,1] is the coefficient of x2 in f(x1,x2) with x1=g1(z1,z2) and x2=g2(z1,z2)

g1[1,1] is the coefficient of z1z2 in g1(z1,z2)

g1[1,0] is the coefficient of z1 in g1(z1,z2)

g1[0,1] is the coefficient of z2 in g1(z1,z2)

g2[1,1] is the coefficient of z1 z2 in g2(z1,z2)

g2[1,0] is the coefficient of z1 in g2(z1,z2)

g2[0,1] is the coefficient of z2 in g1(z1,z2)
```
MFB( [1,1], 2 )
```
```
f[1,1]g1[0,1]g2[1,0] + f[1,1]g1[1,0]g2[0,1] + f[2,0]g1[0,1]g1[1,0] + f[1,0]g1[1,1] + f[0,2]g2[0,1]g2[1,0] + f[0,1]g2[1,1]
```
The coefficient of z1 in f[g1(z1,z2),g2(z1,z2),g3(z1,z2)]
```
MFB( [1,0], 3 )
```
```
f[0,1,0]g2[1,0] + f[1,0,0]g1[1,0] + f[0,0,1]g3[1,0]
```
The coefficient of z1 z2 in f[g1(z1,z2),g2(z1,z2),g3(z1,z2)]
```
MFB( [1,1], 3 )
```
```
f[0,1,1]g2[0,1]g3[1,0] + f[1,0,1]g1[0,1]g3[1,0] + f[1,1,0]g1[0,1]g2[1,0] + f[0,1,1]g2[1,0]g3[0,1] + f[1,0,1]g1[1,0]g3[0,1] + f[1,1,0]g1[1,0]g2[0,1] + f[0,2,0]g2[0,1]g2[1,0] + f[0,1,0]g2[1,1] + f[2,0,0]g1[0,1]g1[1,0] + f[1,0,0]g1[1,1] + f[0,0,2]g3[0,1]g3[1,0] + f[0,0,1]g3[1,1]
```
The coefficient of z1^2 z2 in f[g1(z1,z2),g2(z1,z2)]
```
MFB( [2,1], 2 )
```
```
f[1,2]g1[0,1]g2[1,0]^2 + f[1,1]g1[0,1]g2[2,0] + f[2,1]g1[1,0]^2g2[0,1] + f[1,1]g1[2,0]g2[0,1] + 2f[1,2]g1[1,0]g2[0,1]g2[1,0] + 2f[1,1]g1[1,0]g2[1,1] + 2f[2,1]g1[0,1]g1[1,0]g2[1,0] + 2f[1,1]g1[1,1]g2[1,0] + f[3,0]g1[0,1]g1[1,0]^2 + f[2,0]g1[0,1]g1[2,0] + 2f[2,0]g1[1,0]g1[1,1] + f[1,0]g1[2,1] + f[0,3]g2[0,1]g2[1,0]^2 + f[0,2]g2[0,1]g2[2,0] + 2f[0,2]g2[1,0]g2[1,1] + f[0,1]g2[2,1]
```
The coefficient of z1^2 z2 in f[g1(z1,z2),g2(z1,z2),g3(z1,z2)]
```
MFB( [2,1], 3 )
```
```
Not displayed for readibility reasons
```
The coefficient of z1 z2 z3 in f[g1(z1,z2,z3),g2(z1,z2,z3),g3(z1,z2,z3)]
```
MFB( [1,1,1], 3 )
```
### MFB2Set
#### Description
Secondary function useful for manipulating the result of the MFB function.
#### Usage
```
MFB2Set(sExpr="")
```
#### Argument
sExpr : the output of the MFB function
#### Value
set, a set
#### Examples
# Run 
```
MFB([3], 1)
```
to generate f[3]g[1]^3 + 3f[2]g[1]g[2] + f[1]g[3]
Convert the output of the MFB(c(3),1) into a vector using
```
import numpy as np

np.array(MFB2Set(MFB([3], 1)))
```
The result is the following:
```
[['1' '1' 'f' '3' '1']
 ['1' '1' 'g' '1' '3']
 ['2' '3' 'f' '2' '1']
 ['2' '1' 'g' '1' '1']
 ['2' '1' 'g' '2' '1']
 ['3' '1' 'f' '1' '1']
 ['3' '1' 'g' '3' '1']]
```
### mkmSet
#### Description
The function returns all the partitions of a multi-index, that is a vector of non-negative integers.
Note that these partitions correspond to the subdivisions of a multiset having the input multi-index
as multiplicities.
#### Usage
```
mkmSet(vPar=None, vOutput=False)
```
#### Argument
vPar : vector of non-negative integers

vOutput : optional boolean variable. If equal to TRUE, the function produces a compact
output that is easy to read.
#### Value
list, two-dimensional list: in the first there is the partition, while in the second there
is its multiplicity
#### Examples
Returns [ [[1,1,1],1], [[1,2],3], [[3],1] ]

3 is the multiplicity of a multiset with 3 elements all equal
```
mkmSet([3])
```
```
[[[1, 1, 1], 1], [[1, 2], 3], [[3], 1]]
```
Returns [[[[0, 1], [1, 0], [1, 0]], 1], [[[0, 1], [2, 0]], 1], [[[1, 0], [1, 1]], 2], [[[2, 1]], 1]]

(2,1) is the multiplicity of a multiset with 2 equal elements and a third distinct element
```
mkmSet([2,1])
```
```
[[[[0, 1], [1, 0], [1, 0]], 1], [[[0, 1], [2, 0]], 1], [[[1, 0], [1, 1]], 2], [[[2, 1]], 1]]
```
Or (same output)
```
mkmSet([2,1], False)
```
```
[[[[0, 1], [1, 0], [1, 0]], 1], [[[0, 1], [2, 0]], 1], [[[1, 0], [1, 1]], 2], [[[2, 1]], 1]]
```
Returns the same output of the previous example but in a compact form.
```
mkmSet([2,1], True)
```
```
[(0 1) (1 0) (1 0), 1 ]
[(0 1) (2 0), 1 ]
[(1 0) (1 1), 2 ]
[(2 1), 1 ]


None
```
### mkT
#### Description
Given a multi-index, that is a vector of non-negative integers and a positive integer n, the function
returns all the lists $(v_1,...,v_n)$ of non-negative integer vectors, with the same lenght of the multiindex and such that $v=v_1+...+v_n$.

#### Usage
```
mkT(v=[], n=0, vOutput=False)
```
#### Argument
v : vector of integers

n : integer, number of addends

vOutput : optional boolean variable. If equal to TRUE, the function produces a compact
output that is easy to read.

#### Value
list, the list of n vectors $(v_1,...,v_n)$
#### Warnings
The vector in the first variable must be not empty and must contain all non-negative integers. The
second parameter must be a positive integer
#### Examples
Returns the scompositions of the vector (1,1) in 2 vectors of 2 non-negative integers
such that their sum is (1,1), that is

([1,1],[0,0]) - ([0,0],[1,1]) - ([1,0],[0,1]) - ([0,1],[1,0])
```
mkT([1,1], 2)
```
```
[[[0, 1], [1, 0]], [[1, 0], [0, 1]], [[1, 1], [0, 0]], [[0, 0], [1, 1]]]
```
Or (same output)
```
mkT(|1,1], 2, False)
```
```
[[[0, 1], [1, 0]], [[1, 0], [0, 1]], [[1, 1], [0, 0]], [[0, 0], [1, 1]]]
```
Returns the scompositions of the vector (1,0,1) in 2 vectors of 3 non-negative integers
such that their sum gives (1,0,1), that is

([1,0,1],[0,0,0]) - ([0,0,0],[1,0,1]) - ([1,0,0],[0,0,1]) - ([0,0,1],[1,0,0]).

Note that the second value in each resulting vector is always zero.
```
mkT([1,0,1], 2)
```
```
[[[0, 0, 1], [1, 0, 0]], [[1, 0, 0], [0, 0, 1]], [[1, 0, 1], [0, 0, 0]], [[0, 0, 0], [1, 0, 1]]]
```
Or (same output)
```
mkT([1,0,1], 2, False)
```
```
[[[0, 0, 1], [1, 0, 0]], [[1, 0, 0], [0, 0, 1]], [[1, 0, 1], [0, 0, 0]], [[0, 0, 0], [1, 0, 1]]]
```
Returns the same output of the previous example but in a compact form.
```
mkT([1,0,1], 2, True)
```
```
[( 0 0 1 )( 1 0 0 )]
[( 1 0 0 )( 0 0 1 )]
[( 1 0 1 )( 0 0 0 )]
[( 0 0 0 )( 1 0 1 )]
None
```
Returns the scompositions of the vector (1,1,1) in 3 vectors of 3 non-negative integers
such that their sum gives (1,1,1). The result is given in a compact form.
```
for m in mkT([1, 1, 1], 3):
    for n in m:
        print(n, end=" - ")
    print()
```
### mom2cum
#### Description
The function compute a simple or a multivariate moment in terms of simple or multivariate cumulants.
#### Usage
```
mom2cum(n=1)
```
#### Argument
n : integer or vector of integers
#### Value
str : the expression of the moment in terms of cumulants
#### Warnings
The value of the first parameter is the same as the MFB function in the univariate with univariate case
composition and in the univariate with multivariate case composition.
#### Examples
Returns the simple moment m[5] in terms of the simple cumulants k[1],...,k[5].
```
mom2cum(5)
```
```
k[1]^5 + 10k[1]^3k[2] + 15k[1]k[2]^2 + 10k[1]^2k[3] + 10k[2]k[3] + 5k[1]k[4] + k[5]
```
Returns the multivariate moment m[3,1] in terms of the multivariate cumulants k[i,j] for
i=0,1,2,3 and j=0,1.
```
mom2cum([3,1])
```
```
k[0,1]k[1,0]^3 + 3k[0,1]k[1,0]k[2,0] + k[0,1]k[3,0] + 3k[1,0]^2k[1,1] + 3k[1,0]k[2,1] + 3k[1,1]k[2,0] + k[3,1]
```
### mpCart 
#### Description
Given two lists with elements of the same type, the function returns a new list whose elements are
the joining of the two original lists, except for the last elements, which are multiplied.
#### Usage
```
mpCart(m1=None, m2=None)
```
#### Argument
M1 : list of vectors

M2 : list of vectors

#### Value
list, the list with the joined input lists
#### Examples
```
A = [[[ [1], [2] ], -1],[[ [3] ], 1]]
```
where

-1 is the multiplicative factor of [[1],[2]]

1 is the multiplicative factor of [[3]]
```
B = [[[ [5] ], 7]]
```
where 7 is the multiplicative factor of [[5]]

Return [[[1],[2],[5]], -7] , [[[3],[5]], 7]
```
mpCart(A,B)
```
```
[[[[1], [2], [5]], -7], [[[3], [5]], 7]]
```
```
A = [[[ [1, 0], [1, 0] ], -1], [[ [2, 0] ], 1]]
```
where

- 1 is the multiplicative factor of [[1,0],[1,0]]
  
1 is the multiplicative factor of [[2,0]]
```
B = [[[ [1, 0] ], 1]]
```
where 1 is the multiplicative factor of [[1,0]]

Return [[[1,0],[1,0],[1,0]], -1], [[[2,0],[1,0]],1]
```
mpCart(A,B)
```
```
[[[[1, 0], [1, 0], [1, 0]], -1], [[[2, 0], [1, 0]], 1]]
```
### nKM
#### Description
Given a multivariate data sample, the function returns an estimate of a joint (or multivariate) cumulant with a fixed order
#### Usage
```
nKM(v=None, V=None)
```
#### Argument
v : vector of integers

V : vector of a multivariate data sample
#### Value
float, the value of the multivariate k-statistics
#### Warnings
The size of each data vector must be equal to the length of the vector passed trough the first input
variable.
#### Examples
###### Data assignment
```
data1 = [
    [5.31, 11.16], [3.26, 3.26], [2.35, 2.35], [8.32, 14.34], [13.48, 49.45],
    [6.25, 15.05], [7.01, 7.01], [8.52, 8.52], [0.45, 0.45], [12.08, 12.08], [19.39, 10.42]
]
```
Returns an estimate of the joint cumulant k[2,1]
```
nKM([2,1], data1)
```
```
-23.737902999999278
```
###### Data assignment
```
data2 = [
    [5.31, 11.16, 4.23], [3.26, 3.26, 4.10], [2.35, 2.35, 2.27],
    [4.31, 10.16, 6.45], [3.1, 2.3, 3.2], [3.20, 2.31, 7.3]
]
```
Returns an estimate of the joint cumulant k[2,2,2]
```
nKM([2,2,2], data2)
```
```
678.1045339247212
```
###### Data assignment
```
data3 = [
    [5.31, 11.16, 4.23, 4.22], [3.26, 3.26, 4.10, 4.9], [2.35, 2.35, 2.27, 2.26],
    [4.31, 10.16, 6.45, 6.44], [3.1, 2.3, 3.2, 3.1], [3.20, 2.31, 7.3, 7.2]
]
```
Returns an estimate of the joint cumulant k[2,1,1,1]
```
nKM([2,1,1,1], data3)
```
```
32.053913213909254
```
### nKS
#### Description
Given a data sample, the function returns an estimate of a cumulant with a fixed order.
#### Usage
```
nKS(v=None, V=None)
```
#### Argument
v : integer or one-dimensional vector

V : vector of a data sample

#### Value
float, the value of the k-statistics
#### Examples
```
data = [
    16.34, 10.76, 11.84, 13.55, 15.85, 18.20, 7.51, 10.22, 12.52, 14.68, 16.08,
    19.43, 8.12, 11.20, 12.95, 14.77, 16.83, 19.80, 8.55, 11.58, 12.10, 15.02,
    16.83, 16.98, 19.92, 9.47, 11.68, 13.41, 15.35, 19.11
]
```
```
nKS(7, data)
```
Returns an estimate of the cumulant of order 7
```
```
1322.8183753490448
```
nKS(1, data)
```
Returns an estimate of the cumulant of order 1, that is the mean
```
```
14.021666666666672
```
nKS(2, data)
```
Returns an estimate of the cumulant of order 2, that is the variance
```
12.650069540229737
```
```
nKS(3, data) / (nKS(2, data) ** 0.5) ** 3
```
Returns an estimate of the skewness
```
-0.03216229420531556
```
```
nKS(4, data) / nKS(2, data) ** 2 + 3
```
Returns an estimate of the kurtosis
```
2.114707796531899
```
### nPerm
#### Description
The function returns all possible different permutations of objects in a list or in a vector
#### Usage
```
nPerm(L=[])
```
#### Argument
L : list
#### Value
list, all the permutations of L
#### Examples
permutations of 1,2,3
```
nPerm( [1,2,3] )
```
```
[[3, 1, 2], [1, 3, 2], [1, 2, 3], [3, 2, 1], [2, 3, 1], [2, 1, 3]]
```
permutations of 1,2,1 (two elements are equal)
```
nPerm( [1,2,1] )
```
```
[[1, 1, 2], [1, 2, 1], [2, 1, 1]]
```
permutations of the words "Alice", "Bob","Jack"
```
nPerm( ["Alice", "Bob","Jack"] )
```
```
[['Jack', 'Alice', 'Bob'], ['Alice', 'Jack', 'Bob'], ['Alice', 'Bob', 'Jack'], ['Jack', 'Bob', 'Alice'], ['Bob', 'Jack', 'Alice'], ['Bob', 'Alice', 'Jack']]
```
permutations of the vectors [0,1], [2,3], [7,3]
```
nPerm( [[0,1], [2,3], [7,3]] )
```
```
[[[7, 3], [0, 1], [2, 3]], [[0, 1], [7, 3], [2, 3]], [[0, 1], [2, 3], [7, 3]], [[7, 3], [2, 3], [0, 1]], [[2, 3], [7, 3], [0, 1]], [[2, 3], [0, 1], [7, 3]]]
```
### nPM
#### Description
Given a multivariate data sample, the function returns an estimate of a product of joint cumulants
with fixed orders.

#### Usage
```
nPM(v=None, V=None)
```
#### Argument
v : list of integer vectors

V : vector of a multivariate data sample

#### Value
float, the estimate of the multivariate polykay
#### Examples
Data asignment
```
data1 = [
    [5.31, 11.16], [3.26, 3.26], [2.35, 2.35], [8.32, 14.34], [13.48, 49.45],
    [6.25, 15.05], [7.01, 7.01], [8.52, 8.52], [0.45, 0.45], [12.08, 12.08], [19.39, 10.42]
]
```
Returns an estimate of the product k[2,1]*k[1,0], where k[2,1] and k[1,0] are the
cross-correlation of order (2,1) and the marginal mean of the population distribution
respectively
```
nPM([[2, 1], [1, 0]], data1)
```
```
48.43242806555327
```
Data asignment
```
data2 = [
    [5.31, 11.16, 4.23], [3.26, 3.26, 4.10], [2.35, 2.35, 2.27],
    [4.31, 10.16, 6.45], [3.1, 2.3, 3.2], [3.20, 2.31, 7.3]
]
```
Returns an estimate of the product k[2,0,1]*k[1,1,0], where k[2,0,1] and k[1,1,0]
are joint cumulants of the population distribution
```
nPM([[2, 0, 1], [1, 1, 0]], data2)
```
```
-0.9858162208170143
```
### nPolyk 
#### Description
The master function executes one of the functions to compute simple k-statistics (nKS), multivariate
k-statistics (nKM), simple polykays (nPS) or multivariate polykays (nPM).
#### Usage
```
nPolyk(L=None, data=None, bhelp=None)
```
#### Argument
L : vector of orders

data : vector of a (univariate or multivariate) sample data

bhelp : boolean

#### Value
float, the estimate of the (joint) cumulant or of the (joint) cumulant product
#### Examples
Data assignment
```
data1 = [
    16.34, 10.76, 11.84, 13.55, 15.85, 18.20, 7.51, 10.22, 12.52, 14.68, 16.08,
    19.43, 8.12, 11.20, 12.95, 14.77, 16.83, 19.80, 8.55, 11.58, 12.10, 15.02,
    16.83, 16.98, 19.92, 9.47, 11.68, 13.41, 15.35, 19.11
]
```
Displays "KS: -1.4470595032807978" which indicates the type of subfunction (nKS) called by
the master function nPolyk and gives the estimate of the third cumulant
```
nPolyk([3], data1, True)
```
```
KS:
-1.4470595032807978
```
Displays " -1.4470595032807978" (without the indication of the employed subfunction)
```
nPolyk([3], data1, False)
```
```
-1.4470595032807978
```
Displays "PS: 177.42329372003013" which indicates the type of subfunction (nPS) called by
the master function nPolyk and gives the estimate of the product between the
variance k[2] and the mean k[1]
```
nPolyk([[2], [1]], data1, True)
```
```PS:
177.42329372003013
```

Data assignment
```
data2 = [
    [5.31, 11.16], [3.26, 3.26], [2.35, 2.35], [8.32, 14.34], [13.48, 49.45],
    [6.25, 15.05], [7.01, 7.01], [8.52, 8.52], [0.45, 0.45], [12.08, 12.08], [19.39, 10.42]
]
```
Displays "KM: -23.737902999999278" which indicates the type of subfunction (nKM) called by
the master function nPolyk and gives the estimate of k[2,1]
```
nPolyk([2, 1], data2, True)
```
```
KM:
-23.737902999999278
```
Displays "PM: 48.43242806555327" which indicates the type of subfunction (nPM) called by
the master function nPolyk and gives the estimate of k[2,1]*k[1,0]
```
nPolyk([[2, 1], [1, 0]], data2, True)
```
```
PM:
48.43242806555327
```
### nPS
#### Description
Given a data sample, the function returns an estimate of a product of cumulants with fixed orders.
#### Usage
```
nPS(v=None, V=None)
```
#### Argument
v : vector of integers

V : vector of a data sample
#### Value
float, the estimate of the polykay
#### Examples
Data assignment
```
data = [
    16.34, 10.76, 11.84, 13.55, 15.85, 18.20, 7.51, 10.22, 12.52, 14.68, 16.08,
    19.43, 8.12, 11.20, 12.95, 14.77, 16.83, 19.80, 8.55, 11.58, 12.10, 15.02,
    16.83, 16.98, 19.92, 9.47, 11.68, 13.41, 15.35, 19.11
]
```
Returns an estimate of the product k[2]*k[1], where k[1] and k[2] are the mean and
the variance of the population distribution respectively
```
nPS([2, 1], data)
```
```
177.42329372003013
```
### nStirling2 
#### Description
The function computes the Stirling number of the second kind.
#### Usage
```
nStirling2(n, k)
```
#### Argument
n : integer

k : integer less or equal to n

#### Value
int, the Stirling number of the second kind
#### Examples
Returns the number of ways to split a set of 6 objects into 2 nonempty subsets
```
nStirling2(6,2)
```
```
31
```
### oBellPol
#### Description
The function generates a complete or a partial ordinary Bell polynomial.
#### Usage
```
oBellPol(n=1, m=0)
```
#### Argument
n : integer, the degree of the polynomial

m : integer, the fixed degree of each monomial in the polynomial
#### Value
str, the expression of the polynomial
#### Warning
The value of the first parameter is the same as the MFB function in the univariate with univariate
composition.
#### Examples
Returns the complete ordinary Bell Polynomial for n=5, that is

(y1^5) + 20(y1^3)(y2) + 30(y1)(y2^2) + 60(y1^2)(y3) + 120(y2)(y3) + 120(y1)(y4) + 120(y5)
```
oBellPol(5)
```
```
1/120*( 120(y1**5) + 480(y1**3)(y2) + 360(y1)(y2**2) + 360(y1**2)(y3) + 240(y2)(y3) + 240(y1)(y4) + 120.0(y5) )
```
Or (same output)
```
oBellPol(5,0)
```
```
1/120*( 120(y1**5) + 480(y1**3)(y2) + 360(y1)(y2**2) + 360(y1**2)(y3) + 240(y2)(y3) + 240(y1)(y4) + 120.0(y5) )
```
Returns the partial ordinary Bell polynomial for n=5 and m=3, that is

30(y1)(y2^2) + 60(y1^2)(y3)
```
oBellPol(5,3)
```
```
1/120*( 360(y1)(y2**2) + 360(y1**2)(y3) )
```
### pCart
#### Description
The function returns the cartesian product between vectors.
#### Usage
```
pCart( L )
```
#### Argument
L : list of lists
#### Value
list, the list with the cartesian product
#### Examples
```
A = [1, 2]
B = [3, 4, 5]
```
Returns the cartesian product [[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]]
```
pCart([A, B])
```
```
[[1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]]
```
```
L1 = [[1, 1], [2]]
L2 = [[5, 5], [7]]
```
Return the cartesian product [[1,1],[5,5]], [[1,1],[7]], [[2],[5,5]], [[2],[7]]
and assign the result to L3
```
L3 = pCart([L1, L2])
print(L3)
```
```
[[[1, 1], [5, 5]], [[1, 1], [7]], [[2], [5, 5]], [[2], [7]]]
```
Returns the cartesian product between L3 and [7].

The result is [[1,1],[5,5],[7]], [[1,1],[7],[7]], [[2],[5,5],[7]], [[2],[7],[7]]
```
result = pCart([L3, [7]])
print(result)
```
```
[[[1, 1], [5, 5], [7]], [[1, 1], [7], [7]], [[2], [5, 5], [7]], [[2], [7], [7]]]
```
### powS 
#### Description
The function returns the value of the power sum symmetric polynomial, with fixed degrees and in
one or more sets of variables, when the variables are substituted with the input lists of numerical
values.
#### Usage
```
powS(vn=None, lvd=None)
```
#### Arguments
vn : vector of integers (the powers of the indeterminates)

lvd : list of numerical values in place of the variables

#### Value
int, the value of the polynomial

#### Examples
Returns 1^3 + 2^3 + 3^3 = 36
```
powS([3], [[1], [2], [3]])
```
```
36
```
Returns (1^3 * 4^2) + (2^3 * 5^2) + (3^3 * 6^2) = 1188
```
powS([3, 2], [[1, 4], [2, 5], [3, 6]])
```
```
1188
```
### pPart
#### Description
The function generates the partition polynomial of degree n, whose coefficients are the number of
partitions of n into k parts for k from 1 to n
#### Usage
```
pPart(n=0)
```
#### Argument
n : integer, the degree of the polynomial
#### Value
str, the expression of the polynomial
#### Warning
The value of the first parameter is the same as the MFB function in the univariate with univariate case
composition.

#### Examples
Returns the partition polynomial F[5]
```
pPart(5)
```
```
y^5 + y^4 + 2y^3 + 2y^2 + y
```
### pPoly
#### Description
The function returns the product between polynomials without constant term.
#### Usage
```
pPoly(L=None)
```
#### Argument
L : lists of the coefficients of the polynomials
#### Value
list, the coefficients of the polynomial output of the product
#### Examples
[1,-3] are the coefficients of (x-3x^2), [2] is the coefficient of 2x

Returns [0, 2,-6], coefficients of 2x^2-6x^3 =(x-3x^2)*(2x)

```
pPoly([ [1, -3], [2] ])
```
```
[0, 2, -6]
```
[0,3,-2] are the coefficients of 3x^2-2x^3, [0,2,-1] are the coefficients of (2x^2-x^3)

Return [0,0,0,6,-7,2], coefficients of 6x^4-7x^5+2x^6=(3x^2-2x^3)*(2x^2-x^3)
```
pPoly([ [0, 3, -2], [0, 2, -1] ])
```
```
[0, 0, 0, 6, -7, 2]
```
### Set2expr
#### Description
The function converts a set into a string.
#### Usage
```
Set2expr(v=None)
```
#### Argument
v : set
#### Value
str, the string
#### Examples
To print 6f[3]^2g[2]^5 run
```
Set2expr( [["1","2","f","3","2"],["1","3","g","2","5"]])
```
```
6.0f[3]^2g[2]^5
```
### Evaluate
#### Description
Calculate the value of a given cumulant (from known moments) or moment (from known cumulants).
#### Usage
```
evaluate(s=None, S=None)
```
#### Argument
s : a string containing the values of the moments or cumulants

S : the string to evaluate
#### Value
float, the numerical value of the cumulant/moment
#### Examples

Run 
```
cum2mom(5)
```
to get the cumulant of order 5, that is
```
24m[1]^5 - 60m[1]^3m[2] + 30m[1]m[2]^2 + 20m[1]^2m[3] - 10m[2]m[3] - 5m[1]m[4] + m[5]
```
Then, to calculate the value of the above cumulant given the moments up to order 5 

m[1]=1, m[2]=2, m[3]=3, m[4]=4, m[5]=5.

run 
```
evaluate('m[1]=1, m[2]=2, m[3]=3, m[4]=4, m[5]=5', '24m[1]^5 - 60m[1]^3m[2] + 30m[1]m[2]^2 + 20m[1]^2m[3] - 10m[2]m[3] - 5m[1]m[4] + m[5]')
```
The output is
```
9.0
```
To get the same output, run
```
evaluate('m[1]=1, m[2]=2, m[3]=3, m[4]=4, m[5]=5', cum2mom(5))
```
```
9.0
```
When a value is missing, an error occurs:
```
print(evaluate('m[1]=1, m[2]=2, m[3]=3, m[5]=5', cum2mom(5)))
```
```
ValueError: Undefined variables in expression: ['m[4]']
```
The function is also usable for mom2cum. For example run
```
mom2cum(4)
```
to get
```
k[1]^4 + 6k[1]^2k[2] + 3k[2]^2 + 4k[1]k[3] + k[4]
```
To evaluate the above expression with 
```
k[1] = 2, k[2] = 4, k[3] = 6, k[4] = 8
```
run
```
evaluate('k[1] = 2, k[2] = 4, k[3] = 6, k[4] = 8', 'k[1]^4 + 6k[1]^2k[2] + 3k[2]^2 + 4k[1]k[3] + k[4]')
```
```
216.0
```
Or (same output)
```
evaluate('k[1] = 2, k[2] = 4, k[3] = 6, k[4] = 8', mom2cum(4))
```
```
216.0
```
and if a value is missing
```
evaluate('k[1] = 2, k[2] = 6, k[4] = 8', 'k[1]^4 + 6k[1]^2k[2] + 3k[2]^2 + 4k[1]k[3] + k[4]')
```
```
ValueError: Undefined variables in expression: ['k[3]']
```
Finally, if one tries to evaluate cum2mom giving in input cumulant values instead of moment values, the function produces the following error:
```
evaluate('k[1] = 2, k[2] = 4, k[3] = 6, k[4] = 8', cum2mom(5))
```
```
ValueError: Trying to evaluate cum2mom with values of cumulants
```
or the other way round
```
evaluate('m[1]=1, m[2]=2, m[3]=4, m[4]=3', mom2cum(4))
```
```
ValueError: Trying to evaluate mom2cum with values of moments
```
