"""
Instituto Tecnológico de Costa Rica
Escuela de Ingeniería en Computadores
Introducción a la programación
2026
Grupo 4
Python 3.14.3
Emanuel Rojas Benavides
Proyecto 1
Descripción: Desarrollar un juego en Python, con una interfaz gráfica simple.
Versión del programa: 3.14.3
Requerimientos del sistema: Python 3 y Pillow
"""

# Importar las librerías 
import tkinter as tk #sirve para la interfaz grafica
from tkinter import messagebox #sirve para mostrar mensajes
from PIL import Image, ImageTk #sirve para modificar imagenes
import os #para trabajar con archivos
import random #sirver para hacer cosas aleatorias
import winsound #sirve para poner sonidos



# Clase que guarda los datos de cada personaje.
class Personaje:
    # Guarda los datos iniciales del personaje.
    def __init__(self, nombre, rol, vida, ataque, defensa, archivo_imagen):
        self.nombre = nombre
        self.rol = rol
        self.vida_maxima = int(vida)
        self.vida = int(vida)
        self.ataque = int(ataque)
        self.defensa = int(defensa)
        self.archivo_imagen = archivo_imagen

    # Revisa si el personaje ya no tiene vida.
    def esta_ko(self):
        return self.vida <= 0

    # Devuelve la vida del personaje al máximo.
    def curar_completo(self):
        self.vida = self.vida_maxima

    # Crea una copia del personaje.
    def copiar(self):
        return Personaje(
            self.nombre,
            self.rol,
            self.vida_maxima,
            self.ataque,
            self.defensa,
            self.archivo_imagen
        )


# Clase que guarda un grupo de personajes y sus puntos.
class Equipo:
    # Guarda el nombre, avatar, personajes y puntaje.
    def __init__(self, nombre, avatar):
        self.nombre = nombre
        self.avatar = avatar
        self.personajes = []
        self.pts = 0

    # Revisa si el equipo todavía tiene personajes vivos.
    def tiene_personajes_disponibles(self):
        return len(self.obtener_personajes_disponibles()) > 0

    # Devuelve solo los personajes que no están en KO.
    def obtener_personajes_disponibles(self):
        return [p for p in self.personajes if not p.esta_ko()]

    # Cura todos los personajes del equipo.
    def curar_equipo(self):
        def r(i):
            if i >= len(self.personajes):
                return
            self.personajes[i].curar_completo()
            r(i + 1)
        r(0)


