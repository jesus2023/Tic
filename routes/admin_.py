from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session,g
import pymysql, os
from werkzeug.security import generate_password_hash, check_password_hash

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

@admin_.route('/administrador/signup', methods=['POST', 'GET'])
def signup_():
    
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
            cur.close()

            if users:  # check if user exists
                flash("Username already taken")
                print("Ya existe ", users)
                return redirect(url_for('auth.login_'))
            else:
                conn, cur = get_conn()
                cur=conn.cursor()
                p=generate_password_hash(pw)
                cur.execute(f"INSERT INTO covid.usuarios (cedula, nombre, apellido, rol, usuario, contraseña) VALUES (%s,%s,%s,%s,%s,%s)", (cc, name, lname, rol, username, p))
                conn.commit() 
                flash("Username succesfully added")
                print(p)
                print(check_password_hash(p, request.form['password']))

                return redirect(url_for('admin_.signup_'))
        else:
            return render_template("pregister.html")
    else:
        return redirect(url_for('auth.login'))