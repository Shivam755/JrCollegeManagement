# JrCollegeManagement
A GUI tool that can be used by students, teachers as well as the management for connecting under the hood of the college.

## Dependencies
### **Tkcalendar** :
If you don't have tkcalendar already installed. Install it using: `pip install tkcalendar`

For linux you can run: `sudo apt-get install python3-tkcalendar`

### **Mysql Connector**:
You can install any one of the three versions of mysql-connector whichever suits your PC.

1.`pip install mysql-connector`

2.`pip install mysql-connector-python`

3.`pip install mysql-connector-python-rf`

### **Other libraries:**

Other libraries come preinstalled along with python. They are:

1.Tkinter

2.os

3.datetime

4.random


## Pre-execution changes:
This tool is by default set to connect to your localhost with the database "jr_college".
```
# Connecting to the server
jr_college_db = mysql.connector.connect(
    host='localhost',#host for database
    user='', #user for connecting to database
    passwd='',#user password for database connection
    database='jr_college'#database name
)
```
You can change it to connect with your database.
