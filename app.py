
from flask import Flask
from flask import Flask, render_template, redirect, request, session, session, abort, send_from_directory, send_file, flash
from flask_session import Session
from flaskext.mysql import MySQL
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import os
import pathlib
import requests

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


app=Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_PORT']=3306
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='1234'
app.config['MYSQL_DATABASE_DB']='usuario'
mysql.init_app(app)

app.secret_key = "CodeSpecialist.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "60579329655-odmej9ieav8j30foq983o0hg7osav7mj.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login2")
def login2():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.Session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID, 
        clock_skew_in_seconds=10
    )

    session["google_id"] = id_info.get("sub")
    session["namen"] = id_info.get("name")
    session["email"] = id_info['email']
    session["phone_number"] = id_info.get('phone_number')
    session["birthdate"] = id_info.get('birthdate')


    con=""
    validarN="0"
    validarCOR="0"
    validarCel="0"
    validarContra="0"

    validarD="0"
    con=(validarN,validarCOR,validarCel,validarContra,validarD)
    return render_template('empleados/register_GMAIL.html', con=con)










@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['namen']}!  {session['email']}  {session['phone_number']}  {session['birthdate']}<br/> <a href='/logout'><button>Logout</button></a>"





@app.route('/gmailre', methods=['POST'])
def gmailre():
    sql="INSERT INTO `usuario` (`nombre`, `Correo`, `Numero`, `Nacimiento`, `Contraseña`) VALUES (%s, %s, %s, %s, %s);"
    sql2="SELECT * FROM `usuario`;"
    sql3="SELECT CORREO FROM `usuario` WHERE CORREO = %s;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql3,session["email"]) 
    Correo=cursor.fetchall()       
    conn.commit()
    
 
    validar=0

    
    con=""
    validarN=0
    validarCOR=0
    validarCel=0
    validarContra=0
    validarReContra=1
    validarD=0

    _nombre=session["namen"]
    _Correo=session["email"]
    _celular="00000000"
    _date="2023-05-05"
    _contraseña=request.form['contraseña']
    _REcontraseña=request.form['contraseñaRepeat']

    
    if _contraseña==_REcontraseña:
        validarReContra=0

    if len(_contraseña)<=5:
        validar=1
        validarContra=1
    if Correo:
        if session["email"]==Correo[0][0]:
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
        return render_template('empleados/login.html')

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












    








@app.route('/')
def index():
    
    session["name"] = ""
    session["ID"] = ""
    sql="SELECT * FROM `usuario`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()

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
        sql="INSERT INTO `aparato` (`Procesador`, `Software`, `Conectividad`, `Bateria`, `Precio Max`, `Precio Min`,`Resolucion pantalla`, `Mejor Uso`, `Resumen`, `ADMIN_ID`) VALUES (%s,%s,%s,%s, %s, %s, %s, %s,%s,%s);"
        _Procesador=request.form['Procesador']
        _Software=request.form['Software']
        _Conectividad=request.form['Conectividad']
        _Bateria=request.form['Bateria']
        _PrecioMIN=request.form['Precio Min']
        _PrecioMAX=request.form['Precio Max']
        _Resolucion=request.form['Resolucion']
        _Uso=request.form['Uso normal']
        _Resumen=request.form['Resumen']
        _Admin= session["ID"]
        _user=session["name"]

        datos=(_Procesador,_Software,_Conectividad,_Bateria,_PrecioMIN, _PrecioMAX,_Resolucion,_Uso,_Resumen,_Admin)
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

        conn.commit()
        return render_template('empleados/Actualizar_Aparato.html', aparato=empleados)
    else:
        return render_template('empleados/index.html')
    









