from django.shortcuts import render,get_object_or_404
#importamos modelos para asignarlos a index.html 
from .models import Categoria,Producto

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