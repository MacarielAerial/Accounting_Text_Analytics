'''
This script provides answer for Assignment 2 of AM16 SPR20 Financial Reporting Analytiics in London Business School
The solution is written by Group 7
'''
# import libraries
import os
import re
from config import Config
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import datetime
from datetime import date


# Define exogenous variables
input_folder_path = 'assignment_2_files/letters/'
output_folder_path = 'results/'

# Configure the programme
Config.dir_create(output_folder_path)
register_matplotlib_converters()

class Solve:
	'''Provides answers for Part B of Assignment 2'''
	def __init__(self, input_folder_path, output_folder_path):
		self.input_folder_path = input_folder_path
		self.output_folder_path = output_folder_path
		self.letter_name_list = os.listdir(self.input_folder_path)
		self.type_list = []
		self.date_trans_list = []
		self.df = pd.DataFrame()

	def overview(self):
		'''Obtains a list of letter types and transmission dates followed by analytics'''
		# Extract letter types and transmission dates out of file names
		for letter_name in self.letter_name_list:
			if letter_name != '.DS_Store':
				self.type_list.append(
					''.join(re.findall('[a-zA-Z]+', letter_name)).rstrip('txt')
					)
				match = re.search(r'\d{4}-\d{2}-\d{2}', letter_name)
				self.date_trans_list.append(
					datetime.datetime.strptime(match.group(), '%Y-%m-%d').date().strftime('%Y-%m-%d')
					)
		print('First three letter types:\n' + str(self.type_list[0:3]))
		print('First three transmission dates:\n' + str(self.date_trans_list[0:3]))
		# Store the extracted info in a dataframe
		self.df['letter_type'], self.df['date_trans'] = self.type_list, pd.to_datetime(self.date_trans_list)

	def data_export(self):
		# Produce a histogram of communication date frequency
		plt.figure(figsize = (16, 9))
		self.df['date_trans'].hist(bins = 30)
		plt.title('Total Number of Letters Exchange over Time')
		plt.ylabel('Total Number of Letters)')
		plt.xlabel('First Transmission Date')
		plt.savefig(self.output_folder_path + 'Number_of_Letters_over_Time.png', dpi = 300)
		# Save the extracted structured dataframe to disc
		self.df.to_csv(output_folder_path + 'structured_data.csv', index = False)

	def exec(self):
		self.overview()
		self.data_export()

def main():
	obj = Solve(input_folder_path, output_folder_path)
	obj.exec()

if __name__ == '__main__':
	main()
