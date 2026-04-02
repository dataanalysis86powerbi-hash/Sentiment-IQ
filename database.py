import sqlite3
from datetime import datetime

class DatabaseManager:
    """Clase encargada de la persistencia de datos (Bases de Datos I)"""

    def __init__(self, db_name="sentiment_iq.db"):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Crea las tablas necesarias si no existen"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabla de Usuarios (Para POO y Seguridad)
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')

        # Tabla de Reseñas (Para Análisis de IA)
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto TEXT NOT NULL,
                comentario TEXT NOT NULL,
                sentimiento_ia TEXT,
                fecha TEXT
            )
        ''')
        
        # Insertar usuario admin por defecto si no existe
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                         ('admin', 'admin123', 'Admin'))
            
        conn.commit()
        conn.close()
        print("Base de datos y tablas inicializadas correctamente.")

    def registrar_reviews(self, producto, comentario, sentimiento="Pendiente"):
        """Insertar una nueva reseña en la base de datos"""
        # Corrección del formato de fecha según el informe
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reviews (producto, comentario, sentimiento_ia, fecha)
                VALUES (?, ?, ?, ?)            
            ''' , (producto, comentario, sentimiento, fecha_actual))
            conn.commit()
            return True
                    
        except Exception as e:
            print(f"Error al guardar reseña: {e}")
            return False
        finally:
            conn.close()

    def obtener_usuarios(self):
        """Retorna todos los usuarios"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios

    def validar_login(self, username, password):
        """Valida credenciales contra la DB"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
