#!/usr/bin/Python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import tushare as ts
import sqlite3
import datetime

def GetTickDataInfro(tickData):
    bigIn = 0
    bigOut = 0
    smallIn = 0
    smallOut = 0
    totalCount = len(tickData)
    i = 0
    amount = 200000
    while i < totalCount:
        if tickData[i][5] == "卖盘":
            if int(tickData[i][4]) >= amount:
                bigOut += float(tickData[i][4])
            else:
                smallOut += float(tickData[i][4])
        if tickData[i][5] == "买盘":
            if int(tickData[i][4]) >= amount:
                bigIn += float(tickData[i][4])
            else:
                smallIn += float(tickData[i][4])
        i += 1
    total = bigIn + bigOut + smallIn + smallOut
    if abs(total) < 0.00000001:
        a = [0,0,0,0]
    else:
        a = [bigIn / total, bigOut / total, smallIn / total, smallOut / total]
    return a

def GetNowDate():
    nowTime = datetime.datetime.now()
    date = nowTime.strftime("%Y-%m-%d")
    return date
def GetNextDate(date):
    startTime = datetime.datetime.strptime(date, "%Y-%m-%d")
    startTime = startTime + datetime.timedelta(days=1)
    nextDate = startTime.strftime("%Y-%m-%d")
    return nextDate

class StockData:
    __stockCode = None
    __df = None
    def __init__(self, stockCode):
        self.__stockCode = stockCode
    def GetStockData(self,start, end):
        df = ts.get_hist_data(self.__stockCode,start, end)
        bIn = []
        bOut = []
        sIn = []
        sOut = []
        for dates in df.index:
            tickData = ts.get_tick_data(self.__stockCode,dates, retry_count=8)
            monyeFlow = GetTickDataInfro(tickData.values)
            bIn.append(monyeFlow[0])
            bOut.append(monyeFlow[1])
            sIn.append(monyeFlow[2])
            sOut.append(monyeFlow[3])
            print("Loading")
        df['bIn'] = np.array(bIn)
        df['bOut'] = np.array(bOut)
        df['sIn'] = np.array(sIn)
        df['sOut'] = np.array(sOut)
        return df

    def GetCSVFile(self, start, end):
        filename = self.__stockCode + '.csv'
        df = self.GetStockData(start, end)
        df.to_csv(filename)
        return

    def UpdateCSVFile(self):
        fileName = self.__stockCode + '.csv'
        dftemp = pd.read_csv(fileName)
        fileDate = dftemp['date'][0]
        dftemp = pd.read_csv(fileName, index_col = 0)
        currentDate = GetNowDate()
        start = GetNextDate(fileDate)
        df = self.GetStockData(start, currentDate)
        df = pd.concat([df,dftemp])
        df.to_csv(fileName)
        return

    def CreatTableInDB(self):
        start = '2013-02-25'
        nowTime = datetime.datetime.now()
        end = nowTime.strftime("%Y-%m-%d")
        #end = '2017-03-02'
        df = self.GetStockData(start, end)
        con = sqlite3.connect("Stock.sqlite")
        df.to_sql(name=self.__stockCode, con=con, flavor='sqlite', if_exists='replace', index = True)
        con.close()
        return
    def UpdateTableInDB(self):
        con = sqlite3.connect("Stock.sqlite")
        tableName = "'" + self.__stockCode + "'"
        sql = "select * from" + " " + tableName
        dftemp = pd.read_sql(sql, con, index_col = 'date')
        sql = "select date from" + tableName
        cur = con.cursor()
        resault = cur.execute(sql)
        Date = resault.fetchall()
        nowTime = datetime.datetime.now()
        currentDate = nowTime.strftime("%Y-%m-%d")
        DBDate = Date[len(Date)-1][0]
        if currentDate != DBDate:
            end = currentDate
            startTime = datetime.datetime.strptime(DBDate, "%Y-%m-%d")
            startTime = startTime + datetime.timedelta(days=1)
            start = startTime.strftime("%Y-%m-%d")
            df = self.GetStockData(start, end)
            df = pd.concat([df, dftemp])
            df.to_sql(name=self.__stockCode, con=con, flavor='sqlite', if_exists='replace', index=True)
        con.close()
        return


