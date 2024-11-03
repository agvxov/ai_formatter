import numpy as np
import pickle
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
from tensorflow import keras
from keras import layers

from config import *

@tf.function
def custom_weighted_loss(y_true, y_pred):
	weights = tf.linspace(2.0, 0.1, tf.shape(y_pred)[-1])
	return tf.reduce_mean(tf.square((y_true - y_pred) * weights))

def make_model(dataset : np.array) -> keras.Model:
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
		layers.Dense(MAX_SHIMS)
	])

	model.compile(
		optimizer='adam',
		loss=custom_weighted_loss,
		metrics=['mae']
	)

	model.fit(dataset['in'], dataset['out'],
		verbose=2,
		batch_size=10,
		epochs=50,
		shuffle=True,
	)

	return model

def load_model(path : str) -> keras.Model:
	return keras.models.load_model(path,
				compile=False
	)
