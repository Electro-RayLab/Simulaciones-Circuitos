# grafica_tkinter.py
# Dibuja puntos y una línea que los une usando solo Tkinter (sin librerías externas)

import tkinter as tk

def pedir_float(msg):
    while True:
        s = input(msg).strip()
        try:
            return float(s)
        except ValueError:
            print("⚠️  Ingresa un número válido.")

def pedir_float_pos(msg):
    while True:
        v = pedir_float(msg)
        if v > 0:
            return v
        print("⚠️  Debe ser > 0.")

def pedir_entero_pos(msg):
    while True:
        s = input(msg).strip()
        try:
            n = int(s)
            if n >= 1:
                return n
        except ValueError:
            pass
        print("⚠️  Ingresa un entero ≥ 1.")

def frange(a, b, step):
    vals = []
    if a <= b:
        x = a
        while x <= b + 1e-12:
            vals.append(round(x, 12))
            x += step
    else:
        x = a
        while x >= b - 1e-12:
            vals.append(round(x, 12))
            x -= step
    return vals

# ====== Entrada por consola ======
x_name = input("Nombre de la variable independiente (X): ").strip() or "X"
y_name = input("Nombre de la variable dependiente (Y): ").strip() or "Y"

print("\n--- Rango de X ---")
x_ini = pedir_float("Primer valor de X: ")
x_fin = pedir_float("Último valor de X: ")
dx = pedir_float_pos("Intervalo entre valores de X (>0): ")

print("\n--- Rango de Y ---")
y_ini = pedir_float("Primer valor de Y: ")
y_fin = pedir_float("Último valor de Y: ")
dy = pedir_float_pos("Intervalo entre valores de Y (>0): ")

n = pedir_entero_pos("\n¿Cuántos puntos (x,y) vas a ingresar? ")
puntos = []
for i in range(1, n + 1):
    while True:
        s = input(f"  Punto {i} en formato x,y (ej. 2.5, 3): ").strip().replace(" ", "")
        try:
            xs, ys = s.split(",")
            x = float(xs); y = float(ys)
            puntos.append((x, y))
            break
        except Exception:
            print("   ⚠️  Formato inválido. Ejemplo válido: 1.2, 3.4")

# ====== Preparar ticks y límites ======
xs = [p[0] for p in puntos]
ys = [p[1] for p in puntos]
xmin = min(min(x_ini, x_fin), min(xs))
xmax = max(max(x_ini, x_fin), max(xs))
ymin = min(min(y_ini, y_fin), min(ys))
ymax = max(max(y_ini, y_fin), max(ys))

xticks = frange(min(x_ini, x_fin), max(x_ini, x_fin), dx)
yticks = frange(min(y_ini, y_fin), max(y_ini, y_fin), dy)

# ====== Ventana y Canvas ======
W, H = 800, 600
MARGIN_L, MARGIN_R = 80, 40
MARGIN_T, MARGIN_B = 60, 80

root = tk.Tk()
root.title("Gráfica (Tkinter)")

canvas = tk.Canvas(root, width=W, height=H, bg="white")
canvas.pack()

# Conversión de coordenadas (x,y) -> (X,Y) de pantalla
def to_screen(x, y):
    # evitar división por cero si rango es degenerado
    xd = xmax - xmin if xmax != xmin else 1.0
    yd = ymax - ymin if ymax != ymin else 1.0
    X = MARGIN_L + (x - xmin) * (W - MARGIN_L - MARGIN_R) / xd
    Y = H - MARGIN_B - (y - ymin) * (H - MARGIN_T - MARGIN_B) / yd
    return X, Y

# Marco
canvas.create_rectangle(MARGIN_L, MARGIN_T, W - MARGIN_R, H - MARGIN_B)

# Ejes (si 0 está dentro del rango, dibujar ejes en 0)
def draw_axes():
    # Eje X
    if xmin <= 0 <= xmax:
        X0, Y0 = to_screen(0, ymin)
        X1, Y1 = to_screen(0, ymax)
        canvas.create_line(X0, Y0, X1, Y1)  # eje Y
    # Eje Y
    if ymin <= 0 <= ymax:
        X0, Y0 = to_screen(xmin, 0)
        X1, Y1 = to_screen(xmax, 0)
        canvas.create_line(X0, Y0, X1, Y1)  # eje X

draw_axes()

# Ticks y grid ligerita (no se especifican colores fijos; Tkinter usa el default)
def draw_ticks_and_grid():
    # X ticks
    for xv in xticks:
        X, Y0 = to_screen(xv, ymin)
        _, Y1 = to_screen(xv, ymax)
        # Marcas en el marco inferior
        canvas.create_line(X, H - MARGIN_B, X, H - MARGIN_B + 5)
        canvas.create_text(X, H - MARGIN_B + 18, text=f"{xv}", anchor="n")
        # Grid vertical suave
        canvas.create_line(X, Y0, X, Y1, dash=(2, 4))
    # Y ticks
    for yv in yticks:
        X0, Y = to_screen(xmin, yv)
        X1, _ = to_screen(xmax, yv)
        # Marcas en el marco izquierdo
        canvas.create_line(MARGIN_L - 5, Y, MARGIN_L, Y)
        canvas.create_text(MARGIN_L - 8, Y, text=f"{yv}", anchor="e")
        # Grid horizontal suave
        canvas.create_line(X0, Y, X1, Y, dash=(2, 4))

draw_ticks_and_grid()

# Etiquetas de ejes
canvas.create_text((MARGIN_L + W - MARGIN_R) / 2, H - 40, text=x_name)
canvas.create_text(30, (MARGIN_T + H - MARGIN_B) / 2, text=y_name, angle=90)

# Dibujar puntos y línea que los une en el orden ingresado
screen_pts = [to_screen(x, y) for (x, y) in puntos]

# Línea sólida
for i in range(len(screen_pts) - 1):
    x0, y0 = screen_pts[i]
    x1, y1 = screen_pts[i + 1]
    canvas.create_line(x0, y0, x1, y1)

# Puntos
R = 4
for (x, y), (X, Y) in zip(puntos, screen_pts):
    canvas.create_oval(X - R, Y - R, X + R, Y + R, fill="")

# Título opcional
canvas.create_text(W/2, 20, text="Gráfica de puntos con línea (Tkinter)")

root.mainloop()

