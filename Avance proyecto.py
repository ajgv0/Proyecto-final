from datetime import datetime
import time, os

# Diccionario de usuarios con su contraseña
usuarios = {'Edgar': '123456'}

# Inventario inicial con códigos, nombre, precio y stock
inventario = {
    "A1": {"nombre": "Martillo",       "precio": 180.0,  "stock": 25},
    "A2": {"nombre": "Desarmador",     "precio": 75.0,   "stock": 40},
    "A3": {"nombre": "Taladro",        "precio": 1450.0, "stock": 7},
    "A4": {"nombre": "Pijas (100 pz)", "precio": 120.0,  "stock": 18},
    "A5": {"nombre": "Cinta métrica",  "precio": 95.0,   "stock": 12},
}

LIMITE_REABASTO = 5      # si baja de aquí, conviene surtir
registro_compras = []    # aquí se guardan los tickets de las compras
fecha_sesion = ""        # fecha que pide el sistema al inicio

# Control de inactividad, si se pasa el límite pregunta si quiere seguir
def verificar_inactividad(tiempo_inicio, limite_segundos=5):
    if time.time() - tiempo_inicio > limite_segundos:
        while True:
            dec = input("Límite de tiempo alcanzado, ¿Desea continuar?: ").lower()
            if dec == "si":
                print("Regresando...\n")
                return True
            elif dec == "no":
                print("\nSaliendo del programa\n")
                os._exit(0)
            else:
                print("Respuesta inválida, intenta de nuevo")
    return False

# Muestra todo el inventario con sus datos
def mostrar_inventario():
    print("\nInventario actual")
    print(f"{'Código':<6} {'Producto':<20} {'Precio':>8} {'Cantidad':>10}")
    for codigo, articulo in inventario.items():
        print(f"{codigo:<6} {articulo['nombre']:<20} ${articulo['precio']:>7.2f} {articulo['stock']:>10}")
    print()

# Verifica si hay artículos con poco stock
def alerta_reabasto():
    hay_aviso = False
    for codigo, articulo in inventario.items():
        if articulo["stock"] < LIMITE_REABASTO:
            if not hay_aviso:
                print("Aviso: hay productos con poca existencia")
                hay_aviso = True
            print(f" - {codigo} {articulo['nombre']} (cantidad: {articulo['stock']})")
    if hay_aviso:
        print()

# Calcula el descuento del 10% si se compra más de $1000
def calcular_descuento(subtotal):
    return (subtotal * 0.10, subtotal * 0.90) if subtotal >= 1000 else (0.0, subtotal)

# Función para pedir la cantidad y validarla
def leer_cantidad():
    tiempo_inicio = time.time()
    dato = input("Cantidad: ").strip()
    verificar_inactividad(tiempo_inicio)
    try:
        cantidad = int(dato)
        return cantidad if cantidad > 0 else None
    except ValueError:
        return None

# Proceso de una compra
def realizar_compra():
    carrito = []
    print("\nNueva compra")
    while True:
        mostrar_inventario()
        tiempo_inicio = time.time()
        codigo = input("Código (ENTER para terminar): ").strip().upper()
        verificar_inactividad(tiempo_inicio)
        if codigo == "":
            break
        if codigo not in inventario:
            print("No existe ese código.\n")
            continue
        cantidad = leer_cantidad()
        if not cantidad:
            print("Cantidad no válida.\n")
            continue
        if cantidad > inventario[codigo]["stock"]:
            print(f"No alcanza. Disponibles: {inventario[codigo]['stock']}.\n")
            continue
        precio_unitario = inventario[codigo]["precio"]
        importe = precio_unitario * cantidad
        carrito.append((codigo, inventario[codigo]["nombre"], precio_unitario, cantidad, importe))
        inventario[codigo]["stock"] -= cantidad
        print("Producto agregado.\n")
    if not carrito:
        print("No se agregaron productos.\n")
        return
    subtotal = sum(item[4] for item in carrito)
    descuento, total = calcular_descuento(subtotal)
    print("\nResumen de la compra")
    print(f"{'Código':<6} {'Producto':<20} {'Precio unitario':>15} {'Cantidad':>10} {'Importe':>12}")
    for codigo, nombre, precio_unitario, cantidad, importe in carrito:
        print(f"{codigo:<6} {nombre:<20} ${precio_unitario:>14.2f} {cantidad:>10} ${importe:>11.2f}")
    print(f"\nSubtotal: ${subtotal:,.2f}")
    if descuento > 0:
        print(f"Descuento 10%: -${descuento:,.2f}")
    else:
        print("No hay descuento (menos de $1000).")
    print(f"Total a pagar: ${total:,.2f}\n")

    # Guardar compra en memoria
    registro_compras.append({
        "id": len(registro_compras)+1,
        "fecha": fecha_sesion,
        "items": carrito,
        "subtotal": subtotal,
        "descuento": descuento,
        "total": total
    })

    # También guardarlo en un archivo de texto
    with open("registro_compras.txt", "a", encoding="utf-8") as f:
        f.write(f"ID: {len(registro_compras)}\n")
        f.write(f"Fecha: {fecha_sesion}\n")
        for codigo, nombre, precio_unitario, cantidad, importe in carrito:
            f.write(f"  {codigo} - {nombre} x{cantidad} @ ${precio_unitario:.2f} = ${importe:.2f}\n")
        f.write(f"Subtotal: ${subtotal:.2f}\n")
        f.write(f"Descuento: ${descuento:.2f}\n")
        f.write(f"Total: ${total:.2f}\n")
        f.write("-" * 40 + "\n\n")
    alerta_reabasto()

