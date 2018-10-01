import io
import numpy

# Author : Alexe Simon
# Date : 01 October 2018
# To use for non profit only, and never copy without giving the author credit (plagiarism)

# Tutorial:

# What does this program do?
#	It solves substitution cyphers by comparing the code to words in a dictionary, uses a breadth-first algorithm

# How to use this?
#	Read the "Settings".
#	You need a dictionary of words. Put it in the same folder and change the DICTIONARY variable to its name.
#	You have examples of correct cyphers, order and hint combination in "# Cyphers". The first one is from 9gag and seems to not has an answer.
#	If you want to add your own cypher, you can write it in line 55, after cyphers = between the " and then set CYPHER_TO_SOLVE = 5
#	If you want to solve the sentence in a specific order, set USE_MANUAL_ORDERING = True and edit the MANUAL_ORDER variable corresponding to the cypher.

# How to solve complex, almost impossible substitution cypher? 
# 	Run the program for a very small sample of words, typically 2, at worst 1 (set LIMIT = 2)
# 	You can chose what words using USE_MANUAL_ORDER = True or let the program decides what is best (recommended)
# 	Look up the results in the output file and select the words you think possible in the ones solved
# 	Add them as hints and set USE_HINTS = True
# 	Then increase LIMIT and launch again to find new words
# 	Repeat until either you solve the cypher
# 	If it says "no valid answer", it means the hints are incomplete and do not contain the correct answer, or the cypher is impossible (contains an error)

# Settings
CYPHER_TO_SOLVE = 3 # set to 1 to solve 9gag's cypher at https://9gag.com/gag/a5Mp73y . Or set to 2 to test the script with a long easy sentence, or 3 to test the script with a shorter complex sentence, or 4 which is impossible to solve without using hints (which I did following the Tutorial)
DICTIONARY = "dicoENG3.txt" # must be in same folder, with each line containing a word ; Most 100k used words or complete lexicon recomended ; you can download these online
OUTPUT = "decypherOUTPUT.txt" # output will be in same folder

LIMIT =  0 # number of words to solve, replace by 0 to solve the whole sentence ; Try maximum 3 or 4 for complicated sentence, or it will take too long
REDUCE_MEMORY_USAGE = True # set to True for a slightly slower algorithm but IMMENSELY less memory usage if the cypher is complicated; True by default and recomended.
USE_MANUAL_ORDERING = False # set to False to use automatic ordering with smart heuristic
USE_HINTS = False # Set to True to use hints and greatly limit search space; ! remember to add add hints in "Constant Variables" for this to take effect


# Cyphers
if CYPHER_TO_SOLVE == 1:
	cyphers = "BSY ZTZOQYA BU LZ TTZR XR NG WIIT EPZ MYAVHTC"
	#           0     1    2  3   4   5  6   7    8     9
	MANUAL_ORDER = [4, 7, 1, 9, 8, 3, 5, 2, 6] # if USE_MANUAL_ORDERING is set to True, you can chose the words to solve.
	HINTS = {4:["eery", "oops", "ooze"]} # Add hints as number_of_the_coded_word:["possible word 1", "possible word 2"], ! remember to set USE_HINTS to True for these to take effect
	# This line means "words 4 can either be "eery", "oops" or "ooze".
	
elif CYPHER_TO_SOLVE == 2:
	cyphers = "p jhu uva bzl aopz av zvscl aol pupaphs wyvislt iljhbzl aol zlualujl pz avv zthss huk bzlz uvu jvttvu dvykz huk ohz mhy avv thuf wvzzpisl ylzbsaz iba p jhu wyvcl aopz dvyrz wlymljasf if zvscpun aopz svun zlualujl aoha pz ylhssf lhzf dpao zptwsl dvykz hss wylzlua pu aol zthsslza kpjapvuhyf" 
	USE_MANUAL_ORDERING = False
	HINTS = {}
	
elif CYPHER_TO_SOLVE == 3:
	cyphers = "MIOL OL AF AMMTDHM MG LGSXT A LIGKMTK AFR DGKT EGDHSTV LTFMTFET"
	#           0   1  2     3    4    5   6    7     8   9     10       11
	MANUAL_ORDER = [6, 3, 11, 7, 10, 5, 9, 2, 1, 0, 4, 8]
	HINTS = {}
elif CYPHER_TO_SOLVE == 4:
	cyphers = "UGGR SWEQ MKBOFU MG LGSXT MIOL"
	#           0    1     2    3    4    5
	MANUAL_ORDER = [0, 3, 4, 2, 5, 1]
	HINTS = {0:["zoom", "wool", "weed", "wood", "weep", "week", "took", "soon", "seen", "seer", "seek", "seed", "root", "geek", "good", "hood", "yeel"],
			 3:["to", "so",],
			 5:["take", "talk", "tame", "tane", "tape", "tawn", "taxi", "tear", "teal", "team", "term", "tern", "time", "thin", "this", "that", "them", "thus"]}
elif CYPHER_TO_SOLVE == 5:
	cyphers = ""
	
else:
	print("No cypher selected")
	exit()

# Variables
cyphers = cyphers.lower()
cypher = [word for word in cyphers.split()]

rules_old = []
rules_new = []

dico_file = io.open(DICTIONARY, "r", encoding='utf-8')
dico = [line[:-1] for line in dico_file] # removes \n
output = io.open(OUTPUT, "w+", encoding='utf-8')

