import sqlite3
import time

# Función para crear la base de datos y la tabla si no existen
def crear_db():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cuenta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            saldo REAL,
            pin INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_hora TEXT,
            tipo TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Función para inicializar los datos de la cuenta
def inicializar_cuenta():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM cuenta')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO cuenta (saldo, pin) VALUES (?, ?)', (250000.0, 1234))
        conn.commit()
    conn.close()

# Función para leer el pin desde la base de datos
def leer_pin():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('SELECT pin FROM cuenta WHERE id = 1')
    pin = cursor.fetchone()[0]
    conn.close()
    return pin

# Función para guardar el nuevo pin en la base de datos
def guardar_pin(nuevo_pin):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE cuenta SET pin = ? WHERE id = 1', (nuevo_pin,))
    conn.commit()
    conn.close()

# Función para registrar una transacción
def registrar_transaccion(transaccion):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    fecha_hora = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    cursor.execute('INSERT INTO transacciones (fecha_hora, tipo) VALUES (?, ?)', (fecha_hora, transaccion))
    conn.commit()
    conn.close()

# Función para consultar el saldo
def consultar_saldo():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('SELECT saldo FROM cuenta WHERE id = 1')
    saldo = cursor.fetchone()[0]
    print(f"Saldo Actual: ${saldo:.2f}")
    registrar_transaccion("Consulta de Saldo")
    conn.close()

# Función para retirar dinero
def retirar_saldo():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cantidad = float(input("Ingrese la cantidad a retirar: $"))
    cursor.execute('SELECT saldo FROM cuenta WHERE id = 1')
    saldo = cursor.fetchone()[0]
    if 0 < cantidad <= saldo:
        nuevo_saldo = saldo - cantidad
        cursor.execute('UPDATE cuenta SET saldo = ? WHERE id = 1', (nuevo_saldo,))
        print(f"Retiro realizado. Su saldo actual es de: ${nuevo_saldo:.2f}")
        registrar_transaccion("Retiro")
        conn.commit()
    else:
        print("El saldo en la cuenta es insuficiente para el retiro.")
    conn.close()

# Función para depositar dinero
def depositar_saldo():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cantidad = float(input("Ingrese la cantidad a depositar: $"))
    if cantidad > 0:
        cursor.execute('SELECT saldo FROM cuenta WHERE id = 1')
        saldo = cursor.fetchone()[0]
        nuevo_saldo = saldo + cantidad
        cursor.execute('UPDATE cuenta SET saldo = ? WHERE id = 1', (nuevo_saldo,))
        print(f"Depósito realizado. Su saldo actual es de: ${nuevo_saldo:.2f}")
        registrar_transaccion("Depósito")
        conn.commit()
    else:
        print("Cantidad no valida para realizar el depósito.")
    conn.close()

# Función para cambiar el PIN
def cambiar_pin():
    nuevo_pin = int(input("Ingrese el nuevo PIN: "))
    guardar_pin(nuevo_pin)
    print("El PIN ha sido actualizado.")
    registrar_transaccion("Cambio de PIN")

# Función principal
def main():
    crear_db()
    inicializar_cuenta()
    
    pin_actual = leer_pin()
    pin_ingresado = int(input("Ingrese su PIN: "))

    if pin_ingresado == pin_actual:
        print("Hola. Bienvenida/o al cajero automático.")
        while True:
            print("\nOpciones:\n"
                  "1. Consultar Saldo\n"
                  "2. Retirar Dinero\n"
                  "3. Depositar Dinero\n"
                  "4. Cambiar PIN\n"
                  "5. Salir")
            opcion = int(input("Seleccione una opción: "))

            if opcion == 1:
                consultar_saldo()
            elif opcion == 2:
                retirar_saldo()
            elif opcion == 3:
                depositar_saldo()
            elif opcion == 4:
                cambiar_pin()
            elif opcion == 5:
                print("Gracias por usar el cajero automático. ¡Buen día!")
                break
            else:
                print("Opcion invalida. Por favor seleccione una opcion valida.")
    else:
        print("PIN Incorrecto. No se puede acceder.")

if __name__ == "__main__":
    main()