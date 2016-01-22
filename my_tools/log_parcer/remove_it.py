#!/usr/bin/python2.7 -tt

import re, os, sys, commands, shutil


def items_to_cleanup(mixed_txt_file):
	file_open = open(mixed_txt_file, 'rU')
	content = file_open.read()
  
  # Get list of paths to file and attention reg values
	check_match = re.search(r'\w:\\|HKEY', content)
	if not check_match:
		sys.stderr.write('Attention lines not found !\n')
		sys.exit(1)

	target_list = re.findall('[A-Z]:.+|HKEY.+', content)
	
	list_of_items_to_cleanup = []
	for idx in range(len(target_list)):
		if 'Mozilla\Firefox\Profiles' in target_list[idx]:
			match = re.search(r'[A-Z]:\\\w+\\\w+\\\w+\\\w+\\Mozilla\\Firefox\\Profiles\\\w+\.\w+', content)
			if match.group() not in list_of_items_to_cleanup:
				list_of_items_to_cleanup.append(match.group())
		else:
			list_of_items_to_cleanup.append(target_list[idx])
		
	return list_of_items_to_cleanup
	
	
def backup_before_cleanup(list_of_items_to_cleanup):
	backup_dir = 'remove_it_backup'
	if not os.path.exists(backup_dir):
		os.mkdir(backup_dir)
	backup_dir = (os.path.abspath(backup_dir) + '\\')
				
	for content in list_of_items_to_cleanup:
		if re.search(r'\w:\\', content) and re.search(r'[.]', content[-4:]):
			backup_destination = backup_dir + '\\'.join((content.split('\\'))[1:-1])
			print 'Making backup of', content, '\n', 'in', backup_dir, '\n'
			if not os.path.exists(backup_destination):
				os.makedirs(backup_destination)
			shutil.copy(content, backup_destination)
		
		elif re.search(r'\w:\\', content):
			backup_destination = backup_dir + '\\'.join((content.split('\\'))[1:])
			if not os.path.exists(backup_destination):
				os.makedirs(backup_destination)

		elif content.startswith('HKEY'):
			reg_query = 'REG QUERY "{}"'.format(content)
			if os.system(reg_query) == 0:
				print '"{}"'.format(content), 'found ...', 'Making backup on', '\n', os.path.abspath(backup_dir), '\n'
				backup_filename = (content.split('\\')[-1]) + '.reg'
				reg_export = 'REG EXPORT "{}"'.format(content) + ' ' + '"{}"'.format(backup_dir + backup_filename)
								
				if os.system(reg_export) == 0:
					print 'file', backup_filename, '- passed.', '\n'
					
				else:
					print 'There is an error durring save', backup_filename, 'to', '\n', os.path.abspath(backup_dir), '\n'
		else:
			print  '"{}"'.format(content), "- doesn't exist", '\n'
  
def main():
	args = sys.argv[1:]
 
	if not args:
		print 'usage: logfile'
		sys.exit(1)

	else:
		backup_before_cleanup(items_to_cleanup(sys.argv[1]))
		
if __name__ == '__main__':
	main()
