# TCP based Text Service
There are two main parts of the service:  
  * Server
  * Client
 
## Server
The connection between client and server is established usign TCP communication protocol.  
Server is able to perform following operations:
  * Change text - replaces the words in the string corresponding to the provided dictionary.  
  This operation accepts two files:
      * Txt file that contains initial text.
      * Json file that contains dictionary of replaced words. 
  * Encode decode- encypts or decrypts the message using OTP(one time pad) encryption.
      * Txt file that either contains initial or encrypted text.
      * Key file that contains key.   
      
The execution format is following:  
_python server.py -i 127.0.0.1 -p 1060_  
Where:
* i - interface that server listens. Default value is '127.0.0.1'.
* p - port that server listens. Default value is 1060.


## Client 
Client is able to perform two operations:
  * Change text - replaces the words in the string.  
    Execution format:  
        _python text_service.py --mode change_text myfile.txt myjson.json_   
    Responce is written in the __exchanged.txt__ file.
  * Encode decode -  encrypts or decrypts the message using OTP(one time pad) encryption.    
    Execution format:  
        _python text_service.py --mode encode_decode myfile.txt mykey.txt_   
    Responce is saved in the __cipher.txt__ file.
 
There exist two optional parameters:  
  * --host - host with which client connects
  * -p - port with which client connects
 
 