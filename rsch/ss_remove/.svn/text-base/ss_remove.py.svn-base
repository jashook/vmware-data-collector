#!/usr/bin/env python
################################################################################
################################################################################
#
# Author: Jarret Shook
#
# Module: ss_remove.py
#
# Modifications:
#
# 13-Sept-13: Version 1.0: Last Updated
# 13-Sept-13: Version 1.0: Created
#
# Timeperiod: ev7n
#
################################################################################
################################################################################

import os
import subprocess

################################################################################
################################################################################

def add_extensions(_Names, _ExtensionDict, _Directory):

   _Index = 0

   for _Name in _Names:

      _Names[_Index] = _Directory + _Name + _ExtensionDict[_Name]

      _Index += 1

   return _Names

def ls(_Directory):

   _Process = subprocess.Popen(["ls -l " + _Directory], stdout=subprocess.PIPE, shell=True)

   (_Output, _Error) = _Process.communicate()

   return _Output

def get_int_ending(_String):
   
   _Index = -1

   _Number = 0

   while _String[_Index] >= '0' and _String[_Index] <= '9':

      _Number += (10 ** abs(_Index + 1)) * int(_String[_Index])

      _Index -= 1

   if len(_String) - (_Index + 1) == 1: return _String, _Number

   return _String[:_Index + 1], _Number

def get_lines(_Output):

   _Lines = [_String for _String in _Output.split("\n") if _String is not '' and _String[0] == '-']

   return _Lines

def get_names(_Output):

   _Lines = get_lines(_Output)

   return [_Line.split(" ")[-1] for _Line in _Lines]

def get_sizes(_Output):

   _Lines = get_lines(_Output)

   _Sizes = []

   for _Line in _Lines:

      _LineElements = _Line.split(" ") 

      _Count = 4

      while _LineElements[_Count] is '':

         _Count = _Count + 1

      _Sizes.append(_LineElements[_Count])

   return _Sizes

def get_sizes_and_names(_Output):

   _Sizes = get_sizes(_Output)

   _Names = get_names(_Output)

   return [[_Name, _Size] for _Name, _Size in zip(_Names, _Sizes)]

def remove_same_sizes(_Names):
   
   _Sizes = dict()

   _DeleteList = []

   for _NameSize in _Names:

      _Size = int(_NameSize[1])

      if _Sizes.has_key(_Size): _Sizes[_Size].append(_NameSize[0])

      else: _Sizes[_Size] = [_NameSize[0]]
   
   for _Key in _Sizes:

      _Sizes[_Key].sort()

      _Name = _Sizes[_Key][0]
      
      for _Item in _Sizes[_Key]:

         _StrippedItem, _ItemNumber = get_int_ending(_Name)

         _NextName = _StrippedItem + str(_ItemNumber + 1)

         if _Item == _Name: continue

         elif _Item == _NextName: 
         
            _DeleteList.append(_NextName)

            _Name = _Item

   return _DeleteList

def remove_extensions(_Output):

   _OuterIndex = 0

   _ExtensionDict = dict()

   for _Item in _Output:

      _Item = _Item[0]

      _Index = -1

      while _Item[_Index] != '.':

         _Index -= 1

      _Output[_OuterIndex][0] = _Item[:_Index]
      
      _ExtensionDict[_Output[_OuterIndex][0]] = _Item[_Index:]

      _OuterIndex += 1

   return _Output, _ExtensionDict

def remove_files(_Names):

   for _Name in _Names:

      print "rm " + _Name

      os.system("rm " + _Name)

if __name__ == '__main__':

   _Output = ls("/home/jarret/rsch/")

   _Names = get_sizes_and_names(_Output)

   _Names.sort()
 
   _Names, _Extensions = remove_extensions(_Names)
   
   _Names = remove_same_sizes(_Names)
   
   _Names = add_extensions(_Names, _Extensions, "/home/jarret/rsch/")

   remove_files(_Names)
