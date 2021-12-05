from flask import Flask, render_template, request, session, g, jsonify
import pymysql, os
from routes.auth import auth
from routes.admin_ import admin_
from routes.helper import helper
from routes.med import med

from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), '.env'))




app = Flask(__name__)
app.secret_key = str(os.urandom(256))



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


@app.route('/api/data')
def test():
    conn, cur = get_conn()
    cur=conn.cursor()

#-------------------Gráfica x y--------------------
    
    cur.execute("SELECT regis.fechaExam, sum(CASE WHEN resul.nmresultado = 'positivo' THEN 1 ELSE 0 END) FROM covid.registrar regis, covid.resultado resul where resul.idresultado= regis.resultado  group by regis.fechaExam order by regis.fechaExam")        
    contagiados = cur.fetchall()
    cur.execute("SELECT gest.fecha, sum(CASE WHEN est.idestado = '5' THEN 1 ELSE 0 END) FROM covid.gestion gest, covid.estado est where gest.estado= est.idestado group by gest.fecha order by gest.fecha")        
    muertes = cur.fetchall()
    
    data_fecha_c = []
    for i in range(len(contagiados)):
        data_fecha_c.append(contagiados[i][0].strftime("%d/%m/%y"))
    
    data_c = []
    for i in range(len(contagiados)):
        data_c.append(contagiados[i][1])
    
    data_fecha_m = []
    for i in range(len(muertes)):
        data_fecha_m.append(muertes[i][0].strftime("%d/%m/%y"))
    
    data_m = []
    for i in range(len(muertes)):
        data_m.append(muertes[i][1])

#------------------Gráficos pie 1---------------------

    cur.execute("SELECT sum(CASE WHEN resul.nmresultado = 'positivo' THEN 1 ELSE 0 END) FROM covid.registrar regis, covid.resultado resul where resul.idresultado= regis.resultado ;")        
    n_infectados = cur.fetchall()
    cur.execute("SELECT count(gest.estado) FROM covid.registrar regis, covid.gestion gest, covid.estado est WHERE gest.estado= est.idestado and gest.idcaso=regis.idcaso and gest.estado='5';")        
    n_muertos = cur.fetchall()
    cur.execute("SELECT count(gest.estado) FROM covid.registrar regis, covid.gestion gest, covid.estado est WHERE gest.estado= est.idestado and gest.idcaso=regis.idcaso and gest.estado='4';")        
    n_curados = cur.fetchall()

#------------------Gráficos pie 2---------------------

    cur.execute("SELECT count(gest.estado) FROM covid.registrar regis, covid.gestion gest, covid.estado est WHERE gest.estado= est.idestado and gest.idcaso=regis.idcaso and gest.estado='1';")        
    n_ = cur.fetchall()
    cur.execute("SELECT count(gest.estado)  FROM covid.registrar regis, covid.gestion gest, covid.estado est WHERE gest.estado= est.idestado and gest.idcaso=regis.idcaso and gest.estado='2';")        
    n_hospital = cur.fetchall()
    cur.execute("SELECT count(gest.estado) FROM covid.registrar regis, covid.gestion gest, covid.estado est WHERE gest.estado= est.idestado and gest.idcaso=regis.idcaso and gest.estado='3';")        
    n_UCI = cur.fetchall()
    cur.execute("SELECT count(gest.estado) FROM covid.registrar regis, covid.gestion gest, covid.estado est WHERE gest.estado= est.idestado and gest.idcaso=regis.idcaso and gest.estado='5';")        
    n_death = cur.fetchall()
    
#------------------Gráficos pie 3---------------------

    cur.execute("SELECT sum(CASE WHEN resul.nmresultado = 'positivo' THEN 1 ELSE 0 END) FROM covid.registrar regis, covid.resultado resul where resul.idresultado= regis.resultado  ")        
    n_positivos = cur.fetchall()
    cur.execute("SELECT sum(CASE WHEN resul.nmresultado = 'negativo' THEN 1 ELSE 0 END) FROM covid.registrar regis, covid.resultado resul where resul.idresultado= regis.resultado")        
    n_negativos = cur.fetchall()

    cur.close()
    
    
    
    return jsonify(data_fecha_c, data_c ,data_fecha_m , data_m, 
                n_infectados,n_curados,n_muertos, 
                n_negativos,n_positivos,
                n_death,n_UCI,n_hospital,n_)

@app.route('/')
def index():
    return render_template('Principal.html')

@app.route('/rol')
def rol():
    rol = request.args.get("rol")
    return (rol)

# routes blueprints
app.register_blueprint(auth)
app.register_blueprint(med)
app.register_blueprint(admin_)
app.register_blueprint(helper)

        
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8888)