# number of positive and negetive test and train data is count

count = 500

with open('imdb.vocab') as file:
	em = open('imdbEr.txt')
	final = open('words.txt', 'w')

	cout = -1

	chk = 3

	for line in em:
		line_word = file.readline()
		cout = cout + 1
		if float(line) > 2.5734 or float(line) < -1.5:
			final.write(str(cout) + ' ' + line_word)

		if float(line) >= -1.5 and float(line) < -1.45:
			if chk > 0:
				final.write(str(cout) + ' ' + line_word)
				chk = chk - 1



with open('./test/labeledBow.feat') as file:
	pos_f = open('./test/pos.txt', 'w')
	neg_f = open('./test/neg.txt', 'w')

	# line = file.readlines()
	# print (line[1])

	neg_count = 0
	pos_count = 0


	for line in file:
		tokens = line.strip().split()
		rating = tokens[0]

		if int(rating) > 6:
			if pos_count < count:
				pos_f.write(line)
				pos_count = pos_count + 1
		elif int(rating) < 5:
			if neg_count < count:
				neg_f.write(line)
				neg_count = neg_count + 1
		if pos_count >= count and neg_count >= count:
			break




with open('./train/labeledBow.feat') as file:
	pos_f = open('./train/pos.txt', 'w')
	neg_f = open('./train/neg.txt', 'w')

	# line = file.readlines()
	# print (line[1])

	neg_count = 0
	pos_count = 0


	for line in file:
		tokens = line.strip().split()
		rating = tokens[0]

		if int(rating) > 6:
			if pos_count < count:
				pos_f.write(line)
				pos_count = pos_count + 1
		elif int(rating) < 5:
			if neg_count < count:
				neg_f.write(line)
				neg_count = neg_count + 1
		if pos_count >= count and neg_count >= count:
			break




