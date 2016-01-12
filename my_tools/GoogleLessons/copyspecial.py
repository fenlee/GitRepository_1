#!/usr/bin/python2.7 -tt

import re, os, sys, commands, shutil

def List(dir):
	pathlist = []
	filenames = os.listdir(dir)
	for filename in filenames:
		name = re.search('\w+__\w+__', filename)
		if name:
			path = os.path.join(dir, filename)
			pathlist.append(os.path.abspath(path))
  return pathlist 

def MakeCopy(SourceDir, TargetDir):
	if os.path.exists(TargetDir):
		pass
	else:
		os.mkdir(TargetDir)
	for copy_item in List(SourceDir):
		shutil.copy(copy_item, TargetDir)


def Zip(SourceFiles, ZipName):
	files = ''
	for filename in List(SourceFiles):
		files = files + ' ' + filename

	cmd = 'zip -j ' + ZipName + ' ' + files
	print 'about to do this: ' , cmd

	(status, output) = commands.getstatusoutput(cmd)
	if status:
		sys.stderr.write('there was an error: ' + output + '\n')
		sys.exit(1)
 
def main():
	args = sys.argv[1:]

 
	if not args:
		print 'usage: [--todir dir][--tozip zipfile] dir dir dir '
		sys.exit(1)

	elif args[0] == '--todir':
		SourceDir = args[-1]
		TargetDir = args[1]
		MakeCopy(SourceDir, TargetDir)

	elif args[0] == '--tozip':
		SourceFiles = args[-1]
		ZipName = args[1]
		Zip(SourceFiles, ZipName)

	else:
		for item in List(sys.argv[-1]):
			print item



if __name__ == '__main__':
	main()

