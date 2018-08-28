import math
import random

choose = input(" Enter 1 for exp1 \n Enter 2 for exp2 \n Enter 3 for exp3 \n Enter 4 for exp4 \n Enter 5 for exp5 \n ")

print ("Reading attributes and training data")

word_dict = {}		# dicionary of word_index with the words
word_ind = []		# list of word index
neg_rating = []		# list of neg rating
neg_review = {}		# dict of neg review
pos_rating = []		# list of pos rating
pos_review = {}		# dict of pos review

""" Reading the attributes """

with open('./words.txt') as file:
	for line in file:
		tokens = line.strip().split()
		word_ind.append(int(tokens[0]))
		word_dict[int(tokens[0])] = str(tokens[1])

# print (word_ind)

# print (word_dict)

""" Reading the negative reviews """

with open('./train/neg.txt') as file:
	cnt = 1
	for line in file:
		tokens = line.strip().split()
		rate = tokens[0]
		neg_rating.append(rate)
		del tokens[0]
		lst = []
		for token in tokens:
			t = token.split(":")
			if int(t[0]) in word_ind:
				lst.append(int(t[0]))

		if lst:
			neg_review[cnt] = lst
			cnt = cnt + 1

# print (neg_review)

# print (neg_rating)

""" Reading the positive reviews """

with open('./train/pos.txt') as file:
	cnt = 1
	for line in file:
		tokens = line.strip().split()
		rate = tokens[0]
		pos_rating.append(rate)
		del tokens[0]
		lst = []
		for token in tokens:
			t = token.split(":")
			if int(t[0]) in word_ind:
				lst.append(int(t[0]))

		if lst:		
			pos_review[cnt] = lst
			cnt = cnt + 1

# print (pos_review)

# print (pos_rating)



print ("Done...")


# CALL the insert function here





class Node(object):
	"""docstring for Node"""
	def __init__(self, attribute):
		self.left = None
		self.right = None
		self.attribute = attribute
		self.lable = None

		

	# Left side of tree represents the presence of the attribute
	# Right side of tree represents the absence of the attribute


	""" Takes the list of negative and positive reviews and returns the entropy """


	def Entropy(self, neg_rat, pos_rat):
		pos_count = len(neg_rat)
		neg_count = len(pos_rat)

		total_count = pos_count + neg_count

		if total_count == 0:
			return 0	

		if neg_count > 0:
			neg_count = - (neg_count * math.log(neg_count / total_count) / math.log(2))
		if pos_count > 0:
			pos_count = - (pos_count * math.log(pos_count / total_count) / math.log(2))

		ent = neg_count + pos_count
		ent = ent / total_count

		return ent


	""" 
		Takes dictionary of attribute and list of +ve and -ve reviews  
		Calls the entropy function and gets the parent and child entropy
		Computes the information gain and returns it
	"""


	def InfoGain(self, att, neg_rat, pos_rat):

		entropy_parent = self.Entropy(neg_rat, pos_rat)

		left_neg_rat = {}		#  PRESENT
		left_pos_rat = {}

		right_neg_rat = {}		#  ABSENT
		right_pos_rat = {}

		for key in neg_rat:
			pres = 0
			for num in neg_rat[key]:
				if num == att:
					pres = 1
					break

			if pres == 0:
				right_neg_rat[key] = neg_rat[key]
			elif pres == 1:
				left_neg_rat[key] = neg_rat[key]

			pres = 0

		for key in pos_rat:
			pres = 0
			for num in pos_rat[key]:
				if num == att:
					pres = 1
					break

			if pres == 0:
				right_pos_rat[key] = pos_rat[key]
			elif pres == 1:
				left_pos_rat[key] = pos_rat[key]

			pres = 0


		entropy_left = self.Entropy(left_neg_rat, left_pos_rat)
		entropy_right = self.Entropy(right_neg_rat, right_pos_rat)

		left_count = 0
		right_count = 0

		for key in left_neg_rat:
			left_count = left_count + 1

		for key in left_pos_rat:
			left_count = left_count + 1

		for key in right_neg_rat:
			right_count = right_count + 1

		for key in right_pos_rat:
			right_count = right_count + 1

		total_count = left_count + right_count

		entropy_child = 0
		if total_count > 0:
			entropy_child = ( entropy_left * left_count / total_count ) + ( entropy_right * right_count / total_count )

		info_gain = entropy_parent - entropy_child

		return info_gain

	""" Computes the information gain of each attributes and finds the best attribute for a node and returns it """

	def find_attribute(self, att_list, neg_rat, pos_rat):
		max_ig = 0
		att_ret = None
		for att in att_list:
			ig = self.InfoGain(att, neg_rat, pos_rat)
			if ig > max_ig:
				max_ig = ig
				att_ret = att

		if att_ret in att_list:
			att_list.remove(att_ret)

		return att_ret, att_list


