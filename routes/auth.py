from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session, g
import pymysql, os
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

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

@auth.route('/login_', methods=['POST', 'GET'])
def login_():
    print("entra")

    if request.method == 'POST':
        print("entra")
        username=request.form['username']
        conn, cur = get_conn()
        cur=conn.cursor()
        
        cur.execute("SELECT contraseña, nmrol FROM covid.usuarios, covid.rol WHERE Usuario = '"+username+"' AND rol.idrol = usuarios.rol;")        
        myresult = cur.fetchall()
        cur.close()
        pw=myresult[0]
        rol=myresult[1]
        print(pw,username)
        #check_password_hash(pw, request.form['password'])

        # check if user exists and password is correct
        if username and request.form['password']==pw:
            session['rol'] = rol
            
            if rol == 'administrador':
                return redirect(url_for('admin.signup'))

            elif rol == 'medico':
                return redirect(url_for('medico.map'))

            elif rol == 'ayudante':
                return redirect(url_for('user.register'))

            else:
                return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('auth.login'))
    else:
        return render_template("login.html")

@auth.route('/logout')
@auth.route('/<rol>/logout')
def logout(rol_):
    session.pop('username', None)
    return redirect(url_for('auth.login'))
