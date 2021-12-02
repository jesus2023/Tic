from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session, g
import pymysql, os
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os.path import join, dirname
import googlemaps
from datetime import datetime
import requests
from urllib.parse import urlencode


load_dotenv(join(dirname(__file__), '.env'))

helper = Blueprint('helper', __name__)

api=os.getenv('API')


def extract_lat_lng(address_or_postalcode, data_type = 'json'):
    api_key = api
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address": address_or_postalcode, "key": api_key}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    r = requests.get(url)
    if r.status_code not in range(200, 299): 
        return {}
    latlng = {}
    try:
        latlng = r.json()['results'][0]['geometry']['location']
    except:
        pass
    lat = latlng.get("lat")
    lon = latlng.get("lng")
    return lat, lon

def get_conn():
    if "conn" not in g:
        g.conn = pymysql.connect(
            host=os.getenv('FLASK_DATABASE_HOST'),
            user=os.getenv('FLASK_DATABASE_USER'),
            password=os.getenv('FLASK_DATABASE_PASSWORD'),
            database=os.getenv('FLASK_DATABASE')
        )
        g.cur=g.conn.cursor()
    return g.conn, g.cur

@helper.route('/ayudante/choice', methods=['POST', 'GET'])
def choice():
    return render_template("Helperchoice.html")

