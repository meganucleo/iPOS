#!/usr/bin/python

import MySQLdb as dbapi
import sys
import csv
import commands

#dbServer='10.1.3.23'
#dbPass='jittermysql'
#dbUser='reportes'
#dbSchema='PSA3'

dbServer='127.0.0.1'
dbPass='{MYSQL_PASS}'
dbUser='{MYSQL_USR}'
config="openbravopos.properties"

home=commands.getoutput("echo $HOME")

dbSchema=commands.getoutput("egrep 'db\.URL' "+home+"/"+config+" | egrep -o '[a-zA-Z0-9\_]+$'")
output=home+'/Escritorio/reporteDiario.csv'

#dbQuery="select T0.TICKETID,  T1.LINE, T2.REFERENCE, T2.NAME, T1.UNITS, T1.PRICE, T1.UNITS * T1.PRICE AS TOTAL, DATE_FORMAT( T3.DATENEW, '%Y-%m-%d' ) , T4.RATE, T5.PAYMENT from TICKETS T0 INNER JOIN TICKETLINES T1 ON T0.ID = T1.TICKET INNER JOIN PRODUCTS T2 ON T1.PRODUCT = T2.ID INNER JOIN RECEIPTS T3 ON T1.TICKET = T3.ID INNER JOIN TAXES T4 ON T1.TAXID = T4.ID INNER JOIN PAYMENTS T5 ON T1.TICKET = T5.RECEIPT WHERE DATE( T3.DATENEW ) = CURDATE( ) ORDER BY TICKETID"
dbQuery="SELECT 1, T1.LINE, T2.REFERENCE, T2.NAME, T1.UNITS, 0, T1.PRICE,T4.ID,T0.TICKETID, DATE_FORMAT( T3.DATENEW, '%Y-%m-%d' ) ,  T5.PAYMENT FROM TICKETS T0 INNER JOIN TICKETLINES T1 ON T0.ID = T1.TICKET INNER JOIN PRODUCTS T2 ON T1.PRODUCT = T2.ID INNER JOIN RECEIPTS T3 ON T1.TICKET = T3.ID INNER JOIN TAXES T4 ON T1.TAXID = T4.ID INNER JOIN PAYMENTS T5 ON T1.TICKET = T5.RECEIPT WHERE DATE( T3.DATENEW ) = CURDATE( ) ORDER BY TICKETID"

db=dbapi.connect(host=dbServer,db=dbSchema,user=dbUser,passwd=dbPass)
cur=db.cursor()
cur.execute(dbQuery)

rows=cur.fetchall()
fp=open(output,'w')
fp.write("NUMTICKET,LINEA,CODIGO,DESCRIPCION,UNIDADES,0+'\$',PRECIO,IVA,TICKETID,FECHA,PAGO\r\n")
myFile=csv.writer(fp)
myFile.writerows(rows)
fp.close()

