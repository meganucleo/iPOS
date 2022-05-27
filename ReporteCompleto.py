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

#dbSchema=commands.getoutput("egrep 'db\.URL' "+home+"/"+config+" | egrep -o '[a-zA-Z0-9\_]+$'")
dbSchema=commands.getoutput("egrep 'db\.URL' "+home+"/"+config+" | egrep -o '[a-zA-Z0-9\_\?\\=]+$'  | rev | cut -c 15- | rev")
output=home+'/Escritorio/reporteCompleto.csv'

#dbQuery="select T0.TICKETID,  T1.LINE, T2.REFERENCE, T2.NAME, T1.UNITS, T1.PRICE, T1.UNITS * T1.PRICE AS TOTAL, DATE_FORMAT( T3.DATENEW, '%Y-%m-%d' ) , T4.RATE, T5.PAYMENT from TICKETS T0 INNER JOIN TICKETLINES T1 ON T0.ID = T1.TICKET INNER JOIN PRODUCTS T2 ON T1.PRODUCT = T2.ID INNER JOIN RECEIPTS T3 ON T1.TICKET = T3.ID INNER JOIN TAXES T4 ON T1.TAXID = T4.ID INNER JOIN PAYMENTS T5 ON T1.TICKET = T5.RECEIPT ORDER BY TICKETID"
#dbQuery="SELECT 1, T1.LINE, T2.REFERENCE, T2.NAME, T1.UNITS, 0, T1.PRICE,T4.ID,T0.TICKETID, DATE_FORMAT( T3.DATENEW, '%Y-%m-%d' ) ,  T5.PAYMENT FROM TICKETS T0 INNER JOIN TICKETLINES T1 ON T0.ID = T1.TICKET INNER JOIN PRODUCTS T2 ON T1.PRODUCT = T2.ID INNER JOIN RECEIPTS T3 ON T1.TICKET = T3.ID INNER JOIN TAXES T4 ON T1.TAXID = T4.ID INNER JOIN PAYMENTS T5 ON T1.TICKET = T5.RECEIPT ORDER BY TICKETID"
#dbQuery="select T0.TICKETID, T1.TICKET, T1.LINE, T2.REFERENCE, T2.NAME, T1.UNITS, T1.PRICE, T1.UNITS * T1.PRICE AS SUBTOTAL,T1.UNITS * T1.PRICE *T4.RATE AS TOTAL_IVA ,  (T1.UNITS * T1.PRICE *T4.RATE )+ (T1.UNITS * T1.PRICE) AS TOTALFINALCONIVA, T3.DATENEW, T4.RATE from TICKETS T0 INNER JOIN TICKETLINES T1 ON T0.ID = T1.TICKET INNER JOIN PRODUCTS T2 ON T1.PRODUCT = T2.ID INNER JOIN RECEIPTS T3 ON T1.TICKET = T3.ID INNER JOIN TAXES T4 ON T1.TAXID = T4.ID ORDER BY TICKETID"
dbQuery="select 0 as 'id',T0.TICKETID, DATE_FORMAT( T3.DATENEW, '%d-%m-%Y %T') as 'fecha',T5.NAME as 'cardcode', T1.LINE as 'serie', 0 as 'comments', T2.REFERENCE as 'sku', T2.NAME as 'skuname', T1.UNITS as 'quiantity', T1.PRICE as 'price',0 as 'discount', ( CASE WHEN T4.RATE = '0.16' THEN 'A5' ELSE 'A0' END) codetax, 'TVD' whscode, T0.TICKETID as uticket, T5.NAME as 'usucursal' from TICKETS T0 INNER JOIN TICKETLINES T1 ON T0.ID = T1.TICKET INNER JOIN PRODUCTS T2 ON T1.PRODUCT = T2.ID INNER JOIN RECEIPTS T3 ON T1.TICKET = T3.ID INNER JOIN TAXES T4 ON T1.TAXID = T4.ID inner join PEOPLE T5 ON T0.PERSON = T5.ID WHERE T1.UNITS > 0"

db=dbapi.connect(host=dbServer,db=dbSchema,user=dbUser,passwd=dbPass)
cur=db.cursor()
cur.execute(dbQuery)

rows=cur.fetchall()
fp=open(output,'w')
#fp.write("NUMTICKET,LINEA,CODIGO,DESCRIPCION,UNIDADES,0+'\$',PRECIO,IVA,TICKETID,FECHA,PAGO\r\n")
#fp.write("NUMTICKET,IDTICKET,LINEA,CODIGO,DESCRIPCION,UNIDADES,PRECIO,TOTAL,TICKETID,IVA,PAGO\r\n")
myFile=csv.writer(fp)
myFile.writerows(rows)
fp.close()

