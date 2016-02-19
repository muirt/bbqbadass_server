#spiDriverLime.py	works with A10 Lime

from pyA10Lime import spi
import gpioDriverLime

def setup():
	spi.open("/dev/spidev2.0")
	gpioDriverLime.setup()
	
def spi_cs(level):				
	gpioDriverLime.outputLevel("CS", level)
	
def read():
	bytes = []	
	spi_cs(0)		
	bytes = spi.read(4)		
	spi_cs(1)
	return bytes
	
def close():
	spi.close() 