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
		if re.search(r'\w:\\', content) and not os.path.isdir(content):
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
				print '"{}"'.format(content), 'found', 'Making backup on', '\n', os.path.abspath(backup_dir), '\n'
				backup_filename = (content.split('\\')[-1]) + '.reg'
				reg_export = 'REG EXPORT "{}"'.format(content) + ' ' + '"{}" /y'.format(backup_dir + backup_filename)
								
				if os.system(reg_export) == 0:
					print 'file', backup_filename, '- done', '\n'
					
				else:
					print reg_export, '\n', 'There is an error durring save', backup_filename, 'to', '\n', os.path.abspath(backup_dir), '\n'
		else:
			print  '"{}"'.format(content), "- doesn't exist", '\n'
			
def cleanup_by_sourcelist(list_of_items_to_cleanup):
	list_of_empty_dirs = []
	couter_of_cleaned_items = 0
	couter_of_items_to_cleanup = len(list_of_items_to_cleanup)
	for content in list_of_items_to_cleanup:
		if not content.startswith('HKEY'):
			# print 'working under: ', content, '\n'
			cleanup_cmd = 'del /F /Q "{}"'.format(content)
			if content not in list_of_empty_dirs:
				list_of_empty_dirs.append(content)
			
		else:
			cleanup_cmd = 'REG DELETE "{}" /f'.format(content)
			

		if os.system(cleanup_cmd) == 0:
			print content, '- removed'
			couter_of_cleaned_items += 1
	
	empty_dirs_removal(list_of_empty_dirs)
	summary = 'items found: {}'.format(couter_of_items_to_cleanup) + '\n' + 'items cleaned: {}'.format(couter_of_cleaned_items) + '\n'
	return summary


def empty_dirs_removal(list_of_empty_dirs):
	
	for content in list_of_empty_dirs:
		path_to_empty_dir = '\\'.join((content.split('\\'))[:-1])
		
		if not os.path.isdir(content) and os.path.exists(path_to_empty_dir) and len(os.listdir(path_to_empty_dir)) == 0:
			print 'last file was removed, there is an empty dir :', '\n', path_to_empty_dir, 'removed', '\n'
			shutil.rmtree(path_to_empty_dir)
	
		elif os.path.isdir(content) and len(os.listdir(content)) == 0:
			print '\n', 'there is an empty dir: ', content, 'removed', '\n'
			shutil.rmtree(content)
	else:
		pass
  
def main():
	args = sys.argv[1:]
 
	if not args:
		print 'usage: < --nobackup > logfile'
		sys.exit(1)
	
	elif args[0] == '--nobackup':
		print cleanup_by_sourcelist(items_to_cleanup(sys.argv[-1]))
	
    
	else:
		backup_before_cleanup(items_to_cleanup(sys.argv[1]))
		cleanup_by_sourcelist(items_to_cleanup(sys.argv[1]))
		
if __name__ == '__main__':
	main()
