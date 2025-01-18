from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
#importamos modelos para asignarlos a index.html 
from .models import Categoria,Producto,Cliente,Pedido,PedidoDetalle

# Create your views here.
""" VISTAS PARA EL CATALOGO DE PROUDCTOS """
def index(request):
    #Creamos listado y por medio de Producto accedemos a todos los productos con all
    listaProductos= Producto.objects.all()
    #print(listaProductos)
    #Creamos lista de categorias
    listaCategorias= Categoria.objects.all()

    #context es para diccionario un solo archivo a enviarlo como empaquetado
    context = {
        'productos':listaProductos,
        'categorias':listaCategorias
    }
    return render(request,'index.html',context)

#Creamos vista que tiene un parametro categoria_id
def productosPorCategoria(request,categoria_id):
    """ vista para filtrar productos por categoria """
    #pk es primary key sera igual al parametro que le ponemos en productosPorCategoria
    objCategoria = Categoria.objects.get(pk=categoria_id)
    #Esto nos trae listado de productos pertenecientes a esa categoria
    listaProductos = objCategoria.producto_set.all()
    
    listaCategorias = Categoria.objects.all()
    
    context = {
        'categorias':listaCategorias,
        'productos':listaProductos
    }
    
    return render(request,'index.html',context)
#Creamos vista para usarlo en el buscador 
def productosPorNombre(request):
    """ vista para filtrado de productos por nombre """
    #variable nombre capturara la informacion enviada desde el formulario llamado nombre
    nombre = request.POST['nombre']
    #listadoProductos donde es filtrado por ese valor nombre creado anteriormente
    listaProductos = Producto.objects.filter(nombre__contains=nombre)
    listaCategorias = Categoria.objects.all()
    
    context = {
        'categorias':listaCategorias,
        'productos':listaProductos
    }
    
    return render(request,'index.html',context)
    #Creamos vista para el detalle que tiene de parametro el producto id
def productoDetalle(request,producto_id):
    """ vista para el detalle de producto"""
    
   # objProducto = Producto.objects.get(pk=producto_id)
    objProducto = get_object_or_404(Producto,pk=producto_id)
    context = {
        'producto':objProducto
    }
    
    return render(request,'producto.html',context)

"""VISTAS PARA EL CARRITO DE COMPRAS """
#Importamos de carrito .py el cart
from .carrito import Cart

#Creamos vista que llamara a carrito.html
def carrito(request):
    return render(request,'carrito.html')

##metodo vista agregar carrito con parametro producto_id
def agregarCarrito(request,producto_id):
    #Por metodo POST chapara del name del input llamado cantidad
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    #caso contrario es 1
    else:
        cantidad = 1
#obtenemos producto en base al producto_id
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
#en la variable carritoProducto agregamos el producto y la cantidad
    carritoProducto.add(objProducto,cantidad)
#Imprimir en consola lo que tiene la variable cart
    #print(request.session.get("cart"))
    #si el metodo que estamos esperando es GET
    #que nos retorne a la pagina principal con /
    if request.method == 'GET':
        return redirect('/')
    return render(request,'carrito.html')
#Vista eliminar que tiene parametro producto_id
def eliminarProductoCarrito(request,producto_id):
    #obtenemos productos
    objProducto = Producto.objects.get(pk=producto_id)
    #creamos instancia de Cart
    carritoProducto = Cart(request)
    #Luego ponemos delete que viene de carrito.py, pasandolñe el objecto
    carritoProducto.delete(objProducto)
    #direccionamos a carrito.html
    return render(request,'carrito.html')
#vista de limpiarCarrito limpia todos los productos
def limpiarCarrito(request):
    #metodo llamado clear de carrito.py
    carritoProducto = Cart(request)
    carritoProducto.clear()
    #enviamos a esta vista
    return render(request,'carrito.html')

