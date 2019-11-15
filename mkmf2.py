"""Main mkmf2 script.

From here you can run all the mkmf2 options including: -R, -v, -h
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

from parseShort import writeModules,getAMCPP;
import sys;

if __name__ == "__main__":
	verbose = False
	recursive = False
	vv = False
	mainDir = False
	for i in sys.argv:
		if i == "-R" or i == "--recursive": 
			recursive = True
		if i == "--verbose" or i == "-v":
			verbose = True
		if i == "-vv" or i == "--very-verbose":
			vv = True
		if i == "--maindir":
			mainDir = True
		if i == "-h" or i == "--help":
			print("----------------------------")
			print("Available options for mkmf2")
			print("-v/--verbose         Prints out each step the script is doing")
			print("-vv/--very-verbose   Prints out more detailed steps of the scripts")
			print("-R/--recursive       Run the script recursively, including all sub directories")
			print("--maindir            Specifies that this is a main directory for AMCPPFLAGS")
			print("-h/--help            Available arguments for mkmf2 script")
			sys.exit()
			
	
	writeModules(sys.argv[1], verbose, vv, recursive, mainDir)
	if verbose or vv:
		print("-------------------------------")
		print("All dependencies are resolved.")
		print("-------------------------------")
	
