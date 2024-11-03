from datetime import datetime
from sys import argv
import numpy as np
from argparse import ArgumentParser

from config import *
import model
import data
import tard_wrangler

parser = ArgumentParser()
parser.add_argument('--model', type=str, help='Specify the model to use')
parser.add_argument('file', type=str, help='The file to process')
args = parser.parse_args()

if args.model:
	mymodel = model.load_model(args.model)
else:
	dataset = data.get_data(DATASET_FILE)
	mymodel = model.make_model(dataset)
	timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
	mymodel.save(MODEL_DIRECTORY + f"model_-_{timestamp}.keras")

print(tard_wrangler.full_predict(args.file, args.file + ".norm", mymodel))
