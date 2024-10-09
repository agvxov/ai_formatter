from glob import glob
import numpy as np
import pickle
import sys
from sys import argv

from config import *
import tard_wrangler

#MAX_DATA_LIMIT = sys.maxsize
MAX_DATA_LIMIT = 1000

DATASET_FILE = "training_set/dataset-linux.pkl"

def get_source(path : str, normpath : str) -> [str]:
	'''returns source file in $SOURCE_LINE_BATCH_SIZE line batches'''
	r = []
	# read data
	with open(path, 'r') as f: lines = [line[:-1] for line in f]
	with open(normpath, 'r') as f: normlines = [line[:-1] for line in f]
	# pad with empty lines
	for i in range(int((SOURCE_LINE_BATCH_SIZE-1)/2)):
		lines.insert(0, "")
		normlines.append("")
	# batch
	for i in range(len(lines)-1):
		r.append([lines[i]] + normlines[i:i+SOURCE_LINE_BATCH_SIZE-1])
	return r

def source_to_np_array(source_batches : []) -> np.array:
	'''returns image like array from batches'''
	r = []
	for s in source_batches:
		ascii_list = []
		for l in s:
			l = l[:LINE_WIDTH]			# cut long lines
			l = l.ljust(LINE_WIDTH)		# pad short lines
			l = [ord(i) for i in l]
			ascii_list += l
		n = np.reshape(ascii_list, (3, -1, 1))
		r.append(n)
	r = np.array(r)
	return r

def read_acc(path : str) -> [[int]]:
	r = []
	with open(path, 'r') as file:
		for line in file:
			try:
				l = eval(line)
				if len(l) < MAX_SHIMS: l = l + [0] * (MAX_SHIMS - len(l))
				else: l = l[:MAX_SHIMS]
				r.append(l)
			except: pass
	return r

def whitespace_to_np_array(spaces : []) -> np.array:
	r = spaces
	r = np.array(r).reshape(len(spaces), -1)
	return r

def compile_data(from_dir : str) -> {}:
	r = {'in': [], 'out': [], 'src': []}
	for n, path in enumerate(glob(from_dir + "/*.c")):
		if n > MAX_DATA_LIMIT: break
		acc_path  = path + ".acc"
		norm_path = path + ".norm"
		source_batches = get_source(path, norm_path)
		accumulation   = read_acc(acc_path)
		if len(source_batches) != len(accumulation):
			print(f"WARNING: Some retard fucked up strings in {path}")
			continue
		r['src'].append(path)
		r['in']  += source_batches
		r['out'] += accumulation
		print(f"INFO: Read data from ({n}) {path}")
	r['in']  = source_to_np_array(r['in'])
	r['out'] = whitespace_to_np_array(r['out'])
	return r

def get_data(dataset_file : str) -> {}:
	r = {}
	with open(dataset_file, 'rb') as f: r = pickle.load(f)
	assert len(r['in']) == len(r['out']), (
			"data in and out sizes were inconsistent ("
			+ str(r['in'].shape)
			+ " "
			+ str(r['out'].shape)
			+ "."
	)
	return r

if __name__ == "__main__":
	if len(argv) == 2 and argv[1] == 'c': # clean compile
		with open(DATASET_FILE, 'wb') as f: pickle.dump(compile_data(COMPILE_INPUT_DIRECTORY), f)
	dataset = get_data(DATASET_FILE)
	print(dataset['in'].shape, dataset['out'].shape)
