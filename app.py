from flask import Flask
from flask import Flask, session
from flask_session import Session
from flask import Flask, render_template, redirect, request, session
from flaskext.mysql import MySQL
from flask import send_from_directory
from flask import send_file
from flask import flash


var=""

app=Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
    return render_template('empleados/Crear.html',empleados=empleados, vara=vara)

@app.route('/login.html')
def login():
    Valida="0"
    return render_template('empleados/login.html',valida=Valida)



@app.route('/store_Aparato', methods=['POST'])
def store_Aparato():


    sql="INSERT INTO `aparato` (`Procesador`, `Software`, `Conectividad`, `Bateria`, `Precio medio`, `Resolucion pantalla`, `Mejor Uso`, `Resumen`, `ADMIN_ID`) VALUES (%s,%s,%s, %s, %s, %s, %s,%s,%s);"

    _Procesador=request.form['Procesador']
    _Software=request.form['Software']
    _Conectividad=request.form['Conectividad']
    _Bateria=request.form['Bateria']
    _Precio=request.form['Precio']
    _Resolucion=request.form['Resolucion']
    _Uso=request.form['Uso normal']
    _Resumen=request.form['Resumen']
    _Admin= session["ID"]


    datos=(_Procesador,_Software,_Conectividad,_Bateria,_Precio,_Resolucion,_Uso,_Resumen,_Admin)
    conn=mysql.connect()
    cursor=conn.cursor()      
    cursor.execute(sql,datos)  
    conn.commit()

    return redirect("/Gestion_dispositivos")


@app.route('/Actualizar_AP/<int:id>')
def Actualizar_AP(id):
    sql="SELECT * FROM `aparato` WHERE ID= %s;" 
    conn=mysql.connect()
    cursor=conn.cursor() 
    cursor.execute(sql,(id))  
    empleados=cursor.fetchall()
    print(empleados)
    conn.commit()
    return render_template('empleados/Actualizar_Aparato.html', aparato=empleados)



@app.route('/Actualizar_Aparato/<int:id>', methods=['POST'])
def Actualizar_Aparato(id):


    sql="UPDATE `aparato` SET `Procesador` = %s, `Software` = %s, `Conectividad` = %s, `Bateria` = %s, `Precio medio` = %s, `Resolucion pantalla` = %s, `Mejor Uso` = %s, `Resumen` = %s WHERE `aparato`.`ID` = %s;"

    _Procesador=request.form['Procesador']
    _Software=request.form['Software']
    _Conectividad=request.form['Conectividad']
    _Bateria=request.form['Bateria']
    _Precio=request.form['Precio']
    _Resolucion=request.form['Resolucion']
    _Uso=request.form['Uso normal']
    _Resumen=request.form['Resumen']
    _ID=id


    datos=(_Procesador,_Software,_Conectividad,_Bateria,_Precio,_Resolucion,_Uso,_Resumen,_ID)
    conn=mysql.connect()
    cursor=conn.cursor()      
    cursor.execute(sql,datos)  
    conn.commit()

    return redirect("/Gestion_dispositivos")





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

    
    if _contraseña==_REcontraseña:
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

    if len(_nombre)<=2:
        validar=1
        validarN=1


    con=(validarN,validarCOR,validarCel,validarContra,validarD,validarReContra)
    if validar==1:
        return render_template('empleados/register.html', con=con)

    if validar==0:
        sql="INSERT INTO `usuario` (`nombre`, `Correo`, `Numero`, `Nacimiento`, `Contraseña`,`tipo`) VALUES (%s, %s, %s, %s, %s,%s);"
        sql2="SELECT * FROM `usuario`;"
        __TIPO=['0']
        datos=(_nombre,_Correo,_celular,_date,_contraseña,__TIPO)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql2)       
        cursor.execute(sql,datos)  
        conn.commit()
        empleados=cursor.fetchall()
        return render_template('empleados/login.html')




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
    conn.commit()
 
    
    if usuario:
        ver=(usuario[0][5])
        if ver==_contraseña:
            sql="SELECT * FROM `aparato`;" 
            cursor.execute(sql)  
            empleados=cursor.fetchall()
            conn.commit()
            Valida="0"
            session["name"] = usuario[0][6]
            session["ID"] = usuario[0][0]
            flash('You were successfully logged in')
            return render_template('empleados/Principal.html',valida=Valida, aparato=empleados)
        else:
            Valida="1"
            return render_template('empleados/login.html',valida=Valida)
    else:
        Valida="1"
        return render_template('empleados/login.html',valida=Valida)
        

