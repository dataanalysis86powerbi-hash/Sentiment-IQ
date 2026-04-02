import sqlite3
import os
from database import DatabaseManager
from models import Admin, Customer
from analysis import SentimentModel, DataRepository
from utils import registrar_log, exportar_csv, exportar_excel, iniciar_backup_hilo

class SentimentIQ_App:
    """Clase Maestra: Orquestador del Sistema Integrado"""

    def __init__(self):
        self.db = DatabaseManager()
        self.ia = SentimentModel()
        self.repo = DataRepository()
        self.current_user = None
        
        # Inicialización
        self.ia.entrenar_modelo()
        self.repo.cargar_desde_db()
        iniciar_backup_hilo()
        registrar_log("Sistema Sentiment-IQ iniciado.")

    def login(self):
        """Sistema de Login (Seguridad)"""
        print("\n" + "="*40)
        print(" BIENVENIDO A SENTIMENT-IQ ".center(40, "="))
        username = input("Usuario: ")
        password = input("Contraseña: ")
        
        role = self.db.validar_login(username, password)
        
        if role == "Admin":
            self.current_user = Admin(1, username, password)
            registrar_log(f"Login exitoso: Admin '{username}'")
            return True
        elif role == "Customer":
            self.current_user = Customer(2, username, password)
            registrar_log(f"Login exitoso: Customer '{username}'")
            return True
        else:
            print(">>> Error: Credenciales incorrectas.")
            registrar_log(f"Intento fallido de login: {username}")
            return False

    def menu(self):
        """Interfaz de Usuario (CLI)"""
        while True:
            print(f"\n--- MENÚ PRINCIPAL (Sesión: {self.current_user.username}) ---")
            print(f"Permisos: {self.current_user.get_permissions()}")
            
            if isinstance(self.current_user, Admin):
                print("1. Ejecutar Pipeline de Análisis")
                print("2. Ver Reporte Estratégico")
                print("3. Exportar Datos a CSV")
                print("4. Exportar Datos a Excel (.xlsx)")
                print("5. Buscar Reseña por ID (Hash Map)")
                print("0. Salir")
            else:
                print("1. Registrar nueva reseña")
                print("0. Salir")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "0":
                print("Cerrando sistema...")
                break
            
            if isinstance(self.current_user, Admin):
                if opcion == "1": self.ejecutar_pipeline()
                elif opcion == "2": self.generar_reporte_consultoria()
                elif opcion == "3": exportar_csv()
                elif opcion == "4": exportar_excel()
                elif opcion == "5": self.buscar_en_memoria()
            else:
                if opcion == "1": self.registrar_feedback()

    def registrar_feedback(self):
        """Acción para Customer: Registrar feedback"""
        prod = input("Producto: ")
        rev = input("Comentario: ")
        if self.db.registrar_reviews(prod, rev):
            print(">>> Reseña registrada exitosamente.")
            # Recargar caché
            self.repo.cargar_desde_db()

    def ejecutar_pipeline(self):
        """Procesa las reseñas pendientes usando la IA"""
        print("\n" + "="*40)
        print(" ANALISIS AUTOMATIZADO ".center(40, "="))

        try:
            conn = sqlite3.connect(self.db.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT id, comentario FROM reviews WHERE sentimiento_ia = 'Pendiente'")
            pendientes = cursor.fetchall()

            if not pendientes:
                print(">>> No hay reseñas pendientes por analizar.")
                return
            
            print(f">>>> Se encontraron {len(pendientes)} reseñas nuevas.")
            
            for id_db, comentario in pendientes:
                prediccion = self.ia.predecir(comentario)
                cursor.execute("UPDATE reviews SET sentimiento_ia = ? WHERE id = ?", (prediccion, id_db))
                print(f"ID {id_db}: '{comentario[:30]}...' -> Clasificado como: {prediccion}")

            conn.commit()
            conn.close()
            # Actualizar repositorio en memoria
            self.repo.cargar_desde_db()
            print("\n>>> Base de datos y caché actualizados correctamente")

        except Exception as e:
            print(f"Error en el Pipeline: {e}")

    def generar_reporte_consultoria(self):
        """Módulo de Toma de Decisiones"""
        conn = sqlite3.connect(self.db.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT sentimiento_ia, COUNT(*) FROM reviews GROUP BY sentimiento_ia")
        stats = dict(cursor.fetchall())
        conn.close()

        pos = stats.get("Positivo", 0)
        neg = stats.get("Negativo", 0)

        print("\n" + "=" * 40)
        print("REPORTE ESTRATÉGICO".center(40, "="))
        print(f"Reseñas positivas: {pos}")
        print(f"Reseñas negativas: {neg}")
        
        if neg > pos:
            print("\nALERTA: Se recomienda revisar la calidad de los productos.")
        elif pos > 0:
            print("\nÉXITO: Los clientes están altamente satisfechos.")
        print("="*40)

    def buscar_en_memoria(self):
        """Uso de Estructura de Datos (Hash Map)"""
        try:
            id_buscada = int(input("Ingrese el ID de la reseña a buscar: "))
            resultado = self.repo.buscar_por_id(id_buscada)
            if resultado:
                print(f"\nENCONTRADO (Hash Map O(1)):")
                print(f"Producto: {resultado.producto}")
                print(f"Comentario: {resultado.comentario}")
                print(f"Sentimiento: {resultado.sentimiento}")
            else:
                print(">>> ID no encontrada en memoria.")
        except ValueError:
            print("ID inválida.")

if __name__ == "__main__":
    app = SentimentIQ_App()
    if app.login():
        app.menu()
