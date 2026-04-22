import webview
import threading
import main
import json
import os
import sys

# Cosas de importacion IDK
def resource_path(relative_path):
    """ Obtiene la ruta absoluta de los recursos, compatible con PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class ProyectosAPI:

    def seleccionar_carpeta(self):
        result = window.create_file_dialog(webview.FileDialog.FOLDER)
        if result:
            ruta_real = result[0]
            main.clipsPath = ruta_real #aca asignamos el resultado de la ruta a la variable de MAIN :o
            ruta_para_js = json.dumps(ruta_real) #Para que JS no se vuelva loco con los caracteres
            window.evaluate_js(f"document.getElementById('path-text').innerText = {ruta_para_js}")

            files = os.listdir(ruta_real)
            valid_clips = [f for f in files if f.lower().endswith(('.mp4', '.wav'))]
            clipsQuantity = len(valid_clips)
            print(clipsQuantity)
            window.evaluate_js(f"document.getElementById('clips-found').innerText = 'Clips encontrados: {clipsQuantity}'")
    def iniciar_render(self):
        threading.Thread(target=self._ejecutar_proceso, daemon=True).start()
    def _ejecutar_proceso(self):
        try:
            window.evaluate_js("document.getElementById('render-button').disabled = true")
            window.evaluate_js("document.getElementById('select-button').disabled = true")
            window.evaluate_js("document.getElementById('gpu-switch').disabled = true")

            main.preparar_clips()
            lista_fotos = main.get_frames() 
            previews_json = json.dumps(lista_fotos)
            window.evaluate_js(f"""
                if (window.rotarInterval) clearInterval(window.rotarInterval);

                var previews = {previews_json};
                var index = 0;
                var imgElement = document.getElementById('preview');

                function rotarImagen() {{
                    if (previews.length > 0) {{
                        imgElement.src = previews[index] + "?t=" + new Date().getTime();
                        index = (index + 1) % previews.length;
                    }}
                }}

                rotarImagen();
                // Guardamos el ID en window para poder limpiarlo después
                window.rotarInterval = setInterval(rotarImagen, 4000);                   
            """)
            
            window.evaluate_js("""
                window.actualizarBarra = function(valor, transcurrido, restante) {
                let barra = document.getElementById('barra-progreso');
                let tiempos = document.getElementById('progreso-text');
                if (barra) 
                    {
                    barra.style.width = valor + '%';
                    }
                if (tiempos) {
                    tiempos.innerText = 'Transcurrido: ' + transcurrido + '  |  Restante: ' + restante;
                }
                };
                window.actualizarBarra(0, '00:00', '--:--');  
            """)
            
            main.render_video(window)
            
        except Exception as e: 
            error_msg = json.dumps(str(e))
            window.evaluate_js(f"alert('Error: ' + {error_msg})")
        finally:
            window.evaluate_js("document.getElementById('render-button').disabled = false")
            window.evaluate_js("document.getElementById('select-button').disabled = false")
            window.evaluate_js("document.getElementById('gpu-switch').disabled = false")
            
            # DETENER IMAGENES
            window.evaluate_js("""
                if (window.rotarInterval) {
                    clearInterval(window.rotarInterval);
                    window.rotarInterval = null;
                }
                document.getElementById('preview').src = 'No preview image.jpg';
            """)
                        
    def toggle_gpu(self, valor_switch):
        if valor_switch:
            main.use_gpu = True
        else:
            main.use_gpu = False      

api = ProyectosAPI()
window = webview.create_window(
    title="Lazy Clip",
    url=resource_path("index.html"),
    js_api=api,
    width=900,
    height=650,
    min_size=(900,650)
)

if __name__ == "__main__":
    webview.start()