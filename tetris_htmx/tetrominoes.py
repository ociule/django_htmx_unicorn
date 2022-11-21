I = 1
O = 2
T = 3
J = 4
L = 5
S = 6
Z = 7

from enum import Enum
class Tetrominoes(Enum):
    I = I
    O = O
    T = T
    J = J
    L = L
    S = S
    Z = Z

#Tetrominoes = [I, O, T, J, L, S, Z]
#Tetrominoes.I = I
Tetrominoes.I.height = 4
Tetrominoes.I.footprint = [[I], [I], [I], [I]]
#Tetrominoes.O = O
Tetrominoes.O.height = 2
Tetrominoes.O.footprint = [[O, O, ], [O, O]]
#Tetrominoes.T = T
Tetrominoes.T.height = 2
Tetrominoes.T.footprint = [[T, T, T], [0, T, 0]]
#Tetrominoes.J = J
Tetrominoes.J.height = 3
Tetrominoes.J.footprint = [[0, J], [0, J], [J, J]]
#Tetrominoes.L = L
Tetrominoes.L.height = 3
Tetrominoes.L.footprint = [[L, 0], [L, 0], [L, L]]
#Tetrominoes.S = S
Tetrominoes.S.height = 2
Tetrominoes.S.footprint = [[0, S, S], [S, S, 0]]
#Tetrominoes.Z = Z
Tetrominoes.Z.height = 2
Tetrominoes.Z.footprint = [[Z, Z, 0], [0, Z, Z]]
