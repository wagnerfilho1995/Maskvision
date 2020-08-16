# -*- coding: utf-8 -*-
import numpy as np
import keras as ks

def normalization(x: float, min: float, max: float, range_a: float, range_b: float) -> float:
	"""
		This function is used to normalize a number.

		Input argument(s): a float value, with min and max of the respective parameter 
		and the desired range (a: lower, b: higher) of the output.
		
		Returns: the normalized value as a float.
	"""
	
	z = ((float(range_b) - float(range_a)) * ((x - float(min))/(float(max) - float(min)))) + float(range_a)
	return z

def unnormalization(data: np.array, min: float, max: float, range_a: float, range_b: float) -> np.array:
	"""
		This function is used to unnormalize data.

		Input argument(s): a numpy array (1-D or 2-D), with min and max of the respective parameter 
		and the range (a: lower, b: higher) at which the data was normalized.
		
		Returns: the unnormalized values as a numpy array ( 1 output per line, 1 channel per column).
	"""

	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		for j in range(0, data.shape[1]):
			values.append(((float(data[i][j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
		unnormalized_data.append(values)
	return np.array(unnormalized_data)

def execute(model_path: str, info_path: str, input_path: str) -> np.array:
	"""
		This function is used to predict the Output Power(s) corresponding to the Input Power(s) supplied, 
		using a trained Artificial Neural Network (ANN).
		
		Input argument(s): the path to the trained NN model file (.h5), the path to 
		the model's normalization info file (.txt) and the path to the input(s) file on which 
		the prediction is to be made (.txt, 1 input per line).
		
		Returns: the predicted Output Power(s) as a numpy array (1-D or 2-D; 1 output per line, 1 channel per column).
	"""
	## Reading input data
	with open(input_path, 'r') as input_file:
		input_data = []
		test = []
		lines = input_file.readlines()
		for i in range(0, len(lines)):
			aux = [float(n) for n in lines[i].split()]
			input_data.append(aux)
	
	## Structuring input data
	input_data = np.array(input_data)
	number_of_channels = len(input_data[0][1:])

	## Reading normalization info
	with open(info_path, 'r') as info_file:
		norm_info = [next(info_file).split() for x in range(3)]
	
	max_gset, max_pin, max_pout = [float(n) for n in norm_info[0]]
	min_gset, min_pin, min_pout =  [float(n) for n in norm_info[1]]
	range_a, range_b = [float(n) for n in norm_info[2]]
	
	## Normalizing data using model min and max info
	normalized_input_data = np.zeros((input_data.shape[0], 1+number_of_channels))

	for i in range(0, input_data.shape[0]):
		normalized_input_data[i][0] = normalization(input_data[i][0], min_gset, max_gset, range_a, range_b)
		for j in range(1, 1+number_of_channels):
			normalized_input_data[i][j] = normalization(input_data[i][j], min_pin, max_pin, range_a, range_b)

	## Reading model
	model = ks.models.load_model(model_path)

	## Executing prediction
	normalized_output_data = model.predict(normalized_input_data)

	## Unnormalizing predicted data
	p_out = unnormalization(normalized_output_data, min_pout, max_pout, range_a, range_b)

	# Returning P_out prediction
	return p_out

def start():
	## Input
	model_path = "nn-model-for-group-1-fold-1.h5"
	info_path = "info.txt"
	input_path = "input.txt"
	output_path = "output.txt"

	## Executing prediction
	p_out = execute(model_path, info_path, input_path)

	## Generating output file as .txt
	with open(output_path, 'w') as output_file:
		for i in range(0, p_out.shape[0]):
			new_line = ""
			for j in range(0, p_out.shape[1]):
				new_line += str(p_out[i][j]) + '\t'
			output_file.write(new_line + '\n')