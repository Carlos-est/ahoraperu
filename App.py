import math
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_required, current_user
from flask_mysqldb import MySQL
from werkzeug.exceptions import HTTPException
import funcionesGenerales
import primeraFuncion
import segundaFuncion
import terceraFuncion
import cuartaFuncion
import quintaFuncion

from forms import FormIndicadoresCultivo
from forms import FormBiomasa
from forms import FormNutrientes
from forms import FormRiego
from forms import  EnviarEmail

from datetime import timedelta
import datetime
import config
from datetime import datetime
import os
from pymongo import MongoClient
from forms import LoginForm, CreateAccountForm
import bcrypt
import pymongo
from flask_mail import Mail, Message

app = Flask(__name__)

#MYSQL CONECTION
app.config['MYSQL_HOST'] = 'labsac.com'
app.config['MYSQL_USER'] = 'labsacco_dia'
app.config['MYSQL_PASSWORD'] = 'ciba15153232'
app.config['MYSQL_DB'] = 'labsacco_banano'
mysql = MySQL(app)
 #db=mysql.connector.connect( host="labsac.com",user="labsacco_dia", password="ciba15153232", database="labsacco_banano")
       
#SETTINGS
app.secret_key = 'mysecretkeyRepDom'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)
#variables = variables()

##################conectamos a la base de datos de MONGODB
MONGO_HOST = "200.48.235.251"
MONGO_PUERTO ="27017"
MONGO_PWD = "ciba15153232"
MONGO_USER = "estacionesperu"
MONGO_TIEMPO_FUERA =10000
MONGO_BASEDATOS = "PROYECTO"
MONGO_COLECCION = "users"
MONGO_URI = "mongodb://"+ MONGO_USER +":"+ MONGO_PWD + "@"+MONGO_HOST +":" + MONGO_PUERTO + "/"
#MONGO_URI = "mongodb://"+MONGO_HOST +":" + MONGO_PUERTO + "/"

#connoct to your Mongo DB database
client = MongoClient(MONGO_URI)

baseDatos = client[MONGO_BASEDATOS]
coleccion=baseDatos[MONGO_COLECCION]
##########################  LOGIN
""" login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
def is_authenticated(self):
	return True

def is_active(self):
	return True

def is_anonymous(self):
	return False

def get_id(self):
	return str(self.id)

def is_admin(self):
	return self.admin
@login_manager.user_loader
def load_user(user_id):
    user_found = coleccion.find_one({"name": nombres})
	return Usuarios.query.get(int(user_id))

 """
#assign URLs to have a particular route 

@app.route("/", methods=['post', 'get'])
def login():
    loginForm=LoginForm()
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = coleccion.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('home'))
            else:
                if "email" in session:
                    return redirect(url_for("home"))
                message = 'Error en la contraseña'
                return render_template('accounts/login.html', message=message, form = loginForm)
        else:
            message = 'Email no encontrado'
            return render_template('accounts/login.html', message=message, form = loginForm)

    
    return render_template('accounts/login.html',form = loginForm)

