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
import wordcloud

# Define exogenous variables
input_folder_path = 'assignment_2_files/letters/'
add_input_path = 'additional_input/cik_ticker.csv'
output_folder_path = 'results/'

# Configure the programme
Config.dir_create(output_folder_path)
register_matplotlib_converters()

class Solve:
	'''Provides answers for Part B of Assignment 2'''
	def __init__(self, input_folder_path, add_input_path, output_folder_path):
		self.input_folder_path = input_folder_path
		self.df_ticker = pd.read_csv(add_input_path, sep = '|') # Load ticker and cik match info
		self.output_folder_path = output_folder_path
		self.letter_name_list = os.listdir(self.input_folder_path) # List all file names in a folder
		self.letter_name_list.remove('.DS_Store') # Remove the system file
		self.type_list = []
		self.date_trans_list = []
		self.cik_list = []
		self.df = pd.DataFrame()
		self.df_consolidated = pd.DataFrame()
		self.df_freq_firm = pd.DataFrame()
		self.files_dict = {}

	def read_files(self):
		for filename in self.letter_name_list:
			with open(self.input_folder_path + filename, 'r') as file:
				self.files_dict[filename] = file.read()

	def overview(self):
		'''Obtains a list of letter types and transmission dates and stores in a dataframe'''
		# Extract letter types and transmission dates out of file names
		for letter_name in self.letter_name_list:
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

	def ticker_add(self):
		'''Extracts CIK numbers from file names and joins them with ticker information'''
		# Obtain a list of cik numbers for each letter
		[self.cik_list.append(letter_name[0:10].lstrip('0000')) for letter_name in self.letter_name_list]
		# Add cik number as a column to the consolidated dataframe
		self.df['cik'] = pd.Series(self.cik_list)
		# Join the ticker column with the consolidated dataframe after unifying column names
		self.df_ticker.rename(columns = {'CIK': 'cik'}, inplace = True)
		self.df_ticker = self.df_ticker[['cik', 'Name', 'Business']]
		self.df['cik'] = self.df['cik'].astype('int64')
		self.df_consolidated = self.df.join(self.df_ticker.set_index('cik'), on = 'cik')
		# Sort dataframes based on time of letters communicated
		self.df.sort_values(by = ['date_trans'], inplace = True)

	def analysis(self):
		self.df_freq_firm = self.df_consolidated['Name'].value_counts()

	def data_export(self):
		# Produce a histogram of communication date frequency
		plt.figure(figsize = (16, 9))
		self.df_consolidated['date_trans'].hist(bins = 30)
		plt.title('Total Number of Letters Exchange over Time')
		plt.ylabel('Total Number of Letters)')
		plt.xlabel('First Transmission Date')
		plt.savefig(self.output_folder_path + 'Number_of_Letters_over_Time.png', dpi = 300)
		plt.close()
		plt.figure(figsize = (16, 9))
		self.df_freq_firm.plot(kind = 'barh')
		plt.savefig(self.output_folder_path + 'Frequency_Chart_Firms.png', dpi = 300)
		plt.close()
		# Save the extracted structured dataframe to disc
		self.df_consolidated.to_csv(output_folder_path + 'structured_data.csv', index = False)

	def exec(self):
		self.read_files()
		self.overview()
		self.ticker_add()
		self.ticker_add()
		self.analysis()
		self.data_export()
		print('First 10 rows of the consolidated dataframe:')
		print(self.df_consolidated)
		print('Frequency table of letters communicated based on firms:')
		print(self.df_freq_firm)

def main():
	obj = Solve(input_folder_path, add_input_path, output_folder_path)
	obj.exec()

if __name__ == '__main__':
	main()
