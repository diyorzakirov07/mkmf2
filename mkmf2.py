#!/bin/env python
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
import argparse;

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='mkmf')
	parser.add_argument("path", help="Path to the fortran modules")
	parser.add_argument("-R","--recursive", help="Run the script recursively, including all sub directories", action="store_true")
	parser.add_argument("-v","--verbose", help="Prints out each step the script is doing", action="store_true")
	parser.add_argument("-vv","--veryverbose", help="Prints out more detailed steps of the script", action="store_true")
	parser.add_argument("--maindir", help="Specifies that this is a main directory for AMCPPFLAGS", action="store_true")
	args = parser.parse_args()
	
	writeModules(args.path, args.verbose, args.veryverbose, args.recursive, args.maindir)
	if args.verbose or args.veryverbose:
		print("-------------------------------")
		print("All dependencies are resolved.")
		print("-------------------------------")
	