@app.route("/register", methods=["POST", "GET"])
def register():
    createAccountForm=CreateAccountForm()
    message = ''
    if "email" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        nombres = request.form.get("nombres")
        apellido_paterno = request.form.get("apellido_paterno")
        apellido_materno = request.form.get("apellido_materno")
        email = request.form.get("email")
        ocupacion = request.form.get("ocupacion")
        asociacion = request.form.get("asociacion")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = coleccion.find_one({"name": nombres})
        email_found = coleccion.find_one({"email": email})
        if email_found:
            message = 'Este email ya existe en la base de datos'
            return render_template('accounts/register.html', message=message,form=createAccountForm)
        if password1 != password2:
            message = 'Las contraseñas no coinciden!'
            return render_template('accounts/register.html', message=message,form=createAccountForm)
        else:
            
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'nombres': nombres, 
                        'apellido_paterno': apellido_paterno, 
                        'apellido_materno': apellido_materno,
                        'email': email, 
                        'ocupacion': ocupacion,
                        'asociacion': asociacion,
                        'password': hashed}
            #insert it in the record collection
            print("insert mongo:", user_input)
            coleccion.insert_one(user_input)
            
            #find the new created account and its email
            user_data = coleccion.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            return render_template('home.html', email=new_email)
    return render_template('accounts/register.html', message=message,form=createAccountForm)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    loginForm=LoginForm()
    if "email" in session:
        session.pop("email", None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/home')
#@login_required
def home():
    if "email" in session:
        email = session["email"]
        return render_template('home.html', email=email)
    else:
        return redirect(url_for("login"))

@app.before_request
def do_something_when_a_request_comes_in():
	track_visitor()

@app.route('/formIndicadoresCosecha')
#@login_required
def formIndicadoresCosecha():

    formIndicadoresCultivo = FormIndicadoresCultivo()

    return render_template('formIndicadoresCosecha.html', form = formIndicadoresCultivo)

@app.route('/formIndicadoresFloracion')
#@login_required
def formIndicadoresFloracion():

    formIndicadoresCultivo = FormIndicadoresCultivo()

    return render_template('formIndicadoresFloracion.html', form = formIndicadoresCultivo)

@app.route('/viewIndicadoresCosecha', methods =['POST']) #ACTUALIZADO
#@login_required
def viewIndicadoresCosecha():
    
  if request.method == 'POST':
    fechaCosecha = request.form['fechaCosecha']    
    estacion = request.form['cmbEstacion']
    session['estacion'] = estacion
    session['fechaCosecha'] = fechaCosecha
   
    fechaCosecha = funcionesGenerales.cambiar_formato_fecha(fechaCosecha)

    dict_estaciones = {"1":"Chulucanas","2":"otras"}
    
    estacionName=dict_estaciones[estacion] #BUSCA LA ESTACION 
    session['estacionName'] = estacionName

    # GRADOS DIA BACKWARD
    GDA, fecha_floracion, nSemanas, data = segundaFuncion.EstimacionFechaFloracion(fechaCosecha, int(estacion))
        
    session['GDA'] = str(GDA)
    session['fecha_floracion'] = str(fecha_floracion)
    session['nSemanas'] = str(nSemanas)
    session['data'] = data
    fechasBackward = [row[0] for row in data]
    tempPromedioBackward = [row[1] for row in data]
    gradosDiaBackward = [row[2] for row in data]

 
    return render_template('viewIndicadoresCosecha.html', fechaCosecha=fechaCosecha, GDA = GDA, fecha_floracion = fecha_floracion, nSemanas = nSemanas, fechasBackward=fechasBackward, tempPromedioBackward =tempPromedioBackward,gradosDiaBackward=gradosDiaBackward, data= data, estacionName = estacionName)

@app.route('/viewIndicadoresFloracion', methods =['POST'])
#@login_required
def viewIndicadoresFloracion():
    
  if request.method == 'POST':
    fechaFloracion = request.form['fechaFloracion']    
    estacion = request.form['cmbEstacion']
    session['estacion'] = estacion
    session['fechaFloracion'] = fechaFloracion
   
    fechaFloracion = funcionesGenerales.cambiar_formato_fecha(fechaFloracion)
    dict_estaciones = {"1":"Chulucanas","2":"otras"}
    
    estacionName=dict_estaciones[estacion] #BUSCA LA ESTACION 
    #print("fecha cosecha nueva",fechaCosechaTime )
    
    session['estacionName'] = estacionName 
    # GRADOS DIA FORWARD
    valor1,valor2, valor3, estimacion, data, semana_total, temperatura  = segundaFuncion.EstimacionFechaCosecha(fechaFloracion, int(estacion))
    valor1 = round(valor1)
    nroSemanas = round((int(estimacion)/7),1)
    session['nroSemanas'] = str(nroSemanas)      
    session['valor1'] = str(valor1)
    session['valor2'] = str(valor2)
    session['valor3'] = str(valor3)
    session['estimacion'] = str(estimacion)

    fechas = [row[0] for row in data]
    tempPromedio = [row[1] for row in data]
    tempPromedioProyectada = [row[2] for row in data]
    gradosDia = [row[3] for row in data]
    gradosDiaProyectada = [row[4] for row in data]
    Humedad = [row[5] for row in data]
    HumedadProyectada = [row[6] for row in data]
    print("estimacion de fecha de cosecha")
    #### AÑADIDO NUEVO #####
    if estimacion == 0:
        file_selector = 'viewIndicadoresFloracion-1.html'

    else:
        file_selector = 'viewIndicadoresFloracion.html'   
 
    return render_template(file_selector,   fechaFloracion = fechaFloracion,  valor1 = valor1, valor2 = valor2, valor3 = valor3, fechas = fechas, tempPromedio= tempPromedio, tempPromedioProyectada = tempPromedioProyectada, gradosDia=gradosDia,gradosDiaProyectada=gradosDiaProyectada, datosCompletos = data,  estimacion=estimacion,  estacionName = estacionName, nroSemanas = nroSemanas, semana_total=semana_total, temperatura=temperatura, Humedad=Humedad, HumedadProyectada=HumedadProyectada)

#BIOMASA 

@app.route('/formBiomasa')
#@login_required
def formBiomasa():
    formBiomasa = FormBiomasa()
    return render_template('formBiomasa.html', form = formBiomasa)

@app.route('/formBiomasaProyeccion')
#@login_required
def formBiomasaProyeccion():
    formBiomasa = FormBiomasa()
    return render_template('formBiomasaProyeccion.html', form = formBiomasa)

@app.route('/formNutrientes')
#@login_required
def formNutrientes():
    formNutrientes = FormNutrientes()

    return render_template('formNutrientes.html', form = formNutrientes)

@app.route('/formHidrica')
#@login_required
def formHidrica():
    formRiego = FormRiego()
    return render_template('formHidrica.html', form = formRiego)

@app.route('/formHidricaDemanda')
#@login_required
def formHidricaDemanda():
    formRiego = FormRiego()
    return render_template('formHidricaDemanda.html', form= formRiego)

@app.route('/formHidricaIntervalo')
#@login_required
def formHidricaIntervalo():
    formRiego = FormRiego()
    return render_template('formHidricaIntervalo.html', form= formRiego)


@app.route('/viewBiomasa', methods =['POST'])
#@login_required
def viewBiomasa():
    
  if request.method == 'POST':
    fechaCosecha = request.form['fechaCosecha']  
    Cant_manos = request.form['Cant_manos']
    rPa = request.form['rPa']    
    estacion = request.form['cmbEstacion']
    session['Cant_manos'] = Cant_manos
    session['rPa'] = rPa
    session['fechaCosecha'] = fechaCosecha
    session['estacion'] = estacion
   
    fechaCosecha = funcionesGenerales.cambiar_formato_fecha(fechaCosecha)

    dict_estaciones = {"1":"Chulucanas","2":"otras"}
    estacionName=dict_estaciones[estacion] #BUSCA LA ESTACION 
    session['estacionName'] = estacionName
    fec_string, biomasa_planta, biomasa, semanas = terceraFuncion.EstimacionRacimoCicloAnterior(fechaCosecha, int(estacion),int(rPa), int(Cant_manos))
    
    return render_template('viewBiomasa.html',fec_string = fec_string, biomasa_planta = biomasa_planta, biomasa=biomasa,  estacionName = estacionName, semanas=semanas)

@app.route('/viewBiomasaProyeccion', methods =['POST'])
#@login_required
def viewBiomasaProyeccion():
    
  if request.method == 'POST':
    fechaFloracion = request.form['fechaFloracion']    
    Cant_manos = request.form['Cant_manos']
    nro_semanas = request.form['nro_semanas']
    rPa = request.form['rPa']    
    estacion = request.form['cmbEstacion']
    session['Cant_manos'] = Cant_manos
    session['rPa'] = rPa
    session['fechaFloracion'] = fechaFloracion
    session['estacion'] = estacion
    session['nro_semanas'] = nro_semanas

    fechaFloracion = funcionesGenerales.cambiar_formato_fecha(fechaFloracion)
    dict_estaciones = {"1":"Chulucanas","2":"otras"}
    estacionName=dict_estaciones[estacion] #BUSCA LA ESTACION 
    session['estacionName'] = estacionName
    fec, fec_final,biomasa_planta, biomasa, estimacion, semanas = terceraFuncion.EstimacionRacimoProyeccion(fechaFloracion, int(estacion),int(rPa), int(Cant_manos), int(nro_semanas))
    Cant_manos=int(Cant_manos)
    nro_semanas = int(nro_semanas)
    if estimacion == 0:
        flash('Error: Verifique los datos ingresados')
        #return render_template("formError.html", e=e), 500 
        file_selector = 'formError.html'

    else:
        file_selector = 'viewBiomasaProyeccion.html'   

    return render_template(file_selector,fec = fec, fec_final = fec_final, 
    biomasa_planta=biomasa_planta,biomasa=biomasa,semanas=semanas, estimacion=estimacion, 
    estacionName = estacionName, Cant_manos=Cant_manos, nro_semanas=nro_semanas)



@app.route('/viewNutrientes', methods =['POST'])
#@login_required
def viewNutrientes():
        
  if request.method == 'POST': 
    fec = request.form['fechaCosecha']
    rPa = request.form['rPa']   
    intervalo = request.form['intervalo']   
    estacion = request.form['cmbEstacion']
    session['rPa'] = rPa
    session['intervalo'] = intervalo
    session['estacion'] = estacion
    fechaCosecha = funcionesGenerales.cambiar_formato_fecha(fec)
           
    dict_estaciones = {"1":"Chulucanas","2":"otras"}
    estacionName=dict_estaciones[estacion] #BUSCA LA ESTACION 
    session['estacionName'] = estacionName
    fec, biomasa_planta, biomasa, tupla = cuartaFuncion.nutrientes(fechaCosecha, int(estacion),int(rPa), int(intervalo))
    session['fec'] = str(fec)
    session['biomasa_planta'] = str(biomasa_planta)
    session['biomasa'] = str(biomasa)
    session['tupla'] = tupla

    fechas = [row[0] for row in tupla]
    masa_kg = [row[1] for row in tupla]
    msa_ton = [row[2] for row in tupla]   
 
    return render_template('viewNutrientes.html',fec = fec, biomasa_planta = biomasa_planta, biomasa=biomasa, tupla = tupla, intervalo = intervalo,  estacionName = estacionName)

@app.route('/viewHidrica', methods =['POST'])
#@login_required
def viewHidrica():
    
  if request.method == 'POST':
  
    estacion = request.form['cmbEstacion']
    suelo = request.form['cmbSuelo']
    riego = request.form['cmbRiego']
    dias = request.form['dias']
    fechaFinal=request.form['fechaFinal']

    session['suelo'] = suelo
    session['riego'] = riego
    session['estacion'] = estacion
    session['dias'] = dias
    session['fechaFinal'] = fechaFinal
    fechaFinal = funcionesGenerales.cambiar_formato_fecha(fechaFinal)

    dict_estaciones = {"1":"Chulucanas","2":"otras"}
    estacionName=dict_estaciones[estacion] #BUSCA LA ESTACION 
    session['estacionName'] = estacionName
    NH, data, evp_cultivo, Deficit  = quintaFuncion.nHidrica(int(dias),fechaFinal,int(estacion),suelo, riego) #NH esta en mm
    NH2 = round(NH*10,2) #m3
    session['valor1'] = str(NH)
    session['valor2'] = str(NH2)
    session['data'] = data

    fechas = [row[0] for row in data]
    evap = [row[1] for row in data]
    rain = [row[2] for row in data]
    fechaFinal=data[-1][0]

 
    return render_template('viewHidrica.html', NH= NH,NH2 = NH2,riego=riego, rain=rain, suelo=suelo, fechas = fechas, evap=evap,data=data, estacionName = estacionName, dias=int(dias), fechaFinal=fechaFinal)

@app.route('/viewHidricaDemanda', methods =['POST'])
#@login_required
def viewHidricaDemanda():
    
  if request.method == 'POST':
  
    estacion = request.form['cmbEstacion']
    suelo = request.form['cmbSuelo']
    riego = request.form['cmbRiego']
    fechaFinal = request.form['fechaFinal']
    session['suelo'] = suelo
    session['riego'] = riego
    session['estacion'] = estacion
    session['fechaFinal'] = fechaFinal
    fechaFinal = funcionesGenerales.cambiar_formato_fecha(fechaFinal)

    dict_estaciones = {"1":"Chulucanas","2":"otras"}
    estacionName=dict_estaciones[estacion] #BUSCA LA ESTACION 
    session['estacionName'] = estacionName
    NH, data, evapoAcumulada, deficit = quintaFuncion.nHidricaDemanda(fechaFinal,int(estacion), suelo, riego)
    NH2 = NH*10
    session['NH2'] = str(NH2)
    session['NH2'] = str(NH2)
    session['data'] = data

    fechas = [row[0] for row in data]
    evap = [row[1] for row in data]
    rain = [row[2] for row in data]
    fechaFinal=data[-1][0]
    
    return render_template('viewHidricaDemanda.html', NH= NH, NH2=NH2, fechas = fechas, evap=evap,rain=rain,data=data, estacionName = estacionName, evapoAcumulada=evapoAcumulada, fechaFinal=fechaFinal, deficit=deficit)

@app.route('/viewHidricaIntervalo', methods =['POST'])
#@login_required
def viewHidricaIntervalo():
    
  if request.method == 'POST':
  
    estacion = request.form['cmbEstacion']
    suelo = request.form['cmbSuelo']
    riego = request.form['cmbRiego']
    dias = request.form['dias']
    fechaFinal=request.form['fechaFinal']

    session['suelo'] = suelo
    session['riego'] = riego
    session['estacion'] = estacion
    session['dias'] = dias
    session['fechaFinal'] = fechaFinal
    fechaFinal = funcionesGenerales.cambiar_formato_fecha(fechaFinal)

    dict_estaciones = {"1":"Chulucanas","2":"otras"}
    estacionName=dict_estaciones[estacion] #BUSCA LA ESTACION 
    session['estacionName'] = estacionName
    NH, data, evp_cultivo, intervalo_30, intervalo_50, intervalo_70  = quintaFuncion.nHidricaIntervalo(int(dias),fechaFinal,int(estacion),suelo, riego)

    session['NH'] = str(NH)
    session['data'] = data

    fechas = [row[0] for row in data]
    evap = [row[1] for row in data]
    rain = [row[2] for row in data]
    fechaFinal=data[-1][0]

    return render_template('viewHidricaIntervalo.html', riego=riego, rain=rain, suelo=suelo, fechas = fechas, evap=evap,data=data, estacionName = estacionName, dias=int(dias), fechaFinal=fechaFinal, intervalo_30=intervalo_30, intervalo_50=intervalo_50, intervalo_70=intervalo_70 )


@app.route('/formNroHojas')
#@login_required
def formNroHojas():
    #formBiomasa = FormBiomasa()
    formIndicadoresCultivo = FormIndicadoresCultivo()
    return render_template('formNroHojas.html', form=formIndicadoresCultivo)

@app.route('/viewNroHojas', methods =['POST'])
#@login_required
def viewNroHojas():
    
  if request.method == 'POST':
   
    estacion = request.form['cmbEstacion']
    fechaFinal=request.form['fechaFinal']
    session['estacion'] = estacion
    session['fechaFinal'] = fechaFinal
    fechaFinal = funcionesGenerales.cambiar_formato_fecha(fechaFinal)
    #DICCIONARIO QUE CONTIENE LAS ESTACIONES
    dict_estaciones = {"1":"Chulucanas","2":"otras"}
    
    estacionName=dict_estaciones[estacion] #BUSCA LA ESTACION 
    NHojas14, NHojas28, data = primeraFuncion.NumeroHojas(fechaFinal, int(estacion)) #ENVIA EL NRO DE ESTACION CORRESPONDIENTE
    session['estacionName'] = estacionName
    session['NHojas14'] = str(NHojas14)
    session['NHojas28'] = str(NHojas28)
    session['data'] = data

    fechas = [row[0] for row in data]
    tempPromedio = [row[1] for row in data]
    gradosDia = [row[2] for row in data]

    last_fecha = fechas[-1]
 
    #return render_template('viewBiomasa.html',valor1 = valor1, valor2 = valor2, valor3=valor3,  estacionName = estacionName)
    return render_template('viewNroHojas.html', NHojas14 = NHojas14, NHojas28 = NHojas28, data = data, fechas = fechas, last_fecha = last_fecha ,tempPromedio =tempPromedio,gradosDia = gradosDia ,estacionName = estacionName)


@app.route('/viewNroHojasNroSemanas', methods =['POST'])
#@login_required
def viewNroHojasNroSemanas():
    
  if request.method == 'POST':
   
    estacion = request.form['cmbEstacion']
    nroSemanas = request.form['nroSemanas']
    fechaFinal=request.form['fechaFinal']

    session['fechaFinal'] = fechaFinal
    session['estacion'] = estacion
    session['nroSemanas'] = nroSemanas
    fechaFinal = funcionesGenerales.cambiar_formato_fecha(fechaFinal)
   
   #DICCIONARIO QUE CONTIENE LAS ESTACIONES
    dict_estaciones = {"1":"Chulucanas","2":"otras"}
    estacionName=dict_estaciones[estacion] #BUSCA LA ESTACION 
    session['estacionName'] = estacionName
    NHojas, data = primeraFuncion.NumeroHojasSemanas(fechaFinal, int(estacion), int(nroSemanas))

    session['valor1'] = str(NHojas)
    session['data'] = data

    fechas = [row[0] for row in data]
    tempPromedio = [row[1] for row in data]
    gradosDia = [row[2] for row in data]
 
    return render_template('view14NroSemanas.html', NHojas = NHojas,  data = data, fechas = fechas ,tempPromedio =tempPromedio,gradosDia = gradosDia , estacionName = estacionName, nroSemanas = nroSemanas,fechaFinal=fechaFinal)

@app.route('/EnviarCorreo', methods = [ 'GET','POST'])
def EnviarCorreo():
    enviarEmail=EnviarEmail()
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    # MAIL_DEBUG : default app.debug
    app.config['MAIL_USERNAME'] = 'labsac2022@gmail.com'
    app.config['MAIL_PASSWORD'] = 'elpdxpfshttksfgh'
    # MAIL_DEFAULT_SENDER : default None
    # MAIL_MAX_EMAILS : default None
    # MAIL_SUPPRESS_SEND : default app.testing
    # MAIL_ASCII_ATTACHMENTS : default False
    mail = Mail(app)
    if request.method  == "POST":
        nombres = request.form.get("nombres")
        apellido_paterno = request.form.get("apellido_paterno")
        apellido_materno = request.form.get("apellido_materno")
        email = request.form.get("email")
        asociacion = request.form.get("asociacion")
        Dispositivo = "Laptop o Computadora"
        mensaje = request.form.get("mensaje")
    
        msg = Message("Sugerencias y consultas - °AHora", sender="labsac2022@gmail.com", recipients=["labsac2022@gmail.com"])
        msg.body = "Nombre: {} \nApellidos: {} {}\nEmail: {}\nAsociación: {}\nDispositivo remitente: {}\nMensaje:\n{}".format(nombres, apellido_paterno, apellido_materno, email, asociacion,Dispositivo, mensaje)
        try:
            mail.send(msg)
            return redirect(url_for("MensajeEnviado"))
        except:
            return redirect(url_for("MensajeError"))
    return render_template("EnviarCorreo.html", form=enviarEmail)

@app.route('/MensajeEnviado', methods = [ 'GET','POST'])
def MensajeEnviado():
    return render_template("MensajeEnviado.html")

@app.route('/MensajeError', methods = [ 'GET','POST'])
def MensajeError():
    return render_template("MensajeError.html")

""" @app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    flash('Error: Verifique los datos ingresados')
    return render_template("formError.html", e=e), 500 

 """


def track_visitor():
 print("Estoy en Visitor")
 if not config.is_tracking_allowed():
	 	#print("primer if")
        return
 else:
        print("else....")		
        ip_address = request.remote_addr
        requested_url = request.url
        referer_page = request.referrer
        page_name = request.path
        query_string = request.query_string
        user_agent = request.user_agent.string
                
        if config.track_session():
            log_id = session['log_id'] if 'log_id' in session else 0
            no_of_visits = session['no_of_visits']
            current_page = request.url
            previous_page = session['current_page'] if 'current_page' in session else ''
            
            if previous_page != current_page:
                
                log_visitor(ip_address, requested_url, referer_page, page_name, query_string, user_agent, no_of_visits)
        else:			
            # conn = None
            cursor = None
            
            session.modified = True
            
            try:				
                #conn = mysql.connect()
                # conn = mysql.connection()
                # cursor = conn.cursor()
                cursor = mysql.connection.cursor()
                
                log_id = log_visitor(ip_address, requested_url, referer_page, page_name, query_string, user_agent)
                
                #print('log_id', log_id)
                
                if log_id > 0:				
                    sql = 'select max(no_of_visits) as next from visits_log_peru limit 1'
                    
                    # conn = mysql.connect()
                    # conn = mysql.connection()
                    #cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
                    cursor = mysql.connection.cursor()
                    
                    cursor.execute(sql)
                    row = cursor.fetchone()
                    
                    count = 0
                    if row['next']:
                        count += 1
                    else:
                        count = 1
                    
                    sql = 'UPDATE visits_log_peru set no_of_visits = %s WHERE log_id = %s'
                    data = (count, log_id,)
                    
                    cursor.execute(sql, data)
                    
                    # conn.commit()
                    mysql.connection.commit()
                    
                    session['track_session'] = True
                    session['no_of_visits'] = count
                    session['current_page'] = requested_url				
                else:
                    session['track_session'] = False
            except Exception as e:
                print(e)
                session['track_session'] = False
            finally:
                cursor.close()
                # conn.close()
				
def log_visitor(ip_address, requested_url, referer_page, page_name, query_string, user_agent, no_of_visits=None):
	sql = None
	data = None
	conn = None
	cursor = None
	log_id = 0
	
	print("Voy a insertar")
	if no_of_visits == None:
		sql = "INSERT INTO visits_log_peru(no_of_visits, ip_address, requested_url, referer_page, page_name, query_string, user_agent) VALUES(%s, %s, %s, %s, %s, %s, %s)"
		data = (no_of_visits, ip_address, requested_url, referer_page, page_name, query_string, user_agent,)
	else:
		sql = "INSERT INTO visits_log_peru(ip_address, requested_url, referer_page, page_name, query_string, user_agent) VALUES(%s, %s, %s, %s, %s, %s)"
		data = (ip_address, requested_url, referer_page, page_name, query_string, user_agent,)
	
	try:				
		# conn = mysql.connect()
		# conn = mysql.connection()
		cursor = mysql.connection.cursor()
		
		cursor.execute(sql, data)
		
		mysql.connection.commit()
		
		log_id = cursor.lastrowid
		
		return log_id
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		# conn.close()

if __name__ == '__main__':
    app.run(port=5000, debug=True)