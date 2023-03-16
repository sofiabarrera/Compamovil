from flask import Flask
from flask import render_template,request
from flaskext.mysql import MySQL
from flask import send_from_directory
from flask import send_file



logusuario=""
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
    return render_template('empleados/Crear.html',empleados=empleados, user=logusuario)

@app.route('/login.html')
def login():
    Valida="0"
    return render_template('empleados/login.html',valida=Valida)



@app.route('/store', methods=['POST'])
def store():
    sql="INSERT INTO `usuario` (`nombre`, `Correo`, `Numero`, `Nacimiento`, `Contraseña`) VALUES (%s, %s, %s, %s, %s);"
    sql2="SELECT * FROM `usuario`;"

    validar=0

    
    con=""
    validarN=0
    validarCOR=0
    validarCel=0
    validarContra=0
    validarReContra=1
    validarD=0

    _nombre=request.form['Nombre']
    _Correo=request.form['Correo']
    _celular=request.form['celular']
    _date=request.form['date']
    _contraseña=request.form['contraseña']
    _REcontraseña=request.form['contraseñaRepeat']

    datos=(_nombre,_Correo,_celular,_date,_contraseña)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql2)
    conn.commit()
    if _contraseña==_REcontraseña:
        validar=1
        validarReContra=0

    if len(_contraseña)<=5:
        validar=1
        validarContra=1

    if len(_Correo)<=5:
        validar=1
        validarCOR=1

    if len(_celular)<=5:
        validar=1
        validarCel=1

    if len(_nombre)<=5:
        validar=1
        validarN=1


    con=(validarN,validarCOR,validarCel,validarContra,validarD,validarReContra)
    if validar==1:
        print(con[4])
        return render_template('empleados/register.html', con=con)

    if validar==0:
        cursor.execute(sql,datos)  
        empleados=cursor.fetchall()
        return render_template('empleados/register.html')




@app.route('/validate', methods=['POST'])
def validate():
    _Correo=request.form['Correo']
    _contraseña=request.form['contraseña']
    
    Valida="0"
    sql2="SELECT * FROM `usuario` WHERE `Correo` = %s;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql2,_Correo)
    usuario=cursor.fetchall()
    ver=(usuario[0][5])
    conn.commit()

    if ver==_contraseña:

        logusuario=(usuario[0][1])
        Valida="0"
        return render_template('empleados/Principal.html',valida=Valida, user=logusuario )
    else:
        Valida="1"
        return render_template('empleados/login.html',valida=Valida)
        
    


    


@app.route('/register.html')
def Registro():
    con=""
    validarN="0"
    validarCOR="0"
    validarCel="0"
    validarContra="0"
    validarReContra="1"
    validarD="0"
    con=(validarN,validarCOR,validarCel,validarContra,validarD)
    return render_template('empleados/register.html', con=con)










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