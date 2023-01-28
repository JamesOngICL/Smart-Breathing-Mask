# embedded_iot2

<h2>Running the Server</h2>
<b>To run server locally:</b><br>
  python3 manage.py runserver<br><br>
<b>To run server on specified port:</b><br>
  python3 manage.py runserver 8000 <- port number<br><br>
<b>To run server on local internet for raspberry communications:</b><br>
  python3 manage.py runserver 0.0.0.0:8000 <- port number can be changed<br>
  #Then check your assigned ip to acess it using ipconfig, etc...<br><br>
  
<h2>Core Files</h2>
- extfunctions.py -> imported in views.py<br>
- authentication/views.py -> main backend code<br>
- authentication/urls.py -> link urls and functions in views.py<br>
- templates/authentication -> frontend html stuff<br>
  
<h2>Understanding the backend</h2>
The two important files are views.py and urls.py under authentication folder.<br><br>The only real backend files are under authentication/views.py where all the functions are, the file authentication/urls.py specifies which function should be associated with a specified url. The file extfunctions.py on the outside is imported in views.py to write functions more cleanly.

<h2>Understand the frontend</h2>
The important files for frontend is under templates/authentication. These files are acessed in views.py. We can pass parameters into these html files in views.py by doing something like this:<br><br>return render(request, "authentication/search.html",{'aboutme':extfunctions.getabout(request.user.username)})<br><br>Here this function will render search.html file for the user. The dictionary is passed and can be accessed in the html file. We can extract this data by simply writing {{aboutme}} in the html code.

<h2>Http requests</h2>
The main http request is under home() function in views.py. Try sending a post data using the python file and the data should be recieved by this function. You can try printing request.POST() and see that your JSON data has been received here.

<h2>Other files</h2>
Don't worry about most of the other unmentioned files, they are there by default and are usually not changed.
 
