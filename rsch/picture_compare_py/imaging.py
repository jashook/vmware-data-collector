#!/usr/bin/env python
################################################################################
################################################################################
#
# Author: Jarret Shook
#
# Module: imaging.py
#
# Modifications: 
#
# 22-Jan-14: Version 1.0: Updated
# 22-Jan-14: Version 1.0: Created
#
################################################################################
################################################################################

import os
import sys
import hashlib
from PIL import Image
import re
from image import *

################################################################################
################################################################################

_Hashes = dict()

_StoredPictures = dict()

_ImageNames = []

def build_dictionary(_Directory):

   _Files = os.listdir(_Directory)

   for _File in _Files:

      if _File[0] == '.': continue

      if os.name is "nt" and _Directory[-1] != "/": 
         
         _Directory = _Directory + "\\"

         _Directory = _Directory.replace("\\", "/")

      print _Directory + _File

      _Image = Image.open(_Directory + _File)

      _InImage = image(_File)

      _ImageNames.append(_InImage.m_name)

      _StoredPictures[_InImage.m_name] = _InImage

      _Width, _Height = _Image.size

      _TempWidth = 0

      _TempHeight = 0

      _Offset = 30

      _SecondTime = False

      _SecondTimeWidth = False

      while True:

         _Left = _TempWidth

         _Top = _TempHeight

         _NewSize = [_Left, _Top, _Left + _Offset, _Top + _Offset]

         if (_NewSize[2] > _Width): _NewSize[2] = _Width

         if (_NewSize[3] > _Height): _NewSize[3] = _Height

         _NewPicture = _Image.crop(_NewSize)

         _Hash = hashlib.md5(_NewPicture.tostring()).hexdigest()

         try:
            
            _Hashes[_Hash]

            _Hashes[_Hash].add(_InImage)

         except:

            _List = set()

            _List.add(_InImage)
 
            _Hashes[_Hash] = _List

         _InImage.m_pictures.append(_Hash)

         _TempWidth = _TempWidth + _Offset

         if (_TempWidth > _Width):

            _TempWidth = 0

            _TempHeight = _TempHeight + _Offset

         if (_TempHeight >= _Height):

            break

   return _Hashes

if __name__ == "__main__":

   _Cluster = dict()

   if (len(sys.argv) == 2): 

      _Directory = sys.argv[1]

      _Dictionary = build_dictionary(_Directory)

      while True:
         try:
            
            _Key = iter(_Dictionary).next()

         except:

            break

         _Images = _Dictionary[_Key]

         _Image = iter(_Images).next()

         _Images = _Images - set([_Image])

         _TrackedImages = dict()

         for _Element in _Images:

            _TrackedImages[_Element] = 0

         for _Hash in _Image.m_pictures:

            _Copies = _Dictionary[_Hash] & _Images

            for _Copy in _Copies:

               if _Copy in _TrackedImages:

                  _TrackedImages[_Copy] = _TrackedImages[_Copy] + 1

            _NewTracks = _Dictionary[_Hash] - _Images

            for _NewTrack in _NewTracks:

               _TrackedImages[_NewTrack] = 1

         for _CurrentImage in _TrackedImages:

            _List = list()

            _List.append(_Image)

            if _TrackedImages[_CurrentImage] / len(_Image.m_pictures) > .7:

               _List.append(_TrackedImages[_CurrentImage])

               _Cluster[_Image] = _List

            else:

               _Cluster[_Image] = _List

            for _Hash in _Image.m_pictures:

               try:

                  del _Dictionary[_Hash]

               except:

                  continue

            del _StoredPictures[_Image.m_name]

