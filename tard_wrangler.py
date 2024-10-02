import subprocess
import numpy as np

from config import *

def accumulate(path : str, output : str) -> None:
	process = subprocess.Popen(
				"converter.out accumulate " + path + " > " + output,
				shell=True,
	)

def build(path : str, prediction : np.array):
	with open("build_file", "wb") as file:
		file.write(prediction)
	process = subprocess.Popen(
				"converter.out build " + path + " > out.c",
				shell=True,
	)
