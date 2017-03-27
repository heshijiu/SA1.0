#!/usr/bin/Python
# -*- coding: utf-8 -*-
import StockDataSets
import pandas as pd
import sqlite3
def GetAllTableNameInDB():
    con = sqlite3.connect("Stock.sqlite")
    cur = con.cursor()
    sql = "select name from sqlite_master where type='table'"
    cur.execute(sql)
    name = cur.fetchall()
    tableName = []
    for element1 in name:
        for element2 in element1:
            tableName.append(element2)
    con.close()
    return tableName
def DownLoadCSVFile(stockCode, start, end):
    stock = StockDataSets.StockData(stockCode)
    stock.GetCSVFile(start, end)
    return
def UpdateCSVFile(stockCode):
    stock = StockDataSets.StockData(stockCode)
    stock.UpdateCSVFile()
    return
def CreatTableInDB(stockCode):
    stock = StockDataSets.StockData(stockCode)
    stock.CreatTableInDB()
    return
def UpdateTableInDB(stockCode):
    stock = StockDataSets.StockData(stockCode)
    df = stock.UpdateTableInDB()
    return df
def GetXdata(stockCode, type = 'db'):
    if type == 'db':
        con = sqlite3.connect("Stock.sqlite")
        sql = "select * from" + " " + "'" + stockCode + "'"
        df = pd.read_sql(sql, con)
        con.close()
    if type == 'csv':
        filename = stockCode + '.csv'
        df = pd.read_csv(filename)
    totalCount = len(df['close'])
    X = []
    i = 0
    while i < totalCount:
        data = []
        data.append(df['open'][i])
        data.append(df['high'][i])
        data.append(df['close'][i])
        data.append(df['low'][i])
        data.append(df['volume'][i])
        data.append(df['price_change'][i])
        data.append(df['p_change'][i])
        data.append(df['ma5'][i])
        data.append(df['ma10'][i])
        data.append(df['ma20'][i])
        data.append(df['v_ma5'][i])
        data.append(df['v_ma10'][i])
        data.append(df['v_ma20'][i])
        data.append(df['turnover'][i])
        data.append(df['bIn'][i])
        data.append(df['bOut'][i])
        data.append(df['sIn'][i])
        data.append(df['sOut'][i])
        X.append(data)
        i += 1
    return X
def GetClosePrice(stockCode, type = 'db', days = 8):
    if type == 'db':
        con = sqlite3.connect("Stock.sqlite")
        sql = "select * from" + " " + "'" + stockCode + "'"
        df = pd.read_sql(sql, con)
        con.close()
    if type == 'csv':
        filename = stockCode + '.csv'
        df = pd.read_csv(filename)
    totalCount = days
    X = []
    i = 0
    while i < totalCount:
        data = []
        data.append(df['close'][i])
        X.append(data)
        i += 1
    return X

def NormalData(X):
     nArray = len(X)
     data = X.copy()
     nColoum = len(X[0])
     i = 0
     while i < nColoum:
         totalValue = 0
         j = 0
         while j < nArray:
             totalValue += data[j][i]
             j += 1
         #if nArray > 0:
             # totalValue /= nArray
         if abs(totalValue) > 0.0001:
             j = 0
             while j < nArray:
                 data[j][i] /= totalValue
                 j += 1
         i += 1
     return data




