# backend_alarma.py
import threading
import platform

def sonar_alarma():
    sistema = platform.system()
    try:
        if sistema == "Windows":
            import winsound
            winsound.Beep(1000, 800)  # frecuencia, duración ms
        else:
            print('\a')  # beep en consola (si el terminal lo soporta)
    except Exception:
        pass

def iniciar_alarma(segundos, mensaje, callback):
    def _disparar():
        sonar_alarma()
        if callback is not None:
            callback(mensaje)

    timer = threading.Timer(segundos, _disparar)
    timer.start()
    return timer
