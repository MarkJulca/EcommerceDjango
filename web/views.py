from django.shortcuts import render,get_object_or_404,redirect
#importamos modelos para asignarlos a index.html 
from .models import Categoria,Producto,Cliente

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