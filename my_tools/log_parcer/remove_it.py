#!/usr/bin/python2.7 -tt

import re, os, sys, commands, shutil, argparse


def items_to_clean_up(mixed_txt_file):
	file_open = open(mixed_txt_file, 'rU')
	content = file_open.read()
  
  # Get list of paths to file and attention reg values
	check_match = re.search(r'\w:\\|HKEY', content)
	if not check_match:
		sys.stderr.write('Attention lines not found !\n')
		sys.exit(1)

	target_list = re.findall('[A-Z]:.+|HKEY.+', content)
	list_of_items_to_clean_up = []
	
	for content in target_list:

		if content.startswith('HKEY') and os.system('REG QUERY "{}" >nul'.format(content)) == 0 or os.path.exists(content):
			list_of_items_to_clean_up.append(content)

		else:
			print content, '- not found'
	
	if len(list_of_items_to_clean_up) == 0:
		sys.exit(1)
	return list_of_items_to_clean_up


def backup_before_clean_up(list_of_items_to_clean_up):
	backup_dir = 'remove_it_backup'
	if not os.path.exists(backup_dir):
		os.mkdir(backup_dir)
	backup_dir = (os.path.abspath(backup_dir) + '\\')
				
	for content in list_of_items_to_clean_up:
		if not os.path.isdir(content) and os.path.exists(content):
			backup_destination = backup_dir + '\\'.join((content.split('\\'))[1:-1])
			print 'Making backup of', content, '\n', 'in', backup_dir, '\n'
			if not os.path.exists(backup_destination):
				os.makedirs(backup_destination)
			shutil.copy(content, backup_destination)
			
		elif re.search(r'\w:\\', content):
			backup_destination = backup_dir + '\\'.join((content.split('\\'))[1:])
			if not os.path.exists(backup_destination):
				os.makedirs(backup_destination)

		else:
			backup_filename = (content.split('\\')[-1]) + '.reg'
			reg_export = 'REG EXPORT "{}"'.format(content) + ' ' + '"{}" /y'.format(backup_dir + backup_filename)
			print '"{}"'.format(content), 'found', 'Making backup on', '\n', os.path.abspath(backup_dir), '\n'
			if os.system(reg_export) == 0:
				print 'file', backup_filename, '- done', '\n'
					
			else:
				print reg_export, '\n', 'There is an error durring save', backup_filename, 'to', '\n', os.path.abspath(backup_dir), '\n'
	

def clean_up_by_sourcelist(list_of_items_to_clean_up):
	list_of_empty_dirs = []
	couter_of_cleaned_items = 0
	couter_of_items_to_clean_up = len(list_of_items_to_clean_up)
	for content in list_of_items_to_clean_up:
		if os.path.exists(content):
			clean_up_cmd = 'del /F /Q "{}"'.format(content)
			list_of_empty_dirs.append(content)

		else:
			clean_up_cmd = 'REG DELETE "{}" /f'.format(content)
		
		if os.system(clean_up_cmd) == 0:
			couter_of_cleaned_items += 1

	empty_dirs_removal(list_of_empty_dirs)
	summary = 'items found: {}, cleaned: {}'.format(couter_of_items_to_clean_up, couter_of_cleaned_items)
	return summary

def empty_dirs_removal(list_of_empty_dirs):
	
	for content in list_of_empty_dirs:
		path_to_empty_dir = '\\'.join((content.split('\\'))[:-1])
		
		if not os.path.isdir(content) and os.path.exists(path_to_empty_dir) and len(os.listdir(path_to_empty_dir)) == 0:
			print 'last file was removed, there is an empty dir :', '\n', path_to_empty_dir, '- removed', '\n'
			shutil.rmtree(path_to_empty_dir)
	
		elif os.path.isdir(content) and len(os.listdir(content)) == 0:
			print '\n', 'there is an empty dir: ', content, '- removed', '\n'
			shutil.rmtree(content)
	else:
		pass
  

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('textfile', help='file, with list of paths to file/dir or REG value')
	parser.add_argument('-n', '--nobackup', action='count', help='skip the backup of data before clean-up')
	args = parser.parse_args()
	
	if not args.nobackup:
		backup_before_clean_up(items_to_clean_up(args.textfile))
	print clean_up_by_sourcelist(items_to_clean_up(args.textfile))
	

	
if __name__ == '__main__':
	main()