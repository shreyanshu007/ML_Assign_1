print ("hello")


# word_list = []

# with open('imdb.vocab', 'r') as file_1:
#     # imbd_vocab = file_1.read().replace('\n', '\n')
#     word_list.append('')

# print (imbd_vocab)



for i in range(1000):
	word = i
	word_dict = {}
	rev_dict = {}

	total = 0

	with open('./test/labeledBow.feat') as file:
		for line in file:
			tokens = line.strip().split()
			rev = tokens[0]
			del tokens[0]
			for token in tokens:
				t = token.split(":")
				word_dict[float(t[0])] = float(t[1])

			if word in word_dict.keys():

				total = total + word_dict[word]
				if rev in rev_dict.keys():
					rev_dict[rev].append(word_dict[word])
				else:
					rev_dict[rev] = [word_dict[word]]
				# print(rev,":",word_dict[word])

	neg_avg = 0
	pos_avg = 0

	for rev in rev_dict:

		# print(rev, ":", sum(rev_dict[rev])/len(rev_dict[rev]))
		if int(rev) in [1,2,3,4]:
			neg_avg = sum(rev_dict[rev])/len(rev_dict[rev]) + neg_avg
		elif int(rev) in [7,8,9,10]:
			pos_avg = sum(rev_dict[rev])/len(rev_dict[rev]) + pos_avg
		# print("\n\n\n")

	var = abs(pos_avg/4 - neg_avg/4)
	if var > 0.1:
		print(i, ":", var)
	
	# print(total/25000)