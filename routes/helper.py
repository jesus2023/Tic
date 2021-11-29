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
       
        name = request.form['name']
        Lname = request.form['Lname']
        cc = request.form['cc']
        gender = request.form['gender']
        birth = request.form['birth']
        add = request.form['address']
        jobadd = request.form['jobaddress']
        result = request.form['result']
        result_date = request.form['result_date']

        print(name, Lname, cc, gender, birth, add, jobadd, result, result_date)

        conn, cur = get_conn()
        cur=conn.cursor()

        
        cur.execute("SELECT cedula FROM covid.registrar WHERE cedula = '"+cc+"';")        
        id = cur.fetchall() # get user from database 
        
        if id:  # check if user exists
            
            cur.execute("SELECT * FROM covid.registrar WHERE cedula = '"+cc+"' AND nombre = '"+name+"' AND apellido = '"+Lname+"' AND sexo = '"+gender+"' AND nacimiento = '"+birth+"';")        
            myresult = cur.fetchall() # get user from database 
            print(myresult)
            
            if myresult:
                
                cur.execute(f"INSERT INTO covid.registrar (cedula, nombre, apellido, sexo, nacimiento, dirCasa, dirTrabajo, resultado, fechaExam) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (cc, name, Lname, gender, birth, add, jobadd, result, result_date))
                conn.commit() 
                cur.close()
                flash("Case succesfully added")
                return redirect(url_for('helper.register'))

            else:    
                flash("User data does not match")
                cur.close()
                return redirect(url_for('helper.register'))
        else: 
            cur.execute(f"INSERT INTO covid.registrar (cedula, nombre, apellido, sexo, nacimiento, dirCasa, dirTrabajo, resultado, fechaExam) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (cc, name, Lname, gender, birth, add, jobadd, result, result_date))
            conn.commit() 
            cur.close()
            flash("Case succesfully added")
            return redirect(url_for('helper.register'))           
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