@app.route("/home")
def home():
    sql="SELECT * FROM `aparato`;" 
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)  
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/Principal.html', aparato=empleados)



@app.route("/Gestion_dispositivos")
def gestionar():
    sql="SELECT * FROM `aparato` WHERE `ADMIN_ID` = %s;" 
    empleados=""
    _ID=session["ID"]
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,_ID)  
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/Gestionar_Aparatos.html', dispositivos=empleados)



@app.route('/Borrar/<int:id><string:Tabla>')
def borrar(Tabla,id):
    sql="DELETE FROM "+Tabla+" WHERE id=%s;"   
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,id)  
    conn.commit()
    if Tabla == "aparato":
        return redirect("/Gestion_dispositivos")

    if Tabla == "usuario":
        return redirect("/Gestion_dispositivos")


    


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

@app.route('/Crear_Aparato')
def Registro_Aparato():

    return render_template('empleados/Crear_Aparato.html')



@app.route('/Actualizar_AP/img/crud/filtrar.png')
def imagen():

    return send_file('templates/empleados/img/filtrar.png')


@app.route('/Actualizar_AP/img/carousel1.jpg')
def ind():

    return send_file('templates\empleados\img\carousel1.jpg')


@app.route('/Actualizar_AP/css/style.css')
def indes():

    return send_file('templates\empleados\css\style.css')

@app.route('/Actualizar_AP/lib/tempusdominus/js/moment.min.js')
def indesa():

    return send_file('templates\empleados\css\style.min.css')

@app.route('/Actualizar_AP/lib/tempusdominus/css/tempusdominus-bootstrap-4.min.css')
def a():

    return send_file('templates\empleados\lib\tempusdominus\css\tempusdominus-bootstrap-4.min.css')

@app.route('/Actualizar_AP/js/main.js')
def aa():

    return send_file('templates\empleados\js\main.js')


@app.route('/img/carousel2.jpg')
def aaa():

    return send_file('templates\empleados\img\carousel2.jpg')


@app.route('/img/carousel-1.jpg')
def aaaa():

    return send_file('templates\empleados\img\carousel2.jpg')


@app.route('/img')
def aae():

    return send_file('templates\empleados\img\perro.jpg')





















@app.route('/img/crud/Apple-movil-png.png')
def imagen1():

    return send_file('templates/empleados/img/Apple-movil-png.png')

@app.route('/img/crud/filtrar.png')
def imagen2():

    return send_file('templates/empleados/img/filtrar.png')


@app.route('/img/carousel1.jpg')
def ind1():

    return send_file('templates\empleados\img\carousel1.jpg')


@app.route('/css/style.css')
def indes1():

    return send_file('templates\empleados\css\style.css')

@app.route('/lib/tempusdominus/js/moment.min.js')
def indesa1():

    return send_file('templates\empleados\css\style.min.css')

@app.route('/lib/tempusdominus/css/tempusdominus-bootstrap-4.min.css')
def a1():

    return send_file('templates\empleados\lib\tempusdominus\css\tempusdominus-bootstrap-4.min.css')

@app.route('/js/main.js')
def aa1():

    return send_file('templates\empleados\js\main.js')


if __name__=='__main__':

    app.run(debug=True)