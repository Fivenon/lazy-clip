import customtkinter as ctk
import threading

# Configuracion del tema visual
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

class AppVideo(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lazy Clip")
        self.geometry("1200x700") #Tamaño por defecto de la ventana

        # --- Variables de estado ---
        self.ruta_carpeta = ctk.StringVar(value="No seleccionada")

        # --- UI (Layout) ---
        titleFrame = ctk.CTkFrame(self, fg_color="#0D1117", height=70, corner_radius=0)
        titleFrame.pack(side="top", fill="x")
        titleFrame.pack_propagate(False) 
        
        self.label_titulo = ctk.CTkLabel(titleFrame, text="Editor de Clips Automatizado", font=("Arial", 20))
        self.label_titulo.pack(side="left", padx=30)

        # ----
        mainFrame = ctk.CTkFrame(self, fg_color="#161B22", corner_radius=0)
        mainFrame.pack(fill="both", expand=True)
        mainFrame.pack_propagate(True) 

        leftFrame = ctk.CTkFrame(mainFrame, fg_color="transparent", corner_radius=0)
        leftFrame.pack(side="left", fill="both", expand=True)
        rightFrame = ctk.CTkFrame(mainFrame, fg_color="transparent", corner_radius=0)
        rightFrame.pack(side="right", fill="both", expand=True)

        self.boton_seleccionar = ctk.CTkButton(leftFrame, width=200,height=50, text="Seleccionar Carpeta", command=self.seleccionar_carpeta)
        self.boton_seleccionar.grid(row=1,column=0, padx=10, pady=20)

        self.label_ruta = ctk.CTkLabel(leftFrame, textvariable=self.ruta_carpeta)
        self.label_ruta.grid(row=2,column=0)

        # ----
        bottomFrame = ctk.CTkFrame(self, fg_color="#0D1117", height=65,corner_radius=0)
        bottomFrame.pack(side="bottom", fill="x")
        bottomFrame.pack_propagate(False)

        self.boton_render = ctk.CTkButton(bottomFrame,width=200, text="INICIAR RENDER", fg_color="green", hover_color="darkgreen", command=self.ejecutar_render)
        self.boton_render.pack(side="left",padx=10, pady=5,fill="y")

    def seleccionar_carpeta(self):
        print("AA")

    def ejecutar_render(self):
        print("BB")

# Punto de entrada
if __name__ == "__main__":
    app = AppVideo()
    app.mainloop()      