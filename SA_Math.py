#!/usr/bin/Python
# -*- coding: utf-8 -*-

import cmath

class Point:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        self.x += other.x
        self.y += other.y

class Vector:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __init__(self, p1, p2):
        self.x = p2.x - p1.x
        self.y = p2.y - p1.y
    def Dot(self, v):
        dot =self.x * v.x + self.y * v.y
        return dot.real
    def Normal(self):
        m = cmath.sqrt(self.x * self.x + self.y * self.y)
        m = m.real
        if abs(m ) < 0.00000001:
            return 0
        self.x /= m
        self.y /= m
    def Moudl(self):
        m = cmath.sqrt(self.x * self.x + self.y * self.y)
        return m.real

def Transform(array):
    l = len(array)
    s = len(array[0])
    newArray = []
    i = 0
    while i < s:
        j = 0
        temp = []
        while j < l:
            temp.append(array[j][i])
            j += 1
        newArray.append(temp)
        i += 1
    return newArray
class Samples:
    __array = None
    __count = 0
    __mean = 0
    __variance = 0
    def __init__(self, array = None):
        self.__array = array
        self.__count = len(array)
        self.__Mean()
        self.__Variance()
        return

    def __Mean(self):
        if self.__array == None:
            return
        if self.__count == 0:
            return
        sum = 0
        for item in self.__array:
            sum += item
        self.__mean = sum / self.__count
        return

    def __Variance(self):
        if self.__count < 2:
            return
        if self.__array == None:
            return
        sum = 0
        for item in self.__array:
            sum += (item - self.__mean) * (item - self.__mean)
        self.__variance = sum / (self.__count - 1)
        return

    def mean(self):
        return self.__mean
    def variance(self):
        return self.__variance
