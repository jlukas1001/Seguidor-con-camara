import cv2
import numpy as np
import time

import matplotlib.pyplot as plt

from scipy import interpolate
from scipy.interpolate import griddata
from scipy.interpolate import RectBivariateSpline 

captura = cv2.VideoCapture(0)
captura.set(cv2.CAP_PROP_FPS,90)



captura.set(cv2.CAP_PROP_FRAME_WIDTH,320)
captura.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('salida.avi', fourcc, 20.0, (320,240))

anchoVentana = 320
altoVentana = 240
mitadVentana = anchoVentana//2
tolerancia = 10



def grabarVideo():
	ret,frame = captura.read()

	return frame
	
def filtrar(frame):
	img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	th, img_bw = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	contorno,_ = cv2.findContours(img_bw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	

	for c in contorno:
		x,y,w,h = cv2.boundingRect(c)

		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
		print(w,h)
		#cv2.putText(frame,str((w)),(x,y-40),2,1,(19,244,255),1,cv2.LINE_AA)
		#cv2.putText(frame,str((h)),(x+80,y-40),2,1,(19,244,255),1,cv2.LINE_AA)

	return (contorno,img_bw)
	
def lineaMedia(frame):

	cv2.line(frame,(mitadVentana-tolerancia,0),(mitadVentana-tolerancia,altoVentana),(255,255,0),2)#Linea media de la pantalla
	cv2.line(frame,(mitadVentana+tolerancia,0),(mitadVentana+tolerancia,altoVentana),(255,255,0),2)#Linea media de la pantalla

	for i in range(0,240,50): # Lineas delimitadoras (zonas de estudio)		
		cv2.line(frame,(0,i),(320,i),(0,0,255),2)	
		
	cv2.line(frame,(0,0),(84,240),(0,0,255),2)	
	cv2.line(frame,(100,0),(134,240),(0,0,255),2)	
	cv2.line(frame,(225,0),(189,240),(0,0,255),2)
	cv2.line(frame,(320,0),(230,240),(0,0,255),2)

def mostrarVentanas(frame,umbralizada):
	cv2.imshow("Video Color",frame)
	cv2.imshow("Video umbralizado",umbralizada)


def promedioTiempo(contador):
	suma = 0
	final = 0
	for idx,i in enumerate(contador):
		suma += i
		final = idx
	print("{0} medicion(es) y el promedio es: {1}".format(final,suma/final))	
	
		
def interpolar():
	datos = np.genfromtxt("datosInterpolacion.csv",delimiter=';',dtype=int)
	
	arregloInterpolacion = np.zeros((2,240,320))
	

	x = np.arange(0,320,1)
	y = np.arange(0,240,1)
	
	xx, yy = np.meshgrid(x,y)
	
	valuesX = np.empty((169,))
	valuesY = np.empty((169,))
	
	puntos = np.empty((169,2))

	contador = 0
	for dX,dY,pX,pY in datos[2:,...]:			
		puntos[contador,0] = pX
		puntos[contador,1] = pY
		
		
		valuesX[contador] = dX-64
		valuesY[contador] = dY-64
		
		contador += 1
	


	grid_z0 = griddata(puntos,valuesX, (xx,yy), method='cubic', rescale=True)
	grid_z1 = griddata(puntos,valuesY, (xx,yy), method='nearest', fill_value=True)

	plt.imshow(grid_z0)
	plt.colorbar()
	
	plt.show()
	plt.colorbar()

def programaPrincipal():
	contador = []
	while True:
		tiempoInicial = time.time() 
		
		frame = grabarVideo()	
				
		contorno,umbralizada = filtrar(frame)
		#lineaMedia(frame)
		mostrarVentanas(frame,umbralizada)	
		tiempoFinal = time.time()
		contador.append(tiempoFinal-tiempoInicial)
		
		if(cv2.waitKey(1) & 0xFF == ord('q')):
			promedioTiempo(contador)
			break
			
			
if __name__ == '__main__':
	#programaPrincipal()
	interpolar()
	captura.release()
	cv2.destroyAllWindows()

	
