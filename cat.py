import RPi.GPIO as GPIO 
import time 
from Led import Led 
from time import sleep 
from flask import Flask 
from flask_socketio import SocketIO, send, emit 
from flask import render_template 
import threading


app = Flask(__name__)
socketio = SocketIO(app)
is_running = True
is_blinking = False
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led = Led(24)
# Initialisation de notre GPIO 17 pour recevoir un signal
# Contrairement à nos LEDs avec lesquelles on envoyait un signal

def stop_the_cat():
    buzzer = 22
    GPIO.setup(buzzer, GPIO.OUT)
    broche=17
    GPIO.setup(broche, GPIO.IN)
    global is_blinking
    is_blinking= False
    currentstate = 0
    previousstate = 0
    # Boucle infini jusqu'à CTRL-C
    if is_running==True:
        while is_running:
            # Lecture du capteur
            currentstate = GPIO.input(broche)
            # Si le capteur est déclenché
            if currentstate == 1 and previousstate == 0:
                print("Mouvement détecté !")
                GPIO.output(buzzer, GPIO.HIGH)
                sleep(0.2)
                GPIO.output(buzzer, GPIO.LOW)
                message = 'Le chat a trépassé votre territoire 🙀'
                socketio.emit('alert', message, Broadcast=True)
        # En enregistrer l'état
                previousstate = 1
        # Si le capteur est s'est stabilisé
            elif currentstate == 0 and previousstate == 1:
                print("  Prêt")
                message = "Tout va bien"
                previousstate = 0
            # On attends 10ms
                time.sleep(0.01)
        
    else:
        return render_template('index.html')
read_messages = threading.Thread(target=stop_the_cat)
@app.route("/")
def index():
    global is_running
    is_running  = True
    if read_messages.is_alive():
        return 
    else:
        global read_messages
        read_messages = threading.Thread(target=stop_the_cat)
        read_messages.start()
        print("début de la fonction")
    return render_template('index.html')

def distract_the_cat():
    global led
    i= 30
    global is_blinking
    is_blinking = True
    print("arrêt de la fonction mouvement")
    while i > 0 and is_blinking:
        led.allumer()
        time.sleep(1)
        led.eteindre()
        time.sleep(1)
        i = i-1
    led.eteindre()

distract_cat = threading.Thread(target=distract_the_cat)
@app.route("/test")
def test():
    global is_running
    is_running  = False
    if distract_cat.is_alive():
        return render_template('test.html')
    else:
        global distract_cat
        distract_cat = threading.Thread(target=distract_the_cat)
        distract_cat.start()
        print("début de la fonction")
    return render_template('test.html')
