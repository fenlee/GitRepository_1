#!/usr/bin/python2.7 -tt

import re, os, sys, commands, shutil

def checknumbers(filename):
  f = open(filename, 'rU')
  list = f.read()
  numbermask = re.search(r'[^0-9]\d\d\d\d\d\d\d\d[^0-9]', list)

  if not numbermask:
    status = 0
  else:
    status = 1

  return status
 
def searchnumbers(filename):
  f = open(filename, 'rU')
  list = f.read()
  objectslist = re.findall(r'[^0-9]\d\d\d\d\d\d\d\d[^0-9]', list)
  uniq_numbers_list = []
  for number in objectslist:
    if number in uniq_numbers_list:
      pass
    else:
      uniq_numbers_list.append(number)
#     text = '\n'.join(number)
#     print number
  return uniq_numbers_list
  

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: parcer.py <filename.txt> '
    sys.exit(1)

  else:
    if os.path.exists(sys.argv[-1]):
      if checknumbers(sys.argv[-1]) > 0:
        for text in searchnumbers(sys.argv[-1]):
          number = re.search(r'\d\d\d\d\d\d\d\d', text)
          print number.group()
        print 'The textfile contains', len(searchnumbers(sys.argv[-1])), '8digits numbers.'
      else:
        print 'The text in file has no any 8digits numbers'
    else:
        print 'file: ',"'",sys.argv[-1],"'",' not found'

if __name__ == '__main__':
  main()