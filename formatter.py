import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow
from tensorflow import keras
from keras import layers

from config import *
import data
import tard_wrangler

dataset = data.get_data()

# XXX: add more conv layers
model = keras.Sequential([
	keras.Input(shape=(3, LINE_WIDTH, 1)),
	layers.Conv2D(
		filters=16,
		kernel_size=(3,5),
		strides=(1,1),
		activation='relu',
		padding='valid',
	),
	layers.Flatten(),
	layers.Dense(64, activation='relu'),
	layers.Dense(64, activation='relu'),
	layers.Dense(MAX_SHIMS) #activation='softmax'
])

model.compile(
	optimizer='adam',
	loss='mse',
	metrics=['mae']
)

model.fit(dataset['in'], dataset['out'],
    verbose=2,
    batch_size=10,
    epochs=50,
    shuffle=True,
)

prediction = model.predict(dataset['in'])[0]
prediction = prediction.astype(np.uint8).tobytes()
tard_wrangler.build("data/xop.c.norm", prediction)
