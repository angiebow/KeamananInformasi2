#des.py
import sys

class DES:
	def __init__(self):

		self.key = "1001100111"
		
		self.s0 = [[1, 0, 3, 2],
				[3, 2, 1, 0],
				[0, 2, 1, 3],
				[3, 1, 3, 2]]

		self.s1 = [[0, 1, 2, 3],
				[2, 0, 1, 3],
				[3, 0, 1, 0],
				[2, 1, 0, 3]]

		self.s2 = [[2, 3, 0, 1],
				[1, 0, 3, 2],
				[3, 1, 2, 0],
				[0, 2, 1, 3]]

		self.s3 = [[3, 0, 1, 2],
				[1, 2, 3, 0],
				[0, 1, 2, 3],
				[2, 3, 0, 1]]

		self.s4 = [[0, 3, 1, 2],
				[2, 1, 0, 3],
				[1, 0, 2, 3],
				[3, 2, 1, 0]]

		self.s5 = [[3, 2, 0, 1],
				[0, 1, 3, 2],
				[2, 3, 1, 0],
				[1, 0, 2, 3]]

		self.s6 = [[1, 3, 2, 0],
				[0, 2, 3, 1],
				[3, 0, 1, 2],
				[2, 1, 0, 3]]

		self.s7 = [[2, 1, 3, 0],
				[3, 0, 2, 1],
				[1, 2, 0, 3],
				[0, 3, 1, 2]]

	def getSboxEntry(self, binary,sbox):

		row = binary[0] + binary[3]
		col = binary[1] + binary[2]
	
		row = int(row,2)
		col = int(col,2)
		if sbox == 0:
			binary = bin(self.s0[row][col])[2:]
			if len(binary) == 1:
				binary = "0" + binary
			return binary
		else:
			binary = bin(self.s1[row][col])[2:]
			if len(binary) == 1:
				binary = "0" + binary
			return binary

	def fFunction(self,key, k):
		expansion = key[3]+key[0]+key[1]+key[2]+key[1]+key[2]+key[3]+key[0]

		XOR = bin((int(expansion,2)^int(k,2)))[2:]
		XOR = self.padding(XOR,8)

		left = XOR[:4]
		right = XOR[4:]

		S0 = self.getSboxEntry(left, 0)
		S1 = self.getSboxEntry(right, 1)

		p4 = S0 + S1

		p4 = p4[1]+p4[3]+p4[2]+p4[0]

		return p4

	def kValueGenerator(self, key):
		newKey = key[2] + key[4] + key[1] + key[6] + key[3] + key[9] + key[0] + key[8] + key[7] + key[5]
		left = newKey[0:5]
		right = newKey[5:]

		leftShift = left[1:] + left[0]

		rightShift = right[1:] + right[0]

		k1 = leftShift + rightShift
		k1Permuted = k1[5] + k1[2] + k1[6] + k1[3] + k1[7] + k1[4] + k1[9] + k1[8]

		leftShiftTwice = leftShift[1:] + leftShift[0]

		rightShiftTwice = rightShift[1:] + rightShift[0]

		k2 = leftShiftTwice + rightShiftTwice
		k2Permuted = k2[5] + k2[2] + k2[6] + k2[3] + k2[7] + k2[4] + k2[9] + k2[8]

		return(k1Permuted,k2Permuted)

	def initialPermutation(self,key):
		newKey = key[1] + key[5] + key[2] + key[0] + key[3] + key[7] + key[4] + key[6]
		return newKey

	def reversePermutation(self,key):
		newKey = key[3] + key[0] + key[2] + key[4] + key[6] + key[1] + key[7] + key[5]
		return newKey

	def padding(self,string,length):
		if len(string) == length:
			return string
		while(len(string) < length):
			string = "0" + string
		return string

	def Encryption(self,string):
		permString = self.initialPermutation(string)

		left = permString[0:4]
		right = permString[4:]
		k1,k2 = self.kValueGenerator(self.key)

		firstFOutput = self.fFunction(right,k1)

		firstXOR = bin((int(left,2)^int(firstFOutput,2)))[2:]
		firstXOR = self.padding(firstXOR, 4)
		secondFOutput = self.fFunction(firstXOR,k2)

		secondXOR = bin((int(right,2)^int(secondFOutput,2)))[2:]
		secondXOR = self.padding(secondXOR, 4)
		output = secondXOR + firstXOR

		output = self.reversePermutation(output)
		return output

	def Decryption(self,string):
		permString = self.initialPermutation(string)

		left = permString[0:4]
		right = permString[4:]
		k1,k2 = self.kValueGenerator(self.key)

		firstFOutput = self.fFunction(right,k2)

		firstXOR = bin((int(left,2)^int(firstFOutput,2)))[2:]
		firstXOR = self.padding(firstXOR, 4)
		secondFOutput = self.fFunction(firstXOR,k1)

		secondXOR = bin((int(right,2)^int(secondFOutput,2)))[2:]
		secondXOR = self.padding(secondXOR, 4)
		output = secondXOR + firstXOR

		output = self.reversePermutation(output)
		return output