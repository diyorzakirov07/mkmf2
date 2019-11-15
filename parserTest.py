"""Parser Test.

Simple test of the Fortran file parser.
"""
from parseShort import getModules;
import sys;

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

if __name__ == "__main__":
	verbose = False
	for i in sys.argv:
		if i == "--verbose" or i == "-v":
			verbose = True
	
	print("------------------------------")
	for i in getModules(sys.argv[1], verbose):
		if not verbose:
			print(i)
	print("------------------------------")
	
	
