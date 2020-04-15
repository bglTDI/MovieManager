from os import sys
from random import shuffle
import pandas as pd
from tabulate import tabulate
import re

print('Hello, who are you?')
user_flg = False

while not user_flg:
	user = input()

	if user.lower()[0] == 'b':
		print('Hello Ben.')
		print('You have a nice penis.')
		print()
		user_flg = True
		user = 0

	elif user.lower()[0] == 'c':
		print('Hello Caroline.')
		print('You have a cute butt.')
		print()
		user_flg = True
		user = 1

	else:
		print('Invalid User')

action_flg = False

print('What would you like to do?')
print('==========================')
print('1: Random Movie Selection')
print('2: Submit Movies')
print('3: Review Submitted Movies')
print('4: Delete movies')
print('==========================')
print()

action = input()



if action == '1':
	print('How many contenders?')
	num_to_draw=int(input())

	df=pd.read_csv('Data/Movie List.csv')
	print('Would you like to filter by Intensity? Y/N')
	filter_flg = input().lower()[0]

	if filter_flg == 'y':
		print('Low Intensity or High Intensity? L/H')
		filter_choice=input().lower()[0]

		if filter_choice == 'l':
			df_low = df[df.Intense == 0]
			contenders = df_low.sample(num_to_draw)

		elif filter_choice == 'h':
			df_high = df[df.Intense == 1] 
			contenders = df_high.sample(num_to_draw)
		else: 
			print('Invalid Response')
			print('Do Better')
			raise NotImplementedError

	else:
		contenders = df.sample(num_to_draw)

	while contenders.shape[0] > 1:
		contenders = contenders.reset_index().Movie

		print()
		print(contenders.to_string())
		print()

		valid_kill=False

		while not valid_kill:
			print('Elimate which contender?')
			to_kill=int(input())

			if 0 <= to_kill and to_kill <=contenders.shape[0]:
				valid_kill = True
				contenders=contenders.drop(to_kill)
			else:
				print('Invalid Entry')

	print()
	print("You chose to watch")
	print(contenders.to_string())

if action == 2:
	active_flg = 1
	df_tmp = read_csv('Data/Suggested Movies.csv')

	if user:
		submitter = 'C'
	else:
		submitter = 'B'

	while active_flg:

		print('Title: ')
		title = input()
		
		print('Intensity(l/h): ')
		intensity = input()
		while re.search([^lLhHxX], intensity):
			print('Invalid input. Try again or enter X to exit.')
			print('Intensity(l/h): ')
			if re.search([xX], input()):
       			df_tmp.to_csv('Data/Suggested Movies.csv')
				break
			elif re.search([lL], input()):
				intensity = 0
			elif re.search([hH], input()):
				intensity = 1
			

		submission = {'Movie': title, 'Intense': intensity, 'submitter': submitter}
        df_tmp = df_tmp.append(submission, ignore_index=True)

        print('Continue submitting? (y/n)')
        while re.search([^nNyY], input()):
        	print('Invalid input. Try again.')
       	if re.search([nN], input()):
       		active_flg = 0
       		df_tmp.to_csv('Data/Suggested Movies.csv')


if action == 3:

	df = pd.read_csv('Data/Movie List.csv')
	df_tmp = read_csv('Data/Suggested Movies.csv')

	print('y: Approve\nn: Reject\ns: Skip\n x: Exit')

	if user:
		review = df[df.submitter=='B']
	else:
		review = df[df.submitter=='C']

	while review.shape[0] > 1:
		review = review.reset_index().Movie

		for movie in review:
			print(movie.to_string())
			while re.search([^nNyYsSxX], input()):
        		print('Invalid input. Try again.')
       		if re.search([xX], input()):
       			df.to_csv('Data/Movie List.csv')
       			df_tmp.to_csv('Data/Suggested Movies.csv')