# coding: utf-8
import csv
import sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

f = open('noclotho.csv')
r = csv.reader(f)
# 13, 14, 15

for csvrow in r:
    cur.execute("update funders set chosen=? where flow_number=?", [csvrow[14], csvrow[13].rstrip("'")])
con.commit()
con.close()
f.close()
