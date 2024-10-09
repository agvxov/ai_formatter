import subprocess
import shlex
import numpy as np

from config import *
import data

BUILD_FILE = "build_file.bin"

def build(what : str, predictions : []) -> None:
	print(predictions)
	predictions = b''.join([i.to_bytes(1, byteorder='big', signed=False) for i in predictions])
	with open(BUILD_FILE, "wb") as f: f.write(predictions)
	shell_what = shlex.quote(what)
	shell_what = shell_what[0] + '^' + shell_what[1:]
	process = subprocess.Popen(
				"converter.out build " + shell_what + " " + BUILD_FILE,
				shell=True,
				stdout=subprocess.PIPE,
	)
	r, _ = process.communicate()
	r = r.decode('utf-8')
	return r

def full_predict(path : str, normpath : str, model) -> [str]:
	r = ["\n"]
	batches = data.get_source(path, normpath)
	for b in batches:
		b[0] = r[-1]
		myinput = data.source_to_np_array([b])
		prediction = model.predict(myinput).astype(np.uint8).tobytes()
		predicted_string = build(b[1], prediction)
		r += predicted_string + "\n"
	r = ''.join(r)
	return r
