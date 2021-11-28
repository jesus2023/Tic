from flask import Flask, render_template, request, session, g
import pymysql, os
from routes.auth import auth
from routes.admin import admin



app = Flask(__name__)


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

@app.route('/')
def index():
    return render_template('Principal.html')

@app.route('/rol')
def rol():
    rol = request.args.get("rol")
    print(rol)
    return (rol)

"""@app.route('/login')
def login():
    return render_template('plogin.html')"""

@app.route('/register')
def register():
    return render_template('pregister.html')

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

        
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8888)