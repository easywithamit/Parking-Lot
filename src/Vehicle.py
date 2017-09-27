#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: Amit Kumar
@mail: haywithamit@fb.com
"""
from abc import ABCMeta, abstractmethod


class Vehicle:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._reg_number = None
        self._color = None

    @abstractmethod
    def set_registration(self,registration_number=None):
        pass

    @abstractmethod
    def get_registration(self):
        pass

    @abstractmethod
    def set_color(self, color=None):
        pass

    @abstractmethod
    def get_color(self):
        pass


class Car(Vehicle):
    def __init__(self):
        super(Car, self).__init__()

    def set_registration(self,registration_number=None):
        self._reg_number = registration_number

    def set_color(self, color=None):
        self._color = color

    def get_registration(self):
        return self._reg_number

    def get_color(self):
        return self._color


if __name__ == '__main__':
    v = Car()
    v.set_registration('TS 1432')
    v.set_color('blue')
    print(v.get_color())
    print(v.get_registration())


