import db# Importamos la base de datos.
#Creamos el menu que le aparecera al cliente cuando quiera entrar en la tienda.

def menu_app():
    print("1.Registrar cliente")
    print("2.Iniciar sesión")
    print("3.Comprar")
    print("4.Seguir pedido")
    print("5.Salir")  
# Creamos la funcion registro para que el cliente tenga la opcion registrarse para poder entrar en la tienda. 
def registro():
    try:
        conexion = db.conectar_db()#Establecemos conexion con la base de datos
        cursor = conexion.cursor()
# Son los pasos que debe de seguir el cliente para registrarse
        nombre=str(input("Ingresar nombre: "))
        apellidos=str(input("Ingresar apellidos: "))
        dni=str(input("Ingresar DNI: "))

        
        cursor.execute("select * from CLIENTE where dni = %s", (dni,))#Si el DNI ya esta registrado te dara error.
        if cursor.fetchone():
            print("Error, este usuario ya esta registrado")
        else:
            cursor.execute("insert into cliente (nombre, apellidos, dni) values (%s, %s, %s)", (nombre , apellidos, dni))
            conexion.commit()
            print("Usuario con id: ", cursor.lastrowid, "creado")#Nos aparecera un mensaje que nos afirme que se ha creado correctamente el usuario
            
        conexion.close()#Cerramos conexion con la base de datos
    except ValueError:
        print("Error al crear el usuario.")
#Esta funcion sirve para que una vez el cliente este registrado tenga que inicar sesion con su usuario para asi poder acceder a comprar los productos de la tienda
def iniciar_sesion():
    try:
        conexion = db.conectar_db()#Establecemos conexion con la base de datos
        cursor = conexion.cursor()
        
        inicio_sesion = False
#Estos son los pasos para iniciar sesion        
        dni_usuario=str(input("Ingresar DNI: "))
        cursor.execute("select id_cliente from CLIENTE where dni = %s", (dni_usuario,))
        resultado = cursor.fetchone()
        
        if resultado:  #Si se ha introducido un usuario correcto, se iniciara sesion correctamente y te dejara comprar
            print("Sesión iniciada, entrando en la pagina.")
            inicio_sesion = True
            id_usuario = resultado[0]
        else:#Si te da error tienes que volver a registrarte
            print("Error al iniciar sesión.Usuario no encontrado")
            inicio_sesion = False
            id_usuario = 0
      
        conexion.close()#Cerramos conexion con la base de datos
    except ValueError:
        print("Error al iniciar sesión.")
    
    return inicio_sesion, id_usuario #Si ha iniciado sesión y el id del usuario que lo ha hecho
# Creamos esta funcion para mostrar todos los productos disponibles de la tienda.           
def mostrar_lista_productos():
    try:
        conexion = db.conectar_db()#Establecemos conexion con la base de datos
        cursor = conexion.cursor()
        
        cursor.execute("SELECT * FROM PRODUCTO;")#Mostramos todos los productos de la base de datos
        productos = cursor.fetchall()
        
        if productos:#Nos mostrara los productos de forma ordenada
            print("Lista de productos disponibles: ")
            for id_producto, nombre, precio in productos:
                print(f"ID: {id_producto} | Nombre: {nombre} | Precio: {precio:.2f}")
        else:
            print("No hay productos disponibles en la base de datos.")
              
        conexion.close()#Cerramos conexion con la base de datos
    except ValueError:
        print("Error al iniciar sesión.")  
# Creamos esta funcion para comprar en la tienda
def comprar(inicio_sesion, id_cliente):
    try:
        conexion = db.conectar_db()#Establecemos conexion con la base de datos    
        cursor = conexion.cursor()
        
        if inicio_sesion == True:# Utilizamos el def_mostrar_lista_productos para que le aparezcan los productos y pueda elegir el que quiera.
            print("=====ESTOS SON NUESTROS PRODUCTOS=====")
            mostrar_lista_productos()
            print()           
            quiera_comprar = True
            lista_compra=[]# Creamos la lista para almacenar los productos
            
            while quiera_comprar == True:
                seleccionar_producto= int(input("Ingresar id del producto: "))# Elegira los productos que quiera comprar
                cursor.execute("select id_producto from PRODUCTO where id_producto= %s",(seleccionar_producto, ))
                
                if cursor.fetchone():
                    print("Producto seleccionado.")
                    cantidad= int(input("Ingresar cantidad del producto: "))# Elegira la cantidad de cada producto que eliga.
                    lista_compra.append((seleccionar_producto, cantidad))# Se añadira los productos con su respectiva cantidad a la lista
                    respuesta_usuario= str(input("¿Quieres seguir comprando?, ESCRIBE SI O NO: "))# Si quiere seguir comprando escribira SI si no, escribira NO
                    
                    if respuesta_usuario == "SI": #si quiere seguir comprando
                        quiera_comprar = True
                    else: #no quiere seguir comprando
                        quiera_comprar = False
                        
                        precio_total=0
                        for seleccionar_producto, cantidad in lista_compra:
                            cursor.execute("select precio from PRODUCTO where id_producto = %s",(seleccionar_producto, ))
                            resultado = cursor.fetchone()
                            
                            if resultado:# Calculamos el precio total de la compra
                                precio = resultado[0]
                                precio_total += precio * cantidad
                                
                        print("El precio total es: ", precio_total)

                        for seleccionar_producto, cantidad in lista_compra:
                            cursor.execute("insert into PEDIDO (id_cliente, id_producto) values (%s, %s)", (id_cliente, seleccionar_producto))                             
                        conexion.commit()
                        id_pedido_final= cursor.lastrowid # Mostraremos el id del pedido.
                        print("El id del pedido es: ",id_pedido_final)
                        
                else:
                    print("Este id no existe.")

        else:
            print("Usuario no encontrado, inicia sesion para poder comprar.")

        conexion.close()#Cerramos conexion con la base de datos
    except ValueError:
        print("Error al realizar la compra")
    
# Creamos el def para mostrar el seguimiento del pedido 
def seguir_pedidio():
    try:
        conexion = db.conectar_db()#Establecemos conexion con la base de datos
        cursor = conexion.cursor()
        #Le pedimos al cliente que ingrese el id de su pedido
        id_pedido = int(input("Ingrese el número de su pedido: "))
        #Una vez introducido su id se mostrara todos los datos del cliente y del pedido
        cursor.execute("SELECT p.id_pedido, c.nombre, c.apellidos, c.dni, prod.nombre FROM PEDIDO AS p JOIN CLIENTE AS c ON p.id_cliente = c.id_cliente JOIN PRODUCTO AS prod ON p.id_producto = prod.id_producto WHERE id_pedido = %s", (id_pedido, )) #muestra id_pedido, nombre, apellidos, dni, producto 
        resultado = cursor.fetchall()

        if resultado:# Mostraremos todos los datos del pedido y del cliente.
            print("Este es el pedido con id: ", id_pedido)
            print("Cliente: ", resultado[0][1] + resultado[0][2], "DNI: ", resultado[0][3])
            for registro_pedido in resultado:
                print("Producto: ", registro_pedido[4])
                 #Mostraremos nombre de productos
        else:
            print("No hay datos para este pedido")

        conexion.close()#Cerramos conexion con la base de datos
    except ValueError:
        print("Error al realizar la compra") 




    
    