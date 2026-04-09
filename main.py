import moviepy
from moviepy import concatenate_videoclips
import os

clipsPath = r"C:\Users\retra\OneDrive\Escritorio\Main\Code\clips"
transitionVideo = moviepy.VideoFileClip(os.path.join(r"C:\Users\retra\OneDrive\Escritorio\Main\Code\lazy-clip\transition.mp4")).resized(new_size=(1920, 1080))
clipsRaw = os.listdir(clipsPath)
clips = []

for i,clip in enumerate(clipsRaw):
    if (clip.endswith(".mp4") or clip.endswith(".wav")):
        ruta_completa = os.path.join(clipsPath, clip) 
        video = moviepy.VideoFileClip(ruta_completa).resized(new_size=(1920, 1080)) #Pasar la ruta que es un string al tipo videoFileClip
        clips.append(video) #Ese video lo metes en la lista de clips a juntar
        if (i < len(clipsRaw) - 1):
            clips.append(transitionVideo)


final_video = concatenate_videoclips(clips, method="compose") #Unimos todos los clips en uno
#Renderizamo'
final_video.write_videofile(
    filename = "Final Video.mp4", 
    codec = "libx264",
    audio_bitrate = "320k", 
    threads = 8, 
    preset = "medium",
    fps = 30
    ) 

#----LIBERAMOS MEMORIA :p -------------------------------------
final_video.close() # Liberamos cualquier recurso extra que haya estado en uso
for v in clips:
    v.close()
#--------------------------------------------------------------