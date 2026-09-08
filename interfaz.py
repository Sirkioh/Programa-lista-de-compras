import tkinter as tk
import programa

ventana = tk.Tk()

ventana.title("Lista de compras")
ventana.geometry("350x400")
ventana.configure(bg="#799833")

#titulo
titulo = tk.Frame(
    ventana,
    bg= "#4F7302",
    height=50,
    width=325,
    borderwidth=1,
    relief="solid"
)
titulo.pack_propagate(False)

tk.Label(
    titulo, 
    bg= "#4F7302", 
    text="Lista de compras",
    font= ("Segoe UI", 23, "bold"),
    fg= "#022601"
).pack(anchor="center")

titulo.pack()

#desarrollo
def crearFrame(padre):
    return tk.Frame(
    padre,
    bg= "#799833",
    height=60,
    width=300,
    )
    
def crearEntrada(padre):
    return tk.Entry(
        padre,
        bg="#799833",
        width=35,
        fg= "#022601",
        font= ("Segoe UI", 13, "bold"),
        justify="center"
    )
    
def crearTexto(padre, texto):
    tk.Label(
        padre,
        bg= "#799833",
        text=texto,
        font= ("Segoe UI", 13, "bold"),
        fg= "#022601"
    ).pack()

pedirCompras = tk.Frame(
    ventana,
    bg= "#799833",
    borderwidth= 1,
    relief="flat",
    height=150,
    width=300
)
pedirCompras.pack()

frameUno = crearFrame(pedirCompras)
frameUno.propagate(False)
frameUno.pack(pady=15)

frameDos = crearFrame(pedirCompras)
frameDos.propagate(False)
frameDos.pack()

crearTexto(frameUno, "Ingresa el producto deseado")
crearTexto(frameDos, "Ingresa la cantidad del producto")
entradaProducto = crearEntrada(frameUno)
entradaCantidad = crearEntrada(frameDos)

entradaProducto.pack(ipady=4)
entradaCantidad.pack(ipady=4)

guardarExcelFrame = tk.Frame(
    ventana,
    bg= "#4F7302",
    height=100,
    width=325,
    borderwidth=1,
    relief="solid"
    )
guardarExcelFrame.propagate(False)

tk.Label(
    guardarExcelFrame, 
    bg= "#4F7302", 
    text= "Guardar en Excel",
    font= ("Segoe UI", 15, "bold"),
    fg= "#022601"
).pack(anchor="center")

def botonGuardarExcelfun():
    if programa.compras == {}: return
    else:
        programa.crearExcel()
        return    
    
botonGuardarExcel = tk.Button(
    guardarExcelFrame,
    text="Guardar",
    command= botonGuardarExcelfun,
    borderwidth=1,
    width= 10,
    background="#799833",
    cursor="hand2",
    font= ("Segoe UI", 13, "bold"),
    fg= "#022601"
)
botonGuardarExcel.pack(pady=5)
guardarExcelFrame.pack(side="bottom")

opcionesComprasVentana = None
def crearVentanaOpciones(producto):
    global opcionesComprasVentana
    if opcionesComprasVentana is not None:
        if opcionesComprasVentana.winfo_exists():
            opcionesComprasVentana.lift()
            return
    
    opcionElegida = tk.StringVar()
    def devolverOpcionCompra(numero):
        opcionElegida.set(producto[numero])
        
    
    def crearOpcionCompra(numero, texto):
        return tk.Button(
            pedirOpcion,
            command=lambda numero=numero: devolverOpcionCompra(numero),
            text= texto,
            background="#799833",
            cursor="hand2",
            font= ("Segoe UI", 13, "bold"),
            borderwidth=0,
            fg= "#022601"
        )
    opcionesComprasVentana = tk.Toplevel(ventana)
    opcionesComprasVentana.title("Lista de compras")
    opcionesComprasVentana.geometry("400x550")
    opcionesComprasVentana.configure(bg="#799833")

    opcionesComprasTitulo = tk.Frame(
        opcionesComprasVentana,
        bg= "#4F7302",
        height=50,
        width=400,
        borderwidth=1,
        relief="solid"
    )
    opcionesComprasTitulo.pack_propagate(False)

    tk.Label(
        opcionesComprasTitulo, 
        bg= "#4F7302", 
        text="Elegir producto deseado",
        font= ("Segoe UI", 20, "bold"),
        fg= "#022601"
    ).pack(anchor="center")

    opcionesComprasTitulo.pack()

    pedirOpcion = tk.Frame(
        opcionesComprasVentana,
        bg= "#799833",
        borderwidth= 1,
        relief="solid",
        height=400,
        width=300
    )
    pedirOpcion.pack_propagate(False)
    pedirOpcion.pack(pady=25)

    
    for n,v in enumerate(producto):
        b = crearOpcionCompra(n, v)
        b.pack()
    
    opcionesComprasVentana.wait_variable(opcionElegida)
    
    opcionesComprasVentana.destroy()
    return opcionElegida.get()



def ObtenerDatosCompra():
    p = entradaProducto.get()
    q = entradaCantidad.get()
    if not p or not q: print("colocar valores")
    elif not q.isnumeric():
        print("cantidad no entero")
    else:
        opcionElegidaUsuario = None
        opciones, productos = programa.buscarProductos(p)
        opcionElegidaUsuario = crearVentanaOpciones(opciones)
        
        entradaCantidad.delete(0, tk.END)
        entradaProducto.delete(0, tk.END)

        programa.buscarPrecios(opcionElegidaUsuario, productos, q, p)
        

boton = tk.Button(
    pedirCompras,
    text="Enviar",
    command= ObtenerDatosCompra,
    borderwidth=1,
    width= 10,
    background="#799833",
    cursor="hand2",
    font= ("Segoe UI", 13, "bold"),
    fg= "#022601"
)
boton.pack(pady=5)

ventana.mainloop()