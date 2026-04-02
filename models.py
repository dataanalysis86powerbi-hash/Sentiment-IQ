from abc import ABC, abstractmethod

class User(ABC):
    """Clase Base Abstracta (POO: Abstracción y Polimorfismo)"""

    def __init__(self, user_id, username, password):
        self._user_id = user_id        # Atributo protegido (POO)
        self.username = username
        self.__password = password     # Atributo privado (POO: Encapsulamiento)

    @property
    def user_id(self):
        return self._user_id

    @property
    def password(self):
        """Getter seguro para la contraseña"""
        return "********"

    @abstractmethod
    def get_permissions(self):
        """Método abstracto para Polimorfismo"""
        pass

class Admin(User):
    """Clase para el rol de Administrador (POO: Herencia)"""

    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)
        self.role = "Admin"

    def get_permissions(self):
        """Polimorfismo: El admin tiene acceso total"""
        return ["Ver Reportes", "Analizar Feedback", "Gestionar Usuarios"]

class Customer(User):
    """Clase para el rol de Cliente (POO: Herencia)"""

    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)
        self.role = "Customer"

    def get_permissions(self):
        """Polimorfismo: El cliente solo registra feedback"""
        return ["Registrar Reseña", "Ver Mis Feedback"]

class Review:
    """Clase Entidad: Representa una reseña de producto"""
    def __init__(self, review_id, producto, comentario, sentimiento="Pendiente", fecha=None):
        self.id = review_id
        self.producto = producto
        self.comentario = comentario
        self.sentimiento = sentimiento
        self.fecha = fecha
