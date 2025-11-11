import tkinter as tk
from tkinter import messagebox
from backend_alarma import iniciar_alarma

MAX_HORAS = 23

alarma_activa = None
continuar_contador = False
segundos_restantes = 0
mensaje_actual = ""
pausada = False

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

# -------------------- LÓGICA DE LA ALARMA --------------------

def mostrar_mensaje(mensaje):
    """Se llama cuando el backend dispara la alarma (tiempo cumplido)."""
    global alarma_activa, continuar_contador, segundos_restantes, pausada

    alarma_activa = None
    continuar_contador = False
    pausada = False
    segundos_restantes = 0

    label_estado.config(text="Sin alarma activa", fg="#555555")
    label_digital.config(text="--:--:--")
    btn_activar.config(state="normal")
    btn_pausa_play.config(state="disabled", text="⏸️", bg="#3949ab")

    messagebox.showinfo("Alarma", mensaje)

def callback_backend(msg):
    root.after(0, mostrar_mensaje, msg)

def activar_alarma():
    global alarma_activa, continuar_contador, segundos_restantes, mensaje_actual, pausada

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
    mensaje_actual = mensaje

    segundos_restantes = total_segundos
    continuar_contador = True
    pausada = False

    btn_activar.config(state="disabled")
    btn_pausa_play.config(state="normal", text="⏸️", bg="#3949ab")
    label_estado.config(
        text=f"Alarma programada: {h:02d}:{m:02d}:{s:02d}",
        fg="#2e7d32"
    )
    label_digital.config(text=f"{h:02d}:{m:02d}:{s:02d}")

    if alarma_activa is not None:
        alarma_activa.cancel()
    alarma_activa = iniciar_alarma(total_segundos, mensaje_actual, callback_backend)

    cuenta_regresiva()

def cuenta_regresiva():
    global segundos_restantes, continuar_contador

    if not continuar_contador:
        return

    if segundos_restantes >= 0:
        h = segundos_restantes // 3600
        m = (segundos_restantes % 3600) // 60
        s = segundos_restantes % 60
        label_digital.config(text=f"{h:02d}:{m:02d}:{s:02d}")

        if segundos_restantes > 0:
            segundos_restantes -= 1
            root.after(1000, cuenta_regresiva)

def alternar_pausa_play():
    """Pausa o reanuda con un solo botón (⏸️ / ▶️)."""
    global pausada, continuar_contador, alarma_activa

    # Si no hay alarma activa y no está pausada, no hay nada que hacer
    if alarma_activa is None and not pausada:
        return

    if not pausada:
        # PAUSAR
        pausada = True
        continuar_contador = False
        if alarma_activa is not None:
            alarma_activa.cancel()
            alarma_activa = None
        btn_pausa_play.config(text="▶️", bg="#ff9800")
        label_estado.config(text="Alarma en pausa", fg="#ff9800")
    else:
        # REANUDAR
        pausada = False
        continuar_contador = True
        btn_pausa_play.config(text="⏸️", bg="#3949ab")
        label_estado.config(text="Alarma reanudada", fg="#2e7d32")

        if segundos_restantes > 0:
            alarma_nueva = iniciar_alarma(segundos_restantes, mensaje_actual, callback_backend)
            globals()["alarma_activa"] = alarma_nueva

        cuenta_regresiva()

# -------------------- INTERFAZ PRINCIPAL (480x700) --------------------

root = tk.Tk()
root.title("Alarma con Notificación")
root.geometry("480x700")
root.resizable(False, False)

BG = "#f4f4f7"
CARD = "#ffffff"
PRIMARY = "#3949ab"
TEXT = "#333333"

root.configure(bg=BG)

# Frame principal con más altura para aire
frame = tk.Frame(root, bg=CARD)
frame.place(relx=0.5, rely=0.0, anchor="n", width=440, height=660, y=15)

# Título
titulo = tk.Label(
    frame,
    text="Alarma con notificación",
    bg=CARD,
    fg=PRIMARY,
    font=("Segoe UI", 22, "bold")
)
titulo.pack(pady=(10, 25))

# --- Validación: máx 2 caracteres numéricos ---
def validar_dos_digitos(nuevo_valor):
    if nuevo_valor == "":
        return True
    if len(nuevo_valor) > 2:
        return False
    return nuevo_valor.isdigit()

vcmd = (root.register(validar_dos_digitos), "%P")

# ----- Selector H / M / S -----
selector = tk.Frame(frame, bg=CARD)
selector.pack(pady=(0, 35))

def crear_columna_editable(parent, etiqueta, max_val, vcmd):
    col = tk.Frame(parent, bg=CARD)
    col.pack(side="left", padx=24)

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
    btn_up.pack(pady=(0, 6))

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
        validatecommand=vcmd
    )
    entry.insert(0, "00")
    entry.pack(pady=(0, 6))

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
    lbl_etq.pack(pady=(4, 0))

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
lbl_msg.pack(anchor="w", padx=30, pady=(5, 6))

entry_mensaje = tk.Entry(frame, font=("Segoe UI", 11))
entry_mensaje.pack(padx=30, pady=(0, 25), fill="x")

# ----- Botón Activar -----
btn_activar = tk.Button(
    frame,
    text="Activar alarma",
    bg=PRIMARY,
    fg="white",
    font=("Segoe UI", 12, "bold"),
    relief="flat",
    padx=24,
    pady=6,
    command=activar_alarma
)
btn_activar.pack(pady=(0, 25))

# ----- Display digital -----
display_frame = tk.Frame(frame, bg=CARD)
display_frame.pack(pady=(0, 10))

label_display_title = tk.Label(
    display_frame,
    text="Cuenta regresiva",
    bg=CARD,
    fg="#555555",
    font=("Segoe UI", 11)
)
label_display_title.pack(pady=(0, 6))

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
    font=("Consolas", 34, "bold"),
    bg="#111111",
    fg="#00ff88",
    width=10
)
label_digital.pack(padx=16, pady=10)

# ----- Botón único Pausa/Reanudar debajo del display -----
btn_pausa_play = tk.Button(
    frame,
    text="⏸️",
    bg="#3949ab",
    fg="white",
    font=("Segoe UI", 16, "bold"),
    relief="flat",
    width=4,
    state="disabled",
    command=alternar_pausa_play
)
btn_pausa_play.pack(pady=(14, 16))

# ----- Estado -----
label_estado = tk.Label(
    frame,
    text="Sin alarma activa",
    bg=CARD,
    fg="#555555",
    font=("Segoe UI", 11)
)
label_estado.pack(pady=(8, 0))

# Relleno inferior para centrar mejor
tk.Label(frame, bg=CARD).pack(expand=True, fill="both")

root.mainloop()