# feat is list of attributes

	""" 
		It is recursive function which creates a node and calls itself for left and right node 
		It stops if there is no attributes or either -ve or +ve reviews ends
		Then is assigns the lable to leaf node
		+1 for +ve review
		-1 for -ve review
	"""


	def insert(self, feat, neg_rev_list, pos_rev_list, ratio_threshold = None):

		# print ("1")

		neg = len(neg_rev_list)
		pos = len(pos_rev_list)

		if neg > 0 and pos > 0:


			""" 
				Ratio_threshold is ratio between the size of +ve and -ve review 
				Its intent is to implement early stoping
			"""


			if ratio_threshold:

				pos = float(pos)
				neg = float(neg)

				# rat = float(pos / neg)
				# print (rat)

				if float(pos / neg) < ratio_threshold:
					self.lable = -1

				elif float(neg / pos) < ratio_threshold:
					self.lable = +1
	

			if len(feat) == 0:
				if neg > pos:
					self.lable = -1
				elif neg < pos:
					self.lable = +1

			elif  self.lable == None:

				att, feat = self.find_attribute(feat, neg_rev_list, pos_rev_list)

				if att == None:
					if neg > pos:
						self.lable = -1
					elif neg < pos:
						self.lable = +1
				else:
					# print(att)

					self.attribute = att

					left_neg_rat = {}		#  PRESENT
					left_pos_rat = {}

					right_neg_rat = {}		#  ABSENT
					right_pos_rat = {}

					for key in neg_rev_list:
						pres = 0
						for num in neg_rev_list[key]:
							if num == att:
								pres = 1
								break

						if pres == 0:
							right_neg_rat[key] = neg_rev_list[key]
						elif pres == 1:
							left_neg_rat[key] = neg_rev_list[key]

						pres = 0

					for key in pos_rev_list:
						pres = 0
						for num in pos_rev_list[key]:
							if num == att:
								pres = 1
								break

						if pres == 0:
							right_pos_rat[key] = pos_rev_list[key]
						elif pres == 1:
							left_pos_rat[key] = pos_rev_list[key]

						pres = 0


					self.left = Node(None)
					self.right = Node(None)
					self.left.insert(feat, left_neg_rat, left_pos_rat, ratio_threshold = ratio_threshold)
					self.right.insert(feat, right_neg_rat, right_pos_rat, ratio_threshold = ratio_threshold)

		else:
			if neg == 0:
				self.lable = +1
			elif pos == 0:
				self.lable = -1


		# Find the neg & pos ratio and stop at certain threshold


	""" It takes a review as input and reutrns weather it is +ve or -ve review according to the tree """
		

	def check(self, test_data):
		# print (self)
		if self:
			if self.lable:
				return self.lable

			else:
				lable = None
				if self.attribute in test_data:
					if self.left:
						lable = self.left.check(test_data)
				else:
					if self.right:
						lable = self.right.check(test_data)

				return lable

		return None
	
	""" It takes the whole test data as input and computes the overall accuracy of the decision tree """

	def checkError(self, neg_review, pos_review):
		false_count = 0
		for key in neg_review:
			actual_label = -1

			if actual_label != self.check(neg_review[key]):
				false_count = false_count + 1


		for key in pos_review:
			actual_label = +1

			if actual_label != self.check(pos_review[key]):
				false_count = false_count + 1

		# print("validation error: ", false_count/len(test_data))
		return false_count/len(list(neg_review.keys()) + list(pos_review.keys()))

	""" Prints the attributes of tree in Preorder """

	def print(self):
		print (self.attribute)
		if self.left:
			self.left.print()
		if self.right:
			self.right.print()

		if self.lable:
			print (self.lable)




	def pruning(self):

		
		if self.left and self.left.lable == None :
			self.left.pruning()
		if self.right and self.right.lable == None :
			self.right.pruning()


		if self.left and self.right and self.left.lable and self.right.lable :
			if self.left.lable == +1 and self.right.lable == +1:
				self.lable = +1
				self.left = None
				self.right = None
			elif self.left.lable == -1 and self.right.lable == -1:
				self.lable = -1
				self.left = None
				self.right = None
			elif self.left.lable == +1 and self.right.lable == -1:
				# print(self.left.pos_val, self.right.pos_val, self.left.neg_val, self.right.neg_val)
				if self.pos_val > self.neg_val:
					self.lable = +1
					self.left = None
					self.right = None
				elif self.pos_val < self.neg_val:
					self.lable = -1
					self.left = None
					self.right = None
			elif self.left.lable == -1 and self.right.lable == +1:
				if self.pos_val > self.neg_val:
					self.lable = +1
					self.left = None
					self.right = None
				elif self.pos_val < self.neg_val:
					self.lable = -1
					self.left = None
					self.right = None

			# print ("inside1")

		elif self.left and self.left.lable:
			if self.pos_val > self.neg_val:
				self.lable = +1
				self.left = None
				self.right = None
			elif self.pos_val < self.neg_val:
				self.lable = -1
				self.left = None
				self.right = None

			# print ("inside2")

		elif self.right and self.right.lable:
			if self.pos_val > self.neg_val:
				self.lable = +1
				self.left = None
				self.right = None
			elif self.pos_val < self.neg_val:
				self.lable = -1
				self.left = None
				self.right = None

			# print ("inside3")







