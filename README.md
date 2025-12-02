# 🔔 Aplicación de Alarma con Threading en Python

Alarma hecha con threading en Python + Tkinter para interfaz, práctica de funcionamiento de Sistemas Operativos

## 🚀 Ejecución

Para ejecutar la aplicación, ejecuta el archivo:
```bash
python alarma_gui.py
```

---

## 📚 Explicación del Funcionamiento desde el Enfoque de Sistemas Operativos

### 1. ¿Qué es un Sistema Operativo y su Rol?

Un **Sistema Operativo (SO)** es el software fundamental que administra los recursos de hardware de una computadora y proporciona servicios a los programas de aplicación. En el contexto de esta alarma:

- **Gestión de procesos**: El SO crea y administra el proceso Python que ejecuta nuestra aplicación
- **Gestión de memoria**: Asigna memoria para nuestras variables, objetos y código
- **Gestión de tiempo**: Proporciona mecanismos para medir el tiempo y programar tareas futuras
- **Gestión de recursos**: Coordina el acceso al sonido, pantalla y otros recursos del sistema

### 2. Procesos vs. Hilos (Threads)

#### **Proceso**
Un proceso es una instancia de un programa en ejecución que tiene:
- Su propio espacio de memoria aislado
- Sus propios recursos (archivos abiertos, variables, etc.)
- Un identificador único (PID - Process ID)
- Al menos un hilo de ejecución principal

Cuando ejecutas `python alarma_gui.py`, el SO crea un **proceso Python**.

#### **Hilo (Thread)**
Un hilo es una unidad de ejecución dentro de un proceso que:
- Comparte el mismo espacio de memoria con otros hilos del mismo proceso
- Comparte recursos del proceso (variables globales, archivos abiertos, etc.)
- Tiene su propio flujo de ejecución independiente
- Es más ligero que crear un proceso completo

**Ventaja de los hilos**: Múltiples tareas pueden ejecutarse "simultáneamente" dentro del mismo programa sin duplicar memoria.

### 3. ¿Qué es Threading?

**Threading** es una técnica de programación que permite ejecutar múltiples flujos de ejecución de forma concurrente dentro de un mismo proceso. En Python, el módulo `threading` proporciona las herramientas para trabajar con hilos.

#### **Conceptos Clave de Threading**

1. **Concurrencia**: Múltiples tareas progresan durante el mismo período de tiempo
2. **Paralelismo**: Múltiples tareas se ejecutan literalmente al mismo tiempo (en múltiples CPUs)
3. **GIL (Global Interpreter Lock)**: En Python, solo un hilo puede ejecutar código Python a la vez, pero los hilos pueden "turnarse" tan rápidamente que parece simultáneo

#### **Clases Importantes del Módulo threading**

- **`Thread`**: Clase base para crear hilos personalizados
- **`Timer`**: Clase especializada de Thread que ejecuta una función después de un intervalo de tiempo
- **`Lock`**: Para sincronizar acceso a recursos compartidos
- **`Event`**: Para señalización entre hilos

---

## 🔧 ¿Cómo Funciona el Threading en Esta Aplicación?

### Uso de `threading.Timer`

En `backend_alarma.py`, usamos la clase `threading.Timer`:

```python
timer = threading.Timer(segundos, _disparar)
timer.start()
```

**¿Qué hace `threading.Timer`?**

1. **Creación**: `Timer(segundos, función)` crea un objeto Timer que:
   - Guardará internamente el tiempo de espera (segundos)
   - Guardará la función a ejecutar (_disparar)
   - Crea un nuevo hilo (thread) pero NO lo inicia aún

2. **Inicio**: `timer.start()` hace que:
   - El SO cree un nuevo hilo de ejecución
   - Ese hilo entre en estado de "espera" (sleep) por los segundos especificados
   - Durante la espera, el hilo está bloqueado y no consume CPU activamente
   - El SO usa su planificador para despertar el hilo cuando el tiempo expire

3. **Ejecución**: Cuando el tiempo expira:
   - El SO despierta el hilo
   - El hilo ejecuta la función _disparar()
   - Suena la alarma y se llama al callback
   - El hilo termina automáticamente

### Ventajas de Usar Timer en Esta Aplicación

- **No bloquea la interfaz**: El hilo principal continúa ejecutando la GUI mientras el Timer espera en segundo plano
- **Eficiencia**: El hilo en espera no consume CPU (el SO lo mantiene dormido)
- **Simplicidad**: No necesitamos crear un bucle que verifique constantemente el tiempo

