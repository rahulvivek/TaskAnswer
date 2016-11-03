import math

HASH_CONSTANT = 7
CONSTANT_MULTIPLIER = 37

CHARACTER_SET = "acdegilmnoprstuw"

def hash(string):
	""" Hashing algorithm """
	_hash = HASH_CONSTANT
	
	for i in range(0, len(string)):
		_hash = (_hash * CONSTANT_MULTIPLIER + CHARACTER_SET.index(string[i]))
		
	return _hash


def decode(_hash):
	""" Decode the string from the given hash """
	decoded_string = ""
	position_dict = {}
	i = 0

	while(_hash > CONSTANT_MULTIPLIER):
		position_dict[i] = int(math.floor(_hash % CONSTANT_MULTIPLIER))
		_hash = _hash / 37
		i += 1


	j = len(position_dict) - 1

	while(j >= 0):
		decoded_string += CHARACTER_SET[position_dict[j]]
		j -= 1

	return decoded_string



# Testing the given test cases
# Find the string from hash
print "Finding string from given hash '680131659347' is '%s'" % (decode(680131659347))
print "---------------------------------------------------------"
# Find the hash from string
print "Testing hashing and decoding functions hashing"
print "----------------------------------------------"
hash_test = hash('leepadg')
print "Hash of 'leepadg' is '%s' " % (hash_test)
print "Decoded String from '%s' is '%s'" % (hash_test, decode(hash_test)) 


