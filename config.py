'''
This is the configueration file for the main module analysis.py
'''
import os

class Config:
	'''Provides the programme with an input-output pipeline'''
	def dir_create(path):
		if not os.path.exists(path):
			os.makedirs(path)
