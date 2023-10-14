# pylint:disable = all
from math import sqrt
from re import split
from copy import deepcopy


def wash(x: list):
    x: str = ' '.join(x)
    x: list = split(r"[ \n\t]|,", x)
    try:
        while True:
            x.remove('')
    except ValueError:
        pass
    return x


def cosine(x: list, y: list):
    x = wash(x)
    y = wash(y)
    words = list(set(x) | set(y))
    mapp = {}
    vecx = [0 for i in range(len(words))]
    vecy = deepcopy(vecx)
    for i in range(len(words)):
        mapp[words[i]] = i
    for i in x:
        vecx[mapp[i]] += 1
    for i in y:
        vecy[mapp[i]] += 1
    up = sqx = sqy = 0
    for i in range(len(words)):
        up += vecx[i] * vecy[i]
        sqx += vecx[i] ** 2
        sqy += vecy[i] ** 2
    ratio = up / (sqrt(sqx) * sqrt(sqy))
    if ratio < 0:
        ratio = 0.1 * (-ratio)
    return ratio


def jaccard(x: list, y: list):
    x = wash(x)
    y = wash(y)
    inte = len(set(x) & set(y))
    unio = len(set(x) | set(y))
    return inte / unio
