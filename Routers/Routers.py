from flask import Flask
from flask import render_template,request
from flaskext.mysql import MySQL
from flask import send_from_directory
from flask import send_file




app=Flask(__name__)

mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_PORT']=3307
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='1234'
app.config['MYSQL_DATABASE_DB']='usuario'
mysql.init_app(app)

@app.route('/')
def index():
    sql="SELECT * FROM `usuario`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    print(empleados)
    conn.commit()

    return render_template('empleados/index.html',empleados=empleados)



@app.route('/Crear.html')
def Crear():
    sql2="SELECT * FROM `usuario`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql2)
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/Crear.html',empleados=empleados)

@app.route('/login.html')
def login():
    sql2="SELECT * FROM `usuario`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql2)
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/login.html',empleados=empleados)



@app.route('/store', methods=['POST'])
def store():
    sql="INSERT INTO `usuario` (`nombre`, `Correo`, `Numero`, `Nacimiento`, `Contraseña`) VALUES (%s, %s, %s, %s, %s);"
    sql2="SELECT * FROM `usuario`;"

    _nombre=request.form['Nombre']
    _Correo=request.form['Correo']
    _celular=request.form['celular']
    _date=request.form['date']
    _contraseña=request.form['contraseña']

    datos=(_nombre,_Correo,_celular,_date,_contraseña)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    cursor.execute(sql2)
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/register.html',empleados=empleados)

@app.route('/register.html')
def Registro():

    return render_template('empleados/register.html')










@app.route('/img/carousel1.jpg')
def ind():

    return send_file('templates\empleados\img\carousel1.jpg')


@app.route('/css/style.css')
def indes():

    return send_file('templates\empleados\css\style.css')

@app.route('/lib/tempusdominus/js/moment.min.js')
def indesa():

    return send_file('templates\empleados\css\style.min.css')

@app.route('/lib/tempusdominus/css/tempusdominus-bootstrap-4.min.css')
def a():

    return send_file('templates\empleados\lib\tempusdominus\css\tempusdominus-bootstrap-4.min.css')

@app.route('/js/main.js')
def aa():

    return send_file('templates\empleados\js\main.js')


@app.route('/img/carousel2.jpg')
def aaa():

    return send_file('templates\empleados\img\carousel2.jpg')


@app.route('/img/carousel-1.jpg')
def aaaa():

    return send_file('templates\empleados\img\carousel2.jpg')

if __name__=='__main__':

    app.run(debug=True)