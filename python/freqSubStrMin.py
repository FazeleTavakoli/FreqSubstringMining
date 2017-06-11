#!/usr/bin/python

import os,sys,time
import mmh3
import pickle

class BloomCounterFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hashCount = hash_count
        self.bloomArray = [0]*size
        
    def add(self, string):
        for seed in xrange(self.hashCount):
            result = mmh3.hash(string, seed) % self.size
            self.bloomArray[result] += 1
            
    def lookupFrequent(self, string, frequency):
        for seed in xrange(self.hashCount):
            result = mmh3.hash(string, seed) % self.size
            if self.bloomArray[result] < frequency:
                return False #definitely
        return True #probably

inputFile = sys.argv[1]
frequencyCount = int(sys.argv[2])
foundDumpBloom = False
bf = None
if (os.path.isfile('bloom.pickle')):
	print "Loading from bloom dump file...."
	f = open('bloom.pickle','r')
	bf = pickle.load(f)
	print "Loaded bloom file"
	foundDumpBloom = True
else:
	bf = BloomCounterFilter(10000000, 7) #10 million length array, 7 hash functions
	f = open(sys.argv[1])
	print "Building bloom filter..."
	#First pass, fill the bloom filter
	lineCount = 0
	for line in f.readlines():
		lineCount += 1
		if lineCount % 10000 == 0:
			print "Completed line %d"%lineCount
		line = line.strip() #remove ending control characters
		for windowSize in range(1, 57):
			seen = {} #If 'aa' is in string 'aaaa' do a +1 not +2
			for startPosition in range(0, 56 - windowSize + 1):
				subString = line[startPosition:startPosition+windowSize]
				if subString in seen:
					continue
				else:
					seen[subString] = True
					bf.add(subString)
	f.close()
	print "Done with bloom filter building. Writing to file bloom.pickle."
	with open('bloom.pickle', 'wb') as fp:
		pickle.dump(bf, fp)
	fp.close()

print "Starting hashmap building...."
f = open(sys.argv[1])

#2nd pass, build in memory hashmap counter 
countDict = {}
lineCount = 0
for line in f.readlines():
	lineCount += 1
	line = line.strip()
	if lineCount %10000 == 0:
		print "Completed line %d"%lineCount
		print "Size of hashmap = %d"%(len(countDict))
	for windowSize in range(1, 57):
		seen = {} # If 'aa' is in string 'aaaa' do a +1 not +2
		for startPosition in range(0, 56 - windowSize + 1):
			subString = line[startPosition:startPosition+windowSize]
			if bf.lookupFrequent(subString, frequencyCount): #If true, we still need to confirm by building a hashmap because bloom filter lies sometimes. If false, bloom filter is saying the truth. So we build hashmap only for those items which bloom filter says is n-frequent
				if subString in seen:
					continue
				else:
					if subString in countDict:
						countDict[subString] += 1
					else:
						countDict[subString] = 1
					seen[subString] = True
print "Done building hashmap, now counting..."

count = 0
maxLength = 0
sumLength = 0
for k,v in countDict.items():
	if v >= frequencyCount:
		count += 1
		print "%d frequent -> %s"%(frequencyCount, k)
		if len(k) > maxLength:
			maxLength = len(k)
		sumLength += len(k)
		

print "Total number of frequent strings %d"%count
print "Length of longest frequent string %d"%maxLength
print "Average length of frequent strings %d"%(sumLength/float(count))

print "Done"
