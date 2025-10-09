# tabla_con_etiquetas_horizontales.py

def pedir_entero_positivo(msg: str) -> int:
    while True:
        s = input(msg).strip()
        try:
            n = int(s)
            if n >= 1:
                return n
            print("⚠️  Debe ser un entero >= 1.")
        except ValueError:
            print("⚠️  Ingresa un número entero válido.")

def pedir_texto_no_vacio(msg: str) -> str:
    while True:
        s = input(msg).strip()
        if s:
            return s
        print("⚠️  No puede estar vacío.")

def construir_borde(anchos):
    return "+" + "+".join("-" * (w + 2) for w in anchos) + "+"

def construir_fila(celdas, anchos):
    return "|" + "|".join(f" {str(v).ljust(w)} " for v, w in zip(celdas, anchos)) + "|"

def imprimir_tabla(row_labels, col_headers, data_rows):
    # Anchos
    label_w = max((len(str(x)) for x in row_labels), default=0)
    col_ws = []
    for j in range(len(col_headers)):
        max_dato = max((len(str(data_rows[i][j])) for i in range(len(data_rows))), default=0)
        col_ws.append(max(len(str(col_headers[j])), max_dato))
    anchos = [label_w] + col_ws

    borde = construir_borde(anchos)
    print("\nTabla finalizada:\n")
    print(borde)
    # Encabezado: esquina superior izquierda vacía
    print(construir_fila([""] + col_headers, anchos))
    print(borde)
    # Filas con etiqueta a la izquierda
    for lbl, fila in zip(row_labels, data_rows):
        print(construir_fila([lbl] + fila, anchos))
    print(borde)

def main():
    print("=== Creador de Tabla con Etiquetas de Fila (no cuentan como columna) ===\n")

    num_cols = pedir_entero_positivo("¿Cuántas columnas de datos tendrá la tabla? ")
    num_rows = pedir_entero_positivo("¿Cuántas filas deseas capturar? ")

    # Encabezados de columnas de datos (p.ej. 1, 2, 3)
    print("\nIntroduce los encabezados de las columnas de datos:")
    col_headers = [pedir_texto_no_vacio(f"  Encabezado columna {j+1}: ") for j in range(num_cols)]

    # Etiquetas de fila (p.ej. Frutas, Embutidos, Postres)
    print("\nIntroduce las etiquetas de cada fila:")
    row_labels = [pedir_texto_no_vacio(f"  Etiqueta para la fila {i+1}: ") for i in range(num_rows)]

    # Captura de datos por fila/columna
    print("\nCaptura de datos:")
    data_rows = []
    for i in range(num_rows):
        print(f"\n— {row_labels[i]} —")
        fila = []
        for j in range(num_cols):
            val = input(f"  Valor para columna '{col_headers[j]}' de [{row_labels[i]}]: ").strip()
            fila.append(val)
        data_rows.append(fila)

    imprimir_tabla(row_labels, col_headers, data_rows)

if __name__ == "__main__":
    main()
