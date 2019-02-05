import RPi.GPIO as GPIO
class Led :
    def __init__(self, number):
        self.number= number
        self.statut = GPIO.LOW
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.number, GPIO.OUT)
        GPIO.output(self.number, self.statut)

    def allumer(self):
        self.statut = GPIO.HIGH
        GPIO.output(self.number, self.statut)
    def eteindre(self):
        self.statut = GPIO.LOW
        GPIO.output(self.number, self.statut)
