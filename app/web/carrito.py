#Tenemos una clase llamada cart
class Cart:
    #va a tener constructor init donde estara la variable sesion
    def __init__(self,request):
        self.request = request
        self.session = request.session
        #session get almacena lo de variable sesion llamada cart
        cart = self.session.get("cart")
        #Creamos nueva variable para montoTotal 
        montoTotal = self.session.get("cartMontoTotal")
        #Si no existe esta variable cart session y la cree
        #variable sesion llamada cart es la que usaremos
        if not cart:
            cart = self.session['cart'] = {}
            montoTotal = self.session['cartMontoTotal'] = "0"
    
        self.cart = cart
        self.montoTotal = float(montoTotal)
    
    #metodo agregar
    def add(self,producto,cantidad):
        #validamos con if si el producto.id o el producto NO
        #esta en la variable sessio entonces lo AGREGA
        if str(producto.id) not in self.cart.keys():
        #Asignamos a la variable session llamada cart
        #como clave tendra a producto.id servira para cantidad aumente
        #creamos valores id,nombre,cantidad viene de parametro,subtotal es calculado
        #str es para convertir a string
         self.cart[producto.id] = {
        "producto_id":producto.id,
        "nombre":producto.nombre,
        "cantidad":cantidad,
        "precio":str(producto.precio),
        "imagen":producto.imagen.url,
        "categoria":producto.categoria.nombre,
        "subtotal":str(cantidad * producto.precio)
            }
         #Si esta en la variable session el producto id
        else:
            #actualizamos el producto en el carrito, entonces aumenta la 
            #cantidad y el subtotal se calcula con la cantidad y precio
            #nuevo
            for key,value in self.cart.items():
                if key == str(producto.id):
                    value["cantidad"] = str(int(value["cantidad"]) + cantidad)
                    value["subtotal"] = str(float(value["cantidad"]) * float(value["precio"]))
                    break
        self.save()

    ##metodo eliminar
    def delete(self,producto):
        #creamos variable que almacena convertido a string el producto .id
       producto_id = str(producto.id)
       #validamos si existe
       if producto_id in self.cart:
           #eliminamos
            del self.cart[producto_id]
            self.save()
    #metodo limpiar carro
    def clear(self):
        #limpiar variable session llamada cart
        self.session["cart"] = {}
        self.session["cartMontoTotal"] = "0"
  
       #metodo que guarda los cambios que hara en carrito de compras
    def save(self):
         """ guarda cambios en el carrito de compras"""
         #creamos montoTotal en 0
         montoTotal = 0
        #recorremos en variable session llamada cart
        #chapamos subtotal de carrito.html y sumamos a montoTotal
         for key,value in self.cart.items():
            montoTotal += float(value["subtotal"])
         #asignamos a la session llamada cartMontoTotal el valor de montoTotal
         self.session["cartMontoTotal"] = montoTotal
         #aqui decimos que grabara todo lo que se haga a ala variable
         # session cart y que sea modificable
         self.session["cart"] = self.cart
         self.session.modified = True