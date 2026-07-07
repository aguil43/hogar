var intentos = 0;
var id = undefined;

function encriptar(contraseña){
    const hash = CryptoJS.SHA256(contraseña);
    return hash.toString();
}

function log(){//funcion a la que se llama desde html cuando se hace click en el boton Ingresar
    let nombre = document.querySelector("#nombre").value //variable que guarda el valor introducido en el nombre de ususario
    let contraseña = document.querySelector("#contraseña").value //variable que guarda el valor introducido en la contraseña
    const encriptada = encriptar(contraseña)
    makeRoute = `/${nombre}/${encriptada}`
    setTimeout(() => {
        window.open(makeRoute, "_self")
    }, 1000)
    //usuarios_db(nombre, contraseña); //se llama a la funcion que obtiene la información de la base de datos
}

/*function comprobar_usuario(datos, inputUser, inputPass){ //esta funcion se encarga de combrobar el usuario y contraseña

}*/

function usuarios_db(nombre, contraseña){ //solicita la información a la base de datos para despues utilizarla
    //var info = 0 // variable para posteriormente guardar la informacion de la base de datos
    
    fetch('static/json/user.json')
    .then(respuesta => respuesta.json())
    .then(data => {
        data.forEach(date => {
            comprobar_usuario(date, nombre, contraseña)
        });
    })
}

function log_out(){ //funcion de cierre de sesion
    window.open('/', "_self"); //se redirecciona al usuario a la pantalla de inicio para dar fin a la sesion
    document.cookie = "id=0;expires=1 Mar 1990 00:00:00 GMT"
    document.cookie = "log=none;"
}

function create_user(){
    let valorOfCookie = cookies("log");
    if(valorOfCookie == "True"){
        var new_username = document.querySelector('.new_username').value
        var new_password = document.querySelector('.new_password').value
        let route = `/users/createuser/${new_username}/${new_password}`
        window.open(route, "_self");
    }else{
        alert("Inicie sesion");
        log_out()
    }
}

// ? Como agregar cookies para almacenar el ID y el estdo de log del usuario

function modify_username(){
    let valorOfCookie = cookies("log");
    if(valorOfCookie == "True"){
        var change_user = document.querySelector('#username').value
        valorOfCookie = cookies("id")
        let route = `/users/modify/username/${change_user}/${valorOfCookie}`
        window.open(route, "_self");
    }else{
        alert("Primero inicie sesion");
        log_out()
    }
}

function modify_password(){
    let valorOfCookie = cookies("log")
    if(valorOfCookie == "True"){
        valorOfCookie = cookies("id")
        let old_password = info[valorOfCookie - 1].password
        var input_old_password = document.querySelector('#old_password').value
        var change_password = document.querySelector('#new_password').value
        if(old_password === input_old_password){
            let route = `/users/modify/password/${change_password}/${valorOfCookie}`
            window.open(route, "_self")
        }
    }else{
        alert("Primero inicie sesion")
        log_out()
    }
}

function cookies(nombre){
    var lista = document.cookie.split(";");
    for (i in lista) {
        var busca = lista[i].search(nombre);
        if (busca > -1){
            var micookie=lista[i]
        }
    }
    var igual = micookie.indexOf("=");
    let valorOfCookie = micookie.substring(igual+1);
    return valorOfCookie
}

var info = 0 // variable para posteriormente guardar la informacion de la base de datos
    fetch('static/json/user.json')
    .then(respuesta => respuesta.json())
    .then(data => {
        data.forEach(date => {
            info = data
        });
    })