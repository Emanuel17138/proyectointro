import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random



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
        return Personaje(
            self.nombre,
            self.rol,
            self.vida_maxima,
            self.ataque,
            self.defensa,
            self.archivo_imagen
        )


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
        self.i_pelea_elegidos = []
        self.todos_p = self.cargar_p("personajes.txt")
        self.f_ini = "ibg.png"
        self.f_titulo = "titulo.png"
        self.f_conf = "confi.png"
        self.f_mapa = "mapa.png"
        self.f_pelea = "pelea.png"
        self.bt_inicio = "iniciar.png"
        self.bt_about = "about.png"
        self.bt_salir = "salir.png"
        self.bt_atras = "atras.png"
        self.bt_capilla = "Capilla.png"
        self.bt_patio = "Patio.png"
        self.bt_comedor = "Comedor.png"
        self.bt_entrada = "Entrada.png"
        self.bt_biblioteca = "Biblioteca.png"
        self.bt_capilla_d = "Capilla_derrotado.png"
        self.bt_patio_d = "Patio_derrotado.png"
        self.bt_comedor_d = "Comedor_derrotado.png"
        self.bt_entrada_d = "Entrada_derrotado.png"
        self.bt_biblioteca_d = "Biblioteca_derrotado.png"
        self.bt_ver_eq = "ver_equipo.png"
        self.bt_atacar = "atacar.png"
        self.bt_cambiar = "cambiar_personaje.png"
        self.bt_volver = "volver_mapa.png"
        self.bt_iniciar_b = "iniciar_batalla.png"

        self.lugares = [
            ["Capilla", 616, 202, self.bt_capilla, self.bt_capilla_d],
            ["Patio", 205, 400, self.bt_patio, self.bt_patio_d],
            ["Comedor", 847, 407, self.bt_comedor, self.bt_comedor_d],
            ["Entrada", 614, 640, self.bt_entrada, self.bt_entrada_d],
            ["Biblioteca", 999, 690, self.bt_biblioteca, self.bt_biblioteca_d]
        ]

        self.avatars = [
            ["avatar1", "avatar1.png"],
            ["avatar2", "avatar2.png"],
            ["avatar3", "avatar3.png"]
        ]

        self.hollows = []
        self.i_lugar = None
        self.hollow_ac = None
        self.jugador = None
        self.personajes_pelea = []
        self.disp_pelea = []
        self.pj = None
        self.ph = None
        self.pelea_activa = False
        self.id_pelea = 0

        self.imgs = []
        self.bt_personajes = []
        self.bt_pelea = []
        self.etq_sel = None
        self.etq_sel_pelea = None
        self.txt_accion = None
        self.txt_pts = None
        self.cv_pelea = None
        self.img_pj = None
        self.img_ph = None
        self.info_pj = None
        self.info_ph = None

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.m_ini()

    def ruta_img(self, arch):
        return os.path.join("img", arch)

    def ruta_m(self, arch):
        return os.path.join("sound", arch)

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
        bt = tk.Button(
            self.root,
            image=im,
            command=cmd,
            bg="black",
            activebackground="black",
            bd=0,
            borderwidth=0,
            highlightthickness=0,
            padx=0,
            pady=0,
            relief="flat",
            overrelief="flat",
            takefocus=False,
            cursor="hand2"
        )
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
        messagebox.showinfo("About", "about")

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


        ent = tk.Entry(
            self.root,
            textvariable=self.nombre_var,
            font=("Arial", 14),
            justify="center",
            bd=0,
            relief="flat",
            bg="#151313",
            fg="#d6c18a",
            insertbackground="#d6c18a"
        )
        cv.create_window(self.w // 2, 204, window=ent, width=500, height=34)
        self.crear_avatars(cv, 0, [450, 600, 750])

        self.etq_sel = tk.Label(
            self.root,
            text="0/3 seleccionados",
            font=("Arial", 13, "bold"),
            bg="#111111",
            fg="#d6c18a",
            bd=0,
            highlightthickness=0
        )
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
        bt = tk.Radiobutton(
            self.root,
            image=im,
            variable=self.avatar_elegido,
            value=av_id,
            indicatoron=False,
            width=104,
            height=104,
            selectcolor="#3b1214",
            bg="#111111",
            activebackground="#111111",
            relief="flat",
            bd=2,
            highlightthickness=1,
            highlightbackground="#3a2d24",
            highlightcolor="#b59b63",
            cursor="hand2"
        )
        bt.image = im
        cv.create_window(xs[i], 330, window=bt)
        self.crear_avatars(cv, i + 1, xs)

    def marco_scroll(self, cv, w, h, x, y):
        cont = tk.Frame(self.root, bg="#111111", bd=0, highlightthickness=0)
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
        bt = tk.Button(
            marco,
            image=im,
            width=134,
            height=134,
            bg="#1a1717",
            activebackground="#1a1717",
            relief="flat",
            bd=2,
            highlightthickness=1,
            highlightbackground="#3a2d24",
            cursor="hand2",
            command=lambda n=i: cmd(n)
        )
        bt.image = im
        bt.bind("<MouseWheel>", marco.rueda)
        bt.grid(row=i // cols, column=i % cols, padx=14, pady=10)
        guardado.append(bt)
        self.crear_bt_personajes(marco, i + 1, cols, lista, cmd, guardado)

    def act_cont(self):
        if self.etq_sel is not None:
            self.etq_sel.config(text=f"{len(self.i_elegidos)}/3 seleccionados")

    def act_cont_pelea(self):
        if self.etq_sel_pelea is not None:
            self.etq_sel_pelea.config(text=f"{len(self.i_pelea_elegidos)}/3 seleccionados para la batalla")

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
        self.crear_hollows()
        self.m_mapa()

    def crear_hollows(self):
        self.hollows = []

        def r(i):
            if i >= len(self.lugares):
                return

            hollow = Equipo(f"Hollow {i + 1}", "x")
            elegidos = random.sample(self.todos_p, 3)
            hollow.personajes = [p.copiar() for p in elegidos]

            self.hollows.append(hollow)
            r(i + 1)

        r(0)

    def nombre_lugar(self, i):
        return self.lugares[i][0]

    def m_mapa(self):
        self.limp()
        self.imgs = []
        self.pelea_activa = False
        cv = self.canvas()
        cv.create_image(0, 0, anchor="nw", image=self.img(self.f_mapa, (self.w, self.h)))

        cv.create_text(25, 25, anchor="nw", text=f"Puntaje: {self.jugador.pts}", fill="white", font=("Arial", 16, "bold"))
        self.crear_lugares(cv, 0)
        cv.create_window(420, 730, window=self.bt_img(self.bt_ver_eq, (170, 54), self.m_eq))
        cv.create_window(580, 730, window=self.bt_img(self.bt_salir, (170, 54), self.cerrar))
        if self.gano_juego():
            messagebox.showinfo("Victoria", f"¡Felicidades {self.jugador.nombre}!\nHas derrotado a los 5 Hollows.")

    def crear_lugares(self, cv, i):
        if i >= len(self.lugares):
            return
        nom, x, y, arch, arch_d = self.lugares[i]
        derrotado = not self.hollows[i].tiene_personajes_disponibles()
        bt = self.bt_img(arch_d if derrotado else arch, (170, 64), lambda n=i: self.entrar_pelea(n))
        cv.create_window(x, y, window=bt)
        self.crear_lugares(cv, i + 1)

    def m_eq(self):
        texto = f"Equipo de {self.jugador.nombre}\n\n"
        def r(i, txt):
            if i >= len(self.jugador.personajes):
                return txt
            p = self.jugador.personajes[i]
            est = "KO" if p.esta_ko() else f"HP {p.vida}/{p.vida_maxima}"
            return r(i + 1, txt + f"{p.nombre} - {est} - ATK {p.ataque} DEF {p.defensa}\n")
        messagebox.showinfo("Equipo", r(0, texto))

    def gano_juego(self):
        return len([h for h in self.hollows if h.tiene_personajes_disponibles()]) == 0

    def entrar_pelea(self, i):
        self.i_lugar = i
        self.hollow_ac = self.hollows[i]
        if not self.hollow_ac.tiene_personajes_disponibles():
            messagebox.showinfo("Ubicación limpia", "Ese Hollow ya fue derrotado.")
            return
        self.jugador.curar_equipo()
        if len(self.jugador.obtener_personajes_disponibles()) < 3:
            messagebox.showerror("Equipo incompleto", "Necesitas al menos 3 personajes disponibles para entrar en pelea.")
            return
        self.m_sel_pelea()

    def m_sel_pelea(self):
        self.limp()
        self.imgs = []
        self.bt_pelea = []
        self.i_pelea_elegidos = []
        self.disp_pelea = self.jugador.obtener_personajes_disponibles()
        cv = self.canvas()
        cv.create_image(0, 0, anchor="nw", image=self.img(self.f_pelea, (self.w, self.h)))

        cv.create_text(
            self.w // 2,
            90,
            text=f"Escoge 3 personajes para pelear en {self.nombre_lugar(self.i_lugar)}",
            fill="#d6c18a",
            font=("Arial", 24, "bold")
        )
        self.etq_sel_pelea = tk.Label(
            self.root,
            text="0/3 seleccionados para la batalla",
            font=("Arial", 14, "bold"),
            bg="#111111",
            fg="#d6c18a",
            bd=0,
            highlightthickness=0
        )
        cv.create_window(self.w // 2, 135, window=self.etq_sel_pelea, width=340, height=32)
        marco = self.marco_scroll(cv, 680, 420, self.w // 2, 405)
        self.crear_bt_personajes(marco, 0, 4, self.disp_pelea, self.elegir_p_pelea, self.bt_pelea)
        cv.create_window(485, 735, window=self.bt_img(self.bt_volver, (180, 54), self.m_mapa))
        cv.create_window(710, 735, window=self.bt_img(self.bt_iniciar_b, (200, 54), self.confirmar_pelea))
        self.act_cont_pelea()

    def elegir_p_pelea(self, i):
        if i in self.i_pelea_elegidos:
            self.i_pelea_elegidos.remove(i)
        elif len(self.i_pelea_elegidos) < 3:
            self.i_pelea_elegidos.append(i)
        else:
            messagebox.showwarning("Límite", "Solo puedes seleccionar 3 personajes para esta pelea.")
            return
        self.pintar_bt(self.bt_pelea, self.i_pelea_elegidos, 0)
        self.act_cont_pelea()

    def confirmar_pelea(self):
        if len(self.i_pelea_elegidos) != 3:
            messagebox.showwarning("Falta dato", "Debes seleccionar exactamente 3 personajes para la batalla.")
            return
        self.personajes_pelea = [self.disp_pelea[i] for i in self.i_pelea_elegidos]
        self.pj = self.personajes_pelea[0]
        self.ph = random.choice(self.hollow_ac.obtener_personajes_disponibles())
        self.m_pelea()

    def equipo_pelea_ok(self):
        return len(self.obtener_pelea_ok()) > 0

    def obtener_pelea_ok(self):
        return [p for p in self.personajes_pelea if not p.esta_ko()]

    def m_pelea(self):
        self.limp()
        self.imgs = []
        self.pelea_activa = False
        self.id_pelea += 1
        cv = self.canvas()
        self.cv_pelea = cv
        cv.create_image(0, 0, anchor="nw", image=self.img(self.f_pelea, (self.w, self.h)))

        self.txt_pts = cv.create_text(25, 25, anchor="nw", text=f"Puntaje: {self.jugador.pts}", fill="white", font=("Arial", 16, "bold"))
        cv.create_text(self.w // 2, 38, text=f"Batalla en {self.nombre_lugar(self.i_lugar)}", fill="#f0e6d2", font=("Arial", 26, "bold"))

        self.img_pj = tk.Label(self.root, bg="#080808", bd=0)
        cv.create_window(170, 500, window=self.img_pj, width=180, height=180)
        self.info_pj = tk.Label(self.root, text="", font=("Arial", 12, "bold"), justify="left", bg="#080808", fg="#f0e6d2", bd=0)
        cv.create_window(180, 670, window=self.info_pj, width=300, height=145)

        cv.create_window(420, 610, window=self.bt_img(self.bt_atacar, (190, 56), self.ini_turno))
        cv.create_window(430, 675, window=self.bt_img(self.bt_cambiar, (230, 56), self.abrir_cambio))
        cv.create_window(425, 740, window=self.bt_img(self.bt_volver, (210, 56), self.volver_mapa_pelea))

        self.img_ph = tk.Label(self.root, bg="#080808", bd=0)
        cv.create_window(990, 155, window=self.img_ph, width=180, height=180)
        self.info_ph = tk.Label(self.root, text="", font=("Arial", 12, "bold"), justify="left", bg="#080808", fg="#f0e6d2", bd=0)
        cv.create_window(990, 325, window=self.info_ph, width=300, height=145)

        self.txt_accion = tk.Label(
            self.root,
            text="¡La batalla ha comenzado!",
            font=("Arial", 13, "bold"),
            justify="left",
            wraplength=360,
            bg="#080808",
            fg="#f0e6d2",
            bd=0
        )
        cv.create_window(960, 690, window=self.txt_accion, width=390, height=110)
        self.act_pelea()
        self.reg("¡La batalla ha comenzado!")

    def act_pelea(self):
        im_pj = self.img(self.pj.archivo_imagen, (160, 160))
        im_ph = self.img(self.ph.archivo_imagen, (160, 160))
        self.img_pj.config(image=im_pj)
        self.img_pj.image = im_pj
        self.img_ph.config(image=im_ph)
        self.img_ph.image = im_ph
        self.info_pj.config(text=(
            f"Jugador: {self.jugador.nombre}\n"
            f"Personaje: {self.pj.nombre}\n"
            f"Rol: {self.pj.rol}\n"
            f"Vida: {self.pj.vida}/{self.pj.vida_maxima}\n"
            f"Ataque: {self.pj.ataque}\n"
            f"Defensa: {self.pj.defensa}"
        ))
        self.info_ph.config(text=(
            f"Hollow: {self.hollow_ac.nombre}\n"
            f"Personaje: {self.ph.nombre}\n"
            f"Rol: {self.ph.rol}\n"
            f"Vida: {self.ph.vida}/{self.ph.vida_maxima}\n"
            f"Ataque: {self.ph.ataque}\n"
            f"Defensa: {self.ph.defensa}"
        ))
        if self.cv_pelea is not None and self.txt_pts is not None:
            self.cv_pelea.itemconfig(self.txt_pts, text=f"Puntaje: {self.jugador.pts}")

    def reg(self, txt):
        if self.txt_accion is not None:
            self.txt_accion.config(text=txt)

    def daño(self, at, df):
        d = at.ataque - df.defensa
        if d < 1:
            d = 1
        crit = random.randint(1, 10)
        if crit == 1:
            d = int(round(d * 1.20))
        return d, crit

    def abrir_cambio(self):
        disp = [p for p in self.obtener_pelea_ok() if p != self.pj]
        if len(disp) == 0:
            messagebox.showinfo("Cambio", "No hay otro personaje disponible para cambiar.")
            return
        top = tk.Toplevel(self.root)
        top.title("Cambiar personaje")
        top.geometry("500x350")
        top.configure(bg="#111111")
        tk.Label(top, text="Seleccione un personaje disponible", font=("Arial", 14, "bold"), bg="#111111", fg="#d6c18a").pack(pady=10)
        lista = tk.Listbox(top, width=55, height=10, font=("Arial", 11))
        lista.pack(pady=10)
        self.llenar_lista(lista, disp, 0)

        def ok():
            elegido = lista.curselection()
            if not elegido:
                messagebox.showwarning("Cambio", "Debe seleccionar un personaje.")
                return
            self.pj = disp[elegido[0]]
            self.reg(f"{self.jugador.nombre} cambió a {self.pj.nombre}.")
            self.act_pelea()
            top.destroy()

        tk.Button(top, text="Confirmar cambio", font=("Arial", 12, "bold"), bg="#90e0ef", command=ok).pack(pady=10)

    def llenar_lista(self, lista, disp, i):
        if i >= len(disp):
            return
        p = disp[i]
        lista.insert(tk.END, f"{p.nombre} | HP {p.vida}/{p.vida_maxima} | ATK {p.ataque} | DEF {p.defensa}")
        self.llenar_lista(lista, disp, i + 1)

    def ini_turno(self):
        if self.pelea_activa:
            return
        self.pelea_activa = True
        self.turno(1, self.id_pelea)

    def volver_mapa_pelea(self):
        self.pelea_activa = False
        self.id_pelea += 1
        self.jugador.curar_equipo()
        if self.hollow_ac is not None:
            self.hollow_ac.curar_equipo()
        self.m_mapa()

    def ganar_batalla(self, msg):
        self.pelea_activa = False
        self.id_pelea += 1
        self.jugador.curar_equipo()
        messagebox.showinfo("Victoria", msg)
        self.m_mapa()

    def turno(self, paso, idp):
        if idp != self.id_pelea:
            return
        if not self.equipo_pelea_ok():
            self.derrota()
            return
        if not self.hollow_ac.tiene_personajes_disponibles():
            self.pelea_activa = False
            self.reg(f"{self.hollow_ac.nombre} ha sido derrotado.")
            self.jugador.pts += 1
            self.act_pelea()
            self.ganar_batalla(f"¡Derrotaste a {self.hollow_ac.nombre} en {self.nombre_lugar(self.i_lugar)}!")
            return
        if paso == 1:
            self.ataca_jugador(idp)
            return
        if paso == 2:
            self.revisa_ph(idp)
            return
        if paso == 3:
            self.turno_hollow(idp)
            return
        if paso == 4:
            self.revisa_pj()

    def ataca_jugador(self, idp):
        d, crit = self.daño(self.pj, self.ph)
        self.ph.vida = max(0, self.ph.vida - d)
        txt = f"{self.pj.nombre} ataca a {self.ph.nombre} y hace {d} de daño."
        if crit:
            txt += " ¡Golpe crítico!"
        self.reg(txt)
        self.act_pelea()
        self.root.after(700, lambda: self.turno(2, idp))

    def revisa_ph(self, idp):
        if self.ph.esta_ko():
            self.reg(f"{self.ph.nombre} quedó en KO.")
            self.capturar(self.jugador, self.hollow_ac, self.ph)
            if self.hollow_ac.tiene_personajes_disponibles():
                self.ph = random.choice(self.hollow_ac.obtener_personajes_disponibles())
                self.reg(f"{self.hollow_ac.nombre} envía a {self.ph.nombre}.")
                self.act_pelea()
                self.root.after(700, lambda: self.turno(3, idp))
            else:
                self.pelea_activa = False
                self.jugador.pts += 1
                self.reg(f"{self.hollow_ac.nombre} ya no tiene personajes.")
                self.act_pelea()
                self.ganar_batalla(f"¡Ganaste la batalla en {self.nombre_lugar(self.i_lugar)}!")
            return
        self.root.after(700, lambda: self.turno(3, idp))

    def turno_hollow(self, idp):
        if not self.hollow_ac.tiene_personajes_disponibles():
            self.pelea_activa = False
            self.m_mapa()
            return
        disp = self.hollow_ac.obtener_personajes_disponibles()
        puede_cambiar = len(disp) > 1 and random.choice([True, False])
        candidatos = [p for p in disp if p != self.ph]
        if puede_cambiar and candidatos:
            self.ph = random.choice(candidatos)
            self.reg(f"{self.hollow_ac.nombre} cambió a {self.ph.nombre}.")
            self.act_pelea()
            self.root.after(700, lambda: self.turno(4, idp))
            return
        d, crit = self.daño(self.ph, self.pj)
        self.pj.vida = max(0, self.pj.vida - d)
        txt = f"{self.ph.nombre} ataca a {self.pj.nombre} y hace {d} de daño."
        if crit:
            txt += " ¡Golpe crítico!"
        self.reg(txt)
        self.act_pelea()
        self.root.after(700, lambda: self.turno(4, idp))

    def revisa_pj(self):
        if self.pj.esta_ko():
            self.reg(f"{self.pj.nombre} quedó en KO.")
            if self.equipo_pelea_ok():
                self.pj = self.obtener_pelea_ok()[0]
                self.reg(f"{self.jugador.nombre} envía a {self.pj.nombre}.")
                self.act_pelea()
                self.pelea_activa = False
                return
            self.derrota()
            return
        self.pelea_activa = False

    def derrota(self):
        self.pelea_activa = False
        messagebox.showerror("Derrota", "Los 3 personajes que escogiste quedaron en KO. Fin del juego.")
        self.m_ini()

    def capturar(self, ganador, perdedor, p_derrotado):
        if p_derrotado in perdedor.personajes:
            perdedor.personajes.remove(p_derrotado)
        cap = p_derrotado.copiar()
        cap.curar_completo()
        ganador.personajes.append(cap)
        ganador.pts += 1
        self.reg(f"{ganador.nombre} capturó a {cap.nombre}. Su vida fue restablecida a {cap.vida_maxima}.")
        self.act_pelea()


root = tk.Tk()
juego = Juego(root)
root.mainloop()
