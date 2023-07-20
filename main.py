from download_link import link
from download_videos import clean_and_process_videos
from volume import cambiar_volumen, is_video
import json 
import os 

if __name__ == "__main__":
    # Open the JSON file
    with open('configuration.json', 'r') as file:
        data = json.load(file)

    link(data)
    clean_and_process_videos(data)
    
    carpeta = data['path']
    decibelios_deseados = -.3  

  
    if os.path.isdir(carpeta):
        archivos = os.listdir(carpeta)
        for archivo in archivos:
            archivo_path = os.path.join(carpeta, archivo)
            if is_video(archivo_path):
                video_salida = data['path_volume'] + archivo
                video_path = os.path.join(carpeta, archivo)
                cambiar_volumen(video_path, decibelios_deseados, video_salida)
            else:
                print(f"{archivo} no es un archivo de video y será omitido.")