---

## 🏗️ Arquitectura de la Aplicación

La aplicación está dividida en dos componentes principales:

### 1. **Frontend (alarma_gui.py)** - Hilo Principal
Maneja la interfaz gráfica y la interacción del usuario:
- Interfaz Tkinter (GUI)
- Entrada de tiempo (horas, minutos, segundos)
- Entrada de mensaje personalizado
- Visualización de cuenta regresiva
- Controles de pausa/reanudación

### 2. **Backend (backend_alarma.py)** - Hilo Secundario
Maneja la lógica de temporización:
- Función `iniciar_alarma()`: Crea y ejecuta el Timer
- Función `sonar_alarma()`: Emite sonido según el SO
- Función `_disparar()`: Se ejecuta cuando el Timer termina

---

## 📋 Funcionamiento Paso a Paso

### **Paso 1: Inicialización**
```
1. El usuario ejecuta alarma_gui.py
2. El SO crea un proceso Python
3. Se inicia el hilo principal que ejecuta:
   - Importación de módulos (tkinter, threading)
   - Creación de la ventana GUI
   - Inicialización de variables globales
   - Configuración de botones y controles
4. Se entra en el mainloop() de Tkinter
```

### **Paso 2: Configuración de la Alarma**
```
1. Usuario ingresa tiempo (ej: 00:05:00 - 5 minutos)
2. Usuario ingresa mensaje (opcional)
3. Usuario hace clic en "Activar alarma"
4. Se ejecuta la función activar_alarma():
   - Valida que el tiempo sea > 0
   - Calcula total_segundos (5*60 = 300 segundos)
   - Deshabilita el botón de activar
   - Actualiza el estado visual
```

### **Paso 3: Creación del Thread Timer**
```
1. Se llama a iniciar_alarma(300, mensaje, callback_backend)
2. En backend_alarma.py:
   - Se define la función interna _disparar()
   - Se crea: timer = threading.Timer(300, _disparar)
   - Se ejecuta: timer.start()
3. El SO crea un NUEVO HILO que:
   - Se pone en estado de "espera/sleep" por 300 segundos
   - No consume CPU mientras espera
   - El SO lo mantiene en su tabla de hilos
4. El thread principal (GUI) continúa ejecutándose sin bloquearse
```

### **Paso 4: Cuenta Regresiva Visual (Hilo Principal)**
```
1. En paralelo al Timer, el hilo principal ejecuta cuenta_regresiva()
2. Cada segundo (usando root.after(1000)):
   - Actualiza label_digital con el tiempo restante
   - Decrementa segundos_restantes
   - Re-programa la siguiente actualización
3. Esta cuenta regresiva es INDEPENDIENTE del Timer
4. Es solo visual para informar al usuario
```

**Diagrama de Estados:**
```
[Hilo Principal]              [Hilo Timer]
     |                              |
     |---> Crea Timer              |
     |                              |
     |---> timer.start() -------> [CREA HILO]
     |                              |
     |                         [SLEEP 300s]
     |                              |
[Actualiza GUI]                     |
[cada 1 segundo]                    |
     |                              |
     |                         [DESPIERTA]
     |                              |
     |<-- callback_backend() <-[EJECUTA _disparar()]
     |                              |
[Muestra mensaje]              [TERMINA]
```

### **Paso 5: Expiración del Timer**
```
1. Después de 300 segundos reales:
   - El SO despierta el hilo Timer
   - Se ejecuta la función _disparar()
   
2. _disparar() hace:
   a) Llama a sonar_alarma():
      - En Windows: usa winsound.Beep()
      - En Linux/Mac: imprime '\a' (beep de terminal)
   
   b) Llama a callback(mensaje):
      - Ejecuta callback_backend(mensaje)
      
3. callback_backend() usa root.after(0, ...):
   - Programa mostrar_mensaje() para ejecutarse en el hilo principal
   - IMPORTANTE: Tkinter NO es thread-safe, solo el hilo principal puede modificar la GUI
   
4. mostrar_mensaje() en el hilo principal:
   - Resetea variables globales
   - Actualiza el estado visual
   - Muestra messagebox con el mensaje
```