""" VISTAS PARA CLIENTES Y USUARIOS """
#IMPORTAMOS librerias
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
#decorators es agrega funcionalidad  a otra usaremos login required
#para ver si usuario esta logueado o no esta , le redirige a pagina segun
# el caso
from django.contrib.auth.decorators import login_required

from .forms import ClienteForm
#creamos vista que crea Usuario y redirecciona a login.html
def crearUsuario(request):
    #Al darle al input con submit de login html crearCuenta activa el action
    #redirecciona aqui por metodo post y chapa los name de las cajas
    #validamos y almacenamos en variable  dataUsuario dataPassword
    if request.method == 'POST':
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']
        #usamos el create_user de la libreria User y pasamos dataUsuario y  dataPassword
        nuevoUsuario = User.objects.create_user(username=dataUsuario,password=dataPassword)
        #validamos si no es vacio entonces LOGUEA
        if nuevoUsuario is not None:
            #lleve a login metodo de User con nuevoUsuario pasando de parametro
            login(request,nuevoUsuario)
            #redirecciona a cuenta
            return redirect('/cuenta')

    return render(request,'login.html')


   #creamos vista para loginUsuario 
def loginUsuario(request):
    #variable que chapa en el GET en URL si es next
    #el next indica a la pagina que luego debe ir 
    paginaDestino = request.GET.get('next',None)
     #creamos context vacio 
    context = {
        #variable destino lo asignamos a paginaDestino
        'destino':paginaDestino
    }
    #validamos si request es POST
    if request.method == 'POST':
        #q coja de los name de las cajas de login.html
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']
        #usamos lo de importar el authenticate
        usuarioAuth = authenticate(request,username=dataUsuario,password=dataPassword)
        #validamos que exista que no sea vacio
        if usuarioAuth is not None:
            #loguea
            login(request,usuarioAuth)
            #validamos si dataDestino es diferente de vacio
            if dataDestino != 'None':
                #entonces redirecciona a dataDestino
                return redirect(dataDestino)
            #redirige
            return redirect('/cuenta')
        #si es vacio en context mandamos error
        else:
            context = {
                'mensajeError':'Datos incorrectos'
            }    
    
    return render(request,'login.html',context)    
    ##salida de logout usuario
def logoutUsuario(request):
    logout(request)
    #cuando cierre session le redirige a login
    return render(request,'login.html')
    
def cuentaUsuario(request):
    #ponemos try except
    try:
        #variable almacena lo del modelo Cliente  donde usuario es igual 
        #a request.user lo igualamos con campo del modelo Cliente de usuario
        clienteEditar = Cliente.objects.get(usuario = request.user)
        #donde user es de la BD con tabla auth_user campos first_name,last_name...
        #y de clienteEditar sacamos direccion,telefono,dni,sxo,fecha_nacimiento
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            'direccion':clienteEditar.direccion,
            'telefono':clienteEditar.telefono,
            'dni':clienteEditar.dni,
            'sexo':clienteEditar.sexo,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento
        }
        #caso contrario a dataCliente seteamos con los valores de user
        #solo esos datos del usuario
    except:
         dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email
         }
    #a frmCliente le pasamos el parametro dataCliente al ClientForm
    #para que traiga la data rellenada cuando se LOGUEA
    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente':frmCliente
    }
    
    return render(request,'cuenta.html',context)
    
    
    #vista actualizarCliente,registrara al cliente que acaba de crear
