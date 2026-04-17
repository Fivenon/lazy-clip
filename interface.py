import webview
import threading
import main
import json



class ProyectosAPI:

    def seleccionar_carpeta(self):
        result = window.create_file_dialog(webview.FileDialog.FOLDER)
        if result:
            ruta_real = result[0]
            main.clipsPath = ruta_real
            ruta_para_js = json.dumps(ruta_real) #Para que JS no se vuelva loco con los caracteres
            window.evaluate_js(f"document.getElementById('path-text').innerText = {ruta_para_js}")


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