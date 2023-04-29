from flask import Flask
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from flaskext.mysql import MySQL
from flask import send_from_directory
from flask import send_file
from flask import flash


app=Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_PORT']=3306
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='usuario'
mysql.init_app(app)

@app.route('/')
def index():
    session["name"] = ""
    session["ID"] = ""
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

 if session['name'] == 2:
    sql2="SELECT * FROM `usuario`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql2)
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/Usuarios.html',empleados=empleados)
 else:
     return render_template('empleados/index.html')







@app.route('/login.html')
def login():
    Valida="0"
    return render_template('empleados/login.html',valida=Valida)






@app.route('/store_Aparato', methods=['POST'])
def store_Aparato():

    if session['name'] == 2 or session['name'] == 1:
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
    else:
        return render_template('empleados/index.html')








@app.route('/Actualizar_AP/<int:id>')
def Actualizar_AP(id):

    if session['name'] == 2 or session['name'] == 1:
        sql="SELECT * FROM `aparato` WHERE ID= %s;" 
        conn=mysql.connect()
        cursor=conn.cursor() 
        cursor.execute(sql,(id))  
        empleados=cursor.fetchall()
        print(empleados)
        conn.commit()
        return render_template('empleados/Actualizar_Aparato.html', aparato=empleados)
    else:
        return render_template('empleados/index.html')
    









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
        return render_template('empleados/login.html')



@app.route('/Guardar_ADM', methods=['POST'])
def Guardar():
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
    _TIPO=request.form['Tipo']

    
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
        datos=(_nombre,_Correo,_celular,_date,_contraseña,_TIPO)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql2)       
        cursor.execute(sql,datos)  
        conn.commit()
        empleados=cursor.fetchall()
        return redirect('/Crear.html')




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

    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:
        sql="SELECT * FROM `aparato`;" 
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)  
        empleados=cursor.fetchall()
        conn.commit()
        return render_template('empleados/Principal.html', aparato=empleados)
    else:
        return render_template('empleados/index.html')



@app.route("/Gestion_dispositivos")
def gestionar():
    if session['name'] == 2 or session['name'] == 1:
        sql="SELECT * FROM `aparato` WHERE `ADMIN_ID` = %s;" 
        empleados=""
        _ID=session["ID"]
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,_ID)  
        empleados=cursor.fetchall()
        conn.commit()
        return render_template('empleados/Gestionar_Aparatos.html', dispositivos=empleados)
    else:
        return render_template('empleados/index.html')



@app.route('/Borrar/<int:id><string:Tabla>')
def borrar(Tabla,id):
    if session['name'] == 2 or session['name'] == 1:
        sql="DELETE FROM "+Tabla+" WHERE id=%s;"   
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,id)  
        conn.commit()
        if Tabla == "aparato":
            return redirect("/Gestion_dispositivos")

        if Tabla == "usuario":
            return redirect("/Crear.html")
    else:
        return render_template('empleados/index.html')



    


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

@app.route('/RegistroUser')
def Registro_ADM():
    con=""
    validarN="0"
    validarCOR="0"
    validarCel="0"
    validarContra="0"
    validarReContra="1"
    validarD="0"
    con=(validarN,validarCOR,validarCel,validarContra,validarD)
    return render_template('empleados/Resgistro_ADM.html', con=con)

@app.route("/Gestion_dispositivos")
def Gestion():
    if session['name'] == 2 or session['name'] == 1:
        sql="SELECT * FROM `aparato` WHERE `ADMIN_ID` = %s;" 
        empleados=""
        _ID=session["ID"]
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,_ID)  
        empleados=cursor.fetchall()
        conn.commit()
        return render_template('empleados/Gestionar_Aparatos.html', dispositivos=empleados)
    else:
        return render_template('empleados/index.html')


@app.route("/Editar_Usuario/<int:id>")
def EditarU(id):
    if session['name'] == 2 :
        sql="SELECT * FROM `usuario` WHERE `ID` = %s;" 
        con=""
        validarN="0"
        validarCOR="0"
        validarCel="0"
        validarContra="0"
        validarReContra="1"
        validarD="0"
        con=(validarN,validarCOR,validarCel,validarContra,validarD)
        empleados=""
        _ID=id
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,_ID)  
        empleados=cursor.fetchall()
        conn.commit()
        return render_template('empleados/Editar_User.html', Usuario=empleados, con=con)
    else:
        return render_template('empleados/index.html')





