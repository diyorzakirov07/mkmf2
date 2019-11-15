#!/bin/python
import re;

verbose = True
vv = False
"""open the file and read contens"""
fname = "diag_manager.F90"
if verbose or vv:
	print('open ',fname,' and read contens')
f = open(fname, 'r')
fcontents = f.read()
if vv:
	print(fname, ":\n ",fcontens)
f.close()


""" Set up the regex to find use statements ^\s*use """
module_dependencies = []
findUse = re.compile('^\s*use', re.IGNORECASE)
findOnly = re.compile('only\s*:', re.IGNORECASE)
findUseAmp = re.compile('^\s*use&', re.IGNORECASE)
findUseAmpSpc = re.compile('^\s*use\s+&', re.IGNORECASE)


'''Parse each line of the file for the regex ^\s*use '''
if verbose or vv:
	print('Parse each line of the file for the regex ^\s*use ')
for index, line in enumerate(fcontents.splitlines()):
	if findUse.match(line):	 
		if verbose or vv:
			print(line)
		splitModLineCom = line.split(",")	
		print(splitModLineCom)
		for mods in splitModLineCom:
			if (findUseAmp.match(mods) or findUseAmpSpc.match(mods)):
				if fcontents.splitlines()[index+1].split(",")[1]:
					splitmodLineCom = fcontents.splitlines()[index+1]
					print(splitmodLineCom)
					for mods in splitModLineCom:
						alreadyExists = False
						for md in module_dependencies:
							if md == mods[0]:
								alreadyExists = True
								if vv:
									print(fname,": the module ",md," is listed more than once.  only keeping one")
									break;
							if not alreadyExists:
								module_dependencies.append(mods[0])
				else:
					temp = 2
					while not fcontents.splitlines()[index+temp][1]:
						temp += 1
					splitmodLineCom = fcontents.splitlines()[index+temp]
					for mods in splitModLineCom:
						alreadyExists = False
						for md in module_dependencies:
							if md == mods[0]:
								alreadyExists = True
								if vv:
									print(fname,": the module ",md," is listed more than once.  only keeping one")
									break;
							if not alreadyExists:
								module_dependencies.append(mods[0])				
			if findUse.match(mods) and len(splitModLineCom) > 1:
				mod1 = mods.split()
				alreadyExist = False
				for md in module_dependencies:
					if md == mod1[1]:
						alreadyExist = True
						if vv:
							print(fname,": the module ",md," is listd more than once.  only keeping one")
						break
				if not alreadyExist:
					module_dependencies.append(mod1[1])
		
		
		
		
		
if verbose or vv:
	print("The dependencies for ",fname," are ",module_dependencies)

