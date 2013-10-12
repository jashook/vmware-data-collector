////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//
// Author: Jarret Shook
//
// Module: file_send.java
//
// Modifications:
//
// 6-Sept-13: Version 1.0: Last Updated
// 6-Sept-13: Version 1.0: Created
//
// Timeperiod: ev7n
//
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

import java.io.*;
import java.net.*;

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

public class file_send
{
   
   public static void main(String[] _Args) throws IOException
   {

      String _Ip = "76.187.135.215";

      Socket _Socket = new Socket(_Ip, 2257);

      File _File = new File("/home/jarret/output/output.txt");

      long _Length = _File.length();

      if (_Length > Integer.MAX_VALUE)
      {
         System.err.println("File is too large to transpher");

         System.exit(1);

      }

      byte[] _Bytes = new byte[(int) _Length];

      FileInputStream _FileInput = new FileInputStream(_File);
   
      BufferedInputStream _BufferedInput = new BufferedInputStream(_FileInput);

      BufferedOutputStream _BufferedOutput = new BufferedOutputStream(_Socket.getOutputStream());

      int _Count;

      while ((_Count = _BufferedInput.read(_Bytes)) > 0)
      {
         _BufferedOutput.write(_Bytes, 0, _Count);

      }

      _BufferedOutput.flush();
      _BufferedOutput.close();
      _FileInput.close();
      _BufferedInput.close();
      _Socket.close();

   }

}
