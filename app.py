from flask import Flask, render_template, request
import requests
import datetime

API_KEY = "fd13d5a771ecbb7a7259757162a3505a"

app = Flask(__name__)

class Clima:
    def __init__(self, ciudad, api_key=API_KEY, unidades='metric', idioma='es'):
        self.ciudad = ciudad
        self.api_key = api_key
        self.unidades = unidades
        self.idioma = idioma
        self.url = (
            f"http://api.openweathermap.org/data/2.5/weather?q={self.ciudad}"
            f"&appid={self.api_key}&units={self.unidades}&lang={self.idioma}"
        )

    def obtener_datos(self):
        try:
            respuesta = requests.get(self.url)
            if respuesta.status_code == 200:
                return respuesta.json()
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
        return None

    def procesar_datos(self, datos):
        if datos:
            try:
                temperatura = datos['main']['temp']
                temp_max = datos['main']['temp_max']
                temp_min = datos['main']['temp_min']
                descripcion = datos['weather'][0]['description']
                humedad = datos['main']['humidity']
                viento = datos['wind']['speed']
                icono = datos['weather'][0]['icon']
                salida_sol = self.convertir_hora(datos['sys']['sunrise'])
                puesta_sol = self.convertir_hora(datos['sys']['sunset'])

                return {
                    "nombre_ciudad": datos['name'],
                    "pais": datos['sys']['country'],
                    "temperatura": temperatura,
                    "temp_max": temp_max,
                    "temp_min": temp_min,
                    "descripcion": descripcion.capitalize(),
                    "humedad": humedad,
                    "viento": viento,
                    "icono": icono,
                    "salida_sol": salida_sol,
                    "puesta_sol": puesta_sol
                }
            except KeyError as e:
                print(f"Error procesando datos: {e}")
        return None

    def convertir_hora(self, unix_timestamp):
        return datetime.datetime.utcfromtimestamp(unix_timestamp).strftime('%H:%M:%S')

def saludo_dinamico():
    hora = datetime.datetime.now().hour
    if hora < 12:
        return "¡Buenos días!"
    elif hora < 18:
        return "¡Buenas tardes!"
    return "¡Buenas noches!"

@app.route("/", methods=["GET", "POST"])
def index():
    clima_info = None
    saludo = saludo_dinamico()
    if request.method == "POST":
        ciudad = request.form.get("ciudad")
        if ciudad:
            clima = Clima(ciudad)
            datos_api = clima.obtener_datos()
            clima_info = clima.procesar_datos(datos_api)
    return render_template("index.html", clima_info=clima_info, saludo=saludo)

if __name__ == "__main__":
    app.run(debug=True)