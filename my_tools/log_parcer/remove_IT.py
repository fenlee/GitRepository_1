#!/usr/bin/python2.7 -tt

import re, os, sys, commands, shutil


def List(filename):
	f = open(filename, 'rU')
	text = f.read()
  
  # Get list of paths to file and attention reg values
	check_match = re.search(r'\w:\\|HKEY', text)
	if not check_match:
		sys.stderr.write('Attention lines not found !\n')
		sys.exit(1)

	target_list = re.findall('[A-Z]:.+|HKEY.+', text)
	
	clean_list = []
	for idx in range(len(target_list)):
		if 'Mozilla\Firefox\Profiles' in target_list[idx]:
			match = re.search(r'[A-Z]:\\\w+\\\w+\\\w+\\\w+\\Mozilla\\Firefox\\Profiles\\\w+\.\w+', text)
			if match.group() not in clean_list:
				clean_list.append(match.group())
		else:
			clean_list.append(target_list[idx])
		
	return clean_list
	
	
def backup(list):
	backup_dir = 'remove_it_backup'
	if os.path.exists(backup_dir):
		backup_dir = os.path.abspath(backup_dir)
	else:
		os.mkdir(backup_dir)
		backup_dir = os.path.abspath(backup_dir)
		
	for text in list:
		if re.search(r'\w:\\', text):
			if os.path.exists(text):
				if re.search(r'\w:\\', text):
					if re.search(r'[.]', text[-4:]):
						
						clean_path = '\\'.join((text.split('\\'))[1:-1])
						if os.path.exists(backup_dir + '\\' + clean_path):
							print 'Making backup of', text, '\n', 'in', backup_dir, '\n'
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
			reg_query = 'REG QUERY' +' '+'"'+ text +'"'
			if os.system(reg_query) == 0:
				print '"'+ text +'"', ' exists !!!', 'Making backup on', '\n', os.path.abspath(backup_dir), '\n'
				backup_filename = (text.split('\\')[-1]) + '.reg'
				reg_export = 'REG EXPORT ' +'"'+ text +'"'+ ' ' +'"'+ backup_dir +'\\'+ backup_filename +'"'
				if os.system(reg_export) == 0:
					print backup_filename, ' - stored.', '\n'
					
				else:
						print 'There is an error durring save', backup_filename, 'to', '\n', os.path.abspath(backup_dir), '\n'
						
			else:
				print '"'+ text +'"', "-doesn't exist inside win register", '\n'
						
				
  
def main():
	args = sys.argv[1:]

 
	if not args:
		print 'usage: logfile'
		sys.exit(1)

	else:
		#print List(sys.argv[1])
		backup(List(sys.argv[1]))
		
if __name__ == '__main__':
	main()
