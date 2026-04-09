import customtkinter as ctk
from tkinter import filedialog
from proglog import ProgressBarLogger
import threading
import main

# Configuracion del tema visual
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

class AppVideo(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lazy Clip")
        self.geometry("900x600") #Tamaño por defecto de la ventana

        # --- Variables de estado ---
        self.ruta_carpeta = ctk.StringVar(value="No seleccionada")

        # --- UI (Layout) ---
        titleFrame = ctk.CTkFrame(self, fg_color="#0D1117", height=70, corner_radius=0)
        titleFrame.pack(side="top", fill="x")
        titleFrame.pack_propagate(False) 
        
        #Dentro de titleFrame
        self.label_titulo = ctk.CTkLabel(titleFrame, text="Editor de Clips Automatizado", font=("Arial", 20))
        self.label_titulo.pack(side="left", padx=30)

        # ----
        mainFrame = ctk.CTkFrame(self, fg_color="#161B22", corner_radius=0)
        mainFrame.pack(fill="both", expand=True)
        mainFrame.pack_propagate(True) 

        #Dentro de MainFrame
        leftFrame = ctk.CTkFrame(mainFrame, fg_color="transparent", corner_radius=0)
        leftFrame.pack(side="left", fill="both", expand=True)
        rightFrame = ctk.CTkFrame(mainFrame, fg_color="transparent", corner_radius=0)
        rightFrame.pack(side="right", fill="both", expand=True)

        #Dentro de LeftFrame
        self.boton_seleccionar = ctk.CTkButton(leftFrame, width=200,height=50, text="Seleccionar Carpeta", command=self.seleccionar_carpeta)
        self.boton_seleccionar.grid(row=1,column=0, padx=10, pady=15)
        self.label_ruta = ctk.CTkLabel(leftFrame, textvariable=self.ruta_carpeta)
        self.label_ruta.grid(row=2,column=0, padx=10,pady=5)

        #Dentro de RightFrame
        self.consola = ctk.CTkTextbox(rightFrame, fg_color="#000000", text_color="#2ecc71", font=("Consolas", 12))
        self.consola.pack(fill="both", expand=True, padx=10, pady=(10, 5))
        self.consola.insert("0.0", "> Sistema iniciado. Esperando carpeta...\n") 
        self.progreso = ctk.CTkProgressBar(rightFrame, orientation="horizontal", mode="determinate")
        self.progreso.pack(fill="x", padx=10, pady=(5, 10))
        self.progreso.set(0) # Empezamos en 0%   
        # ----
        bottomFrame = ctk.CTkFrame(self, fg_color="#0D1117", height=65,corner_radius=0)
        bottomFrame.pack(side="bottom", fill="x")
        bottomFrame.pack_propagate(False)

        self.boton_render = ctk.CTkButton(bottomFrame,width=200, text="INICIAR RENDER", fg_color="green", hover_color="darkgreen", command=self.ejecutar_render)
        self.boton_render.pack(side="left",padx=10, pady=5,fill="y")

    def seleccionar_carpeta(self):
        directory = filedialog.askdirectory()
        main.clipsPath = directory
        self.ruta_carpeta.set(directory)

    # CRAP
    def ejecutar_render(self):
        # Desactivamos el boton
        self.boton_render.configure(state="disabled")
        
        # Creamos el hilo. El target es la función que hace el trabajo pesado.
        hilo = threading.Thread(target=self.proceso_pesado_render, daemon=True)
        hilo.start()

    def proceso_pesado_render(self):
        # Aquí es donde realmente llamás a MoviePy pasándole el Logger
        mi_logger = MyLogger(self) # Instanciamos tu logger pasándole esta app
        main.render_video(logger=mi_logger)
        
        # Cuando termina, avisamos y rehabilitamos el botón
        self.consola.insert("end", "> ¡RENDERIZADO FINALIZADO! \n")
        self.boton_render.configure(state="normal")

class MyLogger(ProgressBarLogger):
        def __init__(self, app_instance):
            super().__init__()
            self.app = app_instance # Guardamos la referencia a tu AppVideo

        def callback(self, **changes):
            # Cada vez que MoviePy avanza, este método se ejecuta
            # 'changes' es un diccionario con la info del progreso
            for state in self.state.values():
                if 'index' in state and 'total' in state:
                    actual = state['index']
                    total = state['total']
                
                    # Hacemos la cuenta que mencionaste
                    progreso_decimal = actual / total
                
                    # Actualizamos la barra de tu app
                    self.app.progreso.set(progreso_decimal)
                
                    #Escribir en consola
                    if actual % 5 == 0:
                        self.app.consola.insert("end", f"> Procesando: {actual}/{total}\n")
                        self.app.consola.see("end") # Auto-scroll
                        
                    self.app.update_idletasks() 



# Punto de entrada
if __name__ == "__main__":
    app = AppVideo()
    app.mainloop()      