# Clase principal. Controla ventanas, personajes, mapa, pelea y música.
class Juego:
    # Prepara la ventana, variables, archivos, música y pantalla inicial.
    def __init__(self, root):
        self.root = root
        self.root.title("Coffin")
         # Define el tamaño fijo y el color base de la ventana.
        self.w = 1200
        self.h = 800
        self.root.geometry(f"{self.w}x{self.h}")
        self.root.resizable(False, False)
        self.root.configure(bg="black")

        self.avatar_elegido = tk.StringVar(value="avatar1")
        self.nombre_var = tk.StringVar()
        # Estas listas guardan los personajes escogidos.
        self.i_elegidos = []
        self.i_pelea_elegidos = []
        self.todos_p = self.cargar_p("personajes.txt")# Carga todos los personajes desde el archivo de texto.
        #define todas las imagenes
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
        self.bt_mute_img = "unmute.png"
        self.bt_unmute_img = "mute.png"
        self.m_juego = "song2.wav"
        self.m_batalla = "song1.wav"
        self.mute = False
        self.musica_ac = None
        # Guarda si el sonido está apagado y cuál canción suena.

        self.lugares = [
        # Cada lugar tiene nombre, posición en pantalla e imagen.
            ["Capilla", 616, 202, self.bt_capilla, self.bt_capilla_d],
            ["Patio", 205, 400, self.bt_patio, self.bt_patio_d],
            ["Comedor", 847, 407, self.bt_comedor, self.bt_comedor_d],
            ["Entrada", 614, 640, self.bt_entrada, self.bt_entrada_d],
            ["Biblioteca", 999, 690, self.bt_biblioteca, self.bt_biblioteca_d]
        ]

        self.avatars = [
        # Avatares que puede escoger el jugador.
            ["avatar1", "avatar1.png"],
            ["avatar2", "avatar2.png"],
            ["avatar3", "avatar3.png"]
        ]

        self.hollows = []
        # Borra Hollows anteriores antes de crear nuevos.
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
        # Limpia las imágenes de la pantalla anterior.
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
        # Si se cierra la ventana, también se detiene la música.
        self.play_m(self.m_juego)
        self.m_ini()

    # Devuelve la ruta de una imagen dentro de la carpeta img.
    def ruta_img(self, arch):
        return os.path.join("img", arch)

    # Devuelve la ruta de un sonido dentro de la carpeta sound.
    def ruta_m(self, arch):
        return os.path.join("sound", arch)

    # Lee el archivo de personajes y crea objetos Personaje.
    def cargar_p(self, arch):
        personajes = []
        # Aquí se guardan los personajes que se leen del archivo.
        with open(arch, "r", encoding="utf-8") as f:
        # Abre el archivo de personajes.
            for linea in f:
                linea = linea.strip()
                if linea and not linea.startswith("#"):
                # Ignora líneas vacías o comentadas.
                    p = linea.split("|")
                    if len(p) == 6:
                        personajes.append(Personaje(p[0], p[1], p[2], p[3], p[4], p[5]))
        return personajes

    # Reproduce música en bucle si el mute está apagado.
    def play_m(self, arch):
        self.musica_ac = arch
        # guarda la canción actual.
        if self.mute:
        # Si está en mute, no reproduce música.
            self.stop_m()
            return
        if winsound is not None:
            winsound.PlaySound(
                self.ruta_m(arch),
                winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP
            )

    # Detiene cualquier sonido que se esté reproduciendo
    def stop_m(self):
        if winsound is not None:
            winsound.PlaySound(None, 0)

    # Activa o desactiva el sonido del juego.
    def cambiar_mute(self):
        self.mute = not self.mute
        # Cambia de sonido activo a silencio, o al revés.
        if self.mute:
        # Si está en mute, no reproduce música.
            self.stop_m()
        else:
            self.play_m(self.musica_ac or self.m_juego)
        self.buscar_canvas(self.root.winfo_children(), 0)

    # Busca un Canvas para volver a poner el botón de mute.
    def buscar_canvas(self, lista, i):
        if i >= len(lista):
            return
        if isinstance(lista[i], tk.Canvas):
            self.bt_mute(lista[i])
            return
        self.buscar_canvas(lista, i + 1)

    # Crea el botón de mute sobre el Canvas.
    def bt_mute(self, cv):
        arch = self.bt_unmute_img if self.mute else self.bt_mute_img
        bt = self.bt_img(arch, (54, 54), self.cambiar_mute)
        cv.create_window(1145, 45, window=bt)

    # Abre una imagen, la convierte y le cambia el tamaño.
    def img_pil(self, arch, tam):
        return Image.open(self.ruta_img(arch)).convert("RGBA").resize(tam, Image.LANCZOS)

    # Convierte una imagen para usarla en tkinter y la guarda.
    def img(self, arch, tam):
        im = ImageTk.PhotoImage(self.img_pil(arch, tam))
        # tkinter necesita PhotoImage para mostrar imágenes.
        self.imgs.append(im)
        # Se guarda para evitar que la imagen desaparezca
        return im

    # Crea un botón usando una imagen.
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

    # Borra todos los elementos de la ventana.
    def limp(self):
        elemento = self.root.winfo_children()
        # Toma todos los elementos actuales de la ventana.
        def r(i):
            if i >= len(elemento):
                return
            elemento[i].destroy()
            r(i + 1)
        r(0)

    # Crea el Canvas principal de cada pantalla
    def canvas(self):
        cv = tk.Canvas(self.root, width=self.w, height=self.h, highlightthickness=0, bd=0, bg="black")
        # El Canvas sirve para poner fondo, textos y botones encima.
        cv.pack(fill="both", expand=True)
        return cv

    # Muestra una ventana pequeña con información del juego.
    def m_about(self):
        messagebox.showinfo("About", """
        Instituto Tecnológico de Costa Rica
        Escuela de Ingeniería en Computadores
        Introducción a la programación
        2026
        Grupo 4
        Python 3.14.3
        Emanuel Rojas Benavides
        Proyecto 1
        Descripción: Desarrollar un juego en Python, con una interfaz gráfica simple.
        Versión del programa: 3.14.3
        Requerimientos del sistema: Python 3 y Pillow
        """)

    # Detiene la música y cierra el juego.
    def cerrar(self):
        self.stop_m()
        self.root.destroy()

    # Muestra la pantalla inicial del juego.
    def m_ini(self):
        self.play_m(self.m_juego)
        self.limp()
        self.imgs = []
        # Limpia las imágenes de la pantalla anterior.
        cv = self.canvas()
        cv.create_image(0, 0, anchor="nw", image=self.img(self.f_ini, (self.w, self.h)))
        self.bt_mute(cv)
        cv.create_image(self.w // 2, 210, image=self.img(self.f_titulo, (430, 130)))
        cv.create_window(self.w // 2, 420, window=self.bt_img(self.bt_inicio, (300, 72), self.m_conf))
        cv.create_window(self.w // 2, 505, window=self.bt_img(self.bt_about, (300, 72), self.m_about))
        cv.create_window(self.w // 2, 590, window=self.bt_img(self.bt_salir, (300, 72), self.cerrar))

    # Muestra la pantalla para poner nombre, avatar y personajes.
    def m_conf(self):
        self.play_m(self.m_juego)
        self.limp()
        self.imgs = []
        # Limpia las imágenes de la pantalla anterior.
        self.bt_personajes = []
        self.i_elegidos = []
        cv = self.canvas()
        cv.create_image(0, 0, anchor="nw", image=self.img(self.f_conf, (self.w, self.h)))
        self.bt_mute(cv)

        ent = tk.Entry(
        # Caja donde se escribe el nombre del jugador.
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
        # Texto que muestra cuántos personajes van seleccionados.
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
        # Área con scroll para ver los personajes.
        self.crear_bt_personajes(marco, 0, 3, self.todos_p, self.elegir_p, self.bt_personajes)

        cv.create_window(415, 750, window=self.bt_img(self.bt_atras, (150, 38), self.m_ini))
        cv.create_window(600, 750, window=self.bt_img(self.bt_about, (150, 38), self.m_about))
        cv.create_window(785, 750, window=self.bt_img(self.bt_inicio, (150, 38), self.confirmar_eleccion))
        self.act_cont()

    # Crea los botones para escoger avatar.
    def crear_avatars(self, cv, i, xs):
        if i >= len(self.avatars):
            return
        av_id, arch = self.avatars[i]
        im = self.img(arch, (96, 96))
        # Carga la imagen del avatar.
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

    # Crea un área con barra para subir y bajar.
    def marco_scroll(self, cv, w, h, x, y):
        cont = tk.Frame(self.root, bg="#111111", bd=0, highlightthickness=0)
        # Contenedor general del scroll.
        cv.create_window(x, y, window=cont)
        subcv = tk.Canvas(cont, width=w, height=h, bg="#111111", bd=0, highlightthickness=0)
        barra = tk.Scrollbar(cont, orient="vertical", command=subcv.yview, width=14)
        marco = tk.Frame(subcv, bg="#111111")
        interno = subcv.create_window((0, 0), window=marco, anchor="nw")
        subcv.configure(yscrollcommand=barra.set)

        def config_marco(e):
        # Ajusta el área que se puede mover con la barra.
            subcv.configure(scrollregion=subcv.bbox("all"))

        def config_ancho(e):
            subcv.itemconfig(interno, width=e.width)

        def rueda(e):
        # Permite usar la rueda del mouse.
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

    # Crea los botones de personajes.
    def crear_bt_personajes(self, marco, i, cols, lista, cmd, guardado):
        if i >= len(lista):
            return
        p = lista[i]
        # Personaje actual que se va a mostrar.
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

    # Actualiza el texto de personajes seleccionados.
    def act_cont(self):
        if self.etq_sel is not None:
            self.etq_sel.config(text=f"{len(self.i_elegidos)}/3 seleccionados")

    # Actualiza el texto de personajes seleccionados para pelea.
    def act_cont_pelea(self):
        if self.etq_sel_pelea is not None:
            self.etq_sel_pelea.config(text=f"{len(self.i_pelea_elegidos)}/3 seleccionados para la batalla")

    # Agrega o quita un personaje de la selección inicial.
    def elegir_p(self, i):
        if i in self.i_elegidos:
        # Si ya estaba seleccionado, se quita.
            self.i_elegidos.remove(i)
        elif len(self.i_elegidos) < 3:
        # Si falta espacio, se agrega.
            self.i_elegidos.append(i)
        else:
            messagebox.showwarning("Límite", "Solo puedes seleccionar 3 personajes.")
            return
        self.pintar_bt(self.bt_personajes, self.i_elegidos, 0)
        self.act_cont()

    # Cambia el color de los botones seleccionados.
    def pintar_bt(self, lista, elegidos, i):
        if i >= len(lista):
            return
        if i in elegidos:
        # Si está elegido, se pinta diferente.
            lista[i].config(bg="#4b1b1f", activebackground="#4b1b1f", relief="sunken", bd=3, highlightbackground="#c8a45a")
        else:
            lista[i].config(bg="#1a1717", activebackground="#1a1717", relief="flat", bd=2, highlightbackground="#3a2d24")
        self.pintar_bt(lista, elegidos, i + 1)

    # Revisa nombre y selección, luego crea el equipo del jugador.
    def confirmar_eleccion(self):
        nombre = self.nombre_var.get().strip()
        # Quita espacios antes y después del nombre.
        if not nombre:
        # No deja avanzar sin nombre.
            messagebox.showwarning("Falta dato", "Debes escribir tu nombre.")
            return
        if len(self.i_elegidos) != 3:
        # Obliga a escoger exactamente 3 personajes.
            messagebox.showwarning("Falta dato", "Debes seleccionar exactamente 3 personajes.")
            return
        self.jugador = Equipo(nombre, self.avatar_elegido.get())
        # Crea el equipo del jugador.
        self.jugador.personajes = [self.todos_p[i].copiar() for i in self.i_elegidos]
        self.jugador.pts = 0
        self.crear_hollows()
        self.m_mapa()

    # Crea los equipos enemigos de cada lugar.
    def crear_hollows(self):
        self.hollows = []
        # Borra Hollows anteriores antes de crear nuevos.

        def r(i):
            if i >= len(self.lugares):
                return

            hollow = Equipo(f"Hollow {i + 1}", "x")
            # Crea un Hollow para este lugar.
            elegidos = random.sample(self.todos_p, 3)
            # Escoge 3 personajes aleatorios para el Hollow.
            hollow.personajes = [p.copiar() for p in elegidos]

            self.hollows.append(hollow)
            r(i + 1)

        r(0)

    # Devuelve el nombre del lugar según su índice.
    def nombre_lugar(self, i):
        return self.lugares[i][0]

    # Muestra el mapa con los lugares y el puntaje.
    def m_mapa(self):
        self.play_m(self.m_juego)
        self.limp()
        self.imgs = []
        # Limpia las imágenes de la pantalla anterior.
        self.pelea_activa = False
        cv = self.canvas()
        cv.create_image(0, 0, anchor="nw", image=self.img(self.f_mapa, (self.w, self.h)))
        self.bt_mute(cv)
        cv.create_text(25, 25, anchor="nw", text=f"Puntaje: {self.jugador.pts}", fill="white", font=("Arial", 16, "bold"))
        self.crear_lugares(cv, 0)
        cv.create_window(420, 730, window=self.bt_img(self.bt_ver_eq, (170, 54), self.m_eq))
        cv.create_window(580, 730, window=self.bt_img(self.bt_salir, (170, 54), self.cerrar))
        if self.gano_juego():
            messagebox.showinfo("Victoria", f"¡Felicidades {self.jugador.nombre}!\nHas derrotado a los 5 Hollows.")

    # Coloca los botones de lugares en el mapa.
    def crear_lugares(self, cv, i):
        if i >= len(self.lugares):
            return
        nom, x, y, arch, arch_d = self.lugares[i]
        derrotado = not self.hollows[i].tiene_personajes_disponibles()
        # Revisa si ese lugar ya fue derrotado.
        bt = self.bt_img(arch_d if derrotado else arch, (170, 64), lambda n=i: self.entrar_pelea(n))
        cv.create_window(x, y, window=bt)
        self.crear_lugares(cv, i + 1)

    # Muestra el equipo actual del jugador.
    def m_eq(self):
        texto = f"Equipo de {self.jugador.nombre}\n\n"
        # Texto que se mostrará en la ventana del equipo.
        def r(i, txt):
            if i >= len(self.jugador.personajes):
                return txt
            p = self.jugador.personajes[i]
            est = "KO" if p.esta_ko() else f"HP {p.vida}/{p.vida_maxima}"
            return r(i + 1, txt + f"{p.nombre} - {est} - ATK {p.ataque} DEF {p.defensa}\n")
        messagebox.showinfo("Equipo", r(0, texto))

    # Revisa si todos los Hollows fueron derrotados.
    def gano_juego(self):
        return len([h for h in self.hollows if h.tiene_personajes_disponibles()]) == 0

    # Entra a un lugar y revisa si se puede pelear.
    def entrar_pelea(self, i):
        self.i_lugar = i
        # Guarda cuál lugar fue escogido.
        self.hollow_ac = self.hollows[i]
        if not self.hollow_ac.tiene_personajes_disponibles():
        # Si el Hollow no tiene personajes, gana.
            messagebox.showinfo("Ubicación limpia", "Ese Hollow ya fue derrotado.")
            return
        self.jugador.curar_equipo()
        # Cura al jugador antes de preparar la pelea.
        if len(self.jugador.obtener_personajes_disponibles()) < 3:
            messagebox.showerror("Equipo incompleto", "Necesitas al menos 3 personajes disponibles para entrar en pelea.")
            return
        self.m_sel_pelea()

    # Muestra la pantalla para escoger 3 personajes para batalla.
    def m_sel_pelea(self):
        self.play_m(self.m_juego)
        self.limp()
        self.imgs = []
        # Limpia las imágenes de la pantalla anterior.
        self.bt_pelea = []
        self.i_pelea_elegidos = []
        # Estas listas guardan los personajes escogidos.
        self.disp_pelea = self.jugador.obtener_personajes_disponibles()
        # Solo muestra personajes vivos.
        cv = self.canvas()
        cv.create_image(0, 0, anchor="nw", image=self.img(self.f_pelea, (self.w, self.h)))
        self.bt_mute(cv)
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

    # Agrega o quita personajes para la pelea actual.
    def elegir_p_pelea(self, i):
        if i in self.i_pelea_elegidos:
        # Si ya estaba elegido para pelea, se quita.
            self.i_pelea_elegidos.remove(i)
        elif len(self.i_pelea_elegidos) < 3:
            self.i_pelea_elegidos.append(i)
        else:
            messagebox.showwarning("Límite", "Solo puedes seleccionar 3 personajes para esta pelea.")
            return
        self.pintar_bt(self.bt_pelea, self.i_pelea_elegidos, 0)
        self.act_cont_pelea()

    # Confirma los 3 personajes y escoge el primer enemigo.
    def confirmar_pelea(self):
        if len(self.i_pelea_elegidos) != 3:
            messagebox.showwarning("Falta dato", "Debes seleccionar exactamente 3 personajes para la batalla.")
            return
        self.personajes_pelea = [self.disp_pelea[i] for i in self.i_pelea_elegidos]
        # Guarda los 3 personajes que van a pelear.
        self.pj = self.personajes_pelea[0]
        self.ph = random.choice(self.hollow_ac.obtener_personajes_disponibles())
        # El Hollow inicia con un personaje aleatorio.
        self.m_pelea()

    # Revisa si queda algún personaje vivo en la pelea.
    def equipo_pelea_ok(self):
        return len(self.obtener_pelea_ok()) > 0

    # Devuelve los personajes vivos de la pelea.
    def obtener_pelea_ok(self):
        return [p for p in self.personajes_pelea if not p.esta_ko()]

    # Crea la pantalla de batalla.
    def m_pelea(self):
        self.play_m(self.m_batalla)
        self.limp()
        self.imgs = []
        # Limpia las imágenes de la pantalla anterior.
        self.pelea_activa = False
        self.id_pelea += 1
        # Cambia el número de pelea para evitar turnos viejos.
        cv = self.canvas()
        self.cv_pelea = cv
        cv.create_image(0, 0, anchor="nw", image=self.img(self.f_pelea, (self.w, self.h)))
        self.bt_mute(cv)
        self.txt_pts = cv.create_text(25, 25, anchor="nw", text=f"Puntaje: {self.jugador.pts}", fill="white", font=("Arial", 16, "bold"))
        cv.create_text(self.w // 2, 38, text=f"Batalla en {self.nombre_lugar(self.i_lugar)}", fill="#f0e6d2", font=("Arial", 26, "bold"))

        self.img_pj = tk.Label(self.root, bg="#080808", bd=0)
        # Espacio donde se muestra el personaje del jugador.
        cv.create_window(170, 500, window=self.img_pj, width=180, height=180)
        self.info_pj = tk.Label(self.root, text="", font=("Arial", 12, "bold"), justify="left", bg="#080808", fg="#f0e6d2", bd=0)
        cv.create_window(180, 670, window=self.info_pj, width=300, height=145)

        cv.create_window(420, 610, window=self.bt_img(self.bt_atacar, (190, 56), self.ini_turno))
        cv.create_window(430, 675, window=self.bt_img(self.bt_cambiar, (230, 56), self.abrir_cambio))
        cv.create_window(425, 740, window=self.bt_img(self.bt_volver, (210, 56), self.volver_mapa_pelea))

        self.img_ph = tk.Label(self.root, bg="#080808", bd=0)
        # Espacio donde se muestra el personaje enemigo.
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

    # Actualiza imágenes, vida, datos y puntaje de la pelea.
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

    # Cambia el texto que explica lo que pasó en la pelea.
    def reg(self, txt):
        if self.txt_accion is not None:
            self.txt_accion.config(text=txt)

    # Calcula el daño usando ataque, defensa y posible crítico.
    def daño(self, at, df):
        d = at.ataque - df.defensa
        #ataque menos defensa.
        if d < 1:
        # El daño mínimo siempre es 1.
            d = 1
        crit = random.randint(1, 10)
        if crit == 1:
            d = max(1, int(round(d * 1.20)))
        return d, crit

    # Abre una ventana para cambiar el personaje activo.
    def abrir_cambio(self):
        disp = [p for p in self.obtener_pelea_ok() if p != self.pj]
        # Lista de personajes disponibles para cambiar.
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
            # Revisa qué opción escogió el jugador.
            if not elegido:
                messagebox.showwarning("Cambio", "Debe seleccionar un personaje.")
                return
            self.pj = disp[elegido[0]]
            self.reg(f"{self.jugador.nombre} cambió a {self.pj.nombre}.")
            self.act_pelea()
            top.destroy()

        tk.Button(top, text="Confirmar cambio", font=("Arial", 12, "bold"), bg="#90e0ef", command=ok).pack(pady=10)

    # Llena la lista de personajes disponibles.
    def llenar_lista(self, lista, disp, i):
        if i >= len(disp):
            return
        p = disp[i]
        lista.insert(tk.END, f"{p.nombre} | HP {p.vida}/{p.vida_maxima} | ATK {p.ataque} | DEF {p.defensa}")
        self.llenar_lista(lista, disp, i + 1)

    # Inicia un turno si no hay otro turno activo.
    def ini_turno(self):
        if self.pelea_activa:
        # Evita iniciar dos turnos al mismo tiempo.
            return
        self.pelea_activa = True
        # Marca que el turno está corriendo.
        self.turno(1, self.id_pelea)

    # Cancela la pelea, cura equipos y vuelve al mapa.
    def volver_mapa_pelea(self):
        self.pelea_activa = False
        self.id_pelea += 1
        # Cambia el número de pelea para evitar turnos viejos.
        self.jugador.curar_equipo()
        # Cura al jugador antes de preparar la pelea.
        if self.hollow_ac is not None:
            self.hollow_ac.curar_equipo()
        self.m_mapa()

    # Termina una batalla ganada y vuelve al mapa.
    def ganar_batalla(self, msg):
        self.pelea_activa = False
        self.id_pelea += 1
        # Cambia el número de pelea para evitar turnos viejos.
        self.jugador.curar_equipo()
        # Cura al jugador antes de preparar la pelea.
        messagebox.showinfo("Victoria", msg)
        self.m_mapa()

    # Controla el orden del turno de batalla.
    def turno(self, paso, idp):
        if idp != self.id_pelea:
        # Si cambió la pelea, ignora este turno.
            return
        if paso == 2:
        # Paso 2: se revisa si cayó el enemigo antes de revisar si el Hollow ya no tiene disponibles.
            self.revisa_ph(idp)
            return
        if not self.equipo_pelea_ok():
        # Si no quedan personajes vivos, pierde.
            self.derrota()
            return
        if not self.hollow_ac.tiene_personajes_disponibles():
        # Si el Hollow no tiene personajes, gana.
            self.pelea_activa = False
            self.reg(f"{self.hollow_ac.nombre} ha sido derrotado.")
            self.jugador.pts += 1
            self.act_pelea()
            self.ganar_batalla(f"¡Derrotaste a {self.hollow_ac.nombre} en {self.nombre_lugar(self.i_lugar)}!")
            return
        if paso == 1:
        # Paso 1: ataca el jugador.
            self.ataca_jugador(idp)
            return
        if paso == 3:
        # Paso 3: juega el Hollow.
            self.turno_hollow(idp)
            return
        if paso == 4:
        # Paso 4: se revisa si cayó el jugador.
            self.revisa_pj()

    # Hace que el personaje del jugador ataque.
    def ataca_jugador(self, idp):
        d, crit = self.daño(self.pj, self.ph)
        # Calcula el daño del jugador.
        self.ph.vida = max(0, self.ph.vida - d)
        txt = f"{self.pj.nombre} ataca a {self.ph.nombre} y hace {d} de daño."
        if crit:
            txt += " ¡Golpe crítico!"
        self.reg(txt)
        self.act_pelea()
        self.root.after(700, lambda: self.turno(2, idp))
        # Espera un poco antes del siguiente paso.

    # Revisa si el personaje enemigo quedó en KO.
    def revisa_ph(self, idp):
        if self.ph.esta_ko():
        # Si el enemigo quedó sin vida, se captura.
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

    #turno del Hollow puede cambiar o atacar.
    def turno_hollow(self, idp):
        if not self.hollow_ac.tiene_personajes_disponibles():
        # Si el Hollow no tiene personajes, gana.
            self.pelea_activa = False
            self.m_mapa()
            return
        disp = self.hollow_ac.obtener_personajes_disponibles()
        # Personajes que puede usar el Hollow.
        puede_cambiar = len(disp) > 1 and random.choice([True, False])
        # El Hollow a veces cambia de personaje.
        candidatos = [p for p in disp if p != self.ph]
        if puede_cambiar and candidatos:
            self.ph = random.choice(candidatos)
            self.reg(f"{self.hollow_ac.nombre} cambió a {self.ph.nombre}.")
            self.act_pelea()
            self.root.after(700, lambda: self.turno(4, idp))
            return
        d, crit = self.daño(self.ph, self.pj)
        # Calcula el daño del Hollow.
        self.pj.vida = max(0, self.pj.vida - d)
        txt = f"{self.ph.nombre} ataca a {self.pj.nombre} y hace {d} de daño."
        if crit:
            txt += " ¡Golpe crítico!"
        self.reg(txt)
        self.act_pelea()
        self.root.after(700, lambda: self.turno(4, idp))

    # Revisa si el personaje del jugador quedó en KO.
    def revisa_pj(self):
        if self.pj.esta_ko():
        # Si el personaje del jugador cae, se busca otro.
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

    # Muestra derrota y vuelve al inicio.
    def derrota(self):
        self.pelea_activa = False
        messagebox.showerror("Derrota", "Los 3 personajes que escogiste quedaron en KO. Fin del juego.")
        self.m_ini()

    # Quita el personaje derrotado del perdedor y lo agrega al ganador.
    def capturar(self, ganador, perdedor, p_derrotado):
        if p_derrotado in perdedor.personajes:
            perdedor.personajes.remove(p_derrotado)
        cap = p_derrotado.copiar()
        # Copia el personaje capturado.
        cap.curar_completo()
        ganador.personajes.append(cap)
        # Agrega la copia al equipo ganador.
        if ganador == self.jugador:
            self.personajes_pelea.append(cap)
        # También lo deja disponible en la pelea actual.
        ganador.pts += 1
        self.reg(f"{ganador.nombre} capturó a {cap.nombre}. Su vida fue restablecida a {cap.vida_maxima}.")
        self.act_pelea()


#inicio del programa.
root = tk.Tk()
#Crea la ventana principal.
juego = Juego(root)
root.mainloop()
