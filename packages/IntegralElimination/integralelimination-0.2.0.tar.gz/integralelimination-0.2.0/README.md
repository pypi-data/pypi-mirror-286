# IntegralElimination

This package implements the integral elimination algortihm described in :  
 
* François Lemaire and Louis Roussel. 
*Contribution to Integral
Elimination*. Accepted at CASC 2024. Apr. 2024. https://hal.science/hal-04570612

The source code is availaible at :
```
https://codeberg.org/louis-roussel/IntegralElimination
```
 
# Installation

* **Using pip**
```
python -m pip install IntegralElimination
```
* **Or by building and installing the package**
```
python -m pip install .
```

# How to use ?
Examples are available in the *examples* folder. 

# Details on the implentation
* This implementation in Python uses the SymPy package.
* The functions implemented are as close as possible to those in the article above.
    * A slight modification as been made to the *update_exp* function to correctly handle exponentials that have already been defined.

# Contact


* [Louis Roussel](https://louis-roussel.github.io/) (louis.roussel@univ-lille.fr), Université de Lille, CNRS, Centrale Lille, UMR 9189 CRIStAL, F-59000 Lille, France

 