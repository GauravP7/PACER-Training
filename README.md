<h1>Extracting case information from pacer</h1>

<p> The PACER is an electronic service provided by the government of The United States of America to access the court records (case details) of the country. </p>
<hr/>

<h3>Steps Followed</h3>
<ul>
  <li>
    Learnt about <a href="https://drive.google.com/open?id=1TW6W8uttszW6XMdM2E5MCk092pm_-AJqQ9JYQPi7Ln4">Python</a>, difference with other languages, differnce between tuples and lists, difference between a method and a function, difference between a parameter and an argument, GIL, multithreading, Regex, copy package and old and new style class, tuple packing and unpacking, memory profiling of if-else v. try-catch block to compare the memory consumption and time taken by these two programming constructs.
  </li>
  <li>Learnt about Celery Overview, learnt about Django overview, features and working with the Model-View-Template architecture. Learnt about MySQL - its different engine types, Collation and Character set, difference between Text and JSON datatypes. Brushed up on different normal forms in DBMS and learnt to create a normalized database.</li>
  <li>Created the Requirements analysis document (RAD) which should include the introduction, purpose scope, objective and success criteria of the project.</li>
  <li>Created the Functional Design Document (FDD) that includes the abilities the program must possess: the ability to fetch data based on the different search criteria, ability to store case details, ability to store dta non redundant manner by removing the unwanted characters</li>
  <li>Created the Implementation Design Document (IDD) that includes functional and Non functional requirements of the program.</li>
  <li>Created a detailed database schema with the Entity-Relationship diagram and Relational-Schema diagram, along with the code for the tables of the database.</li>
  <li>Set up the virtual environment and Git in my local system.</li>
  <li>Wrote the detailed steps (algorithm) to code the extraction and storing of the case details from the PACER training site.
      <p>[ Step 1 of 9 ] : Hit the first page of PACER training site and Login.</p>
      <p>[ Step 2 of 9 ] : Validate the Login.</p>
      <p>[ Step 3 of 9 ] : Parse the contents and get cookie.</p>
      <p>[ Step 4 of 9 ] : Query as per the input criteria.</p>
      <p>[ Step 5 of 9 ] : Save the Web page (HTML content) in a folder.</p>
      <p>[ Step 6 of 9 ] : Print the page path.</p>
      <p>[ Step 7 of 9 ] : Print the Search Criteria.</p>
      <p>[ Step 8 of 9 ] : Print the case details.</p> 
      <p>[ Step 9 of 9 ] : Logout from the website.</p>
  </li>
    </li>
  <li>Implemented the Django models and views to Displayed the stored data from the database.</li>
  </ul>
  <h3>Usage</h3>
    <ol>
  <li>Run the SQL schema file from scraping-test/<b>save_case_details.sql</b> in the MySQL prompt </li>
  <li>Run the <b>execute_scraper.py</b> file to login, fetch and store the case details into the database</li>
  <li>Navigate to django-test/mysite directory and run <b>python manage.py runserver<b> and open the server link</b>
  <li>By now you will be able to see all the case details you have saved into the database from the PACER training website</li>
    </ol>
