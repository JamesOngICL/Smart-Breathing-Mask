# embedded_iot2

<h2>Running the Server</h2>
<b>To run server locally:</b><br>
  python3 manage.py runserver<br><br>
<b>To run server on specified port:</b><br>
  python3 manage.py runserver 8000 <- port number<br><br>
<b>To run server on local internet for raspberry communications:</b><br>
  python3 manage.py runserver 0.0.0.0:8000 <- port number can be changed<br>
  #Then check your assigned ip to acess it using ipconfig, etc...<br><br>
  
<h2>Understanding the backend</h2>
The two important files are views.py and urls.py under authentication folder.<br><br>The only real backend files are under authentication/views.py where all the functions are, the file authentication/urls.py specifies which function should be associated with a specified url.
 
