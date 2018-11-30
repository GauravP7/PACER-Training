# Pacer Training 

The aim of the project is to scrape the case related information form the PACER training web site,
and store it in the local databse for future usage.

The case information is queried by the user based on certain search criteria.

The case details can be queried using one or combination of the following:
1. Case Number
2. Case Status - Open/Closed/All
3. Filed date
4. Last Entry Date
5. Name of Suit. e.g. 110 - Insurance
6. Cause of Action. e.g. 02:0437 (02:437 Federal Election Commission)
7. Last/Business Name
8. First Name
9. Middle Name
10. Type - Attorney, Party

The project makes use of the following technologies/modules:
1. The program will be implemented in Python 2.7.
2. Python modules such as urllib2, Beautifulsoup (bs4)
3. Django 1.4 and MySQLdb.
4. The MySQL database, version 5.5  will be used to store the data.
5. DB engine used for the project will be InnoDB which is a default of MySQL version 5.5. 
<h3>Learnings</h3>
<ul>
  <li>
    <a href="https://drive.google.com/open?id=1TW6W8uttszW6XMdM2E5MCk092pm_-AJqQ9JYQPi7Ln4">Learnt about Python</a>, difference with other languages, differnce between tuples and lists, difference between a method and a function, difference between a parameter and an argument, GIL, multithreading, Regex, copy package and old and new style class, tuple packing and unpacking, memory profiling of if-else v. try-catch block to compare the memory consumption and time taken by these two programming constructs.
  </li>
  <li>Learnt about Celery Overview, learnt about Django overview, features and working with the Model-View-Template architecture. Learnt about MySQL - its different engine types, Collation and Character set, difference between Text and JSON datatypes. Brushed up on different normal forms in DBMS and learnt to create a normalized database.</li>
  <li>Created the Requirements analysis document (RAD) which should include the introduction, purpose scope, objective and success criteria of the project.</li>
  <li>Created the Functional Design Document (FDD) that includes the abilities the program must possess: the ability to fetch data based on the different search criteria, ability to store case details, ability to store dta non redundant manner by removing the unwanted characters</li>
  <li>Created the Implementation Design Document (IDD) that includes functional and Non functional requirements of the program.</li>
  <li>Created a detailed database schema with the Entity-Relationship diagram and Relational-Schema diagram, along with the code for the tables of the database.</li>
  <li>Set up the virtual environment and Git in my local system.</li>
  <li>Wrote the detailed steps (algorithm) to code the extraction and storing of the case details from the PACER training site.
<li>Implemented the Django models and views to Displayed the stored data from the database.</li>
</ul>
