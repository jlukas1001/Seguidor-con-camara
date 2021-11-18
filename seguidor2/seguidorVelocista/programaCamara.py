import cv2
import numpy as np
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)

captura = cv2.VideoCapture(0)
captura.set(cv2.CAP_PROP_FPS,90)

captura.set(cv2.CAP_PROP_FRAME_WIDTH,320)
captura.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

#La resolucion de la camara es 640x480 ------> Tamaño de la ventana openCv

anchoVentana = 320
altoVentana = 240
mitadVentana = anchoVentana//2
tolerancia = 10

promAntX = 0


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

def grabarVideo():
	ret,frame = captura.read()
	return frame
	
def filtrar(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    th, img_bw = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    rect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    aux = cv2.morphologyEx(img_bw, cv2.MORPH_DILATE, rect)
    out = aux - img_bw
    return (out,img_bw)

	
def extraerLinea(canny):
	mascara = cv2.findNonZero(canny)
	return mascara
	
def puntosImportantesVentana(frame):	
	cv2.line(frame,(mitadVentana-tolerancia,0),(mitadVentana-tolerancia,altoVentana),(255,255,0),3)#Linea media de la pantalla
	cv2.line(frame,(mitadVentana+tolerancia,0),(mitadVentana+tolerancia,altoVentana),(255,255,0),3)#Linea media de la pantalla
	
	for i in range(0,240,50): # Lineas delimitadoras (zonas de estudio)		
		cv2.line(frame,(0,i),(320,i),(0,0,255),2)


def zona1(frame,mascara):
	global promAntX

	promX = (mascara[:96,0,0].sum())//96
	promY = (mascara[:96,0,1].sum())//96

	if(promX > promAntX+5 or promX < promAntX-5):		
		cv2.circle(frame,(promX,25),3,(0,10,254),-1)
		cv2.line(frame,(promX-tolerancia,0),(promX-tolerancia,50),(0,0,255),3)
		cv2.line(frame,(promX+tolerancia,0),(promX+tolerancia,50),(0,0,255),3)
		promAntX = promX
	else:
		cv2.circle(frame,(promAntX,25),3,(0,10,254),-1)
		cv2.line(frame,(promAntX-tolerancia,0),(promAntX-tolerancia,50),(0,0,255),3)
		cv2.line(frame,(promAntX+tolerancia,0),(promAntX+tolerancia,50),(0,0,255),3)	
		

		if((promAntX-tolerancia)- (mitadVentana-tolerancia) < -23):
			movimientoMotores(20,30) # Mizq, Mder
			print("Aumentar motor Derecho")
		elif((promAntX-tolerancia)- (mitadVentana-tolerancia) > 23):
			movimientoMotores(30,20) # Mizq, Mder
			print("Aumentar motor Izquierdo")
		else:
			movimientoMotores(30,30) # Mizq, Mder
			print("esta centrado")
	
def mostrarVentanas(frame,canny,umbralizada):
	cv2.imshow("Video Color",frame)
	cv2.imshow("Video Canny",canny)
	#cv2.imshow("Video umbralizado",umbralizada)
	
def movimientoMotores(vD,vI):
	
	GPIO.output(motorA1, False)
	GPIO.output(motorA2, True)
	
	GPIO.output(motorB1, True)
	GPIO.output(motorB2, False)
	
	GPIO.output(standBy, True)
		
	intensidadA.ChangeDutyCycle(vD) # Motor Derecho
	intensidadB.ChangeDutyCycle(vI) # Motor Izquierdo

def programaPrincipal():
	contador = []
	while True:
		tiempoInicial = time.time() 
		
		frame = grabarVideo()			
		canny,umbralizada = filtrar(frame)
		mascara = extraerLinea(canny)	
		puntosImportantesVentana(frame)
		
		zona1(frame,mascara)
		
		mostrarVentanas(frame,canny,0)
		
		tiempoFinal = time.time()
		contador.append(tiempoFinal-tiempoInicial)
		
		if(cv2.waitKey(1) & 0xFF == ord('q')):
			suma = 0
			final = 0
			for idx,i in enumerate(contador):
				suma += i
				final = idx
			print("{0} medicion(es) y el promedio es: {1}".format(final,suma/final))
			break
		
if __name__ == '__main__':
	programaPrincipal()
	
	captura.release()
	cv2.destroyAllWindows()
