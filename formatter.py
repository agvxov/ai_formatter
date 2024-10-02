import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow
from tensorflow import keras
from keras import layers

from config import *
import data

dataset = data.get_data()

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

model.fit(dataset['in'], dataset['out'],
    verbose=2,
    batch_size=10,
    epochs=50,
    shuffle=True,
)
