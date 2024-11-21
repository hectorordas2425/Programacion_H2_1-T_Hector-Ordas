import app
def menu():
    inicio_sesion = False
    id_usuario = 0
    while True: 
        app.menu_app()
        opcion = int(input("Introduzca la opcion que desee utilizar: "))
        match opcion:
            case 1:
                app.registro()
            case 2:
                inicio_sesion, id_usuario = app.iniciar_sesion()
            case 3:
                print(inicio_sesion)
                print(id_usuario)
                app.comprar(inicio_sesion, id_usuario)
            case 4:
                app.seguir_pedidio()
            case 5:
                break