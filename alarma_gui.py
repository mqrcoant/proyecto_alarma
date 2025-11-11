import tkinter as tk
from tkinter import messagebox
from backend_alarma import iniciar_alarma

MAX_HORAS = 23

alarma_activa = None
continuar_contador = False

# -------------------- UTILIDADES --------------------

def normalizar_valor(entry, limite):
    """Ajusta el contenido del Entry al rango [0, limite] y lo muestra con 2 dígitos."""
    try:
        val = int(entry.get())
    except ValueError:
        val = 0
    if val < 0:
        val = 0
    if val > limite:
        val = limite
    entry.delete(0, tk.END)
    entry.insert(0, f"{val:02d}")
    return val

def inc(entry, limite):
    val = normalizar_valor(entry, limite)
    val = (val + 1) if val < limite else 0
    entry.delete(0, tk.END)
    entry.insert(0, f"{val:02d}")

def dec(entry, limite):
    val = normalizar_valor(entry, limite)
    val = (val - 1) if val > 0 else limite
    entry.delete(0, tk.END)
    entry.insert(0, f"{val:02d}")

# -------------------- LÓGICA ALARMA --------------------

def mostrar_mensaje(mensaje):
    global alarma_activa, continuar_contador
    alarma_activa = None
    continuar_contador = False

    label_estado.config(text="Sin alarma activa", fg="#555555")
    label_digital.config(text="--:--:--")
    btn_activar.config(state="normal")

    messagebox.showinfo("Alarma", mensaje)

def callback_backend(msg):
    root.after(0, mostrar_mensaje, msg)

def activar_alarma():
    global alarma_activa, continuar_contador

    h = normalizar_valor(entry_horas, MAX_HORAS)
    m = normalizar_valor(entry_min, 59)
    s = normalizar_valor(entry_seg, 59)

    total_segundos = h * 3600 + m * 60 + s
    if total_segundos <= 0:
        messagebox.showerror("Error", "Selecciona un tiempo mayor que 0.")
        return

    mensaje = entry_mensaje.get().strip()
    if not mensaje:
        mensaje = "¡TIEMPO CUMPLIDO! 🔔"

    btn_activar.config(state="disabled")
    label_estado.config(
        text=f"Alarma en {h:02d}:{m:02d}:{s:02d}",
        fg="#2e7d32"
    )

    continuar_contador = True
    label_digital.config(text=f"{h:02d}:{m:02d}:{s:02d}")

    alarma_activa = iniciar_alarma(total_segundos, mensaje, callback_backend)
    cuenta_regresiva(total_segundos)

def cuenta_regresiva(restante):
    global continuar_contador
    if not continuar_contador:
        return

    if restante >= 0:
        h = restante // 3600
        m = (restante % 3600) // 60
        s = restante % 60
        texto = f"{h:02d}:{m:02d}:{s:02d}"

        label_digital.config(text=texto)

        if restante > 0:
            root.after(1000, cuenta_regresiva, restante - 1)
        # al llegar a 0, el backend llama mostrar_mensaje()

# -------------------- INTERFAZ PRINCIPAL (480x600) --------------------

root = tk.Tk()
root.title("Alarma con Notificación")
root.geometry("480x600")
root.resizable(False, False)

BG = "#f4f4f7"
CARD = "#ffffff"
PRIMARY = "#3949ab"
TEXT = "#333333"

root.configure(bg=BG)

frame = tk.Frame(root, bg=CARD)
frame.place(relx=0.5, rely=0.0, anchor="n", width=440, height=580, y=10)

titulo = tk.Label(
    frame,
    text="Alarma con notificación",
    bg=CARD,
    fg=PRIMARY,
    font=("Segoe UI", 20, "bold")
)
titulo.pack(pady=(10, 20))

# --- Validación: máx 2 caracteres numéricos ---
def validar_dos_digitos(nuevo_valor):
    # nuevo_valor = texto resultante si se permite la tecla
    if nuevo_valor == "":
        return True
    if len(nuevo_valor) > 2:
        return False
    return nuevo_valor.isdigit()

vcmd = (root.register(validar_dos_digitos), "%P")

# ----- Selector H / M / S -----
selector = tk.Frame(frame, bg=CARD)
selector.pack(pady=(0, 25))

def crear_columna_editable(parent, etiqueta, max_val, vcmd):
    col = tk.Frame(parent, bg=CARD)
    col.pack(side="left", padx=20)

    btn_up = tk.Button(
        col,
        text="▲",
        font=("Segoe UI", 11, "bold"),
        width=3,
        bg=CARD,
        fg=PRIMARY,
        relief="flat",
        command=lambda: inc(entry, max_val)
    )
    btn_up.pack(pady=(0, 4))

    entry = tk.Entry(
        col,
        width=3,
        justify="center",
        font=("Consolas", 22, "bold"),
        bg="#eeeeee",
        fg=TEXT,
        bd=1,
        relief="solid",
        validate="key",
        validatecommand=vcmd  # máximo 2 dígitos numéricos
    )
    entry.insert(0, "00")
    entry.pack(pady=(0, 4))

    btn_down = tk.Button(
        col,
        text="▼",
        font=("Segoe UI", 11, "bold"),
        width=3,
        bg=CARD,
        fg=PRIMARY,
        relief="flat",
        command=lambda: dec(entry, max_val)
    )
    btn_down.pack(pady=(0, 4))

    lbl_etq = tk.Label(
        col,
        text=etiqueta,
        bg=CARD,
        fg="#777777",
        font=("Segoe UI", 10)
    )
    lbl_etq.pack(pady=(2, 0))

    return entry

entry_horas = crear_columna_editable(selector, "HORAS", MAX_HORAS, vcmd)
entry_min   = crear_columna_editable(selector, "MINUTOS", 59, vcmd)
entry_seg   = crear_columna_editable(selector, "SEGUNDOS", 59, vcmd)

# ----- Mensaje -----
lbl_msg = tk.Label(
    frame,
    text="Mensaje de la alarma:",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 11)
)
lbl_msg.pack(anchor="w", padx=25, pady=(10, 5))

entry_mensaje = tk.Entry(frame, font=("Segoe UI", 11))
entry_mensaje.pack(padx=25, pady=(0, 20), fill="x")

# ----- Botón activar -----
btn_activar = tk.Button(
    frame,
    text="Activar alarma",
    bg=PRIMARY,
    fg="white",
    font=("Segoe UI", 12, "bold"),
    relief="flat",
    padx=20,
    pady=6,
    command=activar_alarma
)
btn_activar.pack(pady=(0, 15))

# ----- Display digital -----
display_frame = tk.Frame(frame, bg=CARD)
display_frame.pack(pady=(5, 5))

label_display_title = tk.Label(
    display_frame,
    text="Cuenta regresiva",
    bg=CARD,
    fg="#555555",
    font=("Segoe UI", 10)
)
label_display_title.pack(pady=(0, 4))

display_box = tk.Frame(
    display_frame,
    bg="#111111",
    bd=2,
    relief="sunken"
)
display_box.pack()

label_digital = tk.Label(
    display_box,
    text="--:--:--",
    font=("Consolas", 30, "bold"),
    bg="#111111",
    fg="#00ff88",
    width=10
)
label_digital.pack(padx=10, pady=8)

# ----- Estado -----
label_estado = tk.Label(
    frame,
    text="Sin alarma activa",
    bg=CARD,
    fg="#555555",
    font=("Segoe UI", 10)
)
label_estado.pack(pady=(10, 0))

tk.Label(frame, bg=CARD).pack(expand=True, fill="both")

root.mainloop()
