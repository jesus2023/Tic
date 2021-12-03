from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session,g, jsonify
import pymysql, os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), '.env'))

med = Blueprint('med', __name__)

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

@med.route('/medico/choice', methods=['POST', 'GET'])
def medico_choice():
    return render_template("doc_choices.html")
    
@med.route('/ubic', methods=['POST', 'GET'])
def ubic():
    cedula = request.args.get("param1")

    conn, cur = get_conn()
    cur=conn.cursor()
    cur.execute("SELECT regis.latitudCasa, regis.longitudCasa, regis.latitudJob, regis.longitudJob FROM covid.registrar regis where regis.cedula='"+cedula+"' and idCaso = (select MAX(idCaso) FROM covid.registrar regis where regis.cedula='"+cedula+"');")        
    myresult = cur.fetchall()
    cur.close()
    return jsonify(myresult)

@med.route('/medico/search', methods=['POST', 'GET'])
def medico_search():
    if request.method == 'POST':
        search=request.form['search']
       
        select=request.form['select']
        conn, cur = get_conn()
        cur=conn.cursor()
        
        if select == "2":
            cur.execute("SELECT  regis.nombre, regis.apellido, regis.cedula, sex.nmsexo Sexo, regis.nacimiento 'Fecha Nacimiento', regis.dirCasa 'Dirección Casa', regis.dirTrabajo 'Dirección Trabajo', nmresultado 'Resultado Test Covid', regis.fechaExam 'Fecha de Prueba Covid'FROM covid.registrar regis, covid.sexo sex, covid.resultado res WHERE regis.sexo = sex.idsexo AND regis.resultado = res.idresultado AND regis.cedula = '"+search+"' order by regis.fechaExam;")        
            myresult = cur.fetchall()
            if myresult:
                cedula=str(myresult[0][2])
                cur.execute("SELECT gest.fecha 'Fecha Nuevo Ingreso', est.nmestado 'Estado del paciente' FROM covid.registrar regis, covid.gestion gest, covid.estado est WHERE gest.estado= est.idestado and regis.cedula='"+cedula+"' and gest.idcaso=regis.idcaso  order by gest.fecha;")        
                result = cur.fetchall()
                cur.close()
                return render_template("docsearch.html", myresult=myresult, result=result, search=search, select=select,cedula=cedula)
            else:
                return render_template("docsearch.html")
        elif select == "1":
            
            cur.execute("SELECT  regis.nombre, regis.apellido, regis.cedula, sex.nmsexo Sexo, regis.nacimiento 'Fecha Nacimiento', regis.dirCasa 'Dirección Casa', regis.dirTrabajo 'Dirección Trabajo', nmresultado 'Resultado Test Covid', regis.fechaExam 'Fecha de Prueba Covid'FROM covid.registrar regis, covid.sexo sex, covid.resultado res WHERE regis.sexo = sex.idsexo AND regis.resultado = res.idresultado AND regis.idCaso = '"+search+"' order by regis.fechaExam;")        
            myresult = cur.fetchall()
            if myresult:
                cedula=str(myresult[0][2])
                cur.execute("SELECT gest.fecha 'Fecha Nuevo Ingreso', est.nmestado 'Estado del paciente' FROM covid.registrar regis, covid.gestion gest, covid.estado est WHERE gest.estado= est.idestado and regis.cedula='"+cedula+"' and gest.idcaso=regis.idcaso  order by gest.fecha;")        
                result = cur.fetchall()
                cur.execute("SELECT regis.idcaso, gest.fecha 'Fecha Nuevo Ingreso', est.nmestado 'Estado del paciente' FROM covid.registrar regis, covid.gestion gest, covid.estado est WHERE gest.estado= est.idestado and regis.cedula='"+cedula+"' and gest.idcaso=regis.idcaso  order by gest.fecha;")        
                result = cur.fetchall()
                print(result)
                if result:
                    estado=result[len(result)-1][2]
                else:
                    estado=""
                cur.close()

                return render_template("docsearch.html", myresult=myresult, result=result, search=search, select=select,cedula=cedula, estado=estado)
            else:
                    return render_template("docsearch.html",cedula="")

    else:
        return render_template("docsearch.html")

@med.route('/medico/mapa', methods=['POST', 'GET'])
def medico_mapa():
    
    conn, cur = get_conn()
    cur=conn.cursor()
    cur.execute("SELECT DISTINCT regis.cedula FROM covid.registrar regis;")        
    myresult = cur.fetchall()

    cedulas = []
    
    for i in range (len(myresult)):
        cedula = str(myresult[i][0])
        cedulas.append(cedula)
        
    print(cedulas)

    cur.close()   
    return render_template("doc_generalmap.html", cedulas = cedulas)

@med.route('/mapa_general', methods=['POST', 'GET'])
def mapa_general():

    conn, cur = get_conn()
    cur=conn.cursor()
    cur.execute("SELECT DISTINCT regis.cedula FROM covid.registrar regis;")        
    myresult = cur.fetchall()

    cedulas = []
    
    for i in range (len(myresult)):
        cedula = str(myresult[i][0])
        cedulas.append(cedula)
        
    print(cedulas)

    cur.close()
    return jsonify(cedulas)

@med.route('/mapa_general_casos', methods=['POST', 'GET'])
def mapa_general_casos():

    cedula = request.args.get("param1")

    conn, cur = get_conn()
    cur=conn.cursor()
    cur.execute("SELECT regis.cedula, regis.latitudCasa, regis.longitudCasa, resul.nmresultado FROM covid.registrar regis, covid.resultado resul where regis.cedula='"+cedula+"' and regis.resultado=resul.idresultado and regis.idCaso = (select MAX(idCaso) FROM covid.registrar regis where regis.cedula='"+cedula+"')")               
    myresult = cur.fetchall()

    print(myresult[0][3])

    cur.close()
    return jsonify(myresult)