@app.route('/Actualizar_Aparato/<int:id>', methods=['POST'])
def Actualizar_Aparato(id):


    sql="UPDATE `aparato` SET `Procesador` = %s, `Software` = %s, `Conectividad` = %s, `Bateria` = %s, `Precio Min` = %s, `Precio Max` = %s, `Resolucion pantalla` = %s, `Mejor Uso` = %s, `Resumen` = %s WHERE `aparato`.`ID` = %s;"
    
    _Procesador=request.form['Procesador']
    _Software=request.form['Software']
    _Conectividad=request.form['Conectividad']
    _Bateria=request.form['Bateria']
    _PrecioMin=request.form['Precio Min']
    _PrecioMax=request.form['Precio Max']
    _Resolucion=request.form['Resolucion']
    _Uso=request.form['Uso normal']
    _Resumen=request.form['Resumen']
    _ID=id


    datos=(_Procesador,_Software,_Conectividad,_Bateria,_PrecioMin,_PrecioMax,_Resolucion,_Uso,_Resumen,_ID)
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
            sql="SELECT aparato.*, ROUND(AVG(valoracion.Valoracion),1) FROM aparato LEFT JOIN `valoracion` ON `aparato`.`ID` = Valoracion.UD_aprato GROUP BY `aparato`.`ID`;"
            cursor.execute(sql)  
            empleados=cursor.fetchall()
            conn.commit()
            Valida="0"
            session["name"] = usuario[0][6]
            session["ID"] = usuario[0][0]
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
        sql="SELECT aparato.*, ROUND(AVG(valoracion.Valoracion),1) FROM aparato LEFT JOIN `valoracion` ON `aparato`.`ID` = Valoracion.UD_aprato GROUP BY `aparato`.`ID`;"


        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)  
        empleados=cursor.fetchall()
        conn.commit()

        Bateria="SELECT Bateria FROM `aparato` GROUP BY 1;"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(Bateria)  
        Ba=cursor.fetchall()
        conn.commit()



        Bateria="SELECT `Mejor uso` FROM `aparato` GROUP BY 1;"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(Bateria)  
        Uso=cursor.fetchall()
        conn.commit()



        Bateria="SELECT `Resolucion pantalla` FROM `aparato` GROUP BY 1;"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(Bateria)  
        Tama=cursor.fetchall()
        conn.commit()



        Bateria="SELECT Conectividad FROM `aparato` GROUP BY 1;"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(Bateria)  
        Conec=cursor.fetchall()
        conn.commit()





        return render_template('empleados/Principal.html', aparato=empleados,Bateria=Ba,Tamaño=Tama,Conectividad=Conec,Uso=Uso)
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



@app.route('/Borrar/<int:id>')
def borrar(id):
    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:

        print(id)

        sql="DELETE FROM `usuario` WHERE id=%s;"    
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,id)  
        conn.commit()

        return redirect("/")
    else:
        return redirect("/")
    
@app.route('/BorrarDP/<int:id>')
def borrarDP(id):
    if session['name'] == 2 or session['name'] == 1:

        print(id)

        sql="DELETE FROM `aparato` WHERE id=%s;"    
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,id)  
        conn.commit()

        return redirect("/Gestion_dispositivos")
    else:
        return redirect("/")



    


@app.route('/register.html')
def Registro():
    con=""
    validarN="0"
    validarCOR="0"
    validarCel="0"
    validarContra="0"

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
    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:
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
    else:
        return redirect('/')

@app.route('/Crear_Aparato')
def Crear_apa():
    if session['name'] == 2 or session['name'] == 1:
        return render_template('empleados/Crear_Aparato.html');
    else:
        return redirect('/')


@app.route('/comparar/<int:id>')
def Compa(id):
    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:
        sql="SELECT aparato.*, ROUND(AVG(valoracion.Valoracion),1) FROM aparato LEFT JOIN `valoracion` ON `aparato`.`ID` = Valoracion.UD_aprato GROUP BY `aparato`.`ID`;"
        sql2="SELECT * FROM `aparato` WHERE `ID` = %s;"  
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)  
        aparato=cursor.fetchall()
        cursor.execute(sql2,id)  
        seleccion=cursor.fetchall()
        conn.commit()
        return render_template('empleados/Principal copy.html', aparato=aparato,selecion=seleccion)
    else:
        return redirect('/')


@app.route('/comparar2/<int:id>:<int:id2>')
def Compa2(id,id2):
    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:
        sql="SELECT aparato.*, ROUND(AVG(valoracion.Valoracion),1) FROM aparato LEFT JOIN `valoracion` ON `aparato`.`ID` = Valoracion.UD_aprato WHERE APARATO.ID = %s GROUP BY `aparato`.`ID`;"
        sql2="SELECT aparato.*, ROUND(AVG(valoracion.Valoracion),1) FROM aparato LEFT JOIN `valoracion` ON `aparato`.`ID` = Valoracion.UD_aprato WHERE APARATO.ID = %s GROUP BY `aparato`.`ID`;"  
        conn=mysql.connect()

        session['APA1']=id
        session['APA2']=id2
        cursor=conn.cursor()
        cursor.execute(sql,id)  
        aparato=cursor.fetchall()


        cursor.execute(sql2,id2)  
        seleccion=cursor.fetchall()
        conn.commit()

        return render_template('empleados/Comparador_2.html', aparato=aparato,selecion=seleccion)
    else:
        return redirect('/')

