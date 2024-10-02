import subprocess
import os
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow
from tensorflow import keras
from keras import layers

LINE_WIDTH = 80
MAX_SHIMS  = LINE_WIDTH - 1


def get_data():
	r = []
	def get_source(path : str) -> [str]:
		'''returns source file 3 line batches'''
		r = []
		with open(path, 'r') as file:
			lines = []
			for line in file:
				lines.append(line.strip())
			r = [lines[i:i + 3] for i in range(0, len(lines), 3)]
		return r
	def source_to_np_array(source_batches : []) -> np.array:
		r = []
		for s in source_batches:
			ascii_list = []
			for l in s:
				l = l[:LINE_WIDTH]
				l = l.ljust(LINE_WIDTH)
				l = [ord(i) for i in l]
				ascii_list += l
			n = np.reshape(ascii_list, (3, -1, 1))
			n = np.expand_dims(n, axis=0)
			r.append(n)
		return r
	def get_whitespace(path : str) -> [int]:
		'''XXX returns the whitespace list of every middle line'''
		r = []
		output_file = "muf_file.txt"
		process = subprocess.Popen(
					"converter.out accumulate " + path + " > " + output_file,
					shell=True,
		)
		with open(output_file, 'r') as file:
			for n, line in enumerate(file):
				if ((n + 2) % 3) != 0: continue
				r.append(eval(line))
		return r
	source = source_to_np_array(get_source("in/xop.c"))
	whitespace = get_whitespace("in/xop.c")
	whitespace = [np.array(i) for i in whitespace]
	r = {'in': source, 'out': whitespace}
	return r

data = get_data()
assert len(data['in']) == len(data['in']), "data in and out sizes were inconsistent."
print(data['in'], data['out'])

model = keras.Sequential([
	layers.Conv2D(
		filters=16,
		kernel_size=(3,3),
		strides=(1,1),
		activation='relu',
		padding='valid',
		input_shape=(3,LINE_WIDTH,1)
	),
	#layers.Conv2D(
	#	filters=32,
	#	kernel_size=(3,7),
	#	activation='relu',
	#	padding='valid'
	#),
	#layers.Conv2D(
	#	filters=64,
	#	kernel_size=(3,13),
	#	activation='relu',
	#	padding='valid'
	#),
	layers.Flatten(),
	layers.Dense(64, activation='relu'),
	layers.Dense(MAX_SHIMS, activation='softmax')
])

model.compile(
	optimizer='adam',
	loss='mse',
	metrics=['accuracy']
)

model.fit(data['in'], data['out'],
    verbose=2,
    batch_size=10,
    epochs=50,
    shuffle=True,
)
