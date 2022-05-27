#!/usr/bin/python

import MySQLdb as dbapi
import sys
import csv
import commands
from datetime import date

dbServer='127.0.0.1'
dbPass='{MYSQL_PASS}'
dbUser='{MYSQL_USR}'
config="openbravopos.properties"

home=commands.getoutput("echo $HOME")

#dbSchema=commands.getoutput("egrep 'db\.URL' "+home+"/"+config+" | egrep -o '[a-zA-Z0-9\_]+$'")
dbSchema=commands.getoutput("egrep 'db\.URL' "+home+"/"+config+" | egrep -o '[a-zA-Z0-9\_\?\\=]+$'  | rev | cut -c 15- | rev")
folder='/Escritorio/shared'
output=home+folder+'/Lines.csv'

now=date.today()
D3=now.strftime("%Y%m%d")
I3=now.strftime("%d.%m.%Y")

if dbSchema == "PSA1":
        cclient="C500000"
elif dbSchema == "PSA2":
        cclient="C500011"
elif dbSchema == "PSA3":
        cclient="C500012"
else:
        cclient="C500000"

content="DocNum,DocType,HandWritten,DocDate,CardCode,CardName,DocCurrency,Series,Comments\r\nNumero de Documento,Tipo de Documento,No Cambiar,DocDate,Clave Cliente,Nombre Cliente,Monea,Series,Comments\r\n1,I,tNO,"+D3+","+cclient+",,$,287,Venta de Sucursal "+dbSchema+" - VENTA "+I3+"\r\n"
output2=home+folder+'/Header.csv'
fp=open(output2,'w')
fp.write(content)
fp.close()

dbQuery="select 1 as 'ParentKey', (1)*(2) as 'LineNum',T2.REFERENCE as 'ItemCode',0 as 'ItemDescription', T1.UNITS as 'Quantity',0 as 'Currency',T1.PRICE as 'UnitPrice', 0 as 'DiscountPercent', T4.RATE as 'TaxCode', 0 as 'WhsCode', T0.TICKETID as 'U_Ticket',0 'U_Sucursal' from TICKETS T0 INNER JOIN TICKETLINES T1 ON T0.ID = T1.TICKET INNER JOIN PRODUCTS T2 ON T1.PRODUCT = T2.ID INNER JOIN RECEIPTS T3 ON T1.TICKET = T3.ID INNER JOIN TAXES T4 ON T1.TAXID = T4.ID WHERE DATE( T3.DATENEW ) = CURDATE( ) ORDER BY TICKETID"


db=dbapi.connect(host=dbServer,db=dbSchema,user=dbUser,passwd=dbPass)
cur=db.cursor()
cur.execute(dbQuery)

rows=cur.fetchall()

#Preprocesing data for customization
rows_ready=[]
line_num=1
for line in rows:
        doc_num,num,code,description,quantity,currency,price,discount,tax,whscode,ticket,sucursal=line
        num=line_num
        description=""
        currency="$"
        if tax == 0.16:
                tax = "A5"
        else:
                tax = "A0"
        whscode="AST"
        sucursal=dbSchema
        line2=[]
        line2.extend((doc_num,num,code,description,quantity,currency,price,discount,tax,whscode,ticket,sucursal))
        rows_ready.append(line2)
        line_num+=1


fp=open(output,'w')
fp.write("ParentKey,LineNum,ItemCode,ItemDescription,Quantity,Currency,UnitPrice,DiscountPercent,TaxCode,WhsCode,U_Ticket,U_Sucursal\r\n")
fp.write("Numero de Documento,Linea,Codigo Articulo,Descripcion,Cantidad,Moneda,Precio por unidad,Porcentaje Desc,Codigo Imp,WhsCode,U_Ticket,U_Sucursal\r\n")
myFile=csv.writer(fp)
myFile.writerows(rows_ready)
fp.close()

#Convirtiendo de unix a windows
status,out1=commands.getstatusoutput("sed -i 's/$/\r/' "+output)
status,out2=commands.getstatusoutput("sed -i 's/$/\r/' "+output2)
