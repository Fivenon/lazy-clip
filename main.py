import moviepy
from moviepy import concatenate_videoclips
import os
import psutil


clipsPath = ""
transitionVideo = moviepy.VideoFileClip(os.path.join(r"C:\Users\retra\OneDrive\Escritorio\Main\Code\lazy-clip\transition.mp4")).resized(new_size=(1920, 1080))
threadsAvailable = psutil.cpu_count() - 1 #Cuantos hilos tiene la PC menos uno


print(f"Se van a usar {threadsAvailable} hilos")

def selec_folder():
    if clipsPath and os.path.exists(clipsPath):
        return os.listdir(clipsPath)
    else:
        print("NO HAY NINGUNA CARPETA SELECCIONADA")
        return [] # Devolvemos lista vacía para que el for no explote :P

def render_video():
    clips = []
    
    for i,clip in enumerate(selec_folder()):
      if (clip.endswith(".mp4") or clip.endswith(".wav")):
            ruta_completa = os.path.join(clipsPath, clip) 
            video = moviepy.VideoFileClip(ruta_completa).resized(new_size=(1920, 1080)) #Pasar la ruta que es un string al tipo videoFileClip
            clips.append(video) #Ese video lo metes en la lista de clips a juntar
            if (i < len(selec_folder()) - 1):
              clips.append(transitionVideo)
    

    

    final_video = concatenate_videoclips(clips, method="compose") #Unimos todos los clips en uno

    #Renderizamo'
    final_video.write_videofile(
        filename = "Final Video.mp4", 
        codec = "libx264",
        audio_bitrate = "320k", 
        threads = threadsAvailable, 
        preset = "medium",
        fps = 30
    ) 

    #----LIBERAMOS MEMORIA :p -------------------------------------
    final_video.close() # Liberamos cualquier recurso extra que haya estado en uso
    for v in clips:
        v.close()
    #--------------------------------------------------------------