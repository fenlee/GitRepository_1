#!/usr/bin/python2.7 -tt

import re, os, sys, commands, shutil, subprocess


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
	
	
def backup_and_remove(list):
	backup_dir = 'remove_it_backup'
	if os.path.exists(backup_dir):
		pass
	else:
		os.mkdir(backup_dir)
	for text in list:
		if re.search(r'\w:\\', text):
			if os.path.exists(text):
				if re.search(r'\w:\\', text):
					if re.search(r'[.]', text[-4:]):
						
						clean_path = '\\'.join((text.split('\\'))[1:-1])
						if os.path.exists(backup_dir + '\\' + clean_path):
							print 'Making backup of', text, '\n', 'in', os.path.abspath(backup_dir), '\n'
							shutil.copy(text, backup_dir + '\\' + clean_path)
						else:
							os.makedirs(backup_dir + '\\' + clean_path)
							shutil.copy(text, backup_dir + '\\' + clean_path)
			
					else:
						clean_path = '\\'.join((text.split('\\'))[1:])
						if os.path.exists(backup_dir + '\\' + clean_path):
							pass
						else:
							os.makedirs(backup_dir + '\\' + clean_path)
			else:
				print 'Path: ',text,"doesn't exist"

		elif re.search('HKEY.+', text):
			
			#reg_query = 'REG QUERY ' + '"' + text + '"'
			#text = '"'+text+'"'
			print text
			reg_query = subprocess.call(['REG', 'QUERY', '"'+ text +'"'])
			print 'REG', 'QUERY', '"'+ text +'"'
			print 'about to do this QUERY: ', reg_query
						
			# (status, output) = commands.getstatusoutput(reg_query)
			# if status:
				# sys.stderr.write('there was a QUERY error: ' + output + '\n')
				# sys.exit(1)
			# else:
			backup_filename = (text.split('\\')[-1]) + '.reg'
				
			print 'Making backup of', text, '\n', 'in', os.path.abspath(backup_dir), '\n'
			
			#reg_export = 'REG EXPORT ' + text, ' ', '"' + backup_dir + '\\' + backup_filename
			print 'REG EXPORT ' + '"'+ text +'"', ' ', '"'+ backup_dir +'\\'+ backup_filename +'"'
			
			reg_export = subprocess.call(['REG', 'EXPORT', '"'+ text +'"' +' ' +'"'+ backup_dir +'\\'+ backup_filename +'"'])
			print 'about to do this EXPORT: ', reg_export
				
			# (status, output) = commands.getstatusoutput(reg_export)
			# if status:
				# sys.stderr.write('there was an EXPORT error: ' + output + '\n')
				# #sys.exit(1)
			# else:
			print backup_filename, ' - stored.'
		
		
		
  
def main():
	args = sys.argv[1:]

 
	if not args:
		print 'usage: logfile'
		sys.exit(1)

	else:
		#print List(sys.argv[1])
		backup_and_remove(List(sys.argv[1]))
		
if __name__ == '__main__':
	main()
