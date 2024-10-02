import numpy as np

from config import *
import tard_wrangler

def get_data():
	r = []
	INPUT_FILE = "data/xop.c"
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
			r.append(n)
		r = np.array(r)
		return r
	def get_whitespace(path : str) -> [int]:
		'''XXX returns the whitespace list of every middle line'''
		r = []
		output = "muf_file.txt"
		tard_wrangler.accumulate(INPUT_FILE, output)
		with open(output, 'r') as file:
			for n, line in enumerate(file):
				if ((n + 2) % 3) != 0: continue
				l = eval(line)
				l = l + [0] * (MAX_SHIMS - len(l))
				r.append(l)
		return r
	def whitespace_to_np_array(spaces : []) -> np.array:
		r = spaces
		r = np.array(r).reshape(20, -1)
		return r
	source = source_to_np_array(get_source(INPUT_FILE))
	whitespace = whitespace_to_np_array(get_whitespace(INPUT_FILE))
	r = {'in': source, 'out': whitespace}
	assert len(r['in']) == len(r['in']), "data in and out sizes were inconsistent."
	return r

if __name__ == "__main__":
	dataset = get_data()
	print(dataset)
	print(dataset['in'].shape, dataset['out'].shape)
