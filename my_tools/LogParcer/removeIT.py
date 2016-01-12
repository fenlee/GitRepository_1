#!/usr/bin/python2.7 -tt

import re, os, sys, commands, shutil


def List(filename):
	f = open(filename, 'rU')
	text = f.read()
  
  # Get list of paths to file and attention reg values
	FilePath_match = re.search(r'\w:\\', text)
	RegPath_match = re.search(r'HKEY', text)
	if not FilePath_match:
		sys.stderr.write('Attention lines not found !\n')
		sys.exit(1)
#  if not RegPath_match:
#	sys.stderr.write('Attention lines not found !\n')
#   sys.exit(1)
#  else:
#    pass
  
# 20:02:59.492	Found	adriver.ru	Tracking Cookie	C:\Users\Knight\AppData\Roaming\Mozilla\Firefox\Profiles\f2qeychw.default\cookies.sqlite: adriver.ru
# 20:04:01.365	Found	Crossrider	Adware, Toolbar	HKEY_CURRENT_USER\Software\AppDataLow\Software\Crossrider
  
	targetlist = re.findall('[A-Z]:.+|HKEY.+', text)
	
	cleanlist = []
	for idx in range(len(targetlist)):
		if 'Mozilla\Firefox\Profiles' in targetlist[idx]:
			match = re.search(r'[A-Z]:\\\w+\\\w+\\\w+\\\w+\\Mozilla\\Firefox\\Profiles\\\w+\.\w+', text)
			if match.group() not in cleanlist:
				cleanlist.append(match.group())
		else:
			cleanlist.append(targetlist[idx])
		
	return cleanlist
	
	
def removebackup(list):
	BackupDir = 'RemoveitBackUp'
	if os.path.exists(BackupDir):
		pass
	else:
		os.mkdir(BackupDir)
	for text in list:
		if re.search(r'\w:\\', text):
			if re.search(r'[.]', text[-4:]):
				splittext = text.split('\\')
				textpath = splittext[1:-1]
				cleanpath = '\\'.join(textpath)

				if os.path.exists(BackupDir + '\\' + cleanpath):
					shutil.copy(text, BackupDir + '\\' + cleanpath)
				else:
					os.makedirs(BackupDir + '\\' + cleanpath)
					shutil.copy(text, BackupDir + '\\' + cleanpath)
			else:
				splittext = text.split('\\')
				textpath = splittext[1:]
				cleanpath = '\\'.join(textpath)

				if os.path.exists(BackupDir + '\\' + cleanpath):
					shutil.copytree(text, BackupDir + '\\')
				else:
					os.makedirs(BackupDir + '\\' + cleanpath)
					shutil.copytree(text, BackupDir + '\\')
				

			
  
def main():
	args = sys.argv[1:]

 
	if not args:
		print 'usage: logfile'
		sys.exit(1)

	else:
		#print List(sys.argv[1])
		removebackup(List(sys.argv[1]))
		
if __name__ == '__main__':
	main()