@helper.route('/ayudante/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
       
        name = request.form['name']
        Lname = request.form['Lname']
        cc = request.form['cc']
        gender = request.form['gender']
        birth = request.form['birth']
        add = request.form['address']
        jobadd = request.form['jobaddress']
        result = request.form['result']
        result_date = request.form['result_date']
        address = add + ", Barranquilla, Atlántico"
        addressjob = jobadd + ", Barranquilla, Atlántico"
        
        lat_add, lon_add = extract_lat_lng(address)
        lat_jobadd, lon_jobadd = extract_lat_lng(addressjob)
        lat_add= str(lat_add)
        lon_add = str(lon_add)
        lat_jobadd = str(lat_jobadd)
        lon_jobadd = str(lon_jobadd)

        conn, cur = get_conn()
        cur=conn.cursor()        
        cur.execute("SELECT cedula FROM covid.registrar WHERE cedula = '"+cc+"';")        
        id = cur.fetchall() # get user from database 
        
        if id:  # check if user exists
            
            cur.execute("SELECT * FROM covid.registrar WHERE cedula = '"+cc+"' AND nombre = '"+name+"' AND apellido = '"+Lname+"' AND sexo = '"+gender+"' AND nacimiento = '"+birth+"';")        
            myresult = cur.fetchall() # get user from database 
            print(myresult)
            m="5"
            cur.execute("SELECT est.nmestado FROM covid.registrar regis, covid.gestion gest, covid.estado est WHERE gest.estado= est.idestado and gest.idcaso=regis.idcaso and gest.estado='"+m+"' and regis.cedula='"+cc+"';")        
            state = cur.fetchall() # get user from database 
            print(state[0][0])
            
            if myresult and state[0][0] != "Muerte":
                cur.execute(f"INSERT INTO covid.registrar (latitudCasa, longitudCasa, latitudJob,longitudJob,cedula, nombre, apellido, sexo, nacimiento, dirCasa, dirTrabajo, resultado, fechaExam) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (lat_add,lon_add,lat_jobadd, lon_jobadd,cc, name, Lname, gender, birth, add, jobadd, result, result_date))
                conn.commit() 
                cur.close()
                flash("Case succesfully added")
                return redirect(url_for('helper.register'))

            else:
                if state[0][0] == "Muerte":
                    flash("No puede registrar este caso, el usuario murio")
                    cur.close()
                    return redirect(url_for('helper.register'))
                else:
                    flash("User data does not match")
                    cur.close()
                    return redirect(url_for('helper.register'))

        else: 
            print(lat_add,lon_add,lat_jobadd, lon_jobadd)
            cur.execute(f"INSERT INTO covid.registrar (cedula, nombre, apellido, sexo, nacimiento, dirCasa, dirTrabajo, resultado, fechaExam, latitudCasa,longitudCasa,latitudJob,longitudJob) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (cc, name, Lname, gender, birth, add, jobadd, result, result_date,lat_add, lon_add, lat_jobadd, lon_jobadd))
            conn.commit() 
            cur.close()
            flash("Case succesfully added")
            return redirect(url_for('helper.register'))           
    else:
        return render_template("Reghelper.html")


@helper.route('/ayudante/manage', methods=['POST', 'GET'])
def manage():
    if request.method == 'POST':
        print("")

        search=request.form['search']
        print(search)
        select=request.form['select']
        conn, cur = get_conn()
        cur=conn.cursor()
        

        if select == "2":
            cur.execute("SELECT regis.idcaso, regis.nombre, regis.apellido, regis.cedula, sex.nmsexo Sexo, regis.nacimiento 'Fecha Nacimiento', regis.dirCasa 'Dirección Casa', regis.dirTrabajo 'Dirección Trabajo', nmresultado 'Resultado Test Covid', regis.fechaExam 'Fecha de Prueba Covid'FROM covid.registrar regis, covid.sexo sex, covid.resultado res WHERE regis.sexo = sex.idsexo AND regis.resultado = res.idresultado AND regis.nombre = '"+search+"' order by regis.fechaExam;")        
            myresult = cur.fetchall()
            cur.close()
            return render_template("Gesthelper.html", myresult=myresult, search=search, select=select)

        elif select == "3":
            cur.execute("SELECT regis.idcaso, regis.nombre, regis.apellido, regis.cedula, sex.nmsexo Sexo, regis.nacimiento 'Fecha Nacimiento', regis.dirCasa 'Dirección Casa', regis.dirTrabajo 'Dirección Trabajo', nmresultado 'Resultado Test Covid', regis.fechaExam 'Fecha de Prueba Covid'FROM covid.registrar regis, covid.sexo sex, covid.resultado res WHERE regis.sexo = sex.idsexo AND regis.resultado = res.idresultado AND regis.cedula = '"+search+"' order by regis.fechaExam;")        
            myresult = cur.fetchall()
            cur.close()
            return render_template("Gesthelper.html", myresult=myresult, search=search, select=select)

        elif select == "1":
            cur.execute("SELECT regis.idcaso, regis.nombre, regis.apellido, regis.cedula, sex.nmsexo Sexo, regis.nacimiento 'Fecha Nacimiento', regis.dirCasa 'Dirección Casa', regis.dirTrabajo 'Dirección Trabajo', nmresultado 'Resultado Test Covid', regis.fechaExam 'Fecha de Prueba Covid'FROM covid.registrar regis, covid.sexo sex, covid.resultado res WHERE regis.sexo = sex.idsexo AND regis.resultado = res.idresultado AND regis.idCaso = '"+search+"' order by regis.fechaExam;")        
            myresult = cur.fetchall()
            cur.close()
            return render_template("Gesthelper.html", myresult=myresult, search=search, select=select)

        else:
            return render_template("Gesthelper.html")
    else:
        return render_template("Gesthelper.html")


@helper.route('/ayudante/manage/add', methods=['POST', 'GET'])
def manage_add():
    if request.method == 'POST':
        cedula=request.form['cedula']        
        conn, cur = get_conn()
        cur=conn.cursor()
        cur.execute("SELECT regis.idcaso, regis.nombre, regis.apellido, regis.cedula, sex.nmsexo Sexo, regis.nacimiento 'Fecha Nacimiento', regis.dirCasa 'Dirección Casa', regis.dirTrabajo 'Dirección Trabajo', nmresultado 'Resultado Test Covid', regis.fechaExam 'Fecha de Prueba Covid'FROM covid.registrar regis, covid.sexo sex, covid.resultado res WHERE regis.sexo = sex.idsexo AND regis.resultado = res.idresultado AND regis.cedula = '"+cedula+"' order by regis.fechaExam;")        
        myresult = cur.fetchall()
        cur.execute("SELECT regis.idcaso, gest.fecha 'Fecha Nuevo Ingreso', est.nmestado 'Estado del paciente' FROM covid.registrar regis, covid.gestion gest, covid.estado est WHERE gest.estado= est.idestado and regis.cedula='"+cedula+"' and gest.idcaso=regis.idcaso  order by gest.fecha;")        
        result = cur.fetchall()
        print(result)

        if result:
            estado=result[len(result)-1][2]
        else:
            estado="NA"
        cur.close()
        if cedula:
            return render_template("Helper_states.html",estado=estado, myresult=myresult, result=result, cedula=cedula)
        else:
            search=request.form['search']
            select=request.form['select']
            
            flash("Por favor elija un usuario antes de gestionar")
            return redirect(url_for('helper.manage', search=search, select=select), code=307)
    else:
        return render_template("Gesthelper.html")


@helper.route('/ayudante/manage/addstate', methods=['POST', 'GET'])
def manage_addstate():
    if request.method == 'POST':
        estado=request.form['estado']
        state=request.form['state']
        cedula=request.form['cedula']
        start=request.form['start']

        if estado == 'Muerte':
            flash("No es posible actualizar estado, la persona ha fallecido")
            return redirect(url_for('helper.manage_add', cedula=cedula), code=307)
        else:

            conn, cur = get_conn()
            cur=conn.cursor()   

            cur.execute("SELECT regis.idcaso, nmresultado FROM covid.registrar regis, covid.resultado res WHERE regis.fechaExam = (select max(regis.fechaExam) from covid.registrar regis where regis.cedula = '"+cedula+"') AND regis.cedula = '"+cedula+"' and regis.resultado = res.idresultado;") 
            myresult = cur.fetchall()
            
            if myresult[0][1]=="Positivo":
                cur.execute(f"INSERT INTO covid.gestion (cedula, estado, idcaso, fecha) VALUES (%s,%s,%s,%s)", (cedula, state, myresult[0][0], start)) 
                conn.commit() 
                cur.close()


        return redirect(url_for('helper.manage_add', cedula=cedula), code=307)
    else:
        return render_template("Gesthelper.html")
        

@helper.route('/logout')
@helper.route('/<rol>/logout')
def logout(rol):
    session.pop('username', None)
    return redirect(url_for('auth.login_'))
