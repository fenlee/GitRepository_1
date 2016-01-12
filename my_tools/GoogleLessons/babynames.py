import sys
import re

#Suggested milestones for incremental development:
# -Extract the year and print it
# -Extract the names and rank numbers and just print them
# -Get the names data into a dict and print it
# -Build the [year, 'name rank', ... ] list and print it
# -Fix main() to use the extract_names list


def extract_names(filename):
	dict = {}
	list_out = []
	f = open(filename, 'rU')
	
	list = f.read()
	year = re.search(r'(\w+\s\in)\s(\d+)', list)
	list_out.append(year.group(2))

	rank_names = re.findall(r'(\d+)<........(\w+)<........(\w+)', list)
	group0 = [x[0] for x in rank_names]
	group1 = [x[1] for x in rank_names]
	group2 = [x[2] for x in rank_names]
	counter = 0
		
	for a in group0:
		dict[group1[counter]] = group0[counter]
		dict[group2[counter]] = group0[counter]
		counter += 1
# Extract all the data tuples with a findall()
  # each tuple is: (rank, boy-name, girl-name)
  tuples = re.findall(r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', text)
  #print tuples


# Better, way for extraction from tuple after findall() "re" functions
# Store data into a dict using each name as a key and that
# name's rank number as the value.
# (if the name is already in there, don't add it, since
# this new rank will be bigger than the previous rank).
#  names_to_rank =  {}
#  for rank_tuple in tuples:
#    (rank, boyname, girlname) = rank_tuple  # unpack the tuple into 3 vars
#    if boyname not in names_to_rank:
#      names_to_rank[boyname] = rank
#    if girlname not in names_to_rank:
#      names_to_rank[girlname] = rank
# You can also write:
# for rank, boyname, girlname in tuples:
#   ...
# To unpack the tuples inside a for-loop.

	
	for key in dict:
		list_out.append((key + " " + dict[key]))
	list_out = sorted(list_out)
	
	
	#for out in range(10):
	#	print list_out[out]
	
	#print list_out
	return list_out
		

def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]
	
	# +++your code here+++
  for filename in args:
	names = extract_names(filename)
	
	text = '\n'.join(names)
	
	if summary:
	  newfile = open((filename + ".summary"), "w")
	  newfile.write(text + '\n')
	  newfile.close()
	else:
	  print text
	
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  
if __name__ == '__main__':
  main()


		
#def main():
#	extract_names(sys.argv[1])
	
#if __name__ == '__main__':
#  main()

####################
# way to build dictionary from list of tuples
####################
# Store data into a dict using each name as a key and that
  # name's rank number as the value.
  # (if the name is already in there, don't add it, since
  # this new rank will be bigger than the previous rank).
 #names_to_rank =  {}
 #for rank_tuple in tuples:
 #  (rank, boyname, girlname) = rank_tuple  # unpack the tuple into 3 vars
 #  if boyname not in names_to_rank:
 #    names_to_rank[boyname] = rank
 #  if girlname not in names_to_rank:
 #    names_to_rank[girlname] = rank
