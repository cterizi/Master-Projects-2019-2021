import sys
import os

if __name__ == "__main__":
	start_N = 500
	end_N = 10000
	step = 500

	while(True):
		if(start_N > end_N):
			break
		os.system("python3 FM_AMS.py " + sys.argv[1] + " 2 " + str(start_N))
		start_N = start_N + step
