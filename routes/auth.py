from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session, g
import pymysql, os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), '.env'))

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
    

    if request.method == 'POST':
       
        username=request.form['username']
        conn, cur = get_conn()
        cur=conn.cursor()
        
        cur.execute("SELECT contraseña, nmrol FROM covid.usuarios, covid.rol WHERE Usuario = '"+username+"' AND rol.idrol = usuarios.rol;")        
        myresult = cur.fetchall()

        cur.close()
        pw="0"
        if myresult:
            pw=myresult[0][0]
            rol=myresult[0][1]
        #check_password_hash(pw, request.form['password'])
        
        # check if user exists and password is correct
        if username and check_password_hash(pw, request.form['password']):

            session['rol'] = rol
            
            if rol == 'Administrador':
                return redirect(url_for('admin_.register_'))

            elif rol == 'Medico':
                return redirect(url_for('medico.map'))

            elif rol == 'Ayudante':
                return redirect(url_for('helper.choice'))

            else:
                return redirect(url_for('auth.login_'))
        else:
            flash("Username or password invalid")
            return redirect(url_for('auth.login_'))
    else:
        return render_template("login.html")

@auth.route('/logout')
@auth.route('/<rol>/logout')
def logout(rol):
    session.pop('username', None)
    return redirect(url_for('auth.login_'))
