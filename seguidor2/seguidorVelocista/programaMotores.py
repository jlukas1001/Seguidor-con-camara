import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

pwmA = 18
motorA1 = 15
motorA2 = 16

pwmB = 7
motorB1 = 11
motorB2 = 13

standBy = 12

GPIO.setup(pwmA,GPIO.OUT)
GPIO.setup(motorA1,GPIO.OUT)
GPIO.setup(motorA2,GPIO.OUT)

GPIO.setup(pwmB,GPIO.OUT)
GPIO.setup(motorB1,GPIO.OUT)
GPIO.setup(motorB2,GPIO.OUT)

GPIO.setup(standBy,GPIO.OUT)

intensidadA = GPIO.PWM(pwmA,100)
intensidadB = GPIO.PWM(pwmB,100)

intensidadA.start(0)
intensidadB.start(0)


def movimientoMotores(vD,vI):
	
	GPIO.output(motorA1, False)
	GPIO.output(motorA2, True)
	
	GPIO.output(motorB1, True)
	GPIO.output(motorB2, False)
	
	GPIO.output(standBy, True)
		
	intensidadA.ChangeDutyCycle(vD) # Motor Derecho
	intensidadB.ChangeDutyCycle(vI) # Motor Izquierdo

