import argparse, os
__author__ = 'th3s3cr3tag3nt'
__modder__ = 'c0d3ma5t3r'
parser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,description='''\
 _ __ ___  _   _ _ __   __ _  ___   _ __  _   _
| \'_ \' _ \| | | | \'_ \ / _\' |/ _ \ | \'_ \| | | |
| | | | | | |_| | | | | (_| |  __/_| |_) | |_| |
|_| |_| |_|\__,_|_| |_|\__, |\___(_) .__/ \__, |
					   |___/       |_|    |___/

Dirty little word munger by Th3 S3cr3t Ag3nt.
'''
)

def replace(w,chars):
	global wordlist
	for c in chars:
		if c in w:
			wordlist.append(w.replace(c,chars[c]))

def append(w,chars):
	global wordlist
	for c in chars:
		wordlist.append(f'{w}{c}')

def basic(w):
	global wordlist
	wordlist.append(w)
	wordlist.append(w.upper())
	wordlist.append(w.capitalize())
	wordlist.append(w.swapcase())

def advanced(w):
	global wordlist
	alts = {'e':'3','a':'4','i':'!','o':'0','s':'$'}
	nums = ('1','123456','12','2','123','!','.',
	'?','_','0','01','69','21','22','23','1234',
	'8','9','10','11','13','3','4','5','6','7')
	basic(w)
	replace(w,alts)
	append(w,nums)

def expert(w):
	global wordlist
	alts = {'a':'@','i':'1','l':'1'}
	nums = ('07','08','09','14','15','16','17','18','19','24','77',
	'88','99','12345','123456789','00','02','03','04','05','06',
	'19','20','25','26','27','28','007','1234567','12345678','111111',
	'111','777','666','101','33','44','55','66','2008','2009','2010',
	'2011','86','87','89','90','91','92','93','94','95','98')
	advanced(w)
	replace(w,alts)
	append(w,nums)

def munge(word, level):
	global wordlist
	if 1 > level > 3:
		print("Error on level, defaulting to 3")
		level = 3
	match level:
		case 1:
			basic(word)
		case 2:
			advanced(word)
		case 3:
			expert(word)

def write_file():
	with open(args.output, 'w') as f:
		for word in wordlist:
				f.writelines(f'{word}\n')

def read_file():
	with open(args.input, 'r') as f:
		for word in f:
			munge(word.strip(), args.level)

def cleanup():
	global wordlist
	for c in wordlist:
		if c == '':
			wordlist.remove(c)


#define arguments for script
parser.add_argument('word',metavar='word',nargs='?',help='word to munge')
parser.add_argument('-l','--level',type=int,default=5,help='munge level [1-3] (default 3)')
parser.add_argument('-i','--input',dest='input',help='input file')
parser.add_argument('-o','--output',dest='output',help='output file')

#get arguments
args = parser.parse_args()

#clamp level 0-3
if args.level > 3:
	args.level = 3
if args.level < 0:
	args.level = 0

#init empty word list
wordlist = []

if args.word:
	word = args.word.lower()
	munge(word, args.level)

elif args.input:
	#Open the file with read only
	try:
		read_file()
	except IOError:
		print(f"Exiting\nCount not read file: {args.input}")
else:
	print("Nothing to do...\nTry -h for help.")

wordlist = sorted(set(wordlist))
cleanup()

if args.output:
	#Open the file with write only
	try:
		write_file()
		print(f"Written to: {args.output}")
	except IOError:
		print(f"Exiting\nCould not write file: {args.input}")
else:
	for word in wordlist:
		print(word)

