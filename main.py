import moviepy
from moviepy import concatenate_videoclips
import os
import psutil
from proglog import ProgressBarLogger
import time
import sys
import tempfile, shutil

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
# Definimos una carpeta temporal fija para esta sesión
THUMBS_DIR = os.path.join(os.getcwd(), "thumbnails")

clipsPath = ""
transitionVideo = moviepy.VideoFileClip(resource_path("transition.mp4")).resized(new_size=(1920, 1080))
transitionVideo = transitionVideo.with_fps(30)
threadsAvailable = psutil.cpu_count() - 1 #Cuantos hilos tiene la PC menos uno
clips = []
use_gpu = False

print(f"Se van a usar {threadsAvailable} hilos")

def selec_folder():
    if clipsPath and os.path.exists(clipsPath):
        return os.listdir(clipsPath)
    else:
        print("NO HAY NINGUNA CARPETA SELECCIONADA")
        return [] # Devolvemos lista vacía para que el for no explote :P

def render_video(ventana_compartida):
    global clips
    clips = []
    
    for i,clip in enumerate(selec_folder()):
      if (clip.endswith(".mp4") or clip.endswith(".wav")):
            ruta_completa = os.path.join(clipsPath, clip)
            video = moviepy.VideoFileClip(ruta_completa) # Pasar la ruta que es un string al tipo videoFileClip
            if video.size != [1920, 1080]: 
                video = video.resized(new_size=(1920, 1080)) 
            if video.fps != 30:
                video = video.with_fps(30)    
            clips.append(video) # Ese video lo metes en la lista de clips a juntar
            if (i < len(selec_folder()) - 1):
              clips.append(transitionVideo)
    
    final_video = concatenate_videoclips(clips, method="chain") # Unimos todos los clips en uno
    total_frames = int(final_video.duration * final_video.fps)  # Calculamos el total de frames ANTES de renderizar
    
    seleccion_codec = "h264_nvenc" if use_gpu else "libx264"
    print(f"Se va a usar el codec: {seleccion_codec}")
    
    #Renderizamo'
    final_video.write_videofile(
        filename = "Final Video.mp4", 
        codec = seleccion_codec,
        audio_bitrate = "320k", 
        threads = threadsAvailable, 
        preset = "medium",
        fps = 30,
        logger = CustomLogger(ventana_compartida, total_frames)
    ) 

    #----LIBERAMOS MEMORIA :p -------------------------------------
    final_video.close() # Liberamos cualquier recurso extra que haya estado en uso
    for v in clips:
        v.close()
    #--------------------------------------------------------------
    
def preparar_clips():
    global clips
    clips = [] # Limpiamos
    for clip in selec_folder():
        if clip.lower().endswith(('.mp4', '.wav')):
            ruta = os.path.join(clipsPath, clip)
            video = moviepy.VideoFileClip(ruta).resized(new_size=(1920, 1080))
            clips.append(video)    
    
    
def get_frames():
    global clips
    if not os.path.exists("THUMBS_DIR"):
        os.makedirs("THUMBS_DIR")
        
    frames = []
    for i, c in enumerate(clips):
        nombre_archivo = f"frame{i}.jpg"
        ruta_frames = os.path.join("THUMBS_DIR", nombre_archivo)
        c.save_frame(ruta_frames, t=1)
        
        frames.append(f"/thumbnails/{nombre_archivo}")
            
    return frames    

def delete_thumbs():
    if os.path.exists("THUMBS_DIR"):
        shutil.rmtree("THUMBS_DIR")

#PROGRESS BAR
class CustomLogger(ProgressBarLogger):
    def __init__(self, api_window, total_frames):
        super().__init__()
        self.window = api_window
        self.ultimo_porcentaje = -1
        self.total_frames = total_frames
        self.tiempo_inicio = None
        
    def callback(self, **changes):
        # Este método es el que MoviePy usa para la consola internamente
        super().callback(**changes)    
    
    # Execute a custom action after the progress bars are updated.
       # Parameters
       # ----------
       # bar
       #   Name/ID of the bar to be modified.
       # attr
       #   Attribute of the bar attribute to be modified
       # value
       #   New value of the attribute
       # old_value (total)
       #   Previous value of this bar's attribute.   
        
    def bars_callback(self, bar, attr, value, total):
        porcentaje = None
        
        if bar == "chunk" and self.total_frames > 0:
            porcentaje = int((value / self.total_frames) * 30)
            porcentaje = min(porcentaje, 30)
        elif bar == "frame_index" and self.total_frames > 0:
            porcentaje = 30 + int((value / self.total_frames) * 70)
            porcentaje = min(porcentaje, 100)
            print(f"chunk {value}/{self.total_frames} = {porcentaje}%") 
            
        if porcentaje is None:
            return
        # TEXTO DEL TIEMPO
        if self.tiempo_inicio is None:
            self.tiempo_inicio = time.time()
            
        tiempo_transcurrido = time.time() - self.tiempo_inicio
            
        if porcentaje > 0:
            tiempo_total_estimado = tiempo_transcurrido / (porcentaje / 100)
            tiempo_restante = int(tiempo_total_estimado - tiempo_transcurrido)
        else:
            tiempo_restante = 0
            
        # Formateamos como mm:ss
        mins_trans = int(tiempo_transcurrido // 60)
        segs_trans = int(tiempo_transcurrido % 60)
        mins_rest = int(tiempo_restante // 60)
        segs_rest = int(tiempo_restante % 60)
        
        # Evitamos saturar la interfaz enviando solo cuando cambia el %
        if porcentaje != self.ultimo_porcentaje:
            self.ultimo_porcentaje = porcentaje
            
            try:
                if self.window:
                    self.window.evaluate_js(f"window.actualizarBarra({porcentaje}, '{mins_trans:02d}:{segs_trans:02d}', '{mins_rest:02d}:{segs_rest:02d}')")
            except:
                pass
            
                
            
                

            