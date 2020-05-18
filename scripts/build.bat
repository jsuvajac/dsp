@echo off
if not exist build mkdir build
pushd build
cl -EHsc -Zi -FC -O2^
    ..\src\* ^
	-Fe:engine.exe^
    -I ..\include -I^
    Shell32.lib^
    -link -SUBSYSTEM:CONSOLE -PDB:vc140.pdb 
popd