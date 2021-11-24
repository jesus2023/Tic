from flask import Flask, render_template, request, session, g
import pymysql, os


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
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('helper.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        pw = request.form['password']
        user = request.form['username']

        conn, cur = get_conn()
        cur=conn.cursor()
        print(user,pw)
        cur.execute("SELECT * FROM covid.Admins WHERE Usuario = Dari AND Contraseña = admin1;")
        myresult = cur.fetchall()
        cur.close()
        print(myresult)

        if len(myresult) == 0:
            return "Entrada no exitosa" 
        else:
           return render_template('register.html') #Redirige a la pagina del administrador --Sebastian

@app.route('/bulma')
def bulma():
    return render_template('bulma.html')

        
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
