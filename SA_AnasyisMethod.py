#!/usr/bin/Python
# -*- coding: utf-8 -*-

import numpy as np
import GetStockData as gd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn import linear_model
import pywt
from scipy import stats
import SA_Math as Math

class AnalysisDirector():
    def __init__(self):
        self.methodBuilder = None
        return

    def Analysis(self):
        self.methodBuilder.Commit()
        return

class MethodBuilder:
    m_stockCode = None

    def __init__(self, code = None):
        self.m_stockCode = code
        return

    def Commit(self):
        return

class Nearest_Neighbors_MethodBuilder(MethodBuilder):
    def __init__(self, code = None, kNeighbors = 3):
        super(Nearest_Neighbors_MethodBuilder,self).__init__()
        self.m_stockCode = code
        self.kNeighbors = kNeighbors
    def Commit(self):
        if self.m_stockCode == None:
            return
        X = gd.GetXdata(self.m_stockCode, type='db')
        count = len(X)
        time = []
        i = 0
        while i < count:
            time.append(count - 1 - i)
            i += 1
        date = np.array(time)
        dataSets = np.array(gd.NormalData(X))
        x = dataSets[1:count, :]
        testPoint = dataSets[0, :]
        nbrs = NearestNeighbors(self.kNeighbors, algorithm='kd_tree').fit(x)
        distances, indices = nbrs.kneighbors(testPoint)
        X = gd.GetXdata(self.m_stockCode, type='db')
        self.ShowResault(np.array(X), date, indices, distances)
        return

    def ShowResault(self,dataSets, date, indices, distances):
        high = dataSets[:, 1]
        close = dataSets[:, 2]
        low = dataSets[:, 3]
        plt.figure()
        plt.plot(date, high)
        plt.plot(date, close)
        plt.plot(date, low)
        i = 0
        for distance in distances[0]:
            plt.plot(date[indices[0, i]], high[indices[0, i]], 'or')
            plt.annotate(str(distance), xy=(date[indices[0, i]], high[indices[0, i]]))
            i += 1
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()

class Wavelets_MethodBuilder(MethodBuilder):
    def __init__(self, code = None, days = 200, type = 'db1',level = 1):
        self.m_stockCode = code
        self.m_days = days
        self.m_waveletsType = type
        self.m_level = level
        return

    def Commit(self):
        single = self.GetSingle()
        reconfigureSingle = self.WaveletsReconfigure(single)
        plt.figure()
        plt.plot(single)
        plt.plot(reconfigureSingle)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()
        return

    def GetSingle(self):
        X = np.array(gd.GetXdata(self.m_stockCode))
        close = X[0:self.m_days, 2]
        single = []
        count = len(close)
        i = 0
        while i < count:
            single.append(close[count - i - 1])
            i += 1
        return single

    def WaveletsReconfigure(self,single):
        cA = pywt.wavedec(single, self.m_waveletsType, level=self.m_level)
        i = 0
        reconfiguredSingle = cA[0]
        while i < self.m_level:
            newsingle = pywt.idwt(reconfiguredSingle, None, self.m_waveletsType)
            reconfiguredSingle = newsingle
            i += 1
        return reconfiguredSingle

class Correlation_MethodBuilder(MethodBuilder):
    def __init__(self, code1 = None, code2 = None, days = 3, display = 1, confidenceLevel = 0.95):
        super(Correlation_MethodBuilder, self).__init__()
        self.m_stockCode = code1
        self.compareStockCode = code2
        self.days = days
        self.displayCount = display
        self.confidenceLevel = confidenceLevel
    def Commit(self):
        closePrice1 = gd.GetClosePrice(self.m_stockCode, days = self.days)
        closePrice2 = gd.GetClosePrice(self.compareStockCode, days = self.days)
        regr = linear_model.LinearRegression()
        regr.fit(closePrice1, closePrice2)
        distance = self.GetDistanceArray(regr, closePrice1, closePrice2, type='List')
        plt.figure()
        self.Plot(regr, closePrice1, closePrice2, distance)
        plt.xlabel('Code1 close price')
        plt.ylabel('Code2 close price')
        plt.show()
        return

    def GetDistanceArray(self,regr, xArray, yArray, type = 'List'):
        w = regr.coef_[0][0]
        b = regr.intercept_[0]
        p1 = Math.Point(0, b)
        p2 = Math.Point(1, w + b)
        v1 = Math.Vector(p1, p2)
        v1.Normal()
        i = 0
        count = len(xArray)
        distanceArray = []
        while i < count:
            temp = []
            x = xArray[i][0]
            y = yArray[i][0]
            pt = Math.Point(x, y)
            v2 = Math.Vector(p1, pt)
            l = abs(v2.Dot(v1))
            s = v2.Moudl()
            d = (s * s - l * l)**0.5
            if y - (w * x + b) < 0 :
                d *= -1
            temp.append(d)
            distanceArray.append(temp)
            i += 1
        if type == 'Array':
            return distanceArray
        if type == 'List':
            temp = Math.Transform(distanceArray)
            distanceArray = temp[0]
            return distanceArray

    def Plot(self, regr, array1, array2, distanceArray):
        distanceSamples = Math.Samples(distanceArray)
        mean = distanceSamples.mean()
        variance = distanceSamples.variance()
        if abs(mean) < 0.00000001:
            mean = 0
        offset = stats.norm.isf((1 - self.confidenceLevel) / 2, loc=mean, scale=variance ** 0.5)
        plt.scatter(array1, array2)
        plt.plot(array1, regr.predict(array1), color = 'blue')
        self.PlotOffsetLine(regr, offset, array1)
        offset = -1 * offset
        self.PlotOffsetLine(regr, offset, array1)
        for i in range(self.displayCount):
            plt.annotate(str(i + 1), xy=(array1[i][0], array2[i][0]))

    def PlotOffsetLine(self, regr, offset = 0, array = None):
        if array == None:
            return
        w = regr.coef_[0][0]
        b = regr.intercept_[0] + (1 + w * w) ** 0.5 * offset
        yPredit = []
        for x in array:
            a = []
            a.append(x[0] * w + b)
            yPredit.append(a)
        plt.plot(array, yPredit, color = 'red')
        return







