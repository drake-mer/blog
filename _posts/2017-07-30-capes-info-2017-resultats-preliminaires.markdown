------------------------
layout: post
title:  "Épreuve d'informatique au capes de maths"
date:   2017-07-30 14:20:34 +0200
categories: jekyll update debian static blogging
published: false
------------------------

# Partie A

## Question 1

Il s'agit de montrer que la somme des chiffres 
présents dans une grille complète fait 45 pour respectivement :
- un carré
- une ligne
- une colonne

Nous pouvons raisonner sur une ligne sans perte de généralité.

Soit un ensemble de 9 chiffres noté $\mathcal{N}$, composé
d'entiers $n$ tels que $n\in |[1, 9]|$ ($1\leq n\leq 9$).

Alors si tous ces entiers sont distincts deux à deux, leur somme
est :
$$ \sum_{i=1}^{9} i = \frac{9\times 10}{2} = 45$$
D'après la formule connue de la somme des termes d'une suite arithmétique.

Supposons maintenant que notre ensemble contienne 9 chiffres, non nécessairement
distincts deux à deux. On devra substituer à la somme précédente le nombre
manquant (il n'y a que neuf chiffres possibles dans cet ensemble) et le
remplacer par un autre. La somme sera donc nécessairement différente
de 45. QED.

## Question 2

Une ligne n'est pas valide si elle contient un zéro ou si la somme
de ses chiffres est différente de 45.

En python nous pouvons écrire :

```python

def is_valid_line(line_number, grid):
    return 0 not in grid[line_number] and sum(grid[line_number])==45
```

La méthode est semblable pour un carré ou une colonne.

## Question 3 : validation du sudoku

Un sudoku est valide si et seulement si tous ses carrés, toutes
ses lignes et toutes ses colonnes ont une somme égale à 45 sans contenir
de chiffre supérieur à 9.

La validation peut donc se faire séquentiellement via un appel
itéré aux fonction is_line_valid, is_column_valid, is_square_valid.

## Question 4

```python

def ligne(L, i):
    chiffre = []
    for j in range(9):
        if L[i][j] > 0:
            chiffre.append(L[i][j])
    return chiffre
```
Remarque, on peut écrire les choses de manière plus
concise en python :

```python

def ligne(L, i):
    return [ chiffre for chiffre in L[i] if chiffre>0 ]
```

De même pour une colonne :

```python

def colonne(L, i):
    return [ chiffre for chiffre in list(zip(*L))[i] if chiffre>0 ]
```

## Question 5

Soit une case quelconque du Sudoku de coordonnées
(i,j).

Posons un nouveau système de coordonnées qui
servira à désigner les carrés 3x3 du Sudoku.

Notons (I,J) ce nouveau système de coordonnées,
avec (I,J) \in \{0,1,2\}^2. De gauche à droite
et de bas en haut, les coordonnées de ces carrés
sont 

(0,0) -> premier carré
(0,1) -> second carré
(0,2) -> troisième
(1,0) -> quatrième
...
(2,2) -> neuvième carré

On voit aisément que :
* si 0<=i<=2, alors I = 0
* si 3<=i<=5, alors I = 1
* si 6<=i<=8, alors I = 2

De même, pour les colonnes, nous avons :
* si 0<=j<=2, alors J = 0
* si 3<=j<=5, alors J = 1
* si 6<=j<=8, alors J = 2

De manière plus générique, on peut écrire:
$$
\forall (i,j) \in |[0,8]|^2, (I,J) = (i/3, j/3)
$$
où l'opérateur $/$ désigne le quotient de la
division euclidienne.

Réciproquement, la case supérieure gauche
de n'importe quel carré de coordonnées (I,J)
a pour coordonnée dans le Sudoku
(i,j) = (I*3, J*3).

D'où le résultat demandé.

## Question 6

La fonction demandée est :
```python
def carre(L, i, j):
    icoin = 3*(i//3)
    jcoin = 3*(j//3)
    chiffre = []
    for i in range(3):
        for j in range(3):
            if L[icoin+i][jcoin+j] > 0:
                chiffre.append(L[icoin+i][jcoin+j])
    return chiffre
```

Ou plus simple avec les itertools :

```python
from itertools import product

def carre(L, i, j):
    icoin, jcoin = 3*(i//3), 3*(j//3)
    coord_map = product(range(icoin,icoin+3),range(jcoin,jcoin+3))
    return [L[l][c] for l, c in coord_map if L[l][c]>0]
```

## Question 7

On cherche à connaître l'ensemble des possibilités pour une case donnée.

On utilise les méthodes implémentées précédemment.
