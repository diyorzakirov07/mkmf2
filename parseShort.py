"""mkmf2

Resolves dependencies between Fortran modules.
""" 

''' 
!***********************************************************************
!*                   GNU Lesser General Public License
!*
!* This file is part of the GFDL Flexible Modeling System (FMS).
!*
!* mkmf2 is free software: you can redistribute it and/or modify it under
!* the terms of the GNU Lesser General Public License as published by
!* the Free Software Foundation, either version 3 of the License, or (at
!* your option) any later version.
!*
!* mkmf2 is distributed in the hope that it will be useful, but WITHOUT
!* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
!* FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
!* for more details.
!*
!* You should have received a copy of the GNU Lesser General Public
!* License along with FMS.  If not, see <http://www.gnu.org/licenses/>.
!*
!* Author: Diyor Zakirov
!***********************************************************************
'''
import re;
import os;


def getModules(fileName, verbose = False, vv = False):
	"""Parses Fortran file and returns module dependencies.

	This function takes in a file to parse through. 
	Using regex to pattern match, populates a module list, cleans up, and returns without duplicates.
	Requires a name of the file to be parsed.  
	"""
	MODS = [] 
	
	fileContents = open(fileName, encoding = 'latin-1').read()

	if verbose or vv:
		print("Open " + fileName + " and read contents")
	
	if vv:
		print("Regex pattern to find matches in the file. Checks for USE and possible & on the same or next line, until module name is found signified by the '?'. Ignores cases and tries to match on all lines")
		print("Regex patter: ^ *USE[ &\n]+.*?[ &\n]*,")
	patternMatch = re.compile('^ *USE[ &\n]+.*?[ &\n]*,', re.IGNORECASE | re.M) 
	
	if verbose or vv:
		print("Parsing the file, finding all possible matches using regex")
		
	"""Finds all possible matches in the file.
	Puts all possible matches in a list.
	"""
	matches = re.findall(patternMatch, fileContents)
	
	"""Grooms and populates return list of modules.
	Removes spaces, characters from pattern matching, and checks for duplicates.
	"""
	for match in matches:
		if verbose or vv:
			print("Match found: " + match)
		match = match.lower().strip()
		badChars = ["use", "&", '\n', ' ', ',']
		for char in badChars:
			match = match.replace(char, '')
		if verbose or vv:
			print("Cleaning up the match: " + match +"\n")
		if not match in MODS:
			MODS.append(match)
	
	if verbose or vv:		
		print("The module dependencies are:")
		for m  in MODS:
			print(m)
		print("\n")
		
	return MODS


def getFileModuleName(fileName):
	"""Returns the module name of a file.
	
	Requires name of file to be parsed.
	"""
	badChars = ["module", "module.", "modules"]
	
	fileContents = open(fileName, encoding = 'latin-1').read()
	
	moduleNameMatch = re.compile('MODULE+.*', re.IGNORECASE)
	
	matches = re.findall(moduleNameMatch, fileContents)
	if not matches or matches[0] in badChars:
		matches = ' '
		return matches
	else:
		return matches[0].split(' ')[1]


def getPathModuleNameList(path):
	"""Returns a list of modules in given path.
	
	Requires a path to be parsed.
	"""
	moduleList = []
	
	fileList = os.listdir(path)
	for file in fileList:
		if os.path.isfile(file) and file != "Makefile.am":
			moduleList.append(getFileModuleName(file))
	
	return moduleList

def getSubdirModuleNameList(path):
	"""Returns a list of modules from sub directories of a path given.
	
	Requires a path to be parsed.
	"""
	subdirModuleList = []
	
	fileList = os.listdir(path)
	
	for file in fileList:
		if os.path.isfile(path + "/" + file) and file != "Makefile.am":
			subdirModuleList.append(getFileModuleName(path + "/" + file))
			
	return subdirModuleList

"""Global value for APCPPFLAGS dictionary"""
amcppDic = {}
def getAMCPP(path):
	
	fortranMatch = re.compile('.*F90', re.IGNORECASE)
	
	fileList = os.listdir(path)
	
	for file in fileList:
		if not os.path.isfile(path + "/" + file):
			getAMCPP(path + "/" + file)
		elif fortranMatch.match(file):
			amcppDic[getFileModuleName(path + "/" + file)] = path.split('/')[len(path.split('/'))-1]
			
	return amcppDic
			
			
