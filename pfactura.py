import datetime
from time import strftime

import pymysql
import pymysql.cursors

###################################### clase Factura ########################################################3
class Factura:
    def __init__(self, fecha):############## Constructor Clase Factura #############################
     self.fecha = fecha
     self.mes = fecha[4:6]
     self.any = fecha[0:4]
     self.n_fact = 'A/'+self.mes+"/"+self.any
     self.base_Imp = 325
     self.ret = 0.19
     self.iva = 0.21
     self.total = self.base_Imp -self.base_Imp*self.ret+self.base_Imp*self.iva
     self.concepte = 'Alquiler Local Colomeres 59,Gavà'
     self.Cif_arrendador = "33962364N"
     self.cif_arrendatari = "39894433J"
     self.nom_arrendador = 'Francesc Vives Boix'
     self.nom_arrendatari = 'Aranzazu Danés Vilallonga'
     self.dom_arrendador = 'Camino de las Arrevueltas S/N, El Molar 28710 , Madrid'
     self.dom_arrendatari = 'Calle Labors Agricoles n 37 B 10 3B, Gavá, Barcelona'
    def guardar(self): ############### metodo guardar()###################################
     print(self.mes, self.n_fact, self.nom_arrendador, self.base_Imp)

    def condb(self): ################# metodo condb() ###################################
      try:
        con = pymysql.connect(host='192.168.1.38',
                user='el6q',
                password='6qcisco',
                db='db_6q',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
        print("conexión establecidad con la Base de Datos")
        cur = con.cursor()
        # cur.execute("""select facturas""")
        sql = "insert into facturas (N_fact,Concepte,Total,Iva,Ret,Base_imp,f_mes,f_any,f_fecha,cif_arrendador,cif_arrendatari,nom_arrendador,nom_arrendatari,dom_arrendador,dom_arrendatari) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #print(sql)
        cur.execute(sql,(self.n_fact,self.concepte,self.total,self.iva,self.ret,self.base_Imp,self.mes,self.any,str(self.fecha),self.Cif_arrendador,self.cif_arrendatari,self.nom_arrendador,self.nom_arrendatari,self.dom_arrendador,self.dom_arrendatari))
        con.commit()
        con.close()
        print("conexión cerrada de la Base de Datos")
      except:
        print('Conexión Fallida a la Base de Datos')

###########################  leerFecha() ###################################################

''' la funció LeerFecha() defineix les dades on es generen les factures 
corresponentes de manera que compararem la data actual i si hi ha una ocurrencia 
generará la factura'''


def leerFecha(fecha): # leer de un json las fechas para remitir las facturas mensuales
  import json
  esfecha = False
  f = open('Calendari_data.json',"r")
  data = json.load(f)
  f.close()
  print(data[fecha]) 
  print(datetime.datetime.today().strftime("%d/%m/%Y"))
  if (datetime.datetime.today().strftime("%d/%m/cd %Y") == data[fecha]):
    print("imprimir fatura")
    esfecha = True
    print(esfecha)
  else:
    print("do nothing today")
    esfecha = False
    print(esfecha)
 
  return esfecha


#########################  crearfacturapdf ()##########################################
def crearfacturapdf(f:Factura):
  # Importing Required Module
 from reportlab.pdfgen import canvas
 from reportlab.lib.pagesizes import A4


 # Creating Canvas
 c = canvas.Canvas("Factura Lloguer "+str(f.any)+str(f.mes)+".pdf",pagesize=A4,bottomup=0)
# Logo Section
 # Setting th origin to (10,40)
 c.translate(30,60)
 # Inverting the scale for getting mirror Image of logo
 c.scale(1,-1)
 # Inserting Logo into the Canvas at required position
 #c.drawImage("Firma_Escanejada.jpg",0,0,width=50,height=30)
 
 # Title Section
 # Again Inverting Scale For strings insertion
 c.scale(1,-1)
 # Again Setting the origin back to (0,0) of top-left
 c.translate(-10,-40)
 # Setting the font for Name title of company
 c.setFont("Helvetica-Bold",12)
 # Inserting the name of the company
 c.drawCentredString(125,30,"Francisco Vives Boix")
 # For under lining the title
 c.line(70,35,180,35)
 # Changing the font size for Specifying Address
 c.setFont("Helvetica-Bold",8)
 c.drawCentredString(125,48,"Camino de las Arrevueltas S/N,")
 c.drawCentredString(125,58,"El Molar - 28710 , Madrid")
 # Changing the font size for Specifying GST Number of firm
 c.setFont("Helvetica-Bold",10)
 c.drawCentredString(125,70,"NIF : 33962364N")


 # Line Seprating the page header from the body
 #c.line(100,70,485,70)

 # Document Information
 # Changing the font for Document title
 c.setFont("Helvetica-Bold",12)
 c.drawCentredString(298,100,"FACTURA ")

 # This Block Consist of Costumer Details
 c.roundRect(100,120,400,80,1,stroke=1,fill=0)
 c.setFont("Helvetica-Bold",10)
 c.drawRightString(200,135,"Nº de Factura. :")
 c.drawRightString(360,135,"Fecha. :")
 c.drawRightString(200,150,"Cliente. :") 
 c.drawRightString(200,165,"CIF. :") 
 c.drawRightString(200,180,"Domicilio. :") 
 c.setFont("Helvetica",10)
 c.drawString(220,135,f.n_fact)
 c.drawString(380,135,f.fecha[6:8]+"/"+f.mes+"/"+f.any)
 c.drawString(220,150,f.nom_arrendatari)
 c.drawString(220,165,f.cif_arrendatari)
 c.drawString(220,180,f.dom_arrendatari)


 # This Block Consist of Item Description
 c.roundRect(100,220,400,130,2,stroke=1,fill=0)
 #c.line(15,120,185,120)
 c.setFont("Helvetica-Bold",8)
 c.drawCentredString(125,230,"Nº SERV.")
 c.drawCentredString(190,230,"DESCRIPCIÓN")
 c.drawCentredString(355,230,"IMPORTE")
 c.drawCentredString(420,230,"UNIDADES")
 c.drawCentredString(470,230,"TOTAL")
 # Drawing table for Item Description
 c.line(100,235,500,235)
 c.line(150,220,150,350)
 c.line(330,220,330,350)
 c.line(390,220,390,350)
 c.line(450,220,450,350)
 c.drawCentredString(125,245,"AL01")
 c.drawString(160,245,f.concepte +" mes "+ f.mes)
 c.drawString(340,245,str(f.base_Imp)+" €")
 c.drawString(400,245,"1")
 c.drawString(460,245,str(f.base_Imp)+" €")

 # Declaration and Signature
 #c.line(300,400,495,400)
 c.roundRect(450,380,50,25,2,stroke=1,fill=0)
 c.setFont("Helvetica-Bold",10)
 c.drawRightString(430,395,"RET. IRPF : ( 19% ) ")
 #c.line(300,430,495,430)
 c.roundRect(450,410,50,25 ,2,stroke=1,fill=0)
 c.drawRightString(430,425,"IVA  : ( 21% ) ")
 c.drawRightString(430,465,"TOTAL :  ")
 c.setFont("Helvetica",10)
 c.drawString(460,395,str(-f.ret*f.base_Imp)+" €")
 c.drawString(460,425,str(f.iva*f.base_Imp)+" €")
 c.setFont("Helvetica-Bold",10)
 c.drawString(460,465,str(f.total)+" €")
 #c.line(100,550,495,550)
 c.drawString(125,600,"Firma del Arrendador")
 c.setFont("Helvetica",10)
 # Firma Section
 # Setting th origin to (10,40)
 c.translate(100,700)
 # Inverting the scale for getting mirror Image of logo
 c.scale(1,-1)
 # Inserting Logo into the Canvas at required position
 c.drawImage("Firma_Escanejada.jpg",0,0,width=150,height=90)
 

 # End the Page and Start with new
 c.showPage()
 # Saving the PDF
 c.save()

################################## enviar el correu amb la factura del mes corresponent#################################
def enviarcorreu():
 import os
 import datetime
 import smtplib  
 import locale
 from email.mime.multipart import MIMEMultipart
 from email.mime.text import MIMEText
 from email.mime.base import MIMEBase
 from email import encoders
 locale.setlocale(locale.LC_TIME, 'es_ES') # this sets the date time formats to es_ES, there are many other options for currency, numbers etc. 'es_ES'
 today=datetime.datetime.now()
 mes_lloguer=today.strftime("%B")
 any_lloguer=today.strftime("%Y")
 mail_content = '''Hola,
 Adjunto Factura del alquiler del local Colomeres 59 B2.



 Saludos 

 Francesc

 ''' 
 #The mail addresses and password
 sender_address = '6q@telefonica.net'
 sender_pass = 'vives0467'
 receiver_address = 'el_6q@hotmail.com'

 print(any_lloguer)
 #Setup the MIME
 message = MIMEMultipart()
 message['From'] = sender_address
 message['To'] = receiver_address

 Titol ='Factura Alquiler Local de Colomeres 59- Gavá  {}-{}  '
 s=Titol.format(mes_lloguer,any_lloguer)
 print(s) 
 message['Subject'] = s
 #The subject line
 #The body and the attachments for the mail
 message.attach(MIMEText(mail_content, 'plain'))
 attach_file_name = 'invoice.pdf'
 attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
 payload = MIMEBase('application', 'octate-stream')
 payload.set_payload((attach_file).read())
 encoders.encode_base64(payload) #encode the attachment
 #add payload header with filename

 payload.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(attach_file_name))
 #dd_header('Content-Disposition', "attachment; filename= %s" % filename)
 message.attach(payload)
 #Create SMTP session for sending the mail
 session = smtplib.SMTP('smtp.telefonica.net') #use gmail with port
 #session.starttls() #enable security
 session.login(sender_address, sender_pass) #login with mail_id and password
 text = message.as_string()
 session.sendmail(sender_address, receiver_address, text)
 session.quit()
 print('Mail Sent')
 print(mes_lloguer)
 print(os.path.basename(attach_file_name))

#######################  main script ###################################################

''' con sys.argv estamos probando el paso de parámetros en la ejecución del script
de Python. La otra alternativa es leer la fecha de un Json y generar 
las faturas según está previsto'''
import sys
if len(sys.argv) == 2: # pasamos una fecha como argumento en formato AAAA/MM/DD 
  print("number of arguments", len(sys.argv),"arguments")
  print("argument List:", str(sys.argv))
  print("fecha:", str(sys.argv[1]))
  d=str(sys.argv[1])
else: 
  d = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
print(d)
f = Factura(d)

print(f.fecha, f.total, f.nom_arrendador, f.mes, f.any)
f.condb()  # establecemos conexión con la base de Datos de Facturas
f.guardar()  # Insertamos registro de nueva factura en Base de Datos
leerFecha("enero")
crearfacturapdf(f)
#enviarcorreu()
  