function alerta()
    {
    var mensaje;
    var opcion = confirm("Clicka en Aceptar o Cancelar");
    if (opcion == true) {
        mensaje = "Has clickado OK";
	} else {
	    mensaje = "Has clickado Cancelar";
	}
	document.getElementById("ejemplo").innerHTML = mensaje;
}

function Eliminar()
{
    ID=document.getElementById("ID").value;
    var opcion = confirm("¿Seguro que desea dar de baja?");
    if (opcion == true) {
        window.location = "/Borrar/"+ID+"1usuario";
	} 

    document.getElementById("ejemplo").innerHTML = ID;
};

function valoracion1()
{
    
valoracion=document.getElementById("VAL1").value;


var opcion = confirm("Recuerde que si usted ya ah echo una valoracion, esta se remplazara, ¿Desea dar esta valoracion?");
    if (opcion == true) {
        window.location = ("/valoracion/"+valoracion+":1")
	} 
}

function valoracion2()
{
    
valoracion=document.getElementById("VAL2").value;


var opcion = confirm("Recuerde que si usted ya ah echo una valoracion, esta se remplazara, ¿Desea dar esta valoracion?");
    if (opcion == true) {
        window.location = ("/valoracion/"+valoracion+":2")
	} 
}

function contra(){
contraNEW = document.getElementById("contraseñaNEW").value
contraNEW2 = document.getElementById("contraseñaNEW2").value

    if(contraNEW != contraNEW2){
     alert("Las dos contraseñas no coinciden")

    }else
    {
        window.location = ("/ActuContra")
    }
    

}