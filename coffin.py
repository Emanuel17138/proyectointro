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
        def r(i):
            if i >= len(self.personajes):
                return
            self.personajes[i].curar_completo()
            r(i + 1)
        r(0)


class Juego:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffin")
        self.w = 1200
        self.h = 800
        self.root.geometry(f"{self.w}x{self.h}")
        self.root.resizable(False, False)
        self.root.configure(bg="black")
        self.avatar_elegido = tk.StringVar(value="avatar1")
        self.nombre_var = tk.StringVar()
        self.i_elegidos = []
        self.todos_p = self.cargar_p("personajes.txt")
        self.f_ini = "ibg.png"
        self.f_titulo = "titulo.png"
        self.f_conf = "confi.png"
        self.bt_inicio = "iniciar.png"
        self.bt_about = "about.png"
        self.bt_salir = "salir.png"
        self.bt_atras = "atras.png"
        self.avatars = [["avatar1", "avatar1.png"], ["avatar2", "avatar2.png"], ["avatar3", "avatar3.png"]]
        self.jugador = None
        self.imgs = []
        self.bt_personajes = []
        self.etq_sel = None
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
        bt = tk.Button(self.root, image=im, command=cmd, bg="black", activebackground="black", bd=0, borderwidth=0, highlightthickness=0, padx=0, pady=0, relief="flat", cursor="hand2")
        bt.image = im
        return bt

    def limp(self):
        hijos = self.root.winfo_children()
        def r(i):
            if i >= len(hijos):
                return
            hijos[i].destroy()
            r(i + 1)
        r(0)

    def canvas(self):
        cv = tk.Canvas(self.root, width=self.w, height=self.h, highlightthickness=0, bd=0, bg="black")
        cv.pack(fill="both", expand=True)
        return cv

    def m_about(self):
        messagebox.showinfo("About", "Versión con selección completa de personajes.")

    def cerrar(self):
        self.root.destroy()

    def m_ini(self):
        self.limp()
        self.imgs = []
        cv = self.canvas()
        cv.create_image(0, 0, anchor="nw", image=self.img(self.f_ini, (self.w, self.h)))
        cv.create_image(self.w // 2, 210, image=self.img(self.f_titulo, (430, 130)))
        cv.create_window(self.w // 2, 420, window=self.bt_img(self.bt_inicio, (300, 72), self.m_conf))
        cv.create_window(self.w // 2, 505, window=self.bt_img(self.bt_about, (300, 72), self.m_about))
        cv.create_window(self.w // 2, 590, window=self.bt_img(self.bt_salir, (300, 72), self.cerrar))

    def m_conf(self):
        self.limp()
        self.imgs = []
        self.bt_personajes = []
        self.i_elegidos = []
        cv = self.canvas()
        cv.create_image(0, 0, anchor="nw", image=self.img(self.f_conf, (self.w, self.h)))
        ent = tk.Entry(self.root, textvariable=self.nombre_var, font=("Arial", 14), justify="center", bd=0, bg="#151313", fg="#d6c18a", insertbackground="#d6c18a")
        cv.create_window(self.w // 2, 204, window=ent, width=500, height=34)
        self.crear_avatars(cv, 0, [450, 600, 750])
        self.etq_sel = tk.Label(self.root, text="0/3 seleccionados", font=("Arial", 13, "bold"), bg="#111111", fg="#d6c18a", bd=0)
        cv.create_window(self.w // 2, 444, window=self.etq_sel, width=230, height=30)
        marco = self.marco_scroll(cv, 520, 240, self.w // 2, 575)
        self.crear_bt_personajes(marco, 0, 3, self.todos_p, self.elegir_p, self.bt_personajes)
        cv.create_window(415, 750, window=self.bt_img(self.bt_atras, (150, 38), self.m_ini))
        cv.create_window(600, 750, window=self.bt_img(self.bt_about, (150, 38), self.m_about))
        cv.create_window(785, 750, window=self.bt_img(self.bt_inicio, (150, 38), self.confirmar_eleccion))
        self.act_cont()

    def crear_avatars(self, cv, i, xs):
        if i >= len(self.avatars):
            return
        av_id, arch = self.avatars[i]
        im = self.img(arch, (96, 96))
        bt = tk.Radiobutton(self.root, image=im, variable=self.avatar_elegido, value=av_id, indicatoron=False, width=104, height=104, selectcolor="#3b1214", bg="#111111", activebackground="#111111", relief="flat", bd=2, cursor="hand2")
        bt.image = im
        cv.create_window(xs[i], 330, window=bt)
        self.crear_avatars(cv, i + 1, xs)

    def marco_scroll(self, cv, w, h, x, y):
        cont = tk.Frame(self.root, bg="#111111", bd=0)
        cv.create_window(x, y, window=cont)
        subcv = tk.Canvas(cont, width=w, height=h, bg="#111111", bd=0, highlightthickness=0)
        barra = tk.Scrollbar(cont, orient="vertical", command=subcv.yview, width=14)
        marco = tk.Frame(subcv, bg="#111111")
        interno = subcv.create_window((0, 0), window=marco, anchor="nw")
        subcv.configure(yscrollcommand=barra.set)
        def config_marco(e):
            subcv.configure(scrollregion=subcv.bbox("all"))
        def config_ancho(e):
            subcv.itemconfig(interno, width=e.width)
        def rueda(e):
            if e.delta > 0:
                subcv.yview_scroll(-1, "units")
            elif e.delta < 0:
                subcv.yview_scroll(1, "units")
        marco.bind("<Configure>", config_marco)
        subcv.bind("<Configure>", config_ancho)
        subcv.bind("<MouseWheel>", rueda)
        marco.bind("<MouseWheel>", rueda)
        subcv.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")
        marco.rueda = rueda
        return marco

    def crear_bt_personajes(self, marco, i, cols, lista, cmd, guardado):
        if i >= len(lista):
            return
        p = lista[i]
        im = self.img(p.archivo_imagen, (126, 126))
        bt = tk.Button(marco, image=im, width=134, height=134, bg="#1a1717", activebackground="#1a1717", relief="flat", bd=2, highlightthickness=1, highlightbackground="#3a2d24", cursor="hand2", command=lambda n=i: cmd(n))
        bt.image = im
        bt.bind("<MouseWheel>", marco.rueda)
        bt.grid(row=i // cols, column=i % cols, padx=14, pady=10)
        guardado.append(bt)
        self.crear_bt_personajes(marco, i + 1, cols, lista, cmd, guardado)

    def act_cont(self):
        if self.etq_sel is not None:
            self.etq_sel.config(text=f"{len(self.i_elegidos)}/3 seleccionados")

    def elegir_p(self, i):
        if i in self.i_elegidos:
            self.i_elegidos.remove(i)
        elif len(self.i_elegidos) < 3:
            self.i_elegidos.append(i)
        else:
            messagebox.showwarning("Límite", "Solo puedes seleccionar 3 personajes.")
            return
        self.pintar_bt(self.bt_personajes, self.i_elegidos, 0)
        self.act_cont()

    def pintar_bt(self, lista, elegidos, i):
        if i >= len(lista):
            return
        if i in elegidos:
            lista[i].config(bg="#4b1b1f", activebackground="#4b1b1f", relief="sunken", bd=3, highlightbackground="#c8a45a")
        else:
            lista[i].config(bg="#1a1717", activebackground="#1a1717", relief="flat", bd=2, highlightbackground="#3a2d24")
        self.pintar_bt(lista, elegidos, i + 1)

    def confirmar_eleccion(self):
        nombre = self.nombre_var.get().strip()
        if not nombre:
            messagebox.showwarning("Falta dato", "Debes escribir tu nombre.")
            return
        if len(self.i_elegidos) != 3:
            messagebox.showwarning("Falta dato", "Debes seleccionar exactamente 3 personajes.")
            return
        self.jugador = Equipo(nombre, self.avatar_elegido.get())
        self.jugador.personajes = [self.todos_p[i].copiar() for i in self.i_elegidos]
        self.jugador.pts = 0
       



root = tk.Tk()
juego = Juego(root)
root.mainloop()