@app.route('/Buscar', methods=['POST'])
def Buscar():

    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:

        sql="SELECT * FROM `aparato` WHERE procesador LIKE %s;"

        Buscar=request.form['Busca']
        Buscar="%"+Buscar+'%'
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,Buscar)  
        aparato=cursor.fetchall()
        conn.commit()

        return render_template('empleados/Principal.html', aparato=aparato)
    else:
        return redirect('/')

@app.route('/valoracion/<int:Val>:<int:op>')
def val(Val,op):
    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:
        DF= session['ID']
        AP1 = session['APA1']
        AP2 = session['APA2']

        if op == 1 :
            sql="SELECT * FROM `valoracion` WHERE ID_user = %s and UD_aprato= %s"
            vala=(DF,AP1)
        if op == 2 :
            sql="SELECT * FROM `valoracion` WHERE ID_user = %s and UD_aprato= %s"
            vala=(DF,AP2)

        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,vala)  
        existe=cursor.fetchall()
        conn.commit()
        comit=(DF,AP1,Val)
        comit2=(DF,AP2,Val)

        if op == 1 and not existe:
            sql="INSERT INTO `valoracion` (`ID_user`, `UD_aprato`, `Valoracion`) VALUES (%s, %s, %s)"
            conn=mysql.connect()
            cursor=conn.cursor()
            cursor.execute(sql,comit)  
            conn.commit()
        else:
            if op==1:
                sql="UPDATE `valoracion` SET   `Valoracion` = '%s' WHERE `valoracion`.`ID_user` = %s and UD_aprato= %s"
                Com=(Val,DF,AP1)
                conn=mysql.connect()
                cursor=conn.cursor()
                cursor.execute(sql,Com)  
                conn.commit()
            

        if op == 2 and not existe:
            sql="INSERT INTO `valoracion` (`ID_user`, `UD_aprato`, `Valoracion`) VALUES (%s, %s, %s)"

            conn=mysql.connect()
            cursor=conn.cursor()
            cursor.execute(sql,comit2)  
            conn.commit()
        else:
            if op==2:
                sql="UPDATE `valoracion` SET   `Valoracion` = '%s' WHERE `valoracion`.`ID_user` = %s and UD_aprato= %s"
                Com=(Val,DF,AP2)
                conn=mysql.connect()
                cursor=conn.cursor()
                cursor.execute(sql,Com)  
                conn.commit()
        
        return redirect('/comparar2/'+str(AP1)+':'+str(AP2))
    else:
        return redirect('/')

@app.route('/Editar_contra')
def Editar_contra():
    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:
        return render_template('empleados/Editar_Contraseña.html', valida=0)
    return redirect('/')



@app.route('/ActuContra',methods=['POST'])
def actualizaContra():
    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:
        sql="SELECT usuario.CONTRASEÑA FROM `usuario` WHERE ID = %s"
        id=session['ID']
        contraOLD=request.form['contraseñaOLD']
        contraNEW=request.form['contraseñaNEW']
        contraNEW2=request.form['contraseñaNEW2']

        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,id)  
        contra=cursor.fetchall()
        conn.commit()
        print(contra)
        print(contraOLD)
        print(contraNEW)
        print(contraNEW2)

        if contraNEW==contraNEW2 and contraOLD==contra[0][0]:
            sql="UPDATE `usuario` SET `CONTRASEÑA` = %s WHERE `usuario`.`ID` = %s"
            com=(contraNEW,id)
            conn=mysql.connect()
            cursor=conn.cursor()
            cursor.execute(sql,com)  
            conn.commit()
            return redirect('/perfil')
        else:
            return render_template('empleados/Editar_Contraseña.html', valida=1)  
    return redirect('/')



@app.route('/Buscar2/<int:id>', methods=['POST'])
def Buscar2(id):

    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:

        sql="SELECT aparato.*, ROUND(AVG(valoracion.Valoracion),1) FROM aparato LEFT JOIN `valoracion` ON `aparato`.`ID` = Valoracion.UD_aprato WHERE aparato.procesador LIKE %s GROUP BY `aparato`.`ID`;"
        sql2="SELECT * FROM `aparato` WHERE `ID` = %s;" 

        Buscar=request.form['Busca']
        Buscar="%"+Buscar+'%'
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,Buscar)  
        aparato=cursor.fetchall()
        conn.commit()


        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql2,id)  
        seleccion=cursor.fetchall()
        conn.commit()

        return render_template('empleados/Principal copy.html', aparato=aparato, selecion=seleccion)
    else:
        return redirect('/')




