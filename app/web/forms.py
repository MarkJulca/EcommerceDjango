#Importamos de libreria de django forms donde convierte 
# esto que parece modelo pero lo convierte a HTML con forms
#tiene validaciones por defecto que sirven
from django import forms
#creamos esta clase que dara formato de date para usarlo en fecha_nacimiento 
#que salga un calendario
class DateInput(forms.DateInput):
    input_type='date'
#creamos clase que representa a formulario
class ClienteForm(forms.Form):
    #asignamos un CHOICE tupla para usarlo en campo sexo de abao
    SEXO_CHOICES = (
        ('M','Masculino'),
        ('F','Femenino')
    )
    #demas campos
    dni = forms.CharField(label='DNI',max_length=8)
    nombre = forms.CharField(label='Nombres',max_length=200,required=True)
    apellidos = forms.CharField(label='Apellidos',max_length=200,required=True)
    email = forms.EmailField(label='Email',required=True)
    #textarea input mas grande
    direccion = forms.CharField(label='Dirección',widget=forms.Textarea)
    telefono = forms.CharField(label='Telefono',max_length=20)
    #combobox
    sexo = forms.ChoiceField(label='Sexo',choices= SEXO_CHOICES)
    #año mes dia y - m -d
    fecha_nacimiento = forms.DateField(label='Fecha Nacimiento',input_formats=['%Y-%m-%d'],widget=DateInput())