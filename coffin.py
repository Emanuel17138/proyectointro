import tkinter as tk
from tkinter import messagebox


class Personaje:
    def __init__(self, nombre, rol, vida, ataque, defensa, archivo_imagen=""):
        self.nombre = nombre
        self.rol = rol
        self.vida_maxima = int(vida)
        self.vida = int(vida)
        self.ataque = int(ataque)
        self.defensa = int(defensa)
        self.archivo_imagen = archivo_imagen

    def copiar(self):
        return Personaje(self.nombre, self.rol, self.vida_maxima, self.ataque, self.defensa, self.archivo_imagen)


class Equipo:
    def __init__(self, nombre, avatar):
        self.nombre = nombre
        self.avatar = avatar
        self.personajes = []
        self.pts = 0

    def tiene_personajes_disponibles(self):
        return len(self.obtener_personajes_disponibles()) > 0

    def obtener_personajes_disponibles(self):
        return [p for p in self.personajes if not p.esta_ko()]



class Juego:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffin")
        self.w = 1200
        self.h = 800
        self.root.geometry(f"{self.w}x{self.h}")
        self.root.resizable(False, False)
        self.root.configure(bg="black")
        self.m_ini()

    def limp(self):
        for elemento in self.root.winfo_children():
            elemento.destroy()

    def m_ini(self):
        self.limp()
        tk.Label(self.root, text="COFFIN", font=("Arial", 42, "bold"), bg="black", fg="white").pack(pady=160)
        tk.Button(self.root, text="Iniciar partida", font=("Arial", 18),).pack(pady=10)
        tk.Button(self.root, text="About", font=("Arial", 18), command=self.m_about).pack(pady=10)
        tk.Button(self.root, text="Salir", font=("Arial", 18), command=self.root.destroy).pack(pady=10)

    def m_about(self):
        messagebox.showinfo("About", "about")



root = tk.Tk()
juego = Juego(root)
root.mainloop()

