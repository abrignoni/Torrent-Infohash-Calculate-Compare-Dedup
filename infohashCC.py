import argparse, sys
import os.path 
from os import path
import glob
import bencoding, hashlib
import io
import shutil
import datetime

parser = argparse.ArgumentParser(description='Calculate and/or compare .torrent infohash values')
parser.add_argument("-o",choices=['calculate', 'compare', 'dedup'], required=True, 
                    help="Calculate or compare infohashes")
parser.add_argument("-p", "--path", required=True, help="Path to .torrent files. For compare include list.txt in same directory as the script")

if len(sys.argv[1:])==0:
    parser.print_help()
    # parser.print_usage() # for just the usage line
    parser.exit()
	
args = parser.parse_args()

script_dir = os.path.dirname(__file__)
caldict = dict()
calfail = dict()
caldedup = dict()
totals = 0
foldername = ("Dedup_Files_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

print ('')
print ('Infohash calculate & compare')
print ('By: @AlexisBrignoni')
print ('Web: abrignoni.com')
print ('')



def infohash(fname):
	objTorrentFile = open(fname, "rb")
	decodedDict = bencoding.bdecode(objTorrentFile.read())
	info_hash = hashlib.sha1(bencoding.bencode(decodedDict[b"info"])).hexdigest()
	return info_hash

#print(args)
print('Selected: ' + args.o)
print('Search directory: '+ args.path) 
#print(args.path)

if args.path is not None:
	pathcheck = os.path.exists(args.path) #verify directory exists
	if pathcheck:
		#If there are .torrent files in it
		#print('Path is real: ' +args.path)
		for filename in glob.iglob(args.path+'/**', recursive=True):
			if os.path.isfile(filename):
				if filename.lower().endswith(('.torrent')):
					try:
						calhash = infohash(filename) #Place values in dictionary
						caldict[calhash] = filename
					except:
						#print(filename+' is not a torrent file') #open text file to save failed values of calc. 
						calhash = 0
						calfail[calhash] = filename
						continue
	else: #Path does not exists
		print('Path is not valid. \n')
		parser.print_help()
		parser.exit()	
		
if args.o == 'calculate':
    if len(caldict) > 0:
        print('Calculated infohashes: ' + str(len(caldict)))
        print('')
        with io.open('./calculated.txt', 'w+', encoding='utf8') as z:
            for key, value in caldict.items():
                print(key+' => '+value)
                name = os.path.basename(value)
                z.write(key + '\t' + name + '\t' + value + '\n')
                #print the array, mention the text file.
            print('')
            print('See calculated.txt')
    else:
        print('No torrents to calculate')
        
elif args.o == 'compare':
	try:
		with io.open(script_dir+ 'list.txt', encoding='utf8') as f:
			lines = f.read().splitlines()#Insert txt values from list.txt in array. If zero values error. if values compare both arrays. Similar in a txt list.
		if len(lines) > 0:
			print('Infohashes to compare: '+ str(len(lines)))
			print('')
			with io.open('./matches.txt', 'w+', encoding='utf8') as w:
				for x in range(len(lines)):
					comparator = lines[x]
					if comparator in caldict.keys():
						print(comparator+' => '+caldict[comparator])
						names = os.path.basename(caldict[comparator])
						w.write(str(comparator) + '\t' + names + '\t' + str(caldict[comparator]) + '\n')
						totals = totals+1
			print('')
			print('Matching infohases total: '+ str(totals))
			if totals > 0:
				print('See matches.txt')
		else:
			print('No matching infohashes. Verify list.txt')
	except:
		print('Compare error.')
        
elif args.o == 'dedup':
	if len(caldict) > 0:
		print('Calculated infohashes: ' + str(len(caldict)))
		print('')
		os.mkdir(foldername)
		with io.open('./'+foldername+'.txt','w+', encoding='utf8') as g:
			for key, value in caldict.items():
				print(key)
				shutil.copy((value),('./'+foldername+'/'+key+'.torrent'))
				g.write(key + '\n')
			print('')
			print('See dedup.txt')
	else:
		print('No torrents to dedup')  