from django.db import models

class UnidadModel(models.Model):
    nombre_unidad = models.CharField(max_length=150,unique=True,verbose_name='Nombre de Unidad')
    detalle_unidad = models.CharField(max_length=150,blank=True,null=True,verbose_name='Detalle de Unidad')
    acronimo_unidad = models.CharField(max_length=150,unique=True,verbose_name='Acronimo del Nombre de Unidad')
    fecha_unidad = models.DateField(verbose_name='Fecha Creación',auto_now_add=True)
    tipo_unidad = models.CharField(max_length=150,blank=True,null=True,verbose_name='Tipo de Unidad')
    ruta_unidad = models.CharField(max_length=150,blank=True,null=True,verbose_name='Ruta de la Unidad')
    estado_unidad = models.BooleanField(verbose_name='Estado de Unidad',default=True)
    superior_unidad = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        verbose_name='Unidad Superior',
        blank=True,
        null=True,
        related_name='children'
    )
    class Meta:
        db_table = 'unidad'
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"
    def __str__(self):
        return self.nombre_unidad
#------------------------------------------------------------------------------
# Cargo Model
#------------------------------------------------------------------------------

class CargoModel(models.Model):
    nombre_cargo = models.CharField(max_length=150,unique=True,verbose_name='Nombre de Cargo')
    detalle_cargo = models.CharField(max_length=150,blank=True,null=True,verbose_name='Detalle de Cargo')
    fecha_cargo = models.DateField(verbose_name='Fecha Creación',auto_now_add=True)
    estado_cargo = models.BooleanField(verbose_name='Estado de Cargo',default=True)
    class Meta:
        db_table = 'cargo'
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
    def __str__(self):
        return self.nombre_cargo

#------------------------------------------------------------------------------
# Usuario Model
#------------------------------------------------------------------------------
class UsuarioModel(models.Model):
    username_usuario = models.CharField(max_length=150,verbose_name='Username')
    password_usuario = models.CharField(max_length=150,verbose_name='Contraseña')
    password_dos_usuario = models.CharField(max_length=150,verbose_name='Contraseña complementaria:',blank=True,null=True)
    firstname_usuario = models.CharField(max_length=150,blank=True,null=True,verbose_name='Nombre de Usuario')
    lastname_usuario = models.CharField(max_length=150,blank=True,null=True,verbose_name='Apellido de Usuario')
    email_usuario = models.EmailField(max_length=150,blank=True,null=True,verbose_name='Correo de Usuario')
    active_usuario = models.BooleanField(default=True,verbose_name='Usuario Activo')
    item_usuario = models.CharField(max_length=150,blank=True,null=True,verbose_name='Item de Usuario')
    tipo_usuario = models.CharField(max_length=150,blank=True,null=True,verbose_name='Tipo de Usuario')
    fecha_usuario = models.DateField(verbose_name='Fecha Creación',auto_now_add=True)
    cargo_usuario = models.ManyToManyField(
        CargoModel,
        verbose_name='Cargo de Usuario',
        blank=True,)
    unidad_usuario = models.ForeignKey(
        UnidadModel,
        on_delete=models.RESTRICT,
        verbose_name='Unidad de Usuario',
        blank=True,
        null=True
    )
    gerente_usuario =models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        verbose_name='Jefe Superior',
        blank=True,
        null=True,
        related_name='children'
    )
    def get_full_name(self):
        return f"{self.firstname_usuario} {self.lastname_usuario}"
    class Meta:
        db_table = 'usuario'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    def __str__(self):
        return self.username_usuario+" - "+self.firstname_usuario+" "+self.lastname_usuario