# Functions and Classes
class Rule: #minimizes memory usage by linking child dictionaries to their parrent dictionaries
	def __init__(self, parrent):
		self.parrent_rules = parrent
		self.new_rules = dict()
	
	def add(self, code, real):
		for i in range(len(code)):
			if self.has(code[i]):
				if self.get(code[i]) != real[i]:
					return False
			elif real[i] in self.list_values():# and code[i] not in dic
				return False
			else:
				self.new_rules[code[i]] = real[i]
		return True
	
	def has(self, letter):
		if letter in self.new_rules:
				return True
		elif self.parrent_rules is not None:
			return self.parrent_rules.has(letter)
		else:
			return False
	
	def get(self, letter):
		if letter in self.new_rules:
			return self.new_rules[letter]
		elif self.parrent_rules is not None:
			return self.parrent_rules.get(letter)
		else:
			return None
	
	def list_values(self):
		if self.parrent_rules is None:
			return list(self.new_rules.values())
		else:
			ans = list(self.new_rules.values())
			ans.extend(self.parrent_rules.list_values())
			return ans
	
	def translate(self, str):
		new = ""
		for char in str:
			if char == ' ':
				new += ' '
			elif not self.has(char):
				new += char.upper()
			else:
				new += self.get(char)
		return new
	
def add_rule(dic, code, real):
	for i in range(len(code)):
		if code[i] in dic:
			if dic[code[i]] != real[i]:
				return False
		elif real[i] in dic.values():# and code[i] not in dic
			return False
		else:
			dic[code[i]] = real[i]
	return True
				

def match(w1, w2):
	if len(w1) != len(w2):
		return False
	else:
		w1_sim = [w1.find(char) for char in w1]
		w2_sim = [w2.find(char) for char in w2]
		return w1_sim == w2_sim

def translate(rule, str):
	new = ""
	for char in str:
		if char == ' ':
			new += ' '
		elif char not in rule:
			new += char.upper()
		else:
			new += rule[char]
	return new

# Solver
print("Sentence is : "+cyphers)
print("Aggregating possible words from dictionary...")
possible_words = [[word.lower() for word in dico if match(hint, word.lower())] for hint in cypher] # for every word (hint) in the coded sentence we select all the words in english that have the same length and same structure using the quick match function
if USE_HINTS:
	print("Using hints.")
	for hint in HINTS: # we add hints
		possible_words[hint] = HINTS[hint]

if not USE_MANUAL_ORDERING:
	print("Using automatic ordering.")
	order = numpy.argsort([len(sublist) for sublist in possible_words]) # we take the one with lowest number of words to init the rules
	#heuristic
	for i in range(1,len(order)):
		char_used = [char for word in numpy.array(cypher)[order[0:i-1]] for char in word]
		best = i
		best_score = len(possible_words[order[i]])/((sum([char_used.count(char) for char in cypher[order[i]]])+1)**2)
		for j in range(i+1,len(order)):
			current_score = len(possible_words[order[j]])/((sum([char_used.count(char) for char in cypher[order[j]]])+1)**2)
			if current_score < best_score:
				best_score = current_score
				best = j
		temp = order[i]
		order[i] = order[best]
		order[best] = temp
else:
	order = MANUAL_ORDER

print("Solving in order : " + str(numpy.array(cypher)[order]))

print("Computing word at index " + str(order[0])+" : \""+cypher[order[0]].upper() + "\"")
if REDUCE_MEMORY_USAGE:
	for possible_word in possible_words[order[0]]:
		temp_dict = Rule(None)
		temp_dict.add(cypher[order[0]], possible_word)
		rules_old.append(temp_dict)
else:
	for possible_word in possible_words[order[0]]:
		temp_dict = dict()
		add_rule(temp_dict, cypher[order[0]], possible_word)
		rules_old.append(temp_dict)
	

if len(rules_old) == 0:
	print("No valid answer.")
	exit()
	
if LIMIT <= 0:
	LIMIT = min(len(cypher), len(order))
	
if REDUCE_MEMORY_USAGE:
	for i in order[1:LIMIT]:
		print("Computing at index " + str(i)+" : \""+cypher[i].upper() + "\"")
		while len(rules_old) > 0:
			rule_tested = rules_old.pop()
			for possible_word in possible_words[i]:
				# for each word, take every rule, check if rule can accept word and if yes put it back in possible rules
				temp_rule = Rule(rule_tested)
				if temp_rule.add(cypher[i], possible_word):
					rules_new.append(temp_rule)
				else:
					del temp_rule
		temp_list = rules_old
		rules_old = rules_new
		rules_new = temp_list

		if len(rules_old) == 0:
			print("No valid answer.")
			break

else:
	for i in order[1:LIMIT]:
		print("Computing word at index " + str(i)+" : \""+cypher[i].upper() + "\"")
		while len(rules_old) > 0:
			rule_tested = rules_old.pop()
			for possible_word in possible_words[i]:
				# for each word, take every rule, check if rule can accept word and if yes put it back in possible rules
				temp_rule = rule_tested.copy()
				if add_rule(temp_rule, cypher[i], possible_word):
					rules_new.append(temp_rule)
				else:
					del temp_rule
		temp_list = rules_old
		rules_old = rules_new
		rules_new = temp_list
		
		if len(rules_old) == 0:
			print("No valid answer.")
			break			

# Output
print("Writing to output file...")
for rule in rules_old:
	if REDUCE_MEMORY_USAGE:
		ans = rule.translate(cyphers)
	else:
		ans = translate(rule, cyphers)
	output.write(ans + '\n')
	
# Tests
# nothing left to test

# TODO
# Combine with more advanced computational linguistic methods (lexical analysis, synthax analysis, semantic analysis, ...)
# Automate the procedure for complex cypher
# Automate the procedure when no valid answer is found (ex: consider OOV words such as NAMES)
# Automate the choice of the dictionary (increasing difficulty, save work as hints for next run)
# Multiple type of hints : yes-words (surely one of these), no-words (surely none of these), maybe-words (prioritize these)
# Add depth first search