#!/usr/bin/python

import MySQLdb as dbapi
import sys
import csv
import commands
import os
from xlsxwriter.workbook import Workbook


#dbServer='10.1.3.23'
#dbPass='jittermysql'
#dbUser='reportes'
#dbSchema='PSA3'

dbServer='127.0.0.1'
dbPass='{MYSQL_PASS}'
dbUser='{MYSQL_USR}'
config="openbravopos.properties"
csvName="reporteCompleto.csv"

home=commands.getoutput("echo $HOME")

#dbSchema=commands.getoutput("egrep 'db\.URL' "+home+"/"+config+" | egrep -o '[a-zA-Z0-9\_]+$'")
dbSchema=commands.getoutput("egrep 'db\.URL' "+home+"/"+config+" | egrep -o '[a-zA-Z0-9\_\?\\=]+$'  | rev | cut -c 15- | rev")

def generateFile(filename) :
	fp=open(filename,'w')
	fp.write("id,fecha,cardcode,series,comments,sku,skuname,quantity,price,discount,codetax,whscode,uticket,usucursal\r\n")
	myFile=csv.writer(fp)
	myFile.writerows(newRows)
	fp.close()
	
	#Agregue strings_to_numbers para quitar apostrofes
	workbook = Workbook(filename[:-4] + '.xlsx', {'strings_to_numbers': True})
	worksheet = workbook.add_worksheet()
	with open(filename, 'rt') as f:
	    reader = csv.reader(f)
	    for r, row in enumerate(reader):
	        for c, col in enumerate(row):
	            worksheet.write(r, c, col)
	workbook.close()




#dbQuery="select 0 as 'id',T0.TICKETID, DATE_FORMAT( T3.DATENEW, '%d-%m-%Y %T') as 'fecha',T5.NAME as 'cardcode', T1.LINE as 'serie', 0 as 'comments', T2.REFERENCE as 'sku', T2.NAME as 'skuname', T1.UNITS as 'quiantity', T1.PRICE as 'price',0 as 'discount', ( CASE WHEN T4.RATE = '0.16' THEN 'A5' ELSE 'A0' END) codetax, 'TVD' whscode, T0.TICKETID as uticket, T5.NAME as 'usucursal' from TICKETS T0 INNER JOIN TICKETLINES T1 ON T0.ID = T1.TICKET INNER JOIN PRODUCTS T2 ON T1.PRODUCT = T2.ID INNER JOIN RECEIPTS T3 ON T1.TICKET = T3.ID INNER JOIN TAXES T4 ON T1.TAXID = T4.ID inner join PEOPLE T5 ON T0.PERSON = T5.ID WHERE T1.UNITS > 0"
#dbQuery="select 0 as 'id', DATE_FORMAT( T3.DATENEW, '%d-%m-%Y %T') as 'fecha',T5.NAME as 'cardcode', T1.LINE as 'serie', 0 as 'comments', T2.REFERENCE as 'sku', T2.NAME as 'skuname', T1.UNITS as 'quiantity', T1.PRICE as 'price',0 as 'discount', ( CASE WHEN T4.RATE = '0.16' THEN 'A5' ELSE 'A0' END) codetax, 'TVD' whscode, T0.TICKETID as uticket, T5.NAME as 'usucursal' from TICKETS T0 INNER JOIN TICKETLINES T1 ON T0.ID = T1.TICKET INNER JOIN PRODUCTS T2 ON T1.PRODUCT = T2.ID INNER JOIN RECEIPTS T3 ON T1.TICKET = T3.ID INNER JOIN TAXES T4 ON T1.TAXID = T4.ID inner join PEOPLE T5 ON T0.PERSON = T5.ID WHERE T1.UNITS > 0"
#dbQuery="select T0.TICKETID as 'id', DATE_FORMAT( T3.DATENEW, '%Y-%m-%d %T') as 'fecha',T5.NAME as 'cardcode', T1.LINE as 'serie', 0 as 'comments', T2.REFERENCE as 'sku', T2.NAME as 'skuname', T1.UNITS as 'quiantity', T1.PRICE as 'price',0 as 'discount', ( CASE WHEN T4.RATE = '0.16' THEN 'A5' ELSE 'A0' END) codetax, 'TVD' whscode, T0.TICKETID as uticket, T5.NAME as 'usucursal' from TICKETS T0 INNER JOIN TICKETLINES T1 ON T0.ID = T1.TICKET INNER JOIN PRODUCTS T2 ON T1.PRODUCT = T2.ID INNER JOIN RECEIPTS T3 ON T1.TICKET = T3.ID INNER JOIN TAXES T4 ON T1.TAXID = T4.ID inner join PEOPLE T5 ON T0.PERSON = T5.ID WHERE T1.UNITS > 0"
dbQuery="select T0.TICKETID as 'id', DATE_FORMAT( T3.DATENEW, '%Y-%m-%d %T') as 'fecha',T5.NAME as 'cardcode', T1.LINE as 'serie', 0 as 'comments', T2.REFERENCE as 'sku', T2.NAME as 'skuname', T1.UNITS as 'quiantity', T1.PRICE * T1.UNITS as 'price',0 as 'discount', ( CASE WHEN T4.RATE = '0.16' THEN 'A5' ELSE 'A0' END) codetax, 'TVD' whscode, T0.TICKETID as uticket, T5.NAME as 'usucursal' from TICKETS T0 INNER JOIN TICKETLINES T1 ON T0.ID = T1.TICKET INNER JOIN PRODUCTS T2 ON T1.PRODUCT = T2.ID INNER JOIN RECEIPTS T3 ON T1.TICKET = T3.ID INNER JOIN TAXES T4 ON T1.TAXID = T4.ID inner join PEOPLE T5 ON T0.PERSON = T5.ID"


db=dbapi.connect(host=dbServer,db=dbSchema,user=dbUser,passwd=dbPass)
cur=db.cursor()
cur.execute(dbQuery)

rows=cur.fetchall()
newRows=()
for row in rows:
        line = ( row[0], row[1], row[2], row[3], row[4], row[5], row[6], int(row[7]), int(row[8]), row[9], row[10], row[11], row[12], row[13])
        newRows=newRows + ( line, )

output=home+'/Escritorio'
if os.path.isdir(output) :
	generateFile(output+'/'+csvName)
#Si hay directorio en ingles, usarlo tambien
output=home+'/Desktop'
if os.path.isdir(output) :
	generateFile(output+'/'+csvName)
	
