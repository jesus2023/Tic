from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session, g
import pymysql, os
from werkzeug.security import generate_password_hash, check_password_hash

admin = Blueprint('admin', __name__)

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

@admin.route('/administrador/signup', methods=['POST', 'GET'])
def signup():
    if session['rol'] == 'administrador':
        if request.method == 'POST':
            username=request.form['username']
            conn, cur = get_conn()
            cur=conn.cursor()
            
            cur.execute("SELECT usuario FROM covid.usuarios WHERE Usuario = '"+username+"';")        
            users = cur.fetchall() # get user from database 
            cur.close()

            if users:  # check if user exists
                flash("Username already taken")
                return redirect(url_for('auth.login'))
            else:
                conn, cur = get_conn()
                cur=conn.cursor()
                cur.execute(f"INSERT INTO usuario (cedula, nombre, apellido, rol, usuario, contraseña) VALUES (%s,%s,%s,%s,%s,%s)", (request.form['cc'], request.form['name'], request.form['lname'], request.form['rol'], request.form['username'], generate_password_hash(request.form['password'])))
                conn.commit() 
                
                return redirect(url_for('admin.signup'))
        else:
            return render_template("pregister.html")
    else:
        return redirect(url_for('auth.login'))