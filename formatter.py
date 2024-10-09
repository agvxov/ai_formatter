from datetime import datetime
from sys import argv
import numpy as np

from config import *
import model
import data
import tard_wrangler

if len(argv) > 1:
	mymodel = model.load_model(argv[1])
else:
	dataset = data.get_data("dataset-linux.pkl")
	mymodel = model.make_model(dataset)
	timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
	mymodel.save(MODEL_DIRECTORY + f"model_-_{timestamp}.keras")

print(tard_wrangler.full_predict("training_set/xop.c", "training_set/xop.c.norm", mymodel))
