import subprocess
import numpy as np

from config import *
import data

def accumulate(path : str, output : str) -> None:
	process = subprocess.Popen(
				"converter.out accumulate " + path + " > " + output,
				shell=True,
	)

def full_predict(path : str, model) -> []:
	r = []
	myinput = data.source_to_np_array(data.get_source(path))
	for i in myinput:
		r += model.predict(np.expand_dims(i, axis=0)).astype(np.uint8).tobytes()
	return r

def build(path : str, predictions : []) -> None:
	predictions = b''.join([i.to_bytes(1, byteorder='big', signed=False) for i in predictions])
	with open("build_file", "wb") as f: f.write(predictions)
	process = subprocess.Popen(
				"converter.out build " + path + " > out.c",
				shell=True,
	)

def cat_build():
	with open("out.c") as f: print(f.read())
