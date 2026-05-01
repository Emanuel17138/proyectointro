import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os


class Personaje:
    def __init__(self, nombre, rol, vida, ataque, defensa, archivo_imagen):
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

    def curar_equipo(self):
        for p in self.personajes:
            p.curar_completo()


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
        self.imgs = []
        self.f_ini = "ibg.png"
        self.f_titulo = "titulo.png"
        self.bt_inicio = "iniciar.png"
        self.bt_about = "about.png"
        self.bt_salir = "salir.png"
        self.m_ini()

    def ruta_img(self, arch):
        return os.path.join("img", arch)

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

    def img_pil(self, arch, tam):
        return Image.open(self.ruta_img(arch)).convert("RGBA").resize(tam, Image.LANCZOS)

    def img(self, arch, tam):
        im = ImageTk.PhotoImage(self.img_pil(arch, tam))
        self.imgs.append(im)
        return im

    def bt_img(self, arch, tam, cmd):
        im = self.img(arch, tam)
        bt = tk.Button(self.root, image=im, command=cmd, bg="black", activebackground="black", bd=0, highlightthickness=0, cursor="hand2")
        bt.image = im
        return bt

    def limp(self):
        for elemento in self.root.winfo_children():
            elemento.destroy()

    def canvas(self):
        cv = tk.Canvas(self.root, width=self.w, height=self.h, highlightthickness=0, bd=0, bg="black")
        cv.pack(fill="both", expand=True)
        return cv

    def m_about(self):
        messagebox.showinfo("About", "About")

    def cerrar(self):
        self.root.destroy()

    def m_ini(self):
        self.limp()
        self.imgs = []
        cv = self.canvas()
        cv.create_image(0, 0, anchor="nw", image=self.img(self.f_ini, (self.w, self.h)))
        cv.create_image(self.w // 2, 210, image=self.img(self.f_titulo, (430, 130)))
        cv.create_window(self.w // 2, 420, window=self.bt_img(self.bt_inicio, (300, 72), self.m_personajes))
        cv.create_window(self.w // 2, 505, window=self.bt_img(self.bt_about, (300, 72), self.m_about))
        cv.create_window(self.w // 2, 590, window=self.bt_img(self.bt_salir, (300, 72), self.cerrar))

    def m_personajes(self):
        self.limp()
        cv = self.canvas()
        cv.create_rectangle(0, 0, self.w, self.h, fill="black")
        cv.create_text(self.w // 2, 60, text="Personajes cargados", fill="white", font=("Arial", 30, "bold"))
        caja = tk.Listbox(self.root, width=85, height=22, font=("Arial", 13))
        cv.create_window(self.w // 2, 390, window=caja)
        for p in self.todos_p:
            caja.insert(tk.END, f"{p.nombre} | {p.rol} | HP {p.vida_maxima} | ATK {p.ataque} | DEF {p.defensa}")
        cv.create_window(self.w // 2, 720, window=tk.Button(self.root, text="Volver", command=self.m_ini, font=("Arial", 16)))



root = tk.Tk()
juego = Juego(root)
root.mainloop()
