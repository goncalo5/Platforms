#!/usr/bin/env python
def sign(number):
    return 1 if number >= 0 else -1


def col(color):
    color = color[1:-1].split(',')
    color = (int(n) for n in color)
    return tuple(color)


def backoff(player, obj):
    pass