def actualizarCliente(request):
    mensaje = ""
    
    if request.method == "POST":
        #todo lo que envia por POST se asigna a la clase Cliente
        frmCliente = ClienteForm(request.POST)
        #valida con is valid todos los campos
        if frmCliente.is_valid():
            #prepara la data para que se guarde en la BD con clenaeddata
            dataCliente = frmCliente.cleaned_data
            
            #actualizar usuario,ya ha sido creado en el registro por correo
            #le pondremos nombres,apellidos y email actualizando por user.id
            #actUsuario tiene la data con get del que se logueo
            actUsuario = User.objects.get(pk=request.user.id)
            #nombre,apellidos,email viene de forms.py de la clase ClienteForm
            actUsuario.first_name = dataCliente["nombre"]
            actUsuario.last_name = dataCliente["apellidos"]
            actUsuario.email = dataCliente["email"]
            #actualiza o guarda el save
            actUsuario.save()
            
            #registrar Cliente,iran los campos direccion
            # dni,direccion,telefono,sexo y fecha nacimiento en cliente
            #creamos objeto de la clase Cliente de models.py
            nuevoCliente = Cliente()
            #seteamos
            nuevoCliente.usuario = actUsuario
            nuevoCliente.dni = dataCliente["dni"]
            nuevoCliente.direccion = dataCliente["direccion"]
            nuevoCliente.telefono = dataCliente["telefono"]
            nuevoCliente.sexo = dataCliente["sexo"]
            nuevoCliente.fecha_nacimiento = dataCliente["fecha_nacimiento"]
            #actualiza o guarda el save
            nuevoCliente.save()
            
            mensaje = "Datos Actualizados"
            #retorna mensaje y al frmCliente
    context ={
        'mensaje':mensaje,
        'frmCliente':frmCliente
    }
            
    
    return render(request,'cuenta.html',context)



""" VISTAS PARA PROCESO DE COMPRA """
#PRUEBA PAYPAL
def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        #correo de business ponemos el que tenemos
        #notify url notifica a paypal
        #return redirecciona a / osea principal
        #si cancela va a logout
        "business": "sb-zw3bu37035416@business.example.com",
        "amount": "100.00",
        "item_name": "producto de prueba edteam",
        "invoice": "100-ED100",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri('/'),
        "cancel_return": request.build_absolute_uri('/logout'),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)

#usando decorators con login_url 
# redirecciona en este caso a /login de urls py
#si es que no esta logueado
@login_required(login_url='/login')
def registrarPedido(request):
    
    #ponemos try except
    try:
        #variable almacena lo del modelo Cliente  donde usuario es igual 
        #a request.user lo igualamos con campo del modelo Cliente de usuario
        clienteEditar = Cliente.objects.get(usuario = request.user)
        #donde user es de la BD con tabla auth_user campos first_name,last_name...
        #y de clienteEditar sacamos direccion,telefono,dni,sxo,fecha_nacimiento
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            'direccion':clienteEditar.direccion,
            'telefono':clienteEditar.telefono,
            'dni':clienteEditar.dni,
            'sexo':clienteEditar.sexo,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento
        }
        #caso contrario a dataCliente seteamos con los valores de user
        #solo esos datos del usuario
    except:
         dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email
         }
    #a frmCliente le pasamos el parametro dataCliente al ClientForm
    #para que traiga la data rellenada cuando se LOGUEA
    
    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente':frmCliente
    }
    
    return render(request,'pedido.html',context)
#prueba de paypal
from paypal.standard.forms import PayPalPaymentsForm

