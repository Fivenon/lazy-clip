import moviepy
from moviepy import concatenate_videoclips
import os
import psutil


clipsPath = ""
transitionVideo = moviepy.VideoFileClip(os.path.join(r"transition.mp4")).resized(new_size=(1920, 1080))
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




def render_video():
    global clips
    clips = []
    
    for i,clip in enumerate(selec_folder()):
      if (clip.endswith(".mp4") or clip.endswith(".wav")):
            ruta_completa = os.path.join(clipsPath, clip)
            video = moviepy.VideoFileClip(ruta_completa) #Pasar la ruta que es un string al tipo videoFileClip
            if video.size != [1920, 1080]: 
                video.resized(new_size=(1920, 1080)) 
            if video.fps != 30:
                video = video.with_fps(30)    
            clips.append(video) #Ese video lo metes en la lista de clips a juntar
            if (i < len(selec_folder()) - 1):
              clips.append(transitionVideo)
    
    final_video = concatenate_videoclips(clips, method="chain") #Unimos todos los clips en uno
    
    seleccion_codec = "h264_nvenc" if use_gpu else "libx264"
    print(f"Se va a usar el codec: {seleccion_codec}")
    
    #Renderizamo'
    final_video.write_videofile(
        filename = "Final Video.mp4", 
        codec = seleccion_codec,
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
    if not os.path.exists("thumbnails"):
        os.makedirs("thumbnails")
        
    frames = []
    for i, c in enumerate(clips):
        ruta_frames = f"thumbnails/frame_{i}.jpg"
        
        c.save_frame(ruta_frames, t=1)
        frames.append(ruta_frames)
            
    return frames    


            