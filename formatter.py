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
	dataset = data.get_data()
	mymodel = model.make_model(dataset)
	timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
	mymodel.save(MODEL_DIRECTORY + f"model_-_{timestamp}.keras")

predictions = tard_wrangler.full_predict("data/xop.c.norm", mymodel)
tard_wrangler.build("data/xop.c.norm", predictions)
tard_wrangler.cat_build()
