from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    categoria = models.ForeignKey(Categoria,on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=200)
    descripcion= models.TextField(null=True)
    precio = models.DecimalField(max_digits=9,decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos',blank=True)
    
    def __str__(self):
        return self.nombre
   # Importamos de la propia libreria de django de modelos usuarios de auth
   #administra usuarios del sistema
from django.contrib.auth.models import User
#creamos clase Cliente
class Cliente(models.Model):
    #relacion 1 a 1 en OneToOne
    usuario = models.OneToOneField(User,on_delete=models.RESTRICT)
    dni = models.CharField(max_length=8)
    sexo = models.CharField(max_length=1,default='M')
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(null=True)
    direccion = models.TextField()
    #cuando se instancia solo retorna el dni por defecto
    def __str__(self):
        return self.dni
    #creamos Modelo Pedido cabecera
class Pedido(models.Model):
    #donde variable tendra 2 estados, con CHOICES tupla
    ESTADO_CHOICES = (
        ('0','Solicitado'),
        ('1','Pagado')
    )
    #creamos campos de este modelo del cliente por asi decirlo
    #el pedido esta ligado o enlazada con clase Cliente
    cliente = models.ForeignKey(Cliente,on_delete=models.RESTRICT)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    nro_pedido = models.CharField(max_length=20,null=True)
    monto_total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    estado = models.CharField(max_length=1,default='0',choices=ESTADO_CHOICES)
    #cuando se instancie pedido saldra el nro_pedido por defecto
    def __str__(self):
        return self.nro_pedido
    
    #creamos Modelo PedidoDetalle detalle de pedido
class PedidoDetalle(models.Model):
    #ponemos campos
    #Modelo Pedido esta relacionado con PedidoDetalle por eso foreign key
    #Igual con la clase Producto foreign key
    pedido = models.ForeignKey(Pedido,on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    cantidad = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)
     #cuando se instancie pedido saldra el nombre del producto
    def __str__(self):
        return self.producto.nombre