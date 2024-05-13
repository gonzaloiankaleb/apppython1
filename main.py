from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Interfaz de usuario (tkinter)
root = Tk()
root.title("Aplicación CRUD con base de datos")
root.geometry("600x400")
# Variables globales 
miid = StringVar()
miNombre = StringVar()
miPuesto = StringVar()  
miSalario = StringVar()

# Conexión a la base de datos 
def conexionbbdd():
    miconexion = sqlite3.connect("base")
    miCursor = miconexion.cursor()
    try:
        miCursor.execute('''
            CREATE TABLE empleado(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE VARCHAR(50) NOT NULL,
                PUESTO VARCHAR(50) NOT NULL,
                SALARIO INTEGER NOT NULL
            )
        ''')
        messagebox.showinfo("CONEXION", "Base de datos creada con éxito")
    except:
        messagebox.showwarning("CONEXION", "La base de datos ya existe")

# Eliminar base de datos 
def eliminarbbdd():
    miconexion = sqlite3.connect("base")
    miCursor = miconexion.cursor()
    if messagebox.askyesno(message="¿Desea eliminar la base de datos? Los datos serán eliminados permanentemente", title="ADVERTENCIA"):
        miCursor.execute("DROP TABLE empleado")
    else:
        pass

def salirAplicacion():
    valor = messagebox.askquestion("SALIR", "¿Desea salir de la aplicación?")
    if valor == "yes":
        root.destroy()

def limpiarCampos():
    miid.set("")
    miNombre.set("")
    miPuesto.set("")  # Se limpia el campo de cargo
    miSalario.set("")

def mensaje():
    acerca = '''
        Aplicación CRUD con base de datos
        Versión 0.1
        Tecnología: Python, Tkinter, SQLite3
        credores: Gonzalo ,Milagros ,Rodrigo ,Elizabeth
        ISTITUTO SUPERIOR 240 V.DEL PINO
    '''
    messagebox.showinfo("info app", acerca)

# Método CRUD
def crear():
    miconexion = sqlite3.connect("base")
    miCursor = miconexion.cursor()
    try:
        datos = (miNombre.get(), miPuesto.get(), miSalario.get())  # Se incluyen los datos del cargo
        miCursor.execute("INSERT INTO empleado VALUES(NULL,?,?,?)", datos)
        miconexion.commit()
        messagebox.showinfo("CREAR", "Registro insertado con éxito")
    except:
        messagebox.showwarning("ADVERTENCIA", "No se pudo CREAR el registro, verifique CONEXION CON BASE DE DATOS")
    limpiarCampos()
    mostrar()

def mostrar():
    miConexion = sqlite3.connect("base")
    miCursor = miConexion.cursor()
    registros = tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
    try:
        miCursor.execute("SELECT * FROM empleado")
        for row in miCursor:
            tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3]))
    except:
        pass

# Crear tabla
tree = ttk.Treeview(height=10, columns=('#0', '#1', '#2', '#3'))
tree.place(x=0, y=130)
tree.column('#0', width=100)
tree.heading('#0', text="ID", anchor=CENTER)
tree.heading('#1', text="Nombre del empleado", anchor=CENTER)
tree.heading('#2', text="Cargo", anchor=CENTER)
tree.column('#3', width=100)
tree.heading('#3', text="Salario", anchor=CENTER)

def seleccionarUsandoClick(event):
    item = tree.identify('item', event.x, event.y)
    miid.set(tree.item(item, "text"))
    miNombre.set(tree.item(item, "values")[0])
    miPuesto.set(tree.item(item, "values")[1])
    miSalario.set(tree.item(item, "values")[2])
    
tree.bind('<Double-1>', seleccionarUsandoClick)



# Actualizar registro
def actualizar():
    miconexion = sqlite3.connect("base")
    miCursor = miconexion.cursor()
    try:
        datos = (miNombre.get(), miPuesto.get(), miSalario.get(), miid.get())  # Se incluyen los datos del cargo y el ID
        miCursor.execute("UPDATE empleado SET NOMBRE=?, Puesto=?, Salario=? where ID =?", datos)
        miconexion.commit()
        messagebox.showinfo("ACTUALIZAR", "Registro actualizado con éxito")
    except:
        messagebox.showwarning("ADVERTENCIA", "No se pudo ACTUALIZAR el registro, verifique CONEXION CON BASE DE DATOS")
    limpiarCampos()
    mostrar()
def eliminar():
    miconexion = sqlite3.connect("base")
    miCursor = miconexion.cursor()
    try:
        if messagebox.askyesno(message="¿Desea eliminar el registro?", title="ADVERTENCIA"):
            miCursor.execute("DELETE FROM empleado WHERE ID = ?", (miid.get(),))
        miconexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "No se pudo ELIMINAR el registro, verifique CONEXION CON BASE DE DATOS")
        pass
    limpiarCampos()
    mostrar()
    
####color widget en la ventana####
####menu####
menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(label="Conectar a base de datos", command=conexionbbdd)
menubasedat.add_command(label="elimnar base de datos", command=eliminarbbdd)
menubasedat.add_command(label="salir", command=salirAplicacion)
menubar.add_cascade(label="inicio", menu=menubasedat)

ayudamenu = Menu(menubar, tearoff=0)
ayudamenu.add_command(label="recetear campos", command=limpiarCampos)
ayudamenu.add_command(label="acerca de", command=mensaje)
menubar.add_cascade(label="ayuda", menu=ayudamenu)
#esta variable recolecta la informacion de las cajas de texto
e1 = Entry(root, textvariable=miid)

l2 = Label(root, text="Nombre")
l2.place(x=50, y=10)
e2 = Entry(root, textvariable=miNombre, width=50)
e2.place(x=100, y=10)

l3 = Label(root, text="cargo")
l3.place(x=50, y=40)
e3 = Entry(root, textvariable=miPuesto, width=50)
e3.place(x=100, y=40)

l4 = Label(root, text="salario")
l4.place(x=280, y=40)
e4 = Entry(root, textvariable=miSalario, width=10)
e4.place(x=320, y=40)

l5 = Label(root, text="USD")
l5.place(x=380, y=40)

####botones####
b1 = Button(root, text="crear registro", command=crear)
b1.place(x=50, y=90)

b2 = Button(root, text="modificar registro", command=actualizar)
b2.place(x=180, y=90)

b3 = Button(root, text="mostrar lista", command=mostrar)
b3.place(x=320, y=90)

b4 = Button(root, text="eliminar registro",bg="red", command=eliminar)
b4.place(x=450, y=90)






root.config(menu=menubar)

root.mainloop()

