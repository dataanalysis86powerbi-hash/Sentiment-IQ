import re
import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from models import Review

class TextProcessor:
    """Algoritmos de limpieza de datos (Sistemas Operativos / IA)"""
    def __init__(self):
        self.stopwords = {"el", "la", "los", "las", "un", "y", "o", "que", "es", "muy"}

    def limpiar_texto(self, texto):
        texto = texto.lower()
        texto = re.sub(r'[^\w\s]', '', texto)
        tokens = texto.split()
        return [p for p in tokens if p not in self.stopwords]

class SentimentModel:
    """Inteligencia Artificial: Multinomial Naive Bayes"""
    def __init__(self):
        self.processor = TextProcessor()
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()
        self.entrenado = False

    def entrenar_modelo(self):
        frases = [
            "excelente producto muy buena calidad", "me encanto funciona perfecto",
            "el mejor servicio que he tenido", "estoy feliz con mi compra",
            "pésimo producto no funciona", "muy mala calidad una decepción",
            "no me gusto llego roto", "el servicio fue horrible"
        ]
        etiquetas = [1, 1, 1, 1, 0, 0, 0, 0]
        
        frases_limpias = [" ".join(self.processor.limpiar_texto(f)) for f in frases]
        x = self.vectorizer.fit_transform(frases_limpias)
        self.model.fit(x, etiquetas)
        self.entrenado = True

    def predecir(self, texto):
        if not self.entrenado: self.entrenar_modelo()
        limpio = " ".join(self.processor.limpiar_texto(texto))
        vector = self.vectorizer.transform([limpio])
        prediccion = self.model.predict(vector)
        return "Positivo" if prediccion[0] == 1 else "Negativo"

class DataRepository:
    """Gestión de Memoria y Estructuras de Datos (Hash Map)"""
    def __init__(self):
        # Diccionario para búsqueda O(1) - Requisito de Estructura de Datos
        self._reviews_cache = {}

    def cargar_desde_db(self, db_name="sentiment_iq.db"):
        """Carga datos de SQLite a memoria (Hash Map)"""
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reviews")
            rows = cursor.fetchall()
            
            for row in rows:
                rev = Review(row[0], row[1], row[2], row[3], row[4])
                self._reviews_cache[rev.id] = rev # Hash Map: ID -> Objeto
            
            conn.close()
            print(f"Memoria: {len(self._reviews_cache)} registros cargados en caché.")
        except Exception as e:
            print(f"Error al cargar caché: {e}")

    def buscar_por_id(self, review_id):
        """Búsqueda eficiente O(1) usando el diccionario"""
        return self._reviews_cache.get(review_id)
