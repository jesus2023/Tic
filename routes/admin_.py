from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session,g
import pymysql, os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), '.env'))

admin_ = Blueprint('admin_', __name__)

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

@admin_.route('/administrador/register', methods=['POST', 'GET'])
def register_():
    
    if session['rol'] == 'Administrador':
        if request.method == 'POST':
            
            username=request.form['user']
            name = request.form['name']
            lname = request.form['lname']
            cc = request.form['cc']
            pw = request.form['password']
            rol = request.form['rol']
            conn, cur = get_conn()
            cur=conn.cursor()

            cur.execute("SELECT usuario FROM covid.usuarios WHERE Usuario = '"+username+"';")        
            users = cur.fetchall() # get user from database 
            cur.execute("SELECT cedula FROM covid.usuarios WHERE Cedula = '"+cc+"';")        
            id = cur.fetchall() # get user from database 
            cur.close()

            if users:  # check if user exists
                flash("Username already taken")
                return redirect(url_for('admin_.register_'))
            elif id:
                flash("Id already taken")
                return redirect(url_for('admin_.register_'))
            else:
                conn, cur = get_conn()
                cur=conn.cursor()
                p=generate_password_hash(pw)
                cur.execute(f"INSERT INTO covid.usuarios (cedula, nombre, apellido, rol, usuario, contraseña) VALUES (%s,%s,%s,%s,%s,%s)", (cc, name, lname, rol, username, p))
                conn.commit() 
                flash("Username succesfully added")
                return redirect(url_for('admin_.register_'))
        else:
            return render_template("pregister.html")
    else:
        return redirect(url_for('auth.login'))