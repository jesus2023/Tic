from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session,g
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


@med.route('/medico/search', methods=['POST', 'GET'])
def medico_search():
    if request.method == 'POST':
        search=request.form['search']
       
        select=request.form['select']
        conn, cur = get_conn()
        cur=conn.cursor()
        
        if select == "2":
            cur.execute("SELECT regis.nombre, regis.apellido, regis.cedula, sex.nmsexo Sexo, regis.nacimiento 'Fecha Nacimiento', regis.dirCasa 'Dirección Casa', regis.dirTrabajo 'Dirección Trabajo', nmresultado 'Resultado Test Covid', regis.fechaExam 'Fecha de Prueba Covid'FROM covid.registrar regis, covid.sexo sex, covid.resultado res WHERE regis.sexo = sex.idsexo AND regis.resultado = res.idresultado AND regis.nombre = '"+search+"' order by regis.fechaExam;")        
            myresult = cur.fetchall()
            cur.close()
            return render_template("docsearch.html", myresult=myresult, search=search, select=select)

        elif select == "3":
            cur.execute("SELECT regis.nombre, regis.apellido, regis.cedula, sex.nmsexo Sexo, regis.nacimiento 'Fecha Nacimiento', regis.dirCasa 'Dirección Casa', regis.dirTrabajo 'Dirección Trabajo', nmresultado 'Resultado Test Covid', regis.fechaExam 'Fecha de Prueba Covid'FROM covid.registrar regis, covid.sexo sex, covid.resultado res WHERE regis.sexo = sex.idsexo AND regis.resultado = res.idresultado AND regis.cedula = '"+search+"' order by regis.fechaExam;")        
            myresult = cur.fetchall()
            cur.close()
            return render_template("docsearch.html", myresult=myresult, search=search, select=select)

        elif select == "1":
            cur.execute("SELECT regis.nombre, regis.apellido, regis.cedula, sex.nmsexo Sexo, regis.nacimiento 'Fecha Nacimiento', regis.dirCasa 'Dirección Casa', regis.dirTrabajo 'Dirección Trabajo', nmresultado 'Resultado Test Covid', regis.fechaExam 'Fecha de Prueba Covid'FROM covid.registrar regis, covid.sexo sex, covid.resultado res WHERE regis.sexo = sex.idsexo AND regis.resultado = res.idresultado AND regis.idCaso = '"+search+"' order by regis.fechaExam;")        
            myresult = cur.fetchall()
            cur.close()
            return render_template("docsearch.html", myresult=myresult, search=search, select=select)

    else:
        return render_template("docsearch.html")