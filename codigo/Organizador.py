import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def organizar_escritorio():
    desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    files = os.listdir(desktop_path)

    al_menos_una_condicion = False
    archivos_movidos = {ruta.get(): 0 for ruta in rutas}

    total_archivos = sum(1 for file in files if os.path.isfile(os.path.join(desktop_path, file)))

    for file in files:
        if os.path.isfile(os.path.join(desktop_path, file)):
            for i in range(6):
                if texto_condiciones[i].get().strip() != "":
                    al_menos_una_condicion = True
                    if file.startswith(texto_condiciones[i].get()):
                        destination_folder = rutas[i].get()
                        shutil.move(os.path.join(desktop_path, file), os.path.join(destination_folder, file))
                        archivos_movidos[destination_folder] += 1
                        break

    if not al_menos_una_condicion:
        messagebox.showerror("Error", "Por favor, ingrese al menos un texto de condición.")

    for ruta, cantidad in archivos_movidos.items():
        if cantidad > 0:
            messagebox.showinfo("Proceso Finalizado", f"Se movieron {cantidad} archivo(s) a la ruta: {ruta}")

    finalizar_aplicacion()

def finalizar_aplicacion():
    # Guardar los textos de condición y rutas en un archivo de texto
    with open("config.txt", "w") as file:
        for i in range(6):
            file.write(f"{texto_condiciones[i].get()},{rutas[i].get()}\n")

    root.destroy()

def seleccionar_ruta(index):
    ruta = filedialog.askdirectory()
    rutas[index].set(ruta)

root = tk.Tk()
root.title("Organizador de Escritorio")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

texto_condiciones = []
rutas = []

# Cargar los textos de condición y rutas desde el archivo de configuración si existe
if os.path.exists("config.txt"):
    with open("config.txt", "r") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if i < 6:
                texto, ruta = line.strip().split(",")
                texto_condicion = tk.StringVar(value=texto)
                texto_condiciones.append(texto_condicion)
                ruta_var = tk.StringVar(value=ruta)
                rutas.append(ruta_var)
            else:
                break
else:
    # Si no existe el archivo de configuración, inicializamos los textos de condición y rutas
    for i in range(6):
        texto_condicion = tk.StringVar()
        texto_condiciones.append(texto_condicion)
        ruta = tk.StringVar()
        rutas.append(ruta)

for i in range(6):
    label_condicion = tk.Label(frame, text=f"Los archivos cuyo nombre inicie con:")
    label_condicion.grid(row=i, column=0, padx=5, pady=5)

    texto_condicion_entry = tk.Entry(frame, textvariable=texto_condiciones[i])
    texto_condicion_entry.grid(row=i, column=1, padx=5, pady=5)

    label_ruta = tk.Label(frame, text=f"se moverán a la ruta:")
    label_ruta.grid(row=i, column=2, padx=5, pady=5)

    ruta_entry = tk.Entry(frame, textvariable=rutas[i])
    ruta_entry.grid(row=i, column=3, padx=5, pady=5)

    button_seleccionar_ruta = tk.Button(frame, text="Seleccionar Ruta", command=lambda i=i: seleccionar_ruta(i))
    button_seleccionar_ruta.grid(row=i, column=4, padx=5, pady=5)

organizar_button = tk.Button(frame, text="Organizar Escritorio", command=organizar_escritorio)
organizar_button.grid(row=6, columnspan=5, pady=10)

finalizar_button = tk.Button(frame, text="Finalizar", command=finalizar_aplicacion)
finalizar_button.grid(row=7, columnspan=5, pady=10)

root.mainloop()
