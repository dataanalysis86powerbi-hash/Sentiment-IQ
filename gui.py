import tkinter as tk
from tkinter import messagebox, ttk
import threading
from database import DatabaseManager
from models import Admin, Customer
from analysis import SentimentModel, DataRepository
from utils import registrar_log, exportar_csv, exportar_excel, iniciar_backup_hilo

class SentimentIQ_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sentiment-IQ: Business Intelligence IA")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f2f5")
        
        # Logica del sistema
        self.db = DatabaseManager()
        self.ia = SentimentModel()
        self.repo = DataRepository()
        self.current_user = None
        
        # Inicializar IA y Datos
        threading.Thread(target=self._inicializar_ia, daemon=True).start()
        
        # Estilos
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 10), padding=5)
        self.style.configure("TLabel", font=("Segoe UI", 10), background="#f0f2f5")
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1a73e8")

        self.pantalla_login()

    def _inicializar_ia(self):
        self.ia.entrenar_modelo()
        self.repo.cargar_desde_db()
        iniciar_backup_hilo()

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def pantalla_login(self):
        self.limpiar_pantalla()
        
        frame = tk.Frame(self.root, bg="white", padx=40, pady=40, highlightbackground="#ddd", highlightthickness=1)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Sentiment-IQ Login", style="Header.TLabel", background="white").pack(pady=(0, 20))

        ttk.Label(frame, text="Usuario:", background="white").pack(anchor="w")
        self.entry_user = ttk.Entry(frame, width=30)
        self.entry_user.pack(pady=(5, 15))

        ttk.Label(frame, text="Contraseña:", background="white").pack(anchor="w")
        self.entry_pass = ttk.Entry(frame, width=30, show="*")
        self.entry_pass.pack(pady=(5, 20))

        ttk.Button(frame, text="Iniciar Sesión", command=self.ejecutar_login).pack(fill="x")

    def ejecutar_login(self):
        user = self.entry_user.get()
        pw = self.entry_pass.get()
        
        role = self.db.validar_login(user, pw)
        
        if role:
            if role == "Admin":
                self.current_user = Admin(1, user, pw)
                self.pantalla_admin()
            else:
                self.current_user = Customer(2, user, pw)
                self.pantalla_customer()
            registrar_log(f"Login GUI exitoso: {user}")
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def pantalla_customer(self):
        self.limpiar_pantalla()
        
        header = tk.Frame(self.root, bg="#1a73e8", height=60)
        header.pack(fill="x")
        tk.Label(header, text=f"Hola, {self.current_user.username}", bg="#1a73e8", fg="white", font=("Segoe UI", 12, "bold")).pack(side="left", padx=20, pady=15)
        ttk.Button(header, text="Cerrar Sesión", command=self.pantalla_login).pack(side="right", padx=20, pady=10)

        main_frame = tk.Frame(self.root, bg="#f0f2f5", padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Registrar Nuevo Feedback", style="Header.TLabel").pack(pady=(0, 20))

        ttk.Label(main_frame, text="Nombre del Producto:").pack(anchor="w")
        self.entry_prod = ttk.Entry(main_frame, width=50)
        self.entry_prod.pack(pady=(5, 15))

        ttk.Label(main_frame, text="Tu Opinión:").pack(anchor="w")
        self.text_rev = tk.Text(main_frame, height=5, width=38, font=("Segoe UI", 10))
        self.text_rev.pack(pady=(5, 20))

        ttk.Button(main_frame, text="Enviar Comentario", command=self.enviar_feedback).pack()

    def enviar_feedback(self):
        prod = self.entry_prod.get()
        rev = self.text_rev.get("1.0", tk.END).strip()
        
        if prod and rev:
            if self.db.registrar_reviews(prod, rev):
                messagebox.showinfo("Éxito", "Feedback guardado correctamente")
                self.entry_prod.delete(0, tk.END)
                self.text_rev.delete("1.0", tk.END)
                self.repo.cargar_desde_db()
        else:
            messagebox.showwarning("Atención", "Por favor completa todos los campos")

    def pantalla_admin(self):
        self.limpiar_pantalla()
        
        header = tk.Frame(self.root, bg="#202124", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Panel de Administración - Sentiment-IQ", bg="#202124", fg="white", font=("Segoe UI", 12, "bold")).pack(side="left", padx=20, pady=15)
        ttk.Button(header, text="Salir", command=self.pantalla_login).pack(side="right", padx=20, pady=10)

        main_frame = tk.Frame(self.root, bg="#f0f2f5", padx=30, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Botones de Acción
        btn_frame = tk.Frame(main_frame, bg="#f0f2f5")
        btn_frame.pack(fill="x", pady=10)

        ttk.Button(btn_frame, text="Analizar Pendientes (IA)", command=self.gui_pipeline).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exportar CSV", command=lambda: exportar_csv()).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exportar Excel", command=lambda: exportar_excel()).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar Reporte", command=self.actualizar_stats).pack(side="left", padx=5)

        # Estadísticas
        self.stats_label = ttk.Label(main_frame, text="Cargando estadísticas...", font=("Segoe UI", 11))
        self.stats_label.pack(pady=20)

        # Lista Simple de Reseñas (Vista rápida)
        self.tree = ttk.Treeview(main_frame, columns=("ID", "Prod", "Sent"), show="headings", height=8)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Prod", text="Producto")
        self.tree.heading("Sent", text="IA")
        self.tree.column("ID", width=40)
        self.tree.pack(fill="both", expand=True)
        
        self.actualizar_stats()

    def gui_pipeline(self):
        import sqlite3
        conn = sqlite3.connect("sentiment_iq.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, comentario FROM reviews WHERE sentimiento_ia = 'Pendiente'")
        pendientes = cursor.fetchall()
        
        if not pendientes:
            messagebox.showinfo("IA", "No hay reseñas nuevas por procesar.")
            return

        for id_db, comentario in pendientes:
            prediccion = self.ia.predecir(comentario)
            cursor.execute("UPDATE reviews SET sentimiento_ia = ? WHERE id = ?", (prediccion, id_db))
        
        conn.commit()
        conn.close()
        self.repo.cargar_desde_db()
        self.actualizar_stats()
        messagebox.showinfo("Éxito", f"Se procesaron {len(pendientes)} reseñas.")

    def actualizar_stats(self):
        import sqlite3
        conn = sqlite3.connect("sentiment_iq.db")
        cursor = conn.cursor()
        cursor.execute("SELECT sentimiento_ia, COUNT(*) FROM reviews GROUP BY sentimiento_ia")
        stats = dict(cursor.fetchall())
        
        # Actualizar Lista
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        cursor.execute("SELECT id, producto, sentimiento_ia FROM reviews ORDER BY id DESC LIMIT 10")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
            
        conn.close()

        pos = stats.get("Positivo", 0)
        neg = stats.get("Negativo", 0)
        pen = stats.get("Pendiente", 0)
        
        texto = f"Resumen: {pos} Positivas | {neg} Negativas | {pen} Pendientes"
        self.stats_label.config(text=texto)

if __name__ == "__main__":
    root = tk.Tk()
    app = SentimentIQ_GUI(root)
    root.mainloop()