@app.route("/Fav")
def Favoritos():

    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:
        sql="SELECT aparato.*, ROUND(AVG(valoracion.Valoracion),1) FROM aparato JOIN `valoracion` ON `aparato`.`ID` = `Valoracion`.`UD_aprato` JOIN favoritos ON `aparato`.`ID` = `favoritos`.`APARATO_ID` WHERE `favoritos`.`USER_ID` = %s GROUP BY `aparato`.`ID`;"
        UID = session['ID']
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,UID)  
        empleados=cursor.fetchall()
        conn.commit()
        return render_template('empleados/Favoritos.html', aparato=empleados)
    else:
        return render_template('empleados/index.html')
    

@app.route('/Metodo', methods=['POST'])
def method():
    sql="SELECT aparato.*, ROUND(AVG(valoracion.Valoracion),1) FROM aparato JOIN `valoracion` ON `aparato`.`ID` = Valoracion.UD_aprato JOIN favoritos ON aparato.ID = favoritos.APARATO_ID WHERE favoritos.APARATO_ID = %s AND USER_ID = %s GROUP BY `aparato`.`ID`;"
    UID = session['ID']
    dato = request.json.get('dato')
    datos=(dato,UID)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)  
    empleados=cursor.fetchall()
    conn.commit()
    print(dato)
    print(empleados)

    if not empleados:
        sql2="INSERT INTO `favoritos` (`APARATO_ID`, `USER_ID`) VALUES (%s, %s)"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql2,datos)
        conn.commit()
        return ("Se ah agregado a favoritos!")
    else:
        return ("El dispositivo ya esta en la lista!")
    

@app.route('/FavQ/<int:id>')
def BorrarFav(id):
    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:

        print(id)
        UID = session['ID']
        datos=(id,UID)    
        sql="DELETE FROM favoritos WHERE favoritos.APARATO_ID = %s AND USER_ID = %s"    
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,datos)  
        conn.commit()

        return redirect("/Fav")
    else:
        return redirect('/')



@app.route('/Filtro', methods=['POST'])
def Filtro():
    if session['name'] == 2 or session['name'] == 1 or session['name'] == 0:
        primero="0"
        Bateria=request.form['Bateria']
        Tamaño=request.form['Tamaño']
        Uso=request.form['Uso']
        Conectividad=request.form['Conectividad']
        sql="SELECT aparato.*, ROUND(AVG(valoracion.Valoracion),1) FROM aparato LEFT JOIN `valoracion` ON `aparato`.`ID` = Valoracion.UD_aprato "
       
        if Bateria != "null" and primero == "0":
            sql=sql+" WHERE Bateria = \""+Bateria+"\""
            primero="1"
            print(sql)



        if Tamaño != "null" and primero == "0":
            sql=sql+"WHERE `Resolucion pantalla`= \""+Tamaño+"\""
            primero="1"
            print(sql)
            
        elif Tamaño != "null":
            sql=sql+" AND `Resolucion pantalla` = \""+Tamaño+"\""
            print(sql)



        if Uso != "null" and primero == "0":
            sql=sql+"WHERE `Mejor uso`= \""+Uso+"\""
            primero="1"
            print(sql)
            
        elif Uso != "null":
            sql=sql+" AND `Mejor uso` = \""+Uso+"\""
            print(sql)



        if Conectividad != "null" and primero == "0":
            sql=sql+"WHERE `Conectividad`= \""+Conectividad+"\""
            primero="1"
            print(sql)
            
        elif Conectividad != "null":
            sql=sql+" AND `Conectividad` = \""+Conectividad+"\""
            print(sql)


        sql=sql+" GROUP BY `aparato`.`ID`;"
        print("SINTAXIS DEL FILTRO")
        print(sql)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)  
        Filtro=cursor.fetchall()
        conn.commit()


        sql="SELECT aparato.*, ROUND(AVG(valoracion.Valoracion),1) FROM aparato LEFT JOIN `valoracion` ON `aparato`.`ID` = Valoracion.UD_aprato GROUP BY `aparato`.`ID`;"


        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)  
        empleados=cursor.fetchall()
        conn.commit()

        Bateria="SELECT Bateria FROM `aparato` GROUP BY 1;"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(Bateria)  
        Ba=cursor.fetchall()
        conn.commit()



        Bateria="SELECT `Mejor uso` FROM `aparato` GROUP BY 1;"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(Bateria)  
        Uso=cursor.fetchall()
        conn.commit()



        Bateria="SELECT `Resolucion pantalla` FROM `aparato` GROUP BY 1;"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(Bateria)  
        Tama=cursor.fetchall()
        conn.commit()



        Bateria="SELECT Conectividad FROM `aparato` GROUP BY 1;"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(Bateria)  
        Conec=cursor.fetchall()
        conn.commit()


        return render_template('empleados/Principal.html', aparato=Filtro,Bateria=Ba,Tamaño=Tama,Conectividad=Conec,Uso=Uso)
    else:
        return redirect('/')













