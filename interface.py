import webview
import threading
import main
import json
import os

class ProyectosAPI:

    def seleccionar_carpeta(self):
        result = window.create_file_dialog(webview.FileDialog.FOLDER)
        if result:
            ruta_real = result[0]
            main.clipsPath = ruta_real #aca asignamos el resultado de la ruta a la variable de MAIN :o
            ruta_para_js = json.dumps(ruta_real) #Para que JS no se vuelva loco con los caracteres
            window.evaluate_js(f"document.getElementById('path-text').innerText = {ruta_para_js}")

            files = main.os.listdir(main.clipsPath)
            valid_clips = [f for f in files if f.lower().endswith(('.mp4,' '.wav'))]
            clipsQuantity = len(valid_clips)
            print(clipsQuantity)
            window.evaluate_js(f"document.getElementById('clips-found').innerText = 'Cantidad de clips encontrados: {clipsQuantity}'  ")

    def iniciar_render(self):
        threading.Thread(target=self._ejecutar_proceso, daemon=True).start()
    def _ejecutar_proceso(self):
        try:
            main.render_video()
        except Exception as e:
            window.evaluate_js(f"alert('Error: {str(e)}')")

api = ProyectosAPI()
window = webview.create_window(
    title="Lazy Clip",
    url="index.html",
    js_api=api,
    width=900,
    height=600
)

if __name__ == "__main__":
    webview.start()