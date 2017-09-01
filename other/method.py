#!/usr/bin/env python3


class Kls(object):
    def __init__(self, data=None):
        self.data = data

    def printd(self):
        print(self.data)

    @staticmethod
    def smethod(*arg):
        print('Static:', arg)

    @classmethod
    def cmethod(cls, *arg):
        print('Class:', arg)

ik = Kls("abc")
Kls.printd(ik)
ik.printd()

Kls.smethod()
ik.smethod()

Kls.cmethod()
ik.cmethod()
