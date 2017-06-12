#!/usr/bin/python

import os,sys,time
import mmh3
import pickle
from multiprocessing import Pool, Queue, cpu_count, Process


finalBloomArray = [0]*10000000  #Merge the cpuCount - 1 bloomArrays into 1

def lookupFrequent(string, frequency):
	for seed in range(3):
		result = mmh3.hash(string, seed) % 10000000
		if finalBloomArray[result] < frequency:
			return False #definitely
	return True #probably


def bloomWorker(workQueue, doneQueue, startTime):
	bloomArray = [0]*10000000
	count = 0
	for line in iter(workQueue.get, 'S'):
		if len(line) != 56:
			print "DAMN %s"%line
		count += 1
		if count % 10000 == 0:
			print "Work queue items left to process = %d. Time elapsed %d seconds"%(workQueue.qsize(), time.time() - startTime)	
		for windowSize in range(1, 57):
			seen = {} #If 'aa' is in string 'aaaa' do a +1 not +2
			for startPosition in range(0, 56 - windowSize + 1):
				subString = line[startPosition:startPosition+windowSize]
				if subString in seen:
					continue
				else:
					seen[subString] = True
					for i in range(3): # 3 hashes for bloom filter
						bit = mmh3.hash(subString, i) % 10000000 # 10 million bits (actually integers) for bloom filter counter
						bloomArray[bit] += 1
	doneQueue.put(bloomArray)
	doneQueue.put('S') #S for stop
	return True

cpuCount = cpu_count()
if __name__ == '__main__':
	start = time.time()

	foundDumpBloom = False
	if (os.path.isfile('bloom.pickle')):
		print "Loading from bloom dump file...."
		f = open('bloom.pickle','r')
		finalBloomArray = pickle.load(f)
		print "Loaded bloom file"
		foundDumpBloom = True
		f.close()

	if not foundDumpBloom:

		f = open(sys.argv[1])
		workQueue = Queue() #Using 2 queues from python multiprocessing module so that worker processes can create their own bloom filters and send them back to master process for merging (map reduce)
		doneQueue = Queue()
		processes = []
	
	
		# Start cpuCount -1 processes
		print "Starting %d processes..." %(cpuCount -1)
		for w in xrange(cpuCount - 1):
			p = Process(target=bloomWorker, args=(workQueue, doneQueue, start))
			p.start()
			processes.append(p)
	
		print "Reading file and pushing to worker processes..."	
		# Read file line by line and push into workQueue
		for line in f.readlines():
			line = line.strip()
			workQueue.put(line) # We could add a line of code here to wait before pushing further if memory is overloaded
		f.close()
		print "File pushed. Workers starting..."
	
		# Add a sentinel code for each process to signal end of queue
		for w in xrange(cpuCount - 1):
			workQueue.put('S') #S for stop
	
		
		doneCount = 0
		count = 0
		bloomArrays = []
		while True:
			count += 1
			# pop is either a 10 million length long bloom array, or a sentinel S to signal end
			pop = doneQueue.get()
			if pop == 'S':
				doneCount += 1 #If we get cpuCount -1 number of S we are done
				if doneCount == cpuCount - 1:
					break
				continue
			else:
				bloomArrays.append(pop) # We receive cpuCount -1 number of bloomArrays
		
		#Wait for the worker processes to die
		for p in processes:
			p.join()
	
		print "Workers done. Merging bloomarrays..."
	
		for i in range(len(finalBloomArray)):	
			total = 0
			for bloomArrayNumber in range(len(bloomArrays)):
				total += bloomArrays[bloomArrayNumber][i]
			finalBloomArray[i] = total
		with open('bloom.pickle', 'wb') as fp:
			pickle.dump(finalBloomArray, fp)
		fp.close()
		del bloomArrays #Free some space
		
		print "Merging done. Building hashmap..."

	f = open(sys.argv[1])
	freqCount = int(sys.argv[2])
	
	subStringHash = {}
	count = 0
	for line in f.readlines():
		line = line.strip()
		count += 1
		if count % 10000 == 0:
			print "%d lines processed. Hashmap size = %d. Time elapsed %d seconds."%(count, len(subStringHash), time.time() - start)
		for windowSize in range(1, 57):
			seen = {} #If 'aa' is in string 'aaaa' do a +1 not +2
			for startPosition in range(0, 56 - windowSize + 1):
				subString = line[startPosition:startPosition+windowSize]
				if lookupFrequent(subString, freqCount):
					if subString in subStringHash:
						subStringHash[subString] += 1
					else:
						subStringHash[subString] = 1

	print "Hashmap built. Printing result..."
	count = 0
	maxLength = 0
	sumLength = 0
	for k,v in subStringHash.items():
		if v >= freqCount:
			count += 1
			print "%d frequent -> %s"%(freqCount, k)
			if len(k) > maxLength:
				maxLength = len(k)
			sumLength += len(k)
       
	print "Total number of frequent strings %d"%count
	print "Length of longest frequent string %d"%maxLength
	print "Average length of frequent strings %d"%(sumLength/float(count))	
	print "Time taken %d seconds"%(time.time() - start)
