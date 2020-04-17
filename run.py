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
			while num_to_draw > df_low.shape[0]:
				print(f'Error: contender count greater than available movies {df_low.shape[0]}')
				print('How many contenders?')
				num_to_draw=int(input())

			contenders = df_low.sample(num_to_draw)


		elif filter_choice == 'h':
			df_high = df[df.Intense == 1] 
			while num_to_draw > df_high.shape[0]:
				print(f'Error: contender count greater than available movies {df_high.shape[0]}')
				print('How many contenders?')
				num_to_draw=int(input())

			contenders = df_high.sample(num_to_draw)
		else: 
			print('Invalid Response')
			print('Do Better')
			raise NotImplementedError

	else:
		while num_to_draw > df.shape[0]:
			print(f'Error: contender count greater than available movies {df.shape[0]}')
			print('How many contenders?')
			num_to_draw=int(input())

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

			if 0 <= to_kill and to_kill < contenders.shape[0]:
				valid_kill = True
				contenders=contenders.drop(to_kill)
			else:
				print('Invalid Entry')

	print()
	print("You chose to watch")
	print(contenders.to_string())

if action == '2':
	active_flg = 1
	submit_flg = 0
	change_flg = 0

	try:
		df_tmp = pd.read_csv('Data/Suggested Movies.csv')
	except:
		df_tmp = pd.DataFrame(columns=['Movie', 'Intense', 'submitter'])

	if user:
		submitter = 'C'
	else:
		submitter = 'B'

	while active_flg:

		print('Title: ')
		title = input()
		
		print('Intensity(l/h): ')
		inp = input()

		while re.search('[^lLhHxX]', inp):
			print('Invalid input. Try again or enter X to exit.')
			print('Intensity(l/h): ')
			inp = input()
			
		if re.search('[xX]', inp):
			active_flg = 0

		elif re.search('[lL]', inp):
			intensity = 0
			print(f'Title: {title}, Intesity: L\nSubmit? (y/n)')
			inp = input()

			while re.search('[^yYnNxX]', inp):
				print('Invalid input. Try again or enter X to exit.')
				print('Approve? (y/n): ')
				inp = input()

			if re.search('[xX]', inp):
				active_flg = 0
			elif re.search('[yY]', inp):
				submit_flg = 1
				change_flg = 1

		elif re.search('[hH]', inp):
			intensity = 1
			print(f'Title: {title}, Intesity: H\nSubmit? (y/n)')
			inp = input()

			while re.search('[^yYnNxX]', inp):
				print('Invalid input. Try again or enter X to exit.')
				print('Approve? (y/n): ')
				inp = input()

			if re.search('[xX]', inp):
				active_flg = 0
			elif re.search('[yY]', inp):
				submit_flg = 1
				change_flg = 1

		if active_flg and submit_flg:
			submission = {'Movie': title, 'Intense': intensity, 'submitter': submitter}
			df_tmp = df_tmp.append(submission, ignore_index=True)

			print('Continue submitting? (y/n)')
			inp = input()

			while re.search('[^nNyY]', inp):
				print('Invalid input. Try again. (y/n)')
				inp = input()

			if re.search('[nN]', inp):
				active_flg = 0

			submit_flag = 0
		
	if change_flg:
		df_tmp.to_csv('Data/Suggested Movies.csv', index=False)
		print('Suggested Movies updated.')

if action == '3':

	active_flg = 1
	change_flg = 0

	try:
		df = pd.read_csv('Data/Movie List.csv')
	except:
		df = pd.DataFrame(columns=['Movie', 'Intense'])

	try:
		df_tmp = pd.read_csv('Data/Suggested Movies.csv')
	except:
		print('No movies to be reviewed.')
		active_flg = 0

	if active_flg:
		if user:
			print('Caroline is reviewing')
			review = df_tmp[df_tmp.submitter=='B'].Movie
			if len(review) == 0:
				print('No movies to be reviewed.')
				active_flg = 0
		else:
			print('Ben is reviewing')
			review = df_tmp[df_tmp.submitter=='C'].Movie
			if len(review) == 0:
				print('No movies to be reviewed.')
				active_flg = 0

	for movie in review:
			print('y: Approve, n: Reject, s: Skip, x: Exit')
			
			print(movie)
			inp = input()

			while re.search('[^nNyYsSxX]', inp):
					print('Invalid input. Try again.')
					
			if re.search('[xX]', inp):
					active_flg = 0	
					break

			elif re.search('[yY]', inp):
				approved = df_tmp[df_tmp.Movie == movie][['Movie', 'Intense']]
				df_tmp = df_tmp[df_tmp.Movie != movie]
				df = pd.concat([df, approved])
				change_flg = 1

			elif re.search('[nN]', inp):
				df_tmp = df_tmp[df_tmp.Movie != movie]
				change_flg = 1

	if change_flg:
		df.to_csv('Data/Movie List.csv', index=False)
		df_tmp.to_csv('Data/Suggested Movies.csv', index=False)
		print('Suggested Movies and Movie List updated.')

if action == '4':
	df=pd.read_csv('Data/Movie List.csv')
	to_del_flag = True

	while to_del_flag:
		print('Here are the movies:')
		print()
		print(df.to_string())

		to_del = input('Enter the index of the movie to delete ')

		try:
			to_del = int(to_del)
			df = df.drop( index = to_del )
				
			del_again = input('Delete Another? Y/N ')

			if del_again.lower()[0] == 'n':
				to_del_flag = False

		except:
			pass

	df.to_csv('Data/Movie List.csv', index=False)