def writeModules(path, verbose = False, vv = False, recursive = False, mainDir = False):
	"""Creates a Makefile.am
	
	Creates a Makefile.am in the path provided, resolving all possible dependencies.
	Requires a path to a folder with Fortran modules. 
	"""
	
	if mainDir:
		getAMCPP(path)
		if verbose or vv:
			print("Creating AMCPPFLAGS dictionary...")
			print(amcppDic)
	
	fortranMatch = re.compile('.*F90', re.IGNORECASE)
	
	"""Runs recursively"""
	if recursive:
		if verbose or vv:
			print("Running recursively...")
		for file in os.listdir(path):
			if file == ".git":
				pass
			else:
				if not os.path.isfile(path + "/" + file):
					writeModules(path + "/" + file, verbose, vv, recursive, mainDir = False)
	
	os.chdir(path)
	
	folder = path.split('/')[len(path.split('/'))-1]
	
	makefile = open('Makefile.am', 'w',)
	
	fileList = os.listdir(path)
	
	subDirModules = []
	
	DONE = False
	
	AMCPPFLAGS_str = ''
	SUBDIRS_str = ''
	SUBDIRSLIB_str = ''
	SOURCES_str = ''
	MODULESINIT_str = ''
	DEPENDENCIES_str = ''
	BUILTSOURCES_str = ''
	
	if verbose or vv:
		print("Setting work directory to " + path + "\n")
		print("Files to parse:\n")
		for f in fileList:
			print(f)
	
	"""Populating the subDirModules if there are any"""
	if recursive:
		for file in fileList:
			if file == ".git":
				break;
			if not os.path.isfile(path + "/" + file):
				subDirModules += (getSubdirModuleNameList(path + "/" + file))
				if verbose or vv:
					print("Creating list of sub directory modules...")
					if vv:
						print(subDirModules)
					

	
	for file in fileList:
		"""List all possible sub directories"""
		if not os.path.isfile(path + "/" + file) and file != ".git":
			if verbose or vv:
				print("Found sub directory: " + file)
			SUBDIRS_str += ("\t" + file + " \\\n")
			SUBDIRSLIB_str += "\tlib" + file + ".la \\\n"
		
		
		"""List Fortran file sources"""
		if fortranMatch.match(file):
			if verbose or vv:
				print("Found source file: " + file)
			SOURCES_str += ("\t" + file + " \\\n")
			MODULESINIT_str += (getFileModuleName(file) + ".$(FC_MODEXT) : " + file.split('.')[0] + ".$(OBJEXT)\n")
			
			"""List dependencies of each file"""
			set1 = set(getModules(file, verbose,vv)).intersection(getPathModuleNameList(path))
			set2 = set(getModules(file, verbose,vv)).intersection(subDirModules)
			"""List AMCPPFLAGS for modules"""
			for mod in getModules(file,vv):
				if mod in amcppDic and not mod in set1 and not mod in set2:
					if amcppDic[mod] in AMCPPFLAGS_str:
						pass; 
					else:
						if vv:
							print("Found module needing AMCPPFLAG: " + mod)
						AMCPPFLAGS_str += "\t-I${top_buildir}/" + amcppDic[mod] + " \\\n"
			if set1 or set2:
				if verbose or vv:
					print("Found dependencies for " + file)
					print("Dependencies...\n")
					print(set1)
					print(set2)
				DEPENDENCIES_str += (file.split('.')[0] + ".$(OBJEXT) : \\\n")
			for mod in set1:
				DONE = True
				DEPENDENCIES_str += ("\t" + mod + ".$(FC_MODEXT) \\\n")
			for mod in set2:
				DONE = True
				DEPENDENCIES_str += ("\t" + mod + ".$(FC_MODEXT) \\\n")
			if DONE:
				DEPENDENCIES_str = DEPENDENCIES_str[0:len(DEPENDENCIES_str)-3] + "\n"
				DONE = False		
			
			"""List all modules files in built_sources"""
			BUILTSOURCES_str += ("\t" + getFileModuleName(file) + ".$(FC_MODEXT) \\\n")
	
	
	"""Write populated strings to the file"""
	if AMCPPFLAGS_str != '':
		if verbose or vv:
			print("\nWriting AMCPPFLAGS... \n")
			if vv:
				print(AMCPPFLAGS_str)
		makefile.write("AM_CPPFLAGS = \\\n" + AMCPPFLAGS_str[0:len(AMCPPFLAGS_str)-2] + '\n')
	
	makefile.write("\n\n")
	
	if SUBDIRS_str != '':
		if verbose or vv:
			print("\nWriting sub directories... \n")
			if vv:
				print(SUBDIRS_str)
		makefile.write("SUBDIRS = \\\n" + SUBDIRS_str[0:len(SUBDIRS_str)-3] + '\n')
		makefile.write('\n\n')
		makefile.write("lib" + folder + "_la_LIBADD = \\\n" + SUBDIRSLIB_str[0:len(SUBDIRSLIB_str)-3] + '\n')
	
	makefile.write("\n\n")
	
	if SOURCES_str != '':
		if verbose or vv:
			print("\nWriting Fortran sources... \n")
			if vv:
				print(SOURCES_str)
		makefile.write("noinst_LTLIBRARIES = lib" + folder + ".la\n" +
					  "lib" + folder +"_la_SOURCES = \\\n" + 
					  SOURCES_str[0:len(SOURCES_str)-2] + '\n')
		
		makefile.write("\n\n")
		
		if verbose or vv:
			print("\nWriting module initializations... \n")
			if vv:
				print(MODULESINIT_str)
		makefile.write(MODULESINIT_str)
		
		makefile.write("\n\n")
		
		if verbose or vv:
			print("\nWriting module dependencies... \n")
			if vv: 
				print(DEPENDENCIES_str)
		makefile.write(DEPENDENCIES_str)
		
		makefile.write("\n\n")
		
		if verbose or vv:
			print("\nWriting built_sources... \n")
			if vv:
				print(BUILTSOURCES_str)
		makefile.write("MODFILES = \\\n" + BUILTSOURCES_str[0:len(BUILTSOURCES_str)-3] + '\n' + 
					"BUILT_SOURCES = $(MODFILES)\n" + 
					"include_HEADERS = $(MODFILES)\n")
		
		makefile.write("\n\n")
	
	
	makefile.write("CLEANFILES = *.$(FC_MODEXT)")
	
	
	
if __name__ == '__main__':
	pass
	#writeModules('/home/Diyor.Zakirov/FMS')

	
	
                                     