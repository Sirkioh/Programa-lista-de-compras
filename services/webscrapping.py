import requests
import re
import json


class ws:
    def __init__(self, xl):
        self.xl = xl
        
    @staticmethod
    def buscarProductos(producto): 
        parametros = {"q": producto,"page": 1,"limit": 24}

        respuestaBusqueda = requests.get("https://ahorroposadas.com/api/search", params=parametros, verify=False)
        datosBusqueda = respuestaBusqueda.json()
        productos = datosBusqueda["products"]
        
        productosNombres = {}
        for p in productos:
            productosNombres[p["normalizedName"]] = p["relevanceScore"]
        
        prodcutosMayoresScore = sorted(productosNombres, key=productosNombres.get, reverse=True)[:10]
        return [prodcutosMayoresScore, productos]

    def buscarPrecios(self, productoElegido, productos, cantidad, producto):
        for p in productos:
            if p["normalizedName"] == productoElegido:
                productoCategoria = p["category"]
                break
        
        datosProducto = requests.get(f"https://ahorroposadas.com/producto/{productoElegido}", verify=False).text
        match = re.search(r'const products = (\[.*?\]);', datosProducto, re.DOTALL)
        
        products = json.loads(match.group(1))
        datosProducto = {
            "precios" : {},
            "nombreNormalizado" : productoElegido,
            "categoria" : productoCategoria
        }
        for p in products:
            datosProducto["precios"][p["supermarket"]] = p["price"]
        

        self.xl.compras[producto] = {"cantidad": int(cantidad)}
        self.xl.compras[producto].update(datosProducto)