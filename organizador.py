import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil

class OrganizadorPro:
    def __init__(self, root):
        self.root = root
        
        self.root.title("Organizador de Archivos")
        self.root.geometry("1100x750")
        self.root.configure(bg="#1e1e1e")

        # --- ICONO PERSONALIZADO ---
        try:
            # Reemplaza 'mi_icono.ico' por el nombre real de tu archivo
            self.root.iconbitmap("organizador.ico")
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}")
        # --------------------------------------

        self.color_bg = "#1e1e1e"
        self.color_fg = "#dddcdc"
        self.color_btn = "#3c3c3c"
        self.color_accent = "#00acc1"

        # Configuración de Paginación
        self.pagina_actual = 0
        self.items_por_pagina = 10
        self.lista_completa_filtrada = []

        self.base_repo = os.path.join(os.path.expanduser("~"), "MiOrganizador")
        self.current_path = self.base_repo
        self.portapapeles = [] 

        if not os.path.exists(self.base_repo):
            os.makedirs(self.base_repo)

        self.aplicar_estilos()
        self.setup_ui()
        self.actualizar_lista()

    def aplicar_estilos(self):
        """Configura los colores globales y elimina el resaltado blanco al pasar el ratón"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configuración base de la tabla
        style.configure("Treeview", 
                        background="#2d2d2d", 
                        foreground="white", 
                        fieldbackground="#2d2d2d", 
                        rowheight=30, 
                        font=("Segoe UI", 10),
                        borderwidth=0)
        
        # Configuración de los encabezados (NOMBRE, TIPO, TAMAÑO)
        style.configure("Treeview.Heading", 
                        background="#3c3c3c", 
                        foreground="white", 
                        relief="flat",
                        font=("Segoe UI", 10, "bold"))

        # ELIMINAR EL COLOR BLANCO AL PASAR EL RATÓN (HOVER)
        # Aquí le decimos que en estado 'active' (mouse encima), mantenga el fondo gris oscuro
        style.map("Treeview", 
                  background=[('selected', '#0078d7'), ('active', '#3c3c3c')],
                  foreground=[('selected', 'white'), ('active', 'white')])
        
        # También quitamos el cambio de color en los encabezados al pasar el ratón
        style.map("Treeview.Heading",
                  background=[('active', '#4a4a4a')],
                  foreground=[('active', 'white')])

    def crear_ventana_oscura(self, titulo, mensaje):
        dialog = tk.Toplevel(self.root)
        dialog.title(titulo)
        dialog.geometry("380x180")
        dialog.configure(bg=self.color_bg)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=mensaje, bg=self.color_bg, fg=self.color_fg, font=("Segoe UI", 10), pady=15).pack()
        entrada = tk.Entry(dialog, bg="#3c3c3c", fg="white", insertbackground="white", relief="flat", width=35, font=("Segoe UI", 10))
        entrada.pack(pady=5, ipady=4)
        entrada.focus_set()

        resultado = {"valor": None}
        def confirmar():
            resultado["valor"] = entrada.get()
            dialog.destroy()

        btn_container = tk.Frame(dialog, bg=self.color_bg)
        btn_container.pack(pady=20)
        tk.Button(btn_container, text="Aceptar", command=confirmar, bg="#0078d7", fg="white", relief="flat", width=12, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_container, text="Cancelar", command=dialog.destroy, bg="#d32f2f", fg="white", relief="flat", width=12, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=10)

        self.root.wait_window(dialog)
        return resultado["valor"]

    def setup_ui(self):
        # Barra de herramientas
        frame_top = tk.Frame(self.root, bg="#252526", pady=10)
        frame_top.pack(fill=tk.X)

        btn_params = {"padx": 12, "pady": 6, "fg": "white", "relief": "flat", "font": ("Segoe UI", 9, "bold"), "cursor": "hand2"}
        tk.Button(frame_top, text="Atrás", bg=self.color_btn, command=self.ir_atras, **btn_params).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Crear Carpeta", bg=self.color_btn, command=self.crear_carpeta, **btn_params).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Subir", bg="#6610f2", command=self.subir_archivo, **btn_params).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Mover", bg=self.color_btn, command=self.cortar_elementos, **btn_params).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Pegar", bg=self.color_btn, command=self.pegar_elementos, **btn_params).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Descargar", bg="#198754", command=self.descargar_seleccion, **btn_params).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Renombrar", bg=self.color_btn, command=self.renombrar_item, **btn_params).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Eliminar", bg="#dc3545", command=self.eliminar_item, **btn_params).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Restablecer", bg=self.color_btn, command=self.restablecer_todo, **btn_params).pack(side=tk.RIGHT, padx=10)

        # Buscador
        frame_search = tk.Frame(self.root, bg=self.color_bg, pady=10)
        frame_search.pack(fill=tk.X)
        tk.Label(frame_search, text="  Buscar:", bg=self.color_bg, fg="#aaaaaa", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.entry_busqueda = tk.Entry(frame_search, bg="#3c3c3c", fg="white", insertbackground="white", relief="flat", width=50, font=("Segoe UI", 11))
        self.entry_busqueda.pack(side=tk.LEFT, padx=10, ipady=3)
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self.reiniciar_y_actualizar())

        # Ruta
        self.lbl_ruta = tk.Label(self.root, text=self.current_path, bg="#333333", fg=self.color_accent, anchor=tk.W, padx=15, pady=5, font=("Consolas", 10))
        self.lbl_ruta.pack(fill=tk.X)

        # Tabla
        self.tree = ttk.Treeview(self.root, columns=("Nombre", "Tipo", "Tamaño"), show="headings", selectmode="extended")
        self.tree.heading("Nombre", text="NOMBRE")
        self.tree.heading("Tipo", text="TIPO")
        self.tree.heading("Tamaño", text="TAMAÑO")
        self.tree.column("Nombre", width=500)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 0))
        self.tree.bind("<Double-1>", self.on_double_click)

        # --- Panel de Paginación (NUEVO) ---
        self.frame_paginacion = tk.Frame(self.root, bg=self.color_bg, pady=15)
        self.frame_paginacion.pack(fill=tk.X)

        self.btn_prev = tk.Button(self.frame_paginacion, text="◀ Anterior", command=self.pagina_anterior, bg=self.color_btn, fg="white", relief="flat", padx=10)
        self.btn_prev.pack(side=tk.LEFT, padx=20)

        self.lbl_paginas = tk.Label(self.frame_paginacion, text="Página 1 de 1", bg=self.color_bg, fg="white", font=("Segoe UI", 10))
        self.lbl_paginas.pack(side=tk.LEFT, expand=True)

        self.btn_next = tk.Button(self.frame_paginacion, text="Siguiente ▶", command=self.pagina_siguiente, bg=self.color_btn, fg="white", relief="flat", padx=10)
        self.btn_next.pack(side=tk.RIGHT, padx=20)

    def reiniciar_y_actualizar(self):
        """Reinicia a la página 1 cuando se busca algo nuevo"""
        self.pagina_actual = 0
        self.actualizar_lista()

    def actualizar_lista(self):
        self.tree.delete(*self.tree.get_children())
        filtro = self.entry_busqueda.get().lower()
        
        # 1. Obtener y filtrar toda la lista de archivos
        try:
            todos_los_items = sorted(os.listdir(self.current_path))
            self.lista_completa_filtrada = []
            
            for entry in todos_los_items:
                tipo = "Carpeta" if os.path.isdir(os.path.join(self.current_path, entry)) else os.path.splitext(entry)[1].upper()
                if filtro in entry.lower() or filtro in tipo.lower():
                    self.lista_completa_filtrada.append(entry)

            # 2. Calcular límites de paginación
            total_items = len(self.lista_completa_filtrada)
            total_paginas = max(1, (total_items + self.items_por_pagina - 1) // self.items_por_pagina)
            
            # Ajustar página actual si queda fuera de rango tras borrar archivos
            if self.pagina_actual >= total_paginas:
                self.pagina_actual = total_paginas - 1

            inicio = self.pagina_actual * self.items_por_pagina
            fin = inicio + self.items_por_pagina
            items_a_mostrar = self.lista_completa_filtrada[inicio:fin]

            # 3. Insertar solo los 10 de la página actual
            for entry in items_a_mostrar:
                full_path = os.path.join(self.current_path, entry)
                es_dir = os.path.isdir(full_path)
                icono = "📁" if es_dir else "📄"
                tipo = "Carpeta" if es_dir else os.path.splitext(entry)[1].upper()
                size = os.path.getsize(full_path) // 1024 
                self.tree.insert("", "end", iid=full_path, values=(f"{icono}  {entry}", tipo, f"{size} KB"))

            # 4. Actualizar etiquetas y botones
            self.lbl_paginas.config(text=f"Página {self.pagina_actual + 1} de {total_paginas} ({total_items} elementos)")
            self.btn_prev.config(state=tk.NORMAL if self.pagina_actual > 0 else tk.DISABLED)
            self.btn_next.config(state=tk.NORMAL if fin < total_items else tk.DISABLED)
            self.lbl_ruta.config(text=f"📂 {self.current_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def pagina_siguiente(self):
        self.pagina_actual += 1
        self.actualizar_lista()

    def pagina_anterior(self):
        self.pagina_actual -= 1
        self.actualizar_lista()

    # --- Resto de funciones ---
    def ir_atras(self):
        if self.current_path != self.base_repo:
            self.current_path = os.path.dirname(self.current_path)
            self.reiniciar_y_actualizar()

    def crear_carpeta(self):
        nombre = self.crear_ventana_oscura("Nueva Carpeta", "Escribe el nombre de la carpeta:")
        if nombre:
            os.makedirs(os.path.join(self.current_path, nombre), exist_ok=True)
            self.actualizar_lista()

    def subir_archivo(self):
        origenes = filedialog.askopenfilenames()
        for o in origenes: shutil.copy(o, self.current_path)
        self.actualizar_lista()

    def eliminar_item(self):
        items = self.tree.selection()
        if items and messagebox.askyesno("Eliminar", "¿Eliminar seleccionados?"):
            for i in items:
                if os.path.isdir(i): shutil.rmtree(i)
                else: os.remove(i)
            self.actualizar_lista()

    def cortar_elementos(self):
        self.portapapeles = self.tree.selection()
        if self.portapapeles: messagebox.showinfo("Mover", "Elementos listos para mover.")

    def pegar_elementos(self):
        if not self.portapapeles: return
        for ruta in self.portapapeles:
            try: shutil.move(ruta, os.path.join(self.current_path, os.path.basename(ruta)))
            except: pass
        self.portapapeles = []
        self.actualizar_lista()

    def descargar_seleccion(self):
        seleccion = self.tree.selection()
        if not seleccion: return
        destino = filedialog.askdirectory()
        if destino:
            for item in seleccion:
                fin = os.path.join(destino, os.path.basename(item))
                if os.path.isdir(item): shutil.copytree(item, fin)
                else: shutil.copy(item, fin)
            messagebox.showinfo("Éxito", "Descarga finalizada.")

    def renombrar_item(self):
        item = self.tree.focus()
        if not item: return
        nuevo = self.crear_ventana_oscura("Renombrar", "Nuevo nombre:")
        if nuevo:
            try:
                os.rename(item, os.path.join(os.path.dirname(item), nuevo))
                self.actualizar_lista()
            except Exception as e: messagebox.showerror("Error", str(e))

    def on_double_click(self, event):
        item = self.tree.focus()
        if not item: return
        if os.path.isdir(item):
            self.current_path = item
            self.reiniciar_y_actualizar()
        else: os.startfile(item)

    def restablecer_todo(self):
        if messagebox.askyesno("Peligro", "Borrar todo?"):
            shutil.rmtree(self.base_repo); os.makedirs(self.base_repo)
            self.current_path = self.base_repo; self.reiniciar_y_actualizar()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrganizadorPro(root)
    root.mainloop()