#que vaya a login si no esta logueado
@login_required(login_url='/login')
def confirmarPedido(request):
    context = {}
    #verificar que haya sido enviado por metodo POST
    if request.method == "POST":
         #actualizamos datos de usuario
         #a partir de User sacamos la data
        actUsuario = User.objects.get(pk=request.user.id)
        #viene de name de pedido.html ese nombre y apellidos
        actUsuario.first_name = request.POST['nombre']
        actUsuario.last_name = request.POST['apellidos']
        #grabamos
        actUsuario.save()
    #registramos o actualizamos cliente
    #try validar que del modelo Cliente buscamos por usuario
    # aca actualiza si existe
        try:
            clientePedido = Cliente.objects.get(usuario=request.user)
             #viene de name de pedido.html ese telefono y direccion
            clientePedido.telefono = request.POST['telefono']
            clientePedido.direccion = request.POST['direccion']
              #grabamos
            clientePedido.save()
            # aca agrega si no existe
            #en caso no tenga creado o no exista creamos nuevo
        except:
            clientePedido = Cliente()
            clientePedido.usuario = actUsuario
            clientePedido.direccion = request.POST['direccion']
            clientePedido.telefono = request.POST['telefono']
            clientePedido.save()   
        #registramos nuevo pedido con estas variables
        nroPedido = ''
        #viene de esta linea de pedido.html  la variable session   
        # <p class="cart-totals-val">$ request.session.cartMontoTotal </p>
        montoTotal = float(request.session.get('cartMontoTotal'))
        #instanciamos en variable nuevoPedido
        nuevoPedido = Pedido()
        # y le pasamos el cliente de arriba
        nuevoPedido.cliente = clientePedido
        #guardamos
        nuevoPedido.save()
        
        #registramos el detalle del pedido
        #chapamos lo de la session llamada cart
        #todo lo que esta en value esta en carrito de compras 
        carritoPedido = request.session.get('cart')
        for key,value in carritoPedido.items():
            productoPedido = Producto.objects.get(pk=value['producto_id'])
            detalle = PedidoDetalle()
            detalle.pedido = nuevoPedido
            detalle.producto = productoPedido
            detalle.cantidad = int(value['cantidad'])
            detalle.subtotal = float(value['subtotal'])
            #registra pedido
            detalle.save()
         #actualizar pedido, damos formato de PED + con strftime string la fecha y solo
         #chapamos el año osea %Y + el id
        nroPedido = 'PED' + nuevoPedido.fecha_registro.strftime('%Y') + str(nuevoPedido.id)
        #asignamos el nroPedido
        nuevoPedido.nro_pedido = nroPedido
        #analogamente el montoTotal
        nuevoPedido.monto_total = montoTotal
        #grabamos
        nuevoPedido.save()
         #registramos el id del pedido en la sesión
        request.session['pedidoId'] = nuevoPedido.id
        
        #Creamos boton de paypal
        #cuando pague ira a una pagina "gracias" 
        #el cancelar nos llevara a principal
        #le pasamos valores y en business copiamos de block de notas
        #el que generamos para pruebas 
        paypal_dict = {
        "business": "sb-zw3bu37035416@business.example.com",
        "amount": montoTotal,
        "item_name": "PEDIDO CODIGO : "+ nroPedido,
        "invoice": nroPedido,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri('/gracias'),
        "cancel_return": request.build_absolute_uri('/')
        }

        # Create the instance.
        formPaypal = PayPalPaymentsForm(initial=paypal_dict)
        
        
        context = {
            #por medio de pedido en compra.html asignaremos valores
            'pedido':nuevoPedido,
            'formPaypal':formPaypal
        }
         #limpiamos carrito de compras
        carrito = Cart(request)
        carrito.clear()
 
    return render(request,'compra.html',context)
#para envio a correo
from django.core.mail import send_mail
#VISTA GRACIAS
#necesita estar logueado si no no aparece vista de gracias
@login_required(login_url='/login')
def gracias(request):
    #validamos que el PayerID que nos da paypal cuando
    #pagamos en URL lo obtenemos
    paypalId = request.GET.get('PayerID',None)
    context = {}
    #validamos que si no es vacio entonces
    if paypalId is not None:
        #cogemos la session pedidoId
        pedidoId = request.session.get('pedidoId')
        pedido = Pedido.objects.get(pk=pedidoId)
        pedido.estado = '1'
        pedido.save()
            #envio de correo
            #en el request.user.email es para el usuario a su email
            #adicional puedes enviar a otros correos como cesarmay...
            #lo enviara de maikiwolfsj@gmail.com
        send_mail(
                'Gracias por tu compra',
                'tu nro de pedido es ' + pedido.nro_pedido,
                'maikiwolfsj@gmail.com',
                [request.user.email],
                fail_silently=False,
            )
        
        context = {
            'pedido' : pedido
        }
    else:   
        return redirect('/')
    return render(request,'gracias.html',context)