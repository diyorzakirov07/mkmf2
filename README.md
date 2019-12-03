# How to run a parser test

1. git clone the master branch.
2. cd to mkmf2. 
3. Run the parserTest.py script that requiers a full path to a .F90 file or use 'diag_manager.F90'.

**Example:** 
```
python parserTest.py path/to/your/file
or
python parserTest.py diag_manager.F90
```

4. The script will print out all the module dependencies the file has.
5. You also can test the Makefile.am creation.
6. Run the mkmf2 script with a full path to the folder with Fortran modules.

**Example:**
```
./mkmf2.py path/to/your/folder
``` 
**Available options for mkmf2.py**
```
-v/--verbose
-vv/--very-verbose
-R/--recursive
--maindir
-h/--help
```
7. Makefile.am will be created in the same path that was given. 

# mkmf2
mkmf2 is a tool to create Makefile.am files based on fortran module depenencies.  
1. mkmf2 is a Python script
2. mkmf2 does not rely on any external programs that are not "commonly" available on target operating systems.
3. mkmf2 searches only the directory given for dependencies, ignoring subdirectories unless a -R --recursive option is given.
4. mkmf2 has an option (-l, --lib-name) to name the final library 
5. mkmf2 ignores all CPP macros when building the dependency tree
6. mkmfs ignores all #include/include statements that include a file not in the given directory/search path(s)
7. mkmf2 has a -v,--verbose option that clearly prints what the program is doing.  There is also a -vv/--very-verbose option
8. Source is (hopefully) clearly documented, including in-code comments, user documentation, etc., especially when the code may be unclear to another developer (e.g. when using complicated regular expressions).
9. mkmf2 has a -h/--help option to give a brief overview of options available.
10. mkmf2 works on *nix operating systems (including Mac OS X).