# Imprime todas las compras registradas
def ver_registro_compras():
    if not registro_compras:
        print("\nNo hay compras registradas.\n")
        return
    print("\nRegistro de compras")
    print(f"{'ID':<4} {'Fecha':<19} {'Artículos':>10} {'Subtotal':>12} {'Descuento':>12} {'Total':>12}")
    for ticket in registro_compras:
        total_articulos = sum(item[3] for item in ticket["items"])
        print(f"{ticket['id']:<4} {ticket['fecha']:<19} {total_articulos:>10} "
              f"${ticket['subtotal']:>10.2f} ${ticket['descuento']:>10.2f} ${ticket['total']:>10.2f}")

# Permite rellenar stock de un producto
def rellenar_stock():
    mostrar_inventario()
    tiempo_inicio = time.time()
    codigo = input("Código del producto a rellenar: ").strip().upper()
    verificar_inactividad(tiempo_inicio)
    if codigo not in inventario:
        print("Ese código no existe.\n")
        return
    cantidad = leer_cantidad()
    if not cantidad:
        print("Cantidad no válida.\n")
        return
    inventario[codigo]["stock"] += cantidad
    print(f"Se añadieron {cantidad} unidades a {inventario[codigo]['nombre']}.")
    print(f"Nuevo stock: {inventario[codigo]['stock']}\n")

# Menú principal con opciones
def menu():
    while True: 
        tiempo_inicio = time.time()
        print("\nMenú principal")
        print("1) Ver inventario")
        print("2) Realizar compra")
        print("3) Ver registro de compras")
        print("4) Rellenar stock")
        print("0) Salir")
        opcion = input("Elige una opción: ").strip()
        verificar_inactividad(tiempo_inicio)
        if opcion == "1":
            mostrar_inventario()
            alerta_reabasto()
        elif opcion == "2":
            realizar_compra()
        elif opcion == "3":
            ver_registro_compras()
        elif opcion == "4":
            rellenar_stock()
        elif opcion == "0":
            print("Gracias por usar FerreTodo.")
            break
        else:
            print("Opción no válida.\n")

# Inicio de sesión con usuario, contraseña y fecha
def iniciar_sesion():
    global fecha_sesion
    while True:   
        tiempo_inicio = time.time()
        nombre = input('Ingresar Usuario: ')
        verificar_inactividad(tiempo_inicio)
        tiempo_inicio = time.time()
        contraseña = input('Ingresar contraseña: ')
        verificar_inactividad(tiempo_inicio)
        if nombre in usuarios and usuarios[nombre] == contraseña:
            print('\n')
            print(f'Bienvenido {nombre}')
            print('\n')
            # Se pide la fecha al inicio y queda fija para toda la sesión
            while True:
                fecha_input = input("Ingresa la fecha de la sesión (dd/mm/aaaa): ").strip()
                try:
                    fecha_valida = datetime.strptime(fecha_input, "%d/%m/%Y")
                    fecha_sesion = fecha_input
                    break
                except ValueError:
                    print("Formato inválido. Intenta de nuevo con el formato dd/mm/aaaa.")
            print('Espere 5 segundos, estamos preparando todo')
            time.sleep(5)
            menu()
            break
        else:
            print("Usuario y/o contraseña no encontrados")
            tiempo_inicio = time.time()
            dec = input("¿Desea intentarlo de nuevo?: ")
            verificar_inactividad(tiempo_inicio)
            if dec.lower() == 'si':
                print('\n')
                continue
            elif dec.lower() == 'no':
                break
            else:
                print("Respuesta inválida")

# Se arranca el programa desde aquí
iniciar_sesion()
