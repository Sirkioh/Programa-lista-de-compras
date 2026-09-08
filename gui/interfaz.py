import tkinter as tk

class gui:
    def __init__(self, excel, webscrapping):
        self.ventana = tk.Tk()
        self.ventana.title("Lista de compras")
        self.ventana.geometry("350x400")
        self.ventana.configure(bg="#799833")
        self.excel = excel
        self.ws = webscrapping
        self.opcionesComprasVentana = None
        self.pedirCompras = tk.Frame(
            self.ventana,
            bg= "#799833",
            borderwidth= 1,
            relief="flat",
            height=150,
            width=300
        )
        self.frameUno = self.crearFrame(self.pedirCompras)
        self.frameUno.propagate(False)
        self.frameDos = self.crearFrame(self.pedirCompras)
        self.frameDos.propagate(False)
        self.entradaProducto = self.crearEntrada(self.frameUno)
        self.entradaCantidad = self.crearEntrada(self.frameDos)

        self.titulo = tk.Frame(
            self.ventana,
            bg= "#4F7302",
            height=50,
            width=325,
            borderwidth=1,
            relief="solid"
        )
        
        self.titulo.pack_propagate(False)

    @staticmethod
    def crearFrame(padre):
        return tk.Frame(
        padre,
        bg= "#799833",
        height=60,
        width=300,
        )
    
    @staticmethod
    def crearEntrada(padre):
        return tk.Entry(
            padre,
            bg="#799833",
            width=35,
            fg= "#022601",
            font= ("Segoe UI", 13, "bold"),
            justify="center"
        )
    
    @staticmethod   
    def crearTexto(padre, texto):
        return tk.Label(
            padre,
            bg= "#799833",
            text=texto,
            font= ("Segoe UI", 13, "bold"),
            fg= "#022601"
        )

    
    def configurar(self):
        tk.Label(
            self.titulo, 
            bg= "#4F7302", 
            text="Lista de compras",
            font= ("Segoe UI", 23, "bold"),
            fg= "#022601"
        ).pack(anchor="center")
        self.titulo.pack()

        self.pedirCompras.pack()

        self.frameUno.pack(pady=15)
        self.frameDos.pack()

        self.crearTexto(self.frameUno, "Ingresa el producto deseado").pack()
        self.crearTexto(self.frameDos, "Ingresa la cantidad del producto").pack()

        self.entradaProducto.pack(ipady=4)
        self.entradaCantidad.pack(ipady=4)

        guardarExcelFrame = tk.Frame(
            self.ventana,
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
            if self.excel.compras == {}: return
            else:
                self.excel.crearExcel()
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
        
        boton = tk.Button(
            self.pedirCompras,
            text="Enviar",
            command= self.ObtenerDatosCompra,
            borderwidth=1,
            width= 10,
            background="#799833",
            cursor="hand2",
            font= ("Segoe UI", 13, "bold"),
            fg= "#022601"
        )
        boton.pack(pady=5)

    def crearVentanaOpciones(self, producto):
        if self.opcionesComprasVentana is not None:
            if self.opcionesComprasVentana.winfo_exists():
                self.opcionesComprasVentana.lift()
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
        self.opcionesComprasVentana = tk.Toplevel(self.ventana)
        self.opcionesComprasVentana.title("Lista de compras")
        self.opcionesComprasVentana.geometry("400x550")
        self.opcionesComprasVentana.configure(bg="#799833")

        opcionesComprasTitulo = tk.Frame(
            self.opcionesComprasVentana,
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
            self.opcionesComprasVentana,
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
        
        self.opcionesComprasVentana.wait_variable(opcionElegida)
        
        self.opcionesComprasVentana.destroy()
        return opcionElegida.get()


    def ObtenerDatosCompra(self):
        p = self.entradaProducto.get()
        q = self.entradaCantidad.get()
        if not p or not q: print("colocar valores")
        elif not q.isnumeric():
            print("cantidad no entero")
        else:
            opcionElegidaUsuario = None
            opciones, productos = self.ws.buscarProductos(p)
            opcionElegidaUsuario = self.crearVentanaOpciones(opciones)
            
            self.entradaCantidad.delete(0, tk.END)
            self.entradaProducto.delete(0, tk.END)

            self.ws.buscarPrecios(opcionElegidaUsuario, productos, q, p)

    def main(self):
        self.configurar()
        self.ventana.mainloop()