### **Paso 6: Funcionalidad de Pausa/Reanudación**
```
1. Usuario hace clic en el botón de Pausa (⏸️):
   - Se llama a alternar_pausa_play()
   - Se cancela el Timer actual: alarma_activa.cancel()
   - El hilo Timer se detiene antes de ejecutar _disparar()
   - Se guarda el tiempo restante en segundos_restantes
   - Se cambia el botón a Play (▶️)

2. Usuario hace clic en el botón de Play (▶️):
   - Se crea un NUEVO Timer con el tiempo restante
   - Se reinicia la cuenta regresiva visual
   - El nuevo hilo Timer comienza a esperar
```

---

## 🔄 Interacción Entre Hilos

### **Hilo Principal (Main Thread)**
- **Responsabilidades**:
  - Ejecutar el event loop de Tkinter (mainloop)
  - Procesar eventos de la GUI (clicks, teclado)
  - Actualizar la interfaz visual
  - Crear y cancelar Timers

- **Características**:
  - Es el único hilo que puede modificar widgets de Tkinter
  - Se mantiene siempre activo mientras la ventana esté abierta
  - Usa root.after() para programar tareas sin bloquear

### **Hilo Timer (Background Thread)**
- **Responsabilidades**:
  - Esperar el tiempo especificado
  - Ejecutar la función _disparar() al expirar
  - Emitir el sonido de alarma

- **Características**:
  - Se crea cada vez que se activa una alarma
  - Está en estado "sleep" la mayor parte del tiempo
  - NO puede modificar la GUI directamente
  - Usa callbacks para comunicarse con el hilo principal

### **Mecanismo de Comunicación Thread-Safe**

Para que el hilo Timer pueda notificar al hilo principal sin violar las reglas de Tkinter:

```python
def callback_backend(msg):
    root.after(0, mostrar_mensaje, msg)
```

- `root.after(0, función, args)`: Programa una función para ejecutarse en el hilo principal
- Esto es thread-safe porque after() es un mecanismo de Tkinter diseñado para comunicación entre hilos
- El mensaje pasa del hilo Timer → queue interna de Tkinter → hilo principal

---

## 🎯 Conceptos de Sistemas Operativos Aplicados

### 1. **Planificación de Procesos (Scheduling)**
- El SO usa su planificador para distribuir tiempo de CPU entre:
  - El hilo principal (GUI)
  - El hilo Timer (cuando está activo)
  - Otros procesos del sistema
  
### 2. **Estados de un Thread**
Los hilos en esta aplicación atraviesan diferentes estados:

```
NUEVO -> LISTO -> EJECUTANDO -> ESPERANDO -> EJECUTANDO -> TERMINADO
```

- **NUEVO**: El Timer fue creado pero no start()
- **LISTO**: Después de start(), esperando turno de CPU
- **EJECUTANDO**: Tiene CPU y está ejecutando código
- **ESPERANDO**: Durante sleep(), liberando CPU
- **TERMINADO**: Después de completar _disparar()

### 3. **Sincronización y Race Conditions**
- Esta aplicación evita race conditions porque:
  - Solo el hilo principal modifica la GUI
  - Las variables compartidas (alarma_activa, segundos_restantes) se acceden de forma controlada
  - Los callbacks garantizan que las actualizaciones ocurran en el hilo correcto

### 4. **Context Switching (Cambio de Contexto)**
- Cuando el SO cambia entre hilos:
  - Guarda el estado del hilo actual (registros, puntero de pila)
  - Carga el estado del siguiente hilo
  - Este proceso es transparente para el programador pero tiene un costo

### 5. **Llamadas al Sistema (System Calls)**
La aplicación usa varias syscalls implícitamente:
- `sleep()`: Para que el Timer espere
- `time()`: Para medir intervalos
- `winsound.Beep()`: Para generar sonido (acceso a hardware)
- GUI rendering: Para dibujar ventanas y widgets

---

## 🧪 Ejemplo de Flujo Temporal Completo

Supongamos que el usuario programa una alarma de **10 segundos**:

