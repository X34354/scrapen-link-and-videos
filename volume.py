from moviepy.editor import VideoFileClip
from moviepy.editor import *
import os

def cambiar_volumen(video_path, decibelios_deseados, video_salida):
    # Validate decibelios_deseados is not None and is a valid number
    if decibelios_deseados is None or not isinstance(decibelios_deseados, (float, int)):
        raise ValueError("decibelios_deseados must be a valid float number.")

    video = VideoFileClip(video_path)

    video = video.audio_normalize()

    video = video.volumex(decibelios_deseados)

    video.write_videofile(video_salida,  codec='libx264', audio_codec='aac',fps=30)

    video.close()

def is_video(file_path):
    video_formats = [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm"]
    ext = os.path.splitext(file_path)[1].lower()
    if ext in video_formats:
        return True
    return False


if __name__ == "__main__":

    carpeta = 'videos_to_narrate/'
    decibelios_deseados = -.3  

    if os.path.isdir(carpeta):
        archivos = os.listdir(carpeta)
        for archivo in archivos:
            archivo_path = os.path.join(carpeta, archivo)
            try: 
                video_salida = 'videos_to_narrate_volume/' + archivo
                video_path = os.path.join(carpeta, archivo)
                cambiar_volumen(video_path, decibelios_deseados, video_salida)
            except:
                print(f"{archivo} error")