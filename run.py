from os import sys
from random import shuffle
import pandas as pd
from tabulate import tabulate

print('Hello, who are you?')
user_flg = False

while not user_flg:
	user = input()

	if user.lower()[0] == 'b':
		print('Hello Ben.')
		print()
		user_flg = True

	elif user.lower()[0] == 'c':
		print('Hello Caroline.')
		print('You have a cute butt.')
		print()
		user_flg = True

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

	df.to_csv('Data/Movie List.csv')




