from pyA10Lime import spi
import time
from pyA10Lime.gpio import gpio
from pyA10Lime.gpio import port
from pyA10Lime.gpio import connector


spi.open("/dev/spidev2.0")


gpio.init() #Initialize module. Always called first


gpio.setcfg(port.PG7, gpio.OUTPUT)		#CS0
gpio.output(port.PG7, gpio.HIGH)

gpio.setcfg(port.PG8, gpio.OUTPUT)		#CS1
gpio.output(port.PG8, gpio.HIGH)

def spi_cs1(level):				##TC AMP
	gpio.output(port.PG8, level)

def spi_cs0(level):				##ADC
	gpio.output(port.PG7, level)


tcBytes = []
for x in range(0,4):
	tcBytes.append(0)

adcBytes = []
for x in range(0,2):
	adcBytes.append(0)


	
while True:
		
	spi_cs1(gpio.LOW)
	tcBytes[x] = spi.read(4) 
	spi_cs1(gpio.HIGH)
	

	spi_cs0(gpio.LOW)
	adcBytes[x] = spi.read(2) 
	spi_cs0(gpio.HIGH)
	
	print " " + str(tcBytes) + " " + str(adcBytes)
	
	
	
	time.sleep(1)
	
	
spi.close() #Close SPI bus
