import time
import math
import sys
import os

if __name__ == "__main__":
	runtime = 200
	totalSeconds = float(sys.argv[1])
	if(totalSeconds < runtime):
		runtime = totalSeconds
		iterations = 1
	else:
		iterations = math.ceil(float(totalSeconds) / runtime)
	
	for i in range(0, iterations):
		os.system("python3 crawler.py " + str(runtime))
		#os.system("python3 readJSON.py ")
		time.sleep(10)
		
