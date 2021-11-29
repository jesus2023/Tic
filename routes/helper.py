from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session, g
import pymysql, os
from werkzeug.security import generate_password_hash, check_password_hash

helper = Blueprint('helper', __name__)

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

@helper.route('/ayudante/choice', methods=['POST', 'GET'])
def choice():
    return render_template("Helperchoice.html")

@helper.route('/ayudante/register', methods=['POST', 'GET'])
def register():
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
        return render_template("Reghelper.html")


@helper.route('/ayudante/manage', methods=['POST', 'GET'])
def manage():
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
            return redirect(url_for('auth.login_'))
    else:
        return render_template("Reghelper.html")

@helper.route('/logout')
@helper.route('/<rol>/logout')
def logout(rol):
    session.pop('username', None)
    return redirect(url_for('auth.login_'))
