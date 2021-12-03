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
    n_casa = cur.fetchall()
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
    print(data_fecha_m, data_fecha_c)

    return render_template('Principal.html', df=data_fecha_c, dc=data_c)

@app.route('/rol')
def rol():
    rol = request.args.get("rol")
    print(rol)
    return (rol)

@med.route('/lineChar', methods=['POST', 'GET'])
def line_Chart():

    
    return render_template("Principal.html")



#--------------------------------Módulo de administrador-------------------------------------------------------    

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        pw = request.form['password']
        user = request.form['username']
        print(pw,user)

        conn, cur = get_conn()
        cur=conn.cursor()
        print(user,pw)
        cur.execute("SELECT * FROM covid.Admins WHERE Usuario = '"+user+"' AND Contraseña = '"+pw+"';")
        myresult = cur.fetchall()
        cur.close()
        print(myresult)

        if len(myresult) == 0:
            return render_template('plogin.html')
        else:
           return render_template('pregister.html') #Redirige a la pagina del administrador --Sebastian
    else:
        return render_template('plogin.html')

@app.route('/admin/register', methods=['POST', 'GET'])
def admin_reg():    

    #if render_template('Reghelper.html') == True: 
    rol = request.args.get("rol")
    print(rol)

    if request.method == 'POST':
        name = request.form['name']
        Lname = request.form['Lname']
        CC = request.form['CC']
        pw = request.form['password']
        user = request.form['user']
        rol1 = request.form['member']
        rol2 = request.args.get("member")
        print(name, Lname, CC, pw, user, rol1, rol2)
        return render_template('Reghelper.html')
    else:
        return render_template('Reghelper.html')
    
    #else:
    #   return render_template('Plogin.html')
#--------------------------------------Módulo de médicos-----------------------------------------------------

@app.route('/medico', methods=['POST', 'GET'])
def medico():
    if request.method == 'POST':
        pw= request.form['password']
        user = request.form['username']
        print(pw,user)

        conn, cur = get_conn()
        cur=conn.cursor()
        print(user,pw)

        cur.execute("SELECT u.usuario Usuario, u.contraseña Contraseña FROM covid.usuarios u, covid.rol rol WHERE u.rol= rol.idrol AND Usuario = '"+user+"' AND Contraseña = '"+pw+"' AND rol.nmrol = 'Medico';")
        myresult = cur.fetchall()
        cur.close()
        print(myresult)

        #Las rutas se ponen de acuerdo los html que sebas cree 

        if len(myresult) == 0:
            return render_template('Mlogin.html')
        else:
           return 'Modulo de médicos' 
    else:
        return render_template('Mlogin.html')

#--------------------------------------Módulo de ayudante-----------------------------------------------------

@app.route('/ayudante', methods=['POST', 'GET'])
def ayudante():
    if request.method == 'POST':
        pw = request.form['password']
        user = request.form['username']
        print(pw,user)

        conn, cur = get_conn()
        cur=conn.cursor()
        print(user,pw)

        cur.execute("SELECT u.usuario Usuario, u.contraseña Contraseña FROM usuarios u, rol rol WHERE u.rol= rol.idrol AND Usuario = '"+user+"' AND Contraseña = '"+pw+"' AND rol.nmrol = 'Ayudante';")
        myresult = cur.fetchall()
        cur.close()
        print(myresult)

        if len(myresult) == 0:
            return render_template('Alogin.html')
        else:
           return render_template('Reghelper.html')
    else:
        return render_template('Alogin.html')
       


#@app.route('/admin', methods=['POST', 'GET'])
#def Registro_Gestion():
   # return 'Registro de caso o Gestión'"""


# routes blueprints
app.register_blueprint(auth)
app.register_blueprint(med)
app.register_blueprint(admin_)
app.register_blueprint(helper)

#app.register_blueprint(user)

        
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8888)