""" Reading the negative reviews for test data """

print ("Reading test data")


t_neg_rating = []		# list of neg rating
t_neg_review = {}		# dict of neg review
t_pos_rating = []		# list of pos rating
t_pos_review = {}		# dict of pos review


with open('./test/neg.txt') as file:
	cnt = 1
	for line in file:
		tokens = line.strip().split()
		rate = tokens[0]
		t_neg_rating.append(rate)
		del tokens[0]
		lst = []
		for token in tokens:
			t = token.split(":")
			if int(t[0]) in word_ind:
				lst.append(int(t[0]))

		if lst:
			t_neg_review[cnt] = lst
			cnt = cnt + 1

# print (neg_review)

# print (neg_rating)

""" Reading the positive reviews for test data """

with open('./test/pos.txt') as file:
	cnt = 1
	for line in file:
		tokens = line.strip().split()
		rate = tokens[0]
		t_pos_rating.append(rate)
		del tokens[0]
		lst = []
		for token in tokens:
			t = token.split(":")
			if int(t[0]) in word_ind:
				lst.append(int(t[0]))

		if lst:		
			t_pos_review[cnt] = lst
			cnt = cnt + 1

# print (pos_review)

# print (pos_rating)



n_neg_review = {}
n_pos_review = {}

n_neg_review = t_neg_review
n_pos_review = t_pos_review

kn = len(list(n_neg_review.keys()))
kp = len(list(neg_review.keys()))


for z in range (100):
	i = random.choice(list(n_neg_review.keys()))
	j = random.choice(list(n_pos_review.keys()))

	tn = n_neg_review[i]
	tp = n_pos_review[j]
	n_neg_review[i] = tp
	n_pos_review[j] = tn



print ("Done...")


# Exp 1

def exp1():
	print ("Exp 1")

	node1 = Node(word_ind)
	node1.insert(word_ind, neg_review, pos_review)

	print("Accuracy on training data set")
	print ((1 - node1.checkError(neg_review, pos_review)) * 100)

	print("Accuracy on test data set")
	print ((1 - node1.checkError(t_neg_review, t_pos_review)) * 100)

	



# Exp 2 => Early Stoping

def exp2():
	print("Exp 2 => Early Stoping")

	node2 = Node(word_ind)
	node2.insert(word_ind, neg_review, pos_review, 0.03)

	print("Accuracy on training data set")
	print ((1 - node2.checkError(neg_review, pos_review)) * 100)

	print("Accuracy on test data set")
	print ((1 - node2.checkError(t_neg_review, t_pos_review)) * 100)

	



# Exp 3 => Adding the noise

def exp3():
	print("Exp 3 => Adding noise( 5% noise)")

	node3 = Node(word_ind)
	node3.insert(word_ind, neg_review, pos_review)

	print("Accuracy on training data set")
	print ((1 - node3.checkError(neg_review, pos_review)) * 100)

	print("Accuracy on test data set")
	print ((1 - node3.checkError(t_neg_review, t_pos_review)) * 100)

	



# Exp 4 => Pruning

def exp4():
	print("Exp 4 => Pruning")

	node4 = Node(word_ind)
	node4.insert(word_ind, neg_review, pos_review)	

	print("Accuracy on training data set")
	print ((1 - node4.checkError(neg_review, pos_review)) * 100)

	print("Accuracy on test data set")
	print ((1 - node4.checkError(t_neg_review, t_pos_review)) * 100)

	

# 10, 250
# 20, 500

# Exp 5 => Forest

def exp5(count, att_size, word_ind):

	print("Exp 5 => Forest")

	sum_train = 0
	sum_test = 0

	for it in range (count):
		word_ind_t = word_ind
		for jt in range (att_size):	
			val = random.choice(word_ind_t)
			word_ind_t.remove(val)
		node5 = Node(word_ind_t)
		node5.insert(word_ind_t, neg_review, pos_review)
		sum_train = sum_train +  (1 - node5.checkError(neg_review, pos_review)) * 100
		sum_test = sum_test +  (1 - node5.checkError(t_neg_review, t_pos_review)) * 100
	
	sum_train = float(sum_train)
	sum_train = sum_train / count

	sum_test = float(sum_test)
	sum_test = sum_test / count

	print("Accuracy on training data set")
	print (sum_train)

	print("Accuracy on test data set")
	print(sum_test)





if choose == str(1):
	exp1()
elif choose == str(2):
	exp2()
elif choose == str(3):
	exp3()
elif choose == str(4):
	exp4()
elif choose == str(5):
	exp5(10, 250, word_ind)
else:
	print("Unknown Input")