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
import Image
from image import *

################################################################################
################################################################################

_Hashes = dict()

_StoredPictures = dict()

_ImageNames = []

if __name__ == "__main__":

   if (len(sys.argv) == 2): 

      _Directory = sys.argv[1]

      _Files = os.listdir(_Directory)

      for _File in _Files:

         if _File[0] == '.': continue

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

               _Hashes[_Hash].append(_InImage)

            except:
 
               _Hashes[_Hash] = list().append(_InImage)

            _InImage.m_pictures.append(_Hash)

            _TempWidth = _TempWidth + _Offset

            if (_TempWidth > _Width):

               _TempWidth = 0

               _TempHeight = _TempHeight + _Offset

            if (_TempHeight >= _Height):

               break
