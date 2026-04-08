import moviepy
from moviepy import concatenate_videoclips
import os

clipsPath = r"C:\Users\retra\OneDrive\Escritorio\Main\Code\clips"
clipsRaw = os.listdir(clipsPath)
clips = []

for clip in clipsRaw:
    if (clip.endswith(".mp4") or clip.endswith(".wav")):
        ruta_completa = os.path.join(clipsPath, clip) 
        video = moviepy.VideoFileClip(ruta_completa) #Pasar la ruta que es un string al tipo videoFileClip
        clips.append(video) #Ese video lo metes en la lista de clips a juntar

final_video = concatenate_videoclips(clips, method="compose") #Unimos todos los clips en uno
#Renderizamo'
final_video.write_videofile(
    filename="Final Video.mp4", 
    codec="libx264", 
    threads = 6, 
    preset="medium",
    fps=30
    ) 

#----LIBERAMOS MEMORIA :p -------------------------------------
final_video.close() # Liberamos cualquier recurso extra que haya estado en uso
for v in clips:
    v.close()
#--------------------------------------------------------------