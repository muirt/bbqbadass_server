

def NumberOfBytes():
	return 4
	
	
def ProcessBytes(bytes):
	result = None		
	if len(bytes) == NumberOfBytes():
		result = (bytes[0] << 24) | ( bytes[1] << 16) | (bytes[2] << 8) | (bytes[3])
		result >>= 18
		if result & 0x00002000:
			result -= 16384
		result *= 0.25
	
	return int(result)
