from datetime import datetime

usuarios=dict([
    ('Edgar Juan', '829103'),
])
# Productos iniciales
inventario = {
    "A1": {"nombre": "Martillo",       "precio": 180.0,  "stock": 25},
    "A2": {"nombre": "Desarmador",     "precio": 75.0,   "stock": 40},
    "A3": {"nombre": "Taladro",        "precio": 1450.0, "stock": 7},
    "A4": {"nombre": "Pijas (100 pz)", "precio": 120.0,  "stock": 18},
    "A5": {"nombre": "Cinta métrica",  "precio": 95.0,   "stock": 12},
}

LIMITE_REABASTO = 5      # si baja de aquí, conviene surtir
registro_compras = []    # tickets

def mostrar_inventario():
    # tabla simple
    print("\nInventario actual")
    print(f"{'Código':<6} {'Producto':<20} {'Precio':>8} {'Cantidad':>10}")
    for codigo, articulo in inventario.items():
        print(f"{codigo:<6} {articulo['nombre']:<20} ${articulo['precio']:>7.2f} {articulo['stock']:>10}")
    print()

def alerta_reabasto():
    # avisa productos bajos
    hay_aviso = False
    for codigo, articulo in inventario.items():
        if articulo["stock"] < LIMITE_REABASTO:
            if not hay_aviso:
                print("Aviso: hay productos con poca existencia")
                hay_aviso = True
            print(f" - {codigo} {articulo['nombre']} (cantidad: {articulo['stock']})")
    if hay_aviso:
        print()

def calcular_descuento(subtotal):
    # 10% desde $1000
    if subtotal >= 1000:
        descuento = subtotal * 0.10
    else:
        descuento = 0.0
    return descuento, subtotal - descuento

def leer_cantidad():
    # lee una cantidad válida (>0)
    dato = input("Cantidad: ").strip()
    try:
        cantidad = int(dato)
        return cantidad if cantidad > 0 else None
    except ValueError:
        return None

def realizar_compra():
    # arma carrito y descuenta del inventario
    carrito = []
    print("\nNueva compra")
    while True:
        mostrar_inventario()
        codigo = input("Código (ENTER para terminar): ").strip().upper()
        if codigo == "":
            break
        if codigo not in inventario:
            print("No existe ese código.\n")
            continue

        cantidad = leer_cantidad()
        if not cantidad:
            print("Cantidad no válida.\n")
            continue

        existencias_disponibles = inventario[codigo]["stock"]
        if cantidad > existencias_disponibles:
            print(f"No alcanza. Disponibles: {existencias_disponibles}.\n")
            continue

        precio_unitario = inventario[codigo]["precio"]
        importe = precio_unitario * cantidad
        carrito.append((codigo, inventario[codigo]["nombre"], precio_unitario, cantidad, importe))
        inventario[codigo]["stock"] -= cantidad
        print("Producto agregado.\n")

    if not carrito:
        print("No se agregaron productos.\n")
        return

    # resumen
    print("\nResumen de la compra")
    print(f"{'Código':<6} {'Producto':<20} {'Precio unitario':>15} {'Cantidad':>10} {'Importe':>12}")
    subtotal = 0.0
    for codigo, nombre, precio_unitario, cantidad, importe in carrito:
        print(f"{codigo:<6} {nombre:<20} ${precio_unitario:>14.2f} {cantidad:>10} ${importe:>11.2f}")
        subtotal += importe

    print(f"\nSubtotal: ${subtotal:,.2f}")
    descuento, total = calcular_descuento(subtotal)
    if descuento > 0:
        print(f"Descuento 10%: -${descuento:,.2f}")
    else:
        print("No hay descuento (menos de $1000).")
    print(f"Total a pagar: ${total:,.2f}\n")

    # guarda ticket
    ticket = {
        "id": len(registro_compras) + 1,
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "items": carrito,
        "subtotal": subtotal,
        "descuento": descuento,
        "total": total
    }
    registro_compras.append(ticket)

    alerta_reabasto()

def ver_registro_compras():
    # listado general (sin detalle por ticket)
    if not registro_compras:
        print("\nNo hay compras registradas.\n")
        return

    print("\nRegistro de compras")
    print(f"{'ID':<4} {'Fecha':<19} {'Artículos':>10} {'Subtotal':>12} {'Descuento':>12} {'Total':>12}")
    for ticket in registro_compras:
        total_articulos = 0
        for _, _, _, cantidad, _ in ticket["items"]:
            total_articulos += cantidad
        print(f"{ticket['id']:<4} {ticket['fecha']:<19} {total_articulos:>10} "
              f"${ticket['subtotal']:>10.2f} ${ticket['descuento']:>10.2f} ${ticket['total']:>10.2f}")

def rellenar_stock():
    # aumenta existencias de un producto
    mostrar_inventario()
    codigo = input("Código del producto a rellenar: ").strip().upper()
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


def menu():
    # menú principal
    while True: 
        print("\nMenú principal")
        print("1) Ver inventario")
        print("2) Realizar compra")
        print("3) Ver registro de compras")
        print("4) Rellenar stock")
        print("0) Salir")
        opcion = input("Elige una opción: ").strip()

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

import time
while True:   
    nombre=input('Ingresar Usuario: ')
    contraseña=input('Ingresar contraseña: ')      

    if nombre in usuarios and usuarios[nombre]==contraseña:
        print('\n')
        print(f'Bienvenido {nombre}')
        print('\n')
        print('Espere 5 segundos, estamos preparando todo')
        time.sleep(5)
        menu()
    else:
        print("Usuario y/o contraseña no encontrados")
        dec=input("¿Desea intentarlo de nuevo?: ")
        if dec.lower()=='si':
            print('\n')
            continue
        if dec.lower()=='no':
            break
            
def cargar_arch(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            print("Contenido del archivo:")
            print(f.read())
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta}' no se encontró.")
    except Exception as e:
        print(f"Otro error al abrir el archivo: {e}")
            

           


