	
import math


	



	



class Node(object):
	"""docstring for Node"""
	def __init__(self, attribute):
		self.left = None
		self.right = None
		self.attribute = attribute
		self.lable = None



	# Left side of tree represents the presence of the attribute
	# Right side of tree represents the absence of the attribute


	def Entropy(self, neg_rat, pos_rat):
		pos_count = 0
		neg_count = 0

		for key in neg_rat:
			neg_count = neg_count + 1
		for key in pos_rat:
			pos_count = pos_count + 1

		total_count = pos_count + neg_count

		if total_count == 0:
			return 0	

		if neg_count > 0:
			neg_count = - (neg_count * math.log(neg_count) / math.log(2))
		if pos_count > 0:
			pos_count = - (pos_count * math.log(pos_count) / math.log(2))

		ent = neg_count + pos_count
		ent = ent / total_count

		return ent



	def InfoGain(self, att, neg_rat, pos_rat):

		entropy_parent = self.Entropy(att, neg_rat, pos_rat)

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


		entropy_left = self.Entropy(att, left_neg_rat, left_pos_rat)
		entropy_right = self.Entropy(att, right_neg_rat, right_pos_rat)

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



	def find_attribute(att_list, neg_rat, pos_rat):
		max_ig = 0
		att_ret = att_list[0]
		for att in att_list:
			ig = self.InfoGain(att, neg_rat, pos_rat)
			if ig > max_ig:
				max_ig = ig
				att_ret = att

		if att_ret in att_list:
			att_list.remove(att_ret)

		return att_ret, att_list


# feat is list of attributes


	def insert(self, feat, neg_rev_list, pos_rev_list):

		neg = len(neg_rev_list)
		pos = len(pos_rev_list)

		if neg > 0 and pos > 0:

			att, feat = self.find_attribute(feat, neg_rev_list, pos_rev_list)

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

			self.left.insert(feat, left_neg_rat, left_pos_rat)
			self.right.insert(feat, right_neg_rat, right_pos_rat)

		else:
			if neg == 0:
				self.lable = +1
			elif pos == 0:
				self.lable = -1


		# Find the neg & pos ratio and stop at certain threshold
		
	
		



	def main(self):
		word_dict = {}		# dicionary of word_index with the words
		word_ind = []		# list of word index
		neg_rating = []		# list of neg rating
		neg_review = {}		# dict of neg review
		pos_rating = []		# list of pos rating
		pos_review = {}		# dict of pos review


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
					lst.append(int(t[0]))
				neg_review[cnt] = lst
				cnt = cnt + 1

		# print (neg_review)

		# print (neg_rating)

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
					lst.append(int(t[0]))
				pos_review[cnt] = lst
				cnt = cnt + 1

		# print (pos_review)

		# print (pos_rating)

		with open('./words.txt') as file:
			for line in file:
				tokens = line.strip().split()
				word_ind.append(int(tokens[0]))
				word_dict[int(tokens[0])] = str(tokens[1])

		# print (word_ind)

		# print (word_dict)


		# CALL the insert function here

		self.insert(word_ind, neg_review, pos_review)

