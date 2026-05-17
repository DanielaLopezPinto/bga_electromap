def validar_entero(prompt, minimo=None, maximo=None):
    while True:
        entrada = input(prompt).strip()
        if not entrada:
            print("el campo no puede estar vacío")
            continue
        if not entrada.lstrip('-').isdigit():
            print("error: ingrese un número entero válido")
            continue
        valor = int(entrada)
        if minimo is not None and valor < minimo:
            print(f"el valor mínimo permitido es {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"el valor máximo permitido es {maximo}.")
            continue
        return valor

def validar_flotante(prompt, minimo=None, maximo=None):
    while True:
        entrada = input(prompt).strip()
        if not entrada:
            print("el campo no puede estar vacío")
            continue
        try:
            valor = float(entrada)
        except ValueError:
            print("error: ingrese un número válido (use punto como decimal)")
            continue
        if minimo is not None and valor < minimo:
            print(f"el valor mínimo permitido es {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"el valor máximo permitido es {maximo}.")
            continue
        return valor

def validar_texto(prompt, max_len=100):
    invalidos = ['<', '>', '/', '\\', '|', '"', '*', '?']
    while True:
        entrada = input(prompt).strip()
        if not entrada:
            print(" el campo no puede estar vacio")
            continue
        if len(entrada) > max_len:
            print(f"  máximo {max_len} caracteres permitidos")
            continue
        if any(c in entrada for c in invalidos):
            print(f"  Caracteres no permitidos: {invalidos}")
            continue
        return entrada

def validar_si_no(prompt):
    while True:
        entrada = input(prompt).strip().lower()
        if entrada in ['s', 'si', 'sí', 'n', 'no']:
            return entrada in ['s', 'si', 'sí']
        print("  ingrese 's' para sí o 'n' para no")