@app.route('/scrips')
def jsScrips():
    return send_file('templates\empleados\js\Alerta.js')
@app.route('/comparar2/scrips')
def jsScr():
    return send_file('templates\empleados\js\Alerta.js')




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




@app.route('/comparar/img/crud/filtrar.png')
def y():

    return send_file('templates/empleados/img/filtrar.png')


@app.route('/comparar/img/carousel1.jpg')
def yy():

    return send_file('templates\empleados\img\carousel1.jpg')


@app.route('/comparar/css/style.css')
def yyy():

    return send_file('templates\empleados\css\style.css')

@app.route('/comparar/lib/tempusdominus/js/moment.min.js')
def yyyy():

    return send_file('templates\empleados\css\style.min.css')

@app.route('/compararP/lib/tempusdominus/css/tempusdominus-bootstrap-4.min.css')
def yyyj():

    return send_file('templates\empleados\lib\tempusdominus\css\tempusdominus-bootstrap-4.min.css')

@app.route('/comparar/js/main.js')
def yj():
    return send_file('templates\empleados\js\main.js')

@app.route('/comparar/img/crud/Apple-movil-png.png')
def imagen12():

    return send_file('templates/empleados/img/Apple-movil-png.png')





@app.route('/comparar2/img/crud/filtrar.png')
def z():

    return send_file('templates/empleados/img/filtrar.png')


@app.route('/comparar2/img/carousel1.jpg')
def zz():

    return send_file('templates\empleados\img\carousel1.jpg')


@app.route('/comparar2/css/style.css')
def zzz():

    return send_file('templates\empleados\css\style.css')

@app.route('/comparar2/lib/tempusdominus/js/moment.min.js')
def zzzz():

    return send_file('templates\empleados\css\style.min.css')

@app.route('/comparar2/lib/tempusdominus/css/tempusdominus-bootstrap-4.min.css')
def zzx():

    return send_file('templates\empleados\lib\tempusdominus\css\tempusdominus-bootstrap-4.min.css')

@app.route('/comparar2/js/main.js')
def zx():
    return send_file('templates\empleados\js\main.js')

@app.route('/comparar2/img/crud/Apple-movil-png.png')
def imagen12a():

    return send_file('templates/empleados/img/Apple-movil-png.png')










@app.route('/Buscar2/img/crud/filtrar.png')
def d():

    return send_file('templates/empleados/img/filtrar.png')


@app.route('/Buscar2/img/carousel1.jpg')
def dd():

    return send_file('templates\empleados\img\carousel1.jpg')


@app.route('/Buscar2/css/style.css')
def ddd():

    return send_file('templates\empleados\css\style.css')

@app.route('/Buscar2/lib/tempusdominus/js/moment.min.js')
def dddd():

    return send_file('templates\empleados\css\style.min.css')

@app.route('/Buscar2/lib/tempusdominus/css/tempusdominus-bootstrap-4.min.css')
def da():

    return send_file('templates\empleados\lib\tempusdominus\css\tempusdominus-bootstrap-4.min.css')

@app.route('/Buscar2/js/main.js')
def daa():
    return send_file('templates\empleados\js\main.js')

@app.route('/Buscar2/img/crud/Apple-movil-png.png')
def egg():

    return send_file('templates/empleados/img/Apple-movil-png.png')


@app.route('/Fave')
def img():
    return send_file('templates/empleados/img/Estrella_amarilla.png')









if __name__=='__main__':

    app.run(debug=True)