```
t=0s:   [Hilo Principal] Usuario hace clic en "Activar"
        [Hilo Principal] Crea Timer(10, _disparar)
        [Hilo Principal] Llama timer.start()
        [SO] Crea nuevo hilo Timer
        [Hilo Timer] Entra en sleep(10)
        [Hilo Principal] Inicia cuenta_regresiva()
        
t=1s:   [Hilo Principal] Actualiza GUI: "00:00:09"
        [Hilo Timer] Sigue durmiendo...
        
t=2s:   [Hilo Principal] Actualiza GUI: "00:00:08"
        [Hilo Timer] Sigue durmiendo...
        
...

t=9s:   [Hilo Principal] Actualiza GUI: "00:00:01"
        [Hilo Timer] Sigue durmiendo...
        
t=10s:  [Hilo Principal] Actualiza GUI: "00:00:00"
        [SO] Despierta al hilo Timer
        [Hilo Timer] Ejecuta _disparar()
        [Hilo Timer] Llama sonar_alarma() -> Beep!
        [Hilo Timer] Llama callback_backend(mensaje)
        [Hilo Timer] Programa mostrar_mensaje() en hilo principal
        [Hilo Timer] Termina y se destruye
        
t=10.1s: [Hilo Principal] Procesa evento de after()
         [Hilo Principal] Ejecuta mostrar_mensaje()
         [Hilo Principal] Muestra messagebox
         [Hilo Principal] Resetea estado
```

---

## 💡 Ventajas de Esta Arquitectura

1. **Responsividad**: La GUI nunca se congela porque el Timer no bloquea el hilo principal
2. **Precisión**: El SO maneja el tiempo de forma precisa usando sus propios temporizadores de hardware
3. **Eficiencia de Recursos**: El hilo Timer usa 0% CPU mientras está en sleep
4. **Simplicidad**: No necesitamos implementar nuestra propia lógica de temporización
5. **Escalabilidad**: Podemos tener múltiples alarmas simultáneas (múltiples Timers)

---

## 🔍 Comparación: Con Threading vs. Sin Threading

### **Sin Threading (Bloqueante)**
```python
# ESTO CONGELARÍA LA GUI ❌
def alarma_bloqueante(segundos):
    time.sleep(segundos)  # Bloquea el hilo principal
    messagebox.showinfo("Alarma", "Tiempo cumplido")
    # Durante el sleep, la GUI no responde a clicks
```

### **Con Threading (No Bloqueante) ✅**
```python
# La GUI permanece responsiva
def alarma_no_bloqueante(segundos):
    timer = threading.Timer(segundos, mostrar_mensaje)
    timer.start()  # Crea un hilo separado
    # El hilo principal continúa inmediatamente
```

---

## 📝 Resumen de Componentes Clave

| Componente | Ubicación | Hilo | Propósito |
|------------|-----------|------|-----------|
| Tkinter mainloop | alarma_gui.py | Principal | Event loop de la GUI |
| activar_alarma() | alarma_gui.py | Principal | Configurar y crear Timer |
| cuenta_regresiva() | alarma_gui.py | Principal | Actualizar display visual |
| threading.Timer | backend_alarma.py | Secundario | Esperar tiempo real |
| _disparar() | backend_alarma.py | Secundario | Ejecutar al expirar |
| callback_backend() | alarma_gui.py | Secundario | Puente hacia hilo principal |
| mostrar_mensaje() | alarma_gui.py | Principal | Actualizar GUI y mostrar alerta |

---

## 🎓 Conceptos Aprendidos

1. **Threading permite concurrencia sin bloquear la aplicación**
2. **Los hilos comparten memoria pero tienen flujos de ejecución independientes**
3. **El SO gestiona la planificación y cambio de contexto entre hilos**
4. **threading.Timer es ideal para tareas programadas en el tiempo**
5. **Las GUIs requieren que solo el hilo principal modifique widgets**
6. **Los callbacks permiten comunicación thread-safe entre hilos**
7. **El estado "sleep" de un hilo no consume CPU**

---

## 🚀 Posibles Mejoras Futuras

1. **Múltiples alarmas simultáneas**: Mantener una lista de Timers activos
2. **Persistencia**: Guardar alarmas en un archivo para restaurarlas al reiniciar
3. **Alarmas recurrentes**: Usar hilos con bucles para alarmas repetitivas
4. **Notificaciones del sistema**: Integrar con el centro de notificaciones del SO
5. **Sincronización con hora del reloj**: Programar alarmas para horas específicas del día

---

## 📚 Referencias y Recursos

- **Documentación oficial de threading**: https://docs.python.org/3/library/threading.html
- **Documentación de Tkinter**: https://docs.python.org/3/library/tkinter.html
- **Conceptos de Sistemas Operativos**: Procesos, Hilos, Planificación, Sincronización
