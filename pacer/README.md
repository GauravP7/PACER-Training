<h1>Extracting case information from pacer</h1>

<p> The PACER is an electronic service provided by the government of The United States of America to access the court records (case details) of the country. </p>
<hr/>

<h3>Steps Followed</h3>
    <code>
     # [ Step 1 of 9 ] : Hit the first page of PACER training site and Login.</p>
     # [ Step 2 of 9 ] : Validate the Login.</p>
     # [ Step 3 of 9 ] : Parse the contents and get cookie.</p>
     # [ Step 4 of 9 ] : Query as per the input criteria.</p>
     # [ Step 5 of 9 ] : Save the Web page (HTML content) in a folder.</p>
     # [ Step 6 of 9 ] : Print the page path.</p>
     # [ Step 7 of 9 ] : Print the Search Criteria.</p>
     # [ Step 8 of 9 ] : Print the case details.</p> 
     # [ Step 9 of 9 ] : Logout from the website.</p></code>
 <hr/>
  <h3>Usage</h3>
    <ol>
  <li>Run the SQL schema file from scraping-test/<b>save_case_details.sql</b> in the MySQL prompt. <br>
    <code>mysql -u root -p</code><br/>
    <code>Enter password:</code><br/>
    <code>mysql>source /home/mydir/save_case_details.sql</code>
  </li><br/>
  <li>Run the <b>execute_scraper.py</b> file to login, fetch and store the case details into the database.<br/>
    <code>python execute_scraper.py</code>
    <br/>
  </li><br/>
  <li>Navigate to django-test/mysite directory and run the server.<br/><code>python manage.py runserver</code>
    </li><br/>
  <li>Browse the URL http://127.0.0.1:8000/index/ and you can see the case details being print on the server</li><br/>
  <li>By now you will be able to see all the case details you have saved into the database from the PACER training website</li>
    </ol>
    <br/>
  <b>Note:</b>&nbsp;&nbsp;&nbsp;&nbsp;The port number :8000 may change depending on the machine. You can run the program in other ports as well.&nbsp;&nbsp;&nbsp;&nbsp;<br/>e.g. <code>python manage.py runserver 8090</code> will run the server on http://127.0.0.1:8090/
