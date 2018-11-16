# PACER-Training
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