@app.route('/Actualizar_U/<int:id>', methods=['POST'])
def ACTUU(id):

    sql2="SELECT * FROM `usuario`;"

    validar=0

    
    con=""
    validarN=0
    validarCOR=0
    validarCel=0
    validarContra=0
    validarReContra=1
    validarD=0

    _ID=id
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
        sql="UPDATE `usuario` SET `nombre` = %s, `Correo` = %s, `Numero` = %s, `Nacimiento` = %s, `Contraseña` = %s, `Tipo` = %s WHERE `usuario`.`ID` = %s"
        sql2="SELECT * FROM `usuario`;"
        __TIPO=request.form['Tipo']
        datos=(_nombre,_Correo,_celular,_date,_contraseña,__TIPO,_ID)
        conn=mysql.connect()
        cursor=conn.cursor()       
        cursor.execute(sql,datos)  
        conn.commit()
        return redirect('/Crear.html')
    
@app.route("/perfil")
def perfil():

    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:
        sql="SELECT * FROM `usuario` WHERE `ID` = %s;" 
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,session['ID'])  
        empleados=cursor.fetchall()
        conn.commit()
        return render_template('empleados/Perfil.html', Usuario=empleados)
    else:
        return render_template('empleados/index.html')
    


@app.route('/Editar_perfil')
def Editar_Perfil():
    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:
        sql="SELECT * FROM `usuario` WHERE `ID` = %s;" 
        con=""
        validarN="0"
        validarCOR="0"
        validarCel="0"
        validarContra="0"
        validarReContra="1"
        validarD="0"
        con=(validarN,validarCOR,validarCel,validarContra,validarD)
        empleados=""
        _ID=session['ID']
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,_ID)  
        empleados=cursor.fetchall()
        conn.commit()
        return render_template('empleados/Editar_perfil.html', Usuario=empleados, con=con)
    else:
        return render_template('empleados/index.html')



@app.route('/Actualizar_P/<int:id>', methods=['POST'])
def Actualizar_Perfi(id):

    sql2="SELECT * FROM `usuario` WHERE `ID` = %s;" 
    conn=mysql.connect()
    cursor=conn.cursor()       
    cursor.execute(sql2,id)  
    User=cursor.fetchall()
    conn.commit()
    validar=0

    
    con=""
    validarN=0
    validarCOR=0
    validarCel=0
    validarContra=0
    validarReContra=1
    validarD=0

    _ID=id
    _nombre=request.form['Nombre']
    _Correo=request.form['Correo']
    _celular=request.form['celular']
    _date=request.form['date']
    _contraseña=request.form['contraseña']
    _contraseña2 = User[0][5]

    
    

    if _contraseña != _contraseña2:
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
        return redirect('/Editar_perfil')

    if validar==0:
        sql="UPDATE `usuario` SET `nombre` = %s, `Correo` = %s, `Numero` = %s, `Nacimiento` = %s WHERE `usuario`.`ID` = %s"
        datos=(_nombre,_Correo,_celular,_date,_ID)
        conn=mysql.connect()
        cursor=conn.cursor()       
        cursor.execute(sql,datos)  
        conn.commit()
        return redirect('/perfil')


























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





















@app.route('/Editar_Usuario/img/crud/filtrar.png')
def q():

    return send_file('templates/empleados/img/filtrar.png')


@app.route('/Editar_Usuario/img/carousel1.jpg')
def qq():

    return send_file('templates\empleados\img\carousel1.jpg')


@app.route('/Editar_Usuario/css/style.css')
def qqq():

    return send_file('templates\empleados\css\style.css')

@app.route('/Editar_Usuario/lib/tempusdominus/js/moment.min.js')
def qqqq():

    return send_file('templates\empleados\css\style.min.css')

@app.route('/Editar_Usuario/lib/tempusdominus/css/tempusdominus-bootstrap-4.min.css')
def qqqqq():

    return send_file('templates\empleados\lib\tempusdominus\css\tempusdominus-bootstrap-4.min.css')

@app.route('/Editar_Usuario/js/main.js')
def qqqqqw():

    return send_file('templates\empleados\js\main.js')



if __name__=='__main__':

    app.run(debug=True)