import sqlite3
import random
from datetime import datetime

def seed_database():
    conn = sqlite3.connect("sentiment_iq.db")
    cursor = conn.cursor()

    productos = [
        "Smartphone X10", "Laptop Pro 15", "Audífonos Bluetooth", 
        "Reloj Inteligente", "Teclado Mecánico", "Monitor 4K",
        "Mouse Gamer", "Cargador Carga Rápida", "Tablet Air", "Cámara Web HD"
    ]

    comentarios_positivos = [
        "Excelente producto, superó mis expectativas.",
        "Muy buena calidad de materiales, lo recomiendo 100%.",
        "Funciona perfecto y la entrega fue muy rápida.",
        "Me encantó el diseño y la duración de la batería.",
        "Es el mejor que he tenido en este rango de precio.",
        "Increíble rendimiento, muy fluido todo.",
        "La pantalla se ve genial, colores muy vivos.",
        "Muy fácil de configurar y usar.",
        "Calidad premium a un precio justo.",
        "Simplemente perfecto, no tengo quejas."
    ]

    comentarios_negativos = [
        "Pésima calidad, se rompió a la semana.",
        "No funciona como dice la descripción, una decepción.",
        "Llegó tarde y la caja estaba golpeada.",
        "Muy lento, se traba todo el tiempo.",
        "La batería no dura ni 2 horas, no lo compren.",
        "El servicio al cliente fue horrible cuando pedí ayuda.",
        "Muy caro para lo que ofrece, hay mejores opciones.",
        "No es compatible con mi sistema, dinero tirado.",
        "Se calienta demasiado a los pocos minutos.",
        "El material se siente muy barato y frágil."
    ]

    # Generar 50 reseñas
    for i in range(50):
        producto = random.choice(productos)
        es_positivo = random.choice([True, False])
        
        if es_positivo:
            comentario = random.choice(comentarios_positivos)
        else:
            comentario = random.choice(comentarios_negativos)
        
        # Mezclamos estados: algunas ya analizadas y otras "Pendiente" para que pruebes el botón de la IA
        sentimiento = random.choice(["Positivo", "Negativo", "Pendiente"])
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        cursor.execute('''
            INSERT INTO reviews (producto, comentario, sentimiento_ia, fecha)
            VALUES (?, ?, ?, ?)
        ''', (producto, comentario, sentimiento, fecha))

    conn.commit()
    conn.close()
    print("✅ ¡Éxito! Se han cargado 50 reseñas de prueba en la base de datos.")

if __name__ == "__main__":
    seed_database()
