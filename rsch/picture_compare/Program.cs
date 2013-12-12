using System;
using System.Drawing;

namespace picture_compare
{
   class Program
   {
      private static int Main(string[] _Args)
      {
         string _FileNameOne, _FileNameTwo;

         if (_Args.Length < 3)
         {
            _FileNameOne = "testOne.JPG";
            _FileNameTwo = "testTwo.JPG";

         }

         else
         {
            _FileNameOne = _Args[0];
            _FileNameTwo = _Args[1];

         }

         Bitmap _ImageOne = new Bitmap(_FileNameOne);
         Bitmap _ImageTwo = new Bitmap(_FileNameTwo);

         int _ErrorCount = 0;

         string _ImageOneRef, _ImageTwoRef;

         for (int _YIndex = 0; _YIndex < _ImageOne.Height; ++_YIndex)
         {
            for (int _XIndex = 0; _XIndex < _ImageOne.Width; ++_XIndex)
            {
               _ImageOneRef = _ImageOne.GetPixel(_XIndex, _YIndex).ToString();

               _ImageTwoRef = _ImageTwo.GetPixel(_XIndex, _YIndex).ToString();

               if (_ImageOneRef != _ImageTwoRef)
               {
                  ++_ErrorCount;

               }

            }

         }

         if (_ErrorCount == 0) Console.WriteLine("The pictures are the same");

         else Console.WriteLine("The two pictures are different");

         //Console.ReadLine();

         return 0;

      }
   }
}
