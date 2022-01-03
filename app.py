import pandas as pd
import statistics
import matplotlib.pyplot as plt
import numpy as np


def getSeparates(word):
	return pd.Series([word[0],word[1],word[2],word[3],word[4]])

def getMatches(word_1, word_2):
	matches = [0,0,0,0,0]
	i=0
	for i in range(5):
		if word_1[i]==word_2[i]:
			matches[i] = 1
		elif word_1[i] in word_2:
			matches[i] = 0.5


	return matches


def getDeadLetters(word,
				  matches,
				  dead_letters):
	for i in range(5):
		if matches[i] == 0:
			dead_letters.append(word[i])
	return dead_letters


def getHalfLetters(word,
				  matches,
				  half_letters):
	for i in range(5):
		if matches[i] == 0.5:
			if word[i] in half_letters:
				half_letters[word[i]].append(i)
			else:
				half_letters[word[i]] = [i]
	return half_letters


def getPositionScore(x, matches, pos_counts):

	score = 0
	half_factor = 0.5
	#MAKE THIS CALCULATE THE NUMBER OF WORDS POSSIBLE
	for i in range(5):
		if matches[i] != 1:
			score += pos_counts[i][x[i]]
			for j in range(5):
				if i != j:
					if matches[j] != 1:
						try:
							score += half_factor * pos_counts[j][x[i]]
						except KeyError:
							pass

	return score



def getNewGuess(word,matches,dead_letters,half_letters,df, ascending=False):

	df = df[df['WORD']!=word]
	for i in range(5):
		if matches[i] == 1:
			df = df[df[i]==word[i]]


	for key in half_letters:
		for i in half_letters[key]:
			#print (key,i)
			df = df[df[i] != key]
		df = df[df['WORD'].str.contains(key)]

	for dead_letter in dead_letters:
		for i in range(5):
			df = df[df[i] != dead_letter]
	
	pos_counts = [None,None,None,None,None]
	pos_counts[0] = df[0].value_counts()
	pos_counts[1] = df[1].value_counts()
	pos_counts[2] = df[2].value_counts()
	pos_counts[3] = df[3].value_counts()
	pos_counts[4] = df[4].value_counts()

	df['pos_score'] = df.apply(lambda x: getPositionScore(x,matches,pos_counts), axis=1)
	df = df.sort_values('pos_score', ascending=ascending)
	#print (df[['WORD','pos_score']])

	good_word = False
	number_of_words = df.shape[0]
	for i in range(number_of_words):		
		if len(''.join(set(df.iloc[i]['WORD']))) == 5:
			new_word = df.iloc[i]['WORD']
			#print ('xxx', new_word)
			good_word = True
			break

	
	if not good_word:
		for i in range(number_of_words):
			if len(''.join(set(df.iloc[i]['WORD']))) == 4:
				new_word = df.iloc[i]['WORD']
				good_word = True
				break

	if not good_word:
		new_word = df.iloc[0]['WORD']


	return df, new_word


def getFirstGuess(df):


	pos_counts = [None,None,None,None,None]
	pos_counts[0] = df[0].value_counts()
	pos_counts[1] = df[1].value_counts()
	pos_counts[2] = df[2].value_counts()
	pos_counts[3] = df[3].value_counts()
	pos_counts[4] = df[4].value_counts()

	matches = [0,0,0,0,0]

	df['pos_score'] = df.apply(lambda x: getPositionScore(x,matches,pos_counts), axis=1)
	df = df.sort_values('pos_score', ascending=False)
	#print (df[['WORD','pos_score']].head(10))

	good_word = False
	number_of_words = df.shape[0]
	for i in range(number_of_words):		
		if len(''.join(set(df.iloc[i]['WORD']))) == 5:
			new_word = df.iloc[i]['WORD']
			#print ('xxx', new_word)
			good_word = True
			break


	return df, new_word


def solveWordle(guess_word, answer, df, ascending=False):

	dead_letters = []
	half_letters = {}
	guess_num = 1
	result = 0
	while result != 5:
		print ("Guess",guess_num,"-",guess_word)			

		matches = getMatches(guess_word,answer)
		result = sum(matches)
		if result==5:
			break

		dead_letters = getDeadLetters(guess_word,matches,dead_letters)

		half_letters = getHalfLetters(guess_word,matches,half_letters)

		df, guess_word = getNewGuess(guess_word,matches,dead_letters,half_letters,df, ascending)
		print (df.shape[0], "possible words")

		guess_num += 1

	return guess_num


def getWordsDF(csv_file='words.csv'):
	df = pd.read_csv(csv_file)

	df[[0,1,2,3,4]] = df.apply(lambda x: getSeparates(x['WORD']), axis=1)

	return df

def runTrials(guess_word=None, answer=None, trials=100, auto_guess=None, ascending=False):

	results = []

	for j in range(trials):
		df = getWordsDF()

		if not guess_word:
			guess_df = df.sample()
			guess_word_ = guess_df.iloc[0]['WORD']
		else:
			guess_word_= guess_word
		if auto_guess:
			df, guess_word_ = getFirstGuess(df)

		if not answer:
			answer_df = df.sample()
			answer_ = answer_df.iloc[0]['WORD']
		else:
			answer_ = answer

		print ("Answer = ", answer_)

		#USE THIS TO AUTOMATE THE FIRST GUESS
		#df, guess_word = getFirstGuess(df)

		guess_num = solveWordle(guess_word_, answer_, df,ascending)

		results.append(guess_num)

		print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", j)

	print ("Number of trials:",trials)
	print (results)
	print ("Mean guesses:",sum(results)/len(results))
	print ("Median guesses:",statistics.median(results))

	bins = np.arange(0, max(results) + 1.5) - 0.5
	plt.hist(results,bins)
	plt.show()



def main(name, data_dir='.'):

	runTrials(guess_word=None,
			answer=None,
			trials=100,
			auto_guess=True)



if __name__ == '__main__':
    import sys
    main(*sys.argv)
