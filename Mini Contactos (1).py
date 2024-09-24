import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

empleados = []

# función para validar solo números
def solo_numeros(char):
    return char.isdigit()

# ventana principal
ventana = tk.Tk()
ventana.title("Base de Datos - Empresa S.A.")
ventana.geometry("700x500")
ventana.configure(bg="#1f2937")  # Fondo más oscuro para contraste

# Estilo de ttk
estilo = ttk.Style()
estilo.theme_use("clam")

# Estilo general
estilo.configure("TLabel", background="#1f2937", foreground="#f0f0f0", font=("Roboto", 12))
estilo.configure("TButton", background="#3b82f6", foreground="#ffffff", font=("Roboto", 12, "bold"), padding=8)
estilo.map("TButton", background=[("active", "#2563eb")])
estilo.configure("TEntry", font=("Roboto", 12), padding=5, borderwidth=2, relief="flat", foreground="#111827", background="#f0f0f0")
estilo.configure("TFrame", background="#1f2937")

# Sombras en botones y lista
ventana.option_add("*TButton.highlightBackground", "#000")
ventana.option_add("*TButton.highlightThickness", 2)
ventana.option_add("*TButton.highlightColor", "#111827")

# Registro para validar entradas numéricas
validate_numeros = ventana.register(solo_numeros)

# ventana secundaria para búsqueda
def abrir_ventana_secundaria():
    ventana_secundaria = tk.Toplevel()
    ventana_secundaria.title("Lista de Empleados")
    ventana_secundaria.geometry("300x200")
    ventana_secundaria.configure(bg="#1f2937")
    
    frame_secundario = ttk.Frame(ventana_secundaria)
    frame_secundario.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    ttk.Label(frame_secundario, text="Buscar por:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    
    entrada_buscar_dato = ttk.Entry(frame_secundario)
    entrada_buscar_dato.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    ttk.Button(frame_secundario, text="Buscar", command=lambda: buscar_por_dato(entrada_buscar_dato)).grid(row=2, column=1, padx=10, pady=5, sticky="ew")

# función para agregar empleado
def agregar_empleado(): 
    nombre, apellido, documento, direccion, legajo, cargo = (entrada_nombre.get(), entrada_apellido.get(), 
                                                              entrada_documento.get(), entrada_direccion.get(), 
                                                              entrada_legajo.get(), entrada_cargo.get())

    if all([nombre, apellido, documento, direccion, legajo, cargo]):
        empleados.append((nombre, apellido, documento, direccion, legajo, cargo))
        limpiar_entradas()
        messagebox.showinfo("Agregar Empleado", "Empleado agregado exitosamente")
        actualizar_lista_empleados()  # actualizar inmediatamente
    else:
        messagebox.showwarning("Agregar Empleado", "Todos los campos deben estar completos")

# función para modificar empleado
def modificar_empleado():
    seleccion = lista_empleados.curselection()
    if not seleccion:
        messagebox.showwarning("Modificar Empleado", "Debe seleccionar un empleado para modificar")
        return
    
    index = seleccion[0]
    empleado = empleados[index]

    # Crear diccionario para modificar campos fácilmente
    campos = ["Nombre", "Apellido", "Documento", "Dirección", "Legajo", "Cargo"]
    nuevo_empleado = []
    for i, campo in enumerate(campos):
        valor = simpledialog.askstring(f"Modificar {campo}", f"Nuevo {campo.lower()} para {empleado[i]}:", initialvalue=empleado[i])
        if valor: nuevo_empleado.append(valor)
        else: return

    empleados[index] = tuple(nuevo_empleado)
    actualizar_lista_empleados()
    messagebox.showinfo("Modificar Empleado", "Empleado modificado exitosamente")

# función para eliminar empleado
def eliminar_empleado():
    seleccion = lista_empleados.curselection()
    if seleccion:
        nombre = lista_empleados.get(seleccion[0])
        if messagebox.askyesno("Confirmar Eliminación", f"¿Deseas eliminar al empleado {nombre}?"):
            empleados.pop(seleccion[0])
            actualizar_lista_empleados()
            messagebox.showinfo("Eliminar Empleado", "Empleado eliminado exitosamente")
    else:
        messagebox.showwarning("Eliminar Empleado", "Debe seleccionar un empleado para eliminar")

# función para actualizar la lista de empleados
def actualizar_lista_empleados():
    lista_empleados.delete(0, tk.END)
    for empleado in empleados:
        lista_empleados.insert(tk.END, empleado[0])

# función para buscar por dato
def buscar_por_dato(entrada_buscar_dato):
    dato = entrada_buscar_dato.get().lower()
    if dato:
        empleados_filtrados = [empleado for empleado in empleados if any(dato in campo.lower() for campo in empleado)]
        lista_empleados.delete(0, tk.END)
        for empleado in empleados_filtrados:
            lista_empleados.insert(tk.END, f"Nombre: {empleado[0]}, Apellido: {empleado[1]}, Documento: {empleado[2]}, Dirección: {empleado[3]}, Legajo: {empleado[4]}, Cargo: {empleado[5]}")
    else:
        messagebox.showwarning("Buscar por", "Debe ingresar dato para la búsqueda")

# función para limpiar campos de entrada
def limpiar_entradas():
    for entrada in [entrada_nombre, entrada_apellido, entrada_documento, entrada_direccion, entrada_legajo, entrada_cargo]:
        entrada.delete(0, tk.END)

# interfaz principal
frame_principal = ttk.Frame(ventana)
frame_principal.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

# lista para mostrar empleados
lista_empleados = tk.Listbox(ventana, width=80, height=10, bg="#111827", fg="#f0f0f0", font=("Roboto", 12), borderwidth=2, relief="flat", selectbackground="#3b82f6")
lista_empleados.grid(row=0, column=0, padx=20, pady=20, columnspan=3, sticky="nsew")

# campos de entrada
entrada_nombre = ttk.Entry(frame_principal)
entrada_apellido = ttk.Entry(frame_principal)
entrada_documento = ttk.Entry(frame_principal, validate="key", validatecommand=(validate_numeros, '%S'))
entrada_direccion = ttk.Entry(frame_principal)
entrada_legajo = ttk.Entry(frame_principal, validate="key", validatecommand=(validate_numeros, '%S'))
entrada_cargo = ttk.Entry(frame_principal)

# etiquetas y entradas organizadas
etiquetas_campos = [("Nombre:", entrada_nombre), ("Apellido:", entrada_apellido), ("Documento:", entrada_documento), 
                    ("Dirección:", entrada_direccion), ("Legajo:", entrada_legajo), ("Cargo:", entrada_cargo)]

for i, (texto, entrada) in enumerate(etiquetas_campos):
    ttk.Label(frame_principal, text=texto).grid(row=i, column=0, padx=10, pady=5, sticky="e")
    entrada.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

# botones
frame_botones = ttk.Frame(ventana)
frame_botones.grid(row=1, column=2, padx=20, pady=20, sticky="ns")

botones_acciones = [("Agregar Empleado", agregar_empleado), ("Modificar Empleado", modificar_empleado), 
                    ("Eliminar Empleado", eliminar_empleado), ("Ver Lista de Empleados", abrir_ventana_secundaria)]

for texto, comando in botones_acciones:
    ttk.Button(frame_botones, text=texto, command=comando).pack(pady=10, fill="x")

ventana.mainloop()
