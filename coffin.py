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

    def esta_ko(self):
        return self.vida <= 0

    def curar_completo(self):
        self.vida = self.vida_maxima

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
        self.todos_p = self.cargar_p("personajes.txt")
        self.m_ini()

    def cargar_p(self, arch):
        personajes = []
        with open(arch, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea and not linea.startswith("#"):
                    p = linea.split("|")
                    if len(p) == 6:
                        personajes.append(Personaje(p[0], p[1], p[2], p[3], p[4], p[5]))

        return personajes

    def limp(self):
        for elemento in self.root.winfo_children():
            elemento.destroy()

    def m_ini(self):
        self.limp()
        tk.Label(self.root, text="COFFIN", font=("Arial", 42, "bold"), bg="black", fg="white").pack(pady=150)
        tk.Button(self.root, text="Ver personajes cargados", font=("Arial", 18), command=self.m_personajes).pack(pady=10)
        tk.Button(self.root, text="About", font=("Arial", 18), command=self.m_about).pack(pady=10)
        tk.Button(self.root, text="Salir", font=("Arial", 18), command=self.root.destroy).pack(pady=10)

    def m_about(self):
        messagebox.showinfo("About", "About")

    def m_personajes(self):
        self.limp()
        tk.Label(self.root, text="Personajes cargados", font=("Arial", 28), bg="black", fg="white").pack(pady=30)
        Listbox = tk.Listbox(self.root, width=90, height=20, font=("Arial", 14))
        Listbox.pack(pady=20)
        for p in self.todos_p:
            Listbox.insert(tk.END, f"{p.nombre} | {p.rol} | HP {p.vida_maxima} | ATK {p.ataque} | DEF {p.defensa}")
        tk.Button(self.root, text="Volver", font=("Arial", 18), command=self.m_ini).pack(pady=20)



root = tk.Tk()
juego = Juego(root)
root.mainloop()
