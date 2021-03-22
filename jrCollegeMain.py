from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from datetime import date
import mysql.connector
import random
import os

# Creating colour variables
background = '#2e383f'
txt = '#ececeb'
panels = '#07617d'
btns = '#f9a828'

# Creating font variables
page_txt = ('Times New Roman', 18)
college_txt = ('Times New Roman', 24, 'bold')
label_txt = ('Helvectica', 12)
entry_txt = ('Helvectica', 10)
text_txt = ('Helvectica', 14)

# pattern for color storage: background, txt, panels, btns
themes = {
          "t0": ["#373331", "#fff3e1", "#29cdb5", "#9bf4d5"],
          "t1": ["#5d5d5a", "#fff4e3", "#ff8a5c", "#ffa45c"],
          "t2": ["#1b3c59", "#f2f2f0", "#456173", "#a6ed8e"],
          "t3": ["#32424a", "#f5f5f5", "#0090ad", "#01ecd5"],
          "t4": ["#2e383f", "#ececeb", "#07617d", "#f9a828"],
          "t5": ["#000000", "#fff5f5", "#24b273", "#b2d430"],
          't6': ["#000000", "#f5eded", "#3e3636", "#d72323"],
          't7': ['#2b2024', '#fff4e3', '#a80038', '#fd0054'],
}

theme_num = 0

def change_theme():
    global theme_num, change_theme_btn, background, txt, panels, btns
    if theme_num < len(themes)-1:
        theme_num += 1
    else:
        theme_num = 0
    background, txt, panels, btns = themes[f"t{theme_num}"]
    for i in root_window.winfo_children():
        i.destroy()
    root_window.configure(bg=background)
    change_theme_btn = Button(root_window, text="Change Theme", bg=panels, fg=txt, font=label_txt,
                              activebackground=btns, activeforeground=txt, command=change_theme)
    change_theme_btn.pack(anchor=NE)
    Log_in(root_window)


# Connecting to the server
jr_college_db = mysql.connector.connect(
    host='localhost',#host for database
    user='',#userid to connect to database
    passwd='',#root password for database connection
    database='jr_college'#database name
)

# Creating a cursor to access global database
cursor = jr_college_db.cursor(buffered=True)


# Creating database
cursor.execute('CREATE DATABASE IF NOT EXISTS jr_college')

# Creating student table
cursor.execute("""CREATE TABLE IF NOT EXISTS student (
                  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  first_name VARCHAR(50) NOT NULL,
                  last_name VARCHAR(50),
                  dob DATE NOT NULL,
                  gender VARCHAR(15),
                  email VARCHAR(100) NOT NULL UNIQUE,
                  phone_number VARCHAR(13) NOT NULL,
                  address VARCHAR(300) NOT NULL,
                  pincode VARCHAR(10) NOT NULL,
                  stream_name VARCHAR(12) NOT NULL,
                  user_id VARCHAR(10) UNIQUE,
                  passwd VARCHAR(20) NOT NULL ,
                  standard VARCHAR(12) NOT NULL,
                  result VARCHAR(8) DEFAULT 'Pursuing',
                  date_of_admission DATE NOT NULL,
                  points INT DEFAULT 0,
                  key_val INT,
                  number_of_tasks INT(2) DEFAULT 0
)""")

# Creating faculty table
cursor.execute('''CREATE TABLE IF NOT EXISTS faculty(
                  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  first_name VARCHAR(50) NOT NULL,
                  last_name VARCHAR(50),
                  dob DATE NOT NULL,
                  gender VARCHAR(15),
                  email VARCHAR(100) UNIQUE,
                  phone_number VARCHAR(13) NOT NULL,
                  address VARCHAR(300) NOT NULL,
                  pincode VARCHAR(10) NOT NULL,
                  subject_id INT NOT NULL,
                  is_hod VARCHAR(3) DEFAULT 'NO',
                  user_id VARCHAR(10) UNIQUE NOT NULL,
                  passwd VARCHAR(20) NOT NULL,
                  key_val INT,
                  number_of_tasks INT(2) DEFAULT 0
)''')

# Creating a table stream
cursor.execute('''CREATE TABLE IF NOT EXISTS stream(
                  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  name VARCHAR(12) NOT NULL UNIQUE
)''')

# Creating Subject Table
cursor.execute("""CREATE TABLE IF NOT EXISTS subject (
                  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  stream_id INT NOT NULL,
                  subject_id INT NOT NULL,
                  name VARCHAR(20) NOT NULL,
                  faculty_id VARCHAR(10) NOT NULL,
                  hod_id INT NOT NULL,
                  code INT NOT NULL UNIQUE
                  )""")

# Creating Assignments Table
cursor.execute("""CREATE TABLE IF NOT EXISTS assignment (
                  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  faculty_id VARCHAR(15) NOT NULL,
                  stream_id INT NOT NULL,
                  subject_id INT NOT NULL,
                  subject_name VARCHAR(20) NOT NULL,
                  standard VARCHAR(3) NOT NULL,
                  subject_code INT NOT NULL,
                  email VARCHAR(100) NOT NULL,
                  assignment_code VARCHAR(15) NOT NULL,
                  assignment_id VARCHAR(15) NOT NULL UNIQUE DEFAULT 'TBD',
                  assignment_topic VARCHAR(50) NOT NULL,
                  assignment_description VARCHAR(500) NOT NULL UNIQUE,
                  submitted INT NOT NULL DEFAULT 0)""")

# Creating Submissions Table
cursor.execute("""CREATE TABLE IF NOT EXISTS submission (
                  assignment_id VARCHAR(15) NOT NULL,
                  student_id VARCHAR(15) NOT NULL,
                  submission_id VARCHAR(45) NOT NULL UNIQUE,
                  student_f_name VARCHAR(30) NOT NULL,
                  student_l_name VARCHAR(30) NULL,
                  marks INT NOT NULL DEFAULT 0,
                  turned_in INT NOT NULL DEFAULT 0)""")

# Creating Management Table
cursor.execute("""CREATE TABLE IF NOT EXISTS management(
                  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  first_name VARCHAR(50) NOT NULL,
                  last_name VARCHAR(50),
                  dob DATE NOT NULL,
                  gender VARCHAR(15),
                  email VARCHAR(100) UNIQUE,
                  phone_number VARCHAR(13) NOT NULL,
                  address VARCHAR(300) NOT NULL,
                  pincode VARCHAR(10) NOT NULL,
                  post VARCHAR(20) NOT NULL,
                  user_id VARCHAR(75) NOT NULL UNIQUE,
                  passwd VARCHAR(20) NOT NULL,
                  key_val INT,
                  number_of_tasks INT(2) DEFAULT 0
)""")

# Creating tables for to_do_list in local database
cursor.execute('''CREATE TABLE IF NOT EXISTS todo_list(
                            task_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                            user_id VARCHAR(10) NOT NULL,
                            task VARCHAR(500) NOT NULL                           
)''')

# Creating a Syllabus Table
cursor.execute("""CREATE TABLE IF NOT EXISTS syllabus (                   
                            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,                   
                            subject_code INT NOT NULL,                   
                            standard VARCHAR(3) NOT NULL,                   
                            code VARCHAR(10) NOT NULL,                   
                            chapter VARCHAR(45) NOT NULL)""")


# Creating an encoder for password
class Encoder:

    def __init__(self, plain_passwd, access=random.randint(1, 26)):
        self.key = access
        self.encoded_passwd = ''
        for i in range(0, len(plain_passwd)):
            encoded_char = chr(ord(plain_passwd[i]) + self.key)
            self.encoded_passwd += encoded_char


# Creating a login page
class Log_in:

    def __init__(self, root):
        # Login page
        self.login_frame = Frame(root, bg=background)
        self.login_frame.pack(anchor='center', pady=(70, 0))

        # College title
        self.college_title = Label(self.login_frame, text="Junior College", bg=background, fg=btns,
                                   font=college_txt,)
        self.college_title.grid(row=0, column=0, columnspan=5)

        # Frame title
        self.login_title = Label(self.login_frame, text="Login Page", bg=background, fg=btns,
                                 font=page_txt)
        self.login_title.grid(row=1, column=0, columnspan=5)

        # Taking input for userid
        self.user_id_label = Label(self.login_frame, text="User ID: ", bg=background, fg=txt, font=label_txt)
        self.user_id_label.grid(row=2, column=1, sticky='e')

        self.user_id_entry = Entry(self.login_frame, bg=txt, fg=background, font=entry_txt)
        self.user_id_entry.grid(row=2, column=3, sticky='w')

        # Taking password
        self.passwd_label = Label(self.login_frame, text="Password : ", bg=background, fg=txt, font=label_txt)
        self.passwd_label.grid(row=3, column=1)

        self.passwd_entry = Entry(self.login_frame, show='*', bg=txt, fg=background, font=entry_txt)
        self.passwd_entry.grid(row=3, column=3)

        # login button
        self.login_button = Button(self.login_frame, text="Login", bg=panels, fg=txt, font=label_txt,
                                   activebackground=btns, activeforeground=txt,
                                   command=lambda: self.login_func(self.user_id_entry.get(), self.passwd_entry.get(),
                                                                   root))
        self.login_button.grid(row=4, column=2)

    def login_func(self, user_id, passwd, root):
        try:
            # Login for student
            if user_id[0] == 's':
                cursor.execute('SELECT key_val FROM student WHERE user_id = %s', (user_id,))
                log_key = cursor.fetchone()
                if log_key is None:
                    messagebox.showerror('Error', 'Invalid User ID!!')
                else:
                    log_enc = Encoder(passwd, log_key[0])
                    cursor.execute('SELECT * FROM student WHERE user_id = %s AND passwd = %s',
                                   (user_id, log_enc.encoded_passwd))
                    verify = cursor.fetchone()
                    if verify is None:
                        messagebox.showerror('Error', 'Invalid Password!!')
                    else:
                        self.user_id_entry.delete(0, END)
                        self.passwd_entry.delete(0, END)
                        self.login_frame.pack_forget()
                        self.stud_dict = {
                            "f_name": verify[1].title(),
                            "l_name": verify[2].title(),
                            "dob": verify[3],
                            "gender": verify[4],
                            "email": verify[5],
                            "phone_number": verify[6],
                            "stream_name": verify[9],
                            "user_id": verify[10],
                            "standard": verify[12],
                            "result": verify[13],
                            "date_of_admission": verify[14],
                            "points": verify[15],
                            "passwd": verify[11],
                            "key": verify[16]
                        }
                        Student(root, self.stud_dict)
                        change_theme_btn.destroy()

            # Login for faculties
            elif user_id[0] == 'f':
                cursor.execute('SELECT key_val FROM faculty WHERE user_id = %s', (user_id,))
                log_key = cursor.fetchone()
                if log_key is None:
                    messagebox.showerror('Error', 'Invalid User ID!!')
                else:
                    log_enc = Encoder(passwd, log_key[0])
                    cursor.execute('SELECT * FROM faculty WHERE user_id = %s AND passwd = %s',
                                   (user_id, log_enc.encoded_passwd))
                    verify = cursor.fetchone()
                    if verify is None:
                        messagebox.showerror('Error', 'Invalid Password!!')
                    else:
                        self.user_id_entry.delete(0, END)
                        self.passwd_entry.delete(0, END)
                        self.login_frame.pack_forget()
                        self.faculty_dict = {"f_name": verify[1].title(),
                                             "l_name": verify[2].title(),
                                             "dob": verify[3],
                                             "gender": verify[4],
                                             "email": verify[5],
                                             "phone_number": verify[6],
                                             "subject_id": verify[9],
                                             "is_hod": verify[10],
                                             "user_id": verify[11],
                                             "passwd": verify[12],
                                             "key": verify[13]
                                             }
                        Faculty(root, self.faculty_dict)
                        change_theme_btn.destroy()

            # Login for management
            elif user_id[0] == 'm':
                cursor.execute('SELECT key_val FROM management WHERE user_id = %s', (user_id,))
                log_key = cursor.fetchone()
                if log_key is None:
                    messagebox.showerror('Error', 'Invalid UserID!!')
                else:
                    log_enc = Encoder(passwd, log_key[0])
                    cursor.execute('SELECT * FROM management WHERE user_id = %s AND passwd = %s',
                                   (user_id, log_enc.encoded_passwd))
                    verify = cursor.fetchone()
                    if verify is None:
                        messagebox.showerror('Error', 'Invalid Password!!')
                    else:
                        self.user_id_entry.delete(0, END)
                        self.passwd_entry.delete(0, END)
                        self.login_frame.pack_forget()
                        self.management_dict = {"f_name": verify[1].title(),
                                                "l_name": verify[2].title(),
                                                "dob": verify[3],
                                                "gender": verify[4],
                                                "email": verify[5],
                                                "phone_number": verify[6],
                                                "post": verify[9],
                                                "user_id": verify[10],
                                                "passwd": verify[11],
                                                "key": verify[12]
                                                }
                        Management(root, self.management_dict)
                        change_theme_btn.destroy()

            # Handling invalid id
            else:
                messagebox.showerror('Error', 'INVALID USER ID!!')

        except IndexError:
            messagebox.showerror('Oops...', "You forgot to enter the user id.")


# Creating a to_do list
class Todo:

    def __init__(self, master, user_id):
        # Creating variables to monitor tasks
        self.num_of_tasks = 0
        self.task = []

        # Main Frame
        self.todo_frame = Frame(master, bg=background)
        self.todo_frame.columnconfigure(1, weight=1)
        self.todo_frame.rowconfigure(1, weight=1)
        self.todo_frame.pack(fill=BOTH, expand=1)

        # Personal Tasks Frame
        self.task_frame = Frame(self.todo_frame, bg=background)
        self.task_frame.columnconfigure(1, weight=1)
        self.task_frame.rowconfigure(1, weight=1)
        self.task_frame.grid(row=0, column=0, columnspan=12, sticky=NSEW)

        # Extracting tasks from database
        cursor.execute('SELECT task FROM todo_list WHERE user_id = %s', (user_id,))
        self.task_list = cursor.fetchall()

        # Creating a checkbutton for existing tasks
        for i in range(len(self.task_list)):
            self.recover_task(self.task_list[i][0], user_id, i)

        # Todo_Frame Components -- Add new Task
        self.new_task = Text(self.todo_frame, height=3, width=1000, bg=txt, fg=background, font=entry_txt)
        self.new_task.grid(row=1, column=0, columnspan=8, sticky="sw")

        self.add_task_button = Button(self.todo_frame, text="Add Task", height=2, width=20, bg=btns, fg=background,
                                      font=label_txt,
                                      command=lambda: self.add_task(self.new_task.get(1.0, END), user_id))
        self.add_task_button.grid(row=1, column=9, columnspan=2, sticky="se")

    def recover_task(self, task_text, user_id, i):
        self.task.append(Checkbutton(self.task_frame, text=task_text, bg=background, fg=txt, font=label_txt,
                                     activebackground=background, activeforeground=txt,
                                     command=lambda: self.delete_task(task_text, user_id)))
        self.task[i].deselect()
        self.task[i].grid(row=i, column=0, sticky='w')
        self.num_of_tasks += 1

    def add_task(self, task_text, user_id):
        for task in self.task:
            if task.cget('text') == task_text:
                messagebox.showerror('ERROR', 'The entered task already exists')
                return
        if task_text.strip() == '':
            messagebox.showerror('ERROR', 'Please enter some info about the task:')
        else:
            if user_id[0] == 's':
                # Extracting the number of tasks for a specified user
                cursor.execute('SELECT number_of_tasks FROM student WHERE user_id = %s', (user_id,))
                no_task = cursor.fetchone()
                self.num_of_tasks = no_task[0]

                self.task.append(Checkbutton(self.task_frame, text=task_text, bg=background, fg=txt, font=label_txt,
                                             activebackground=background, activeforeground=txt,
                                             command=lambda: self.delete_task(task_text, user_id)))
                self.task[self.num_of_tasks].deselect()
                self.task[self.num_of_tasks].grid(row=self.num_of_tasks, column=0, sticky='w')
                self.num_of_tasks += 1

                self.new_task.delete(1.0, END)
                # updating changes to database
                cursor.execute('INSERT INTO todo_list(user_id, task) VALUES(%s, %s)', (user_id, task_text))
                cursor.execute('UPDATE student SET number_of_tasks = %s WHERE user_id = %s',
                               (self.num_of_tasks, user_id))

            elif user_id[0] == 'f':
                # Extracting the number of tasks for a specified user
                cursor.execute('SELECT number_of_tasks FROM faculty WHERE user_id = %s', (user_id,))
                no_task = cursor.fetchone()
                self.num_of_tasks = no_task[0]

                self.task.append(Checkbutton(self.task_frame, text=task_text, bg=background, fg=txt, font=label_txt,
                                             activebackground=background, activeforeground=txt,
                                             command=lambda: self.delete_task(task_text, user_id)))
                self.task[self.num_of_tasks].deselect()
                self.task[self.num_of_tasks].grid(row=self.num_of_tasks, column=0, sticky='w')
                self.num_of_tasks += 1

                self.new_task.delete(1.0, END)
                # updating changes to database
                cursor.execute('INSERT INTO todo_list(user_id, task) VALUES(%s, %s)', (user_id, task_text))
                cursor.execute('UPDATE faculty SET number_of_tasks = %s WHERE user_id = %s',
                               (self.num_of_tasks, user_id))

            elif user_id[0] == 'm':
                # Extracting the number of tasks for a specified user
                cursor.execute('SELECT number_of_tasks FROM management WHERE user_id = %s', (user_id,))
                no_task = cursor.fetchone()
                self.num_of_tasks = no_task[0]

                self.task.append(Checkbutton(self.task_frame, text=task_text, bg=background, fg=txt, font=label_txt,
                                             activebackground=background, activeforeground=txt,
                                             command=lambda: self.delete_task(task_text, user_id)))
                self.task[self.num_of_tasks].deselect()
                self.task[self.num_of_tasks].grid(row=self.num_of_tasks, column=0, sticky='w')
                self.num_of_tasks += 1

                self.new_task.delete(1.0, END)
                # updating changes to database
                cursor.execute('INSERT INTO todo_list(user_id, task) VALUES(%s, %s)', (user_id, task_text))
                cursor.execute('UPDATE management SET number_of_tasks = %s WHERE user_id = %s',
                               (self.num_of_tasks, user_id))

            jr_college_db.commit()

    def delete_task(self, task_text, user_id):
        # Extracting index of the check button
        i = 0
        for btn in range(len(self.task)):
            if self.task[btn].cget('text') == task_text:
                i = btn
                self.task[btn].destroy()
                break

        self.task.pop(i)
        # reallocating rows to other task
        for i in range(len(self.task)):
            self.task[i].grid(row=i, column=0, sticky='w')
        # making changes to database
        cursor.execute('DELETE FROM todo_list WHERE task = %s AND user_id = %s', (task_text, user_id))
        self.num_of_tasks -= 1
        if user_id[0] == 's':
            cursor.execute('UPDATE student SET number_of_tasks = %s WHERE user_id = %s', (self.num_of_tasks, user_id))

        elif user_id[0] == 'f':
            cursor.execute('UPDATE faculty SET number_of_tasks = %s WHERE user_id = %s', (self.num_of_tasks, user_id))

        elif user_id[0] == 'm':
            cursor.execute('UPDATE management SET number_of_tasks = %s WHERE user_id = %s',
                           (self.num_of_tasks, user_id))
        jr_college_db.commit()


# Creating a homeframe
class Main:
    def __init__(self, root, user_id):
        root.geometry("1100x650")
        # A variable for change passwd
        self.passwd_changed = False
        # Creating a frame to hold panels
        self.main_frame = Frame(root, bg=background)
        self.main_frame.pack(fill=BOTH, expand=1)

        # Creating a top panel
        self.top_panel = PanedWindow(self.main_frame, orient=VERTICAL, relief="flat", bg=panels)
        self.top_panel.pack(fill="both", expand=1)

        self.top_frame = Frame(self.top_panel, bg=panels)
        self.top_panel.add(self.top_frame, height=50)

        # A label to hold college name
        college_name = Label(self.top_frame, text="Junior College", justify='center', bg=panels, fg=btns,
                             font=college_txt)
        college_name.place(relx=0.05, rely=0.5, anchor='w')

        # A button to open profile
        self.profile_button = Button(self.top_frame, text="", relief='groove', command=self.profile,
                                     height=2, width=30, justify='center', bg=panels, fg=txt, font=label_txt,
                                     activebackground=btns, activeforeground=txt)
        self.profile_button.place(relx=0.945, rely=0.5, anchor="e")

        # Creating the left panel
        self.left_panel = PanedWindow(self.top_panel, relief='raised', orient=HORIZONTAL, bg=panels)
        self.top_panel.add(self.left_panel)

        self.left_frame = Frame(self.left_panel, bg=panels)
        self.left_panel.add(self.left_frame, width=250)

        # configuring the right frame
        Grid.columnconfigure(self.left_frame, 0, weight=1)
        Grid.rowconfigure(self.left_frame, 0, weight=1)
        Grid.rowconfigure(self.left_frame, 1, weight=1)
        Grid.rowconfigure(self.left_frame, 2, weight=1)
        Grid.rowconfigure(self.left_frame, 3, weight=1)
        Grid.rowconfigure(self.left_frame, 4, weight=1)
        Grid.rowconfigure(self.left_frame, 5, weight=1)
        Grid.rowconfigure(self.left_frame, 6, weight=1)
        Grid.rowconfigure(self.left_frame, 7, weight=1)
        Grid.rowconfigure(self.left_frame, 8, weight=1)
        Grid.rowconfigure(self.left_frame, 9, weight=1)

        # Creating buttons for left frame
        # Home button
        self.home_button = Button(self.left_frame, text="Home", relief='raised', command=lambda: self.home(user_id),
                                  justify='center', bg=panels, fg=txt, font=label_txt,
                                  activebackground=btns, activeforeground=txt)
        self.home_button.grid(row=0, column=0, sticky=NSEW)

        # Assignment button
        self.assignment_button = Button(self.left_frame, text="Assignment",
                                        bg=panels, fg=txt, font=label_txt, justify='center',
                                        activebackground=btns, activeforeground=txt)
        self.assignment_button.grid(row=1, column=0, sticky=NSEW)

        # Syllabus button
        self.syllabus_button = Button(self.left_frame, text="Syllabus", justify='center',
                                      bg=panels, fg=txt, font=label_txt,
                                      activebackground=btns, activeforeground=txt)
        self.syllabus_button.grid(row=2, column=0, sticky=NSEW)

        # Creating the right panel
        self.right_panel = PanedWindow(self.top_panel, relief='sunken', bg=background)
        self.left_panel.add(self.right_panel)

        self.right_frame = Canvas(self.right_panel, highlightthickness=0, bg=background)
        self.right_panel.add(self.right_frame)
        self.home(user_id)

    def profile(self, user_dict):
        self.destroy_all()
        self.profile_frame = Frame(self.right_frame, height=525, width=900, bg=background)

        # Creating labels to show in profile
        # Title
        self.profile_title = Label(self.profile_frame, text="My Profile", bg=background, fg=btns, font=page_txt)
        self.profile_title.grid(row=0, column=0, columnspan=5)

        # User ID
        self.user_id_label = Label(self.profile_frame, text='User ID:', bg=background, fg=txt, font=label_txt)
        self.user_id_label.grid(row=1, column=1, sticky='w')

        self.user_id_value = Label(self.profile_frame, text=user_dict['user_id'], bg=background, fg=txt, font=label_txt)
        self.user_id_value.grid(row=1, column=3, sticky='w')

        # First name
        self.first_name_label = Label(self.profile_frame, text="First name: ", bg=background, fg=txt, font=label_txt)
        self.first_name_label.grid(row=2, column=1, sticky='w')

        self.first_name_value = Label(self.profile_frame, text=user_dict['f_name'], bg=background, fg=txt,
                                      font=label_txt)
        self.first_name_value.grid(row=2, column=3, sticky='w')

        # Last name
        self.last_name_label = Label(self.profile_frame, text="Last name: ", bg=background, fg=txt, font=label_txt)
        self.last_name_label.grid(row=3, column=1, sticky='w')

        self.last_name_value = Label(self.profile_frame, text=user_dict['l_name'], bg=background, fg=txt,
                                     font=label_txt)
        self.last_name_value.grid(row=3, column=3, sticky='w')

        # Date of Birth
        self.date_of_birth = Label(self.profile_frame, text="Date of Birth: ", bg=background, fg=txt, font=label_txt)
        self.date_of_birth.grid(row=4, column=1, sticky='w')

        self.date_of_birth_value = Label(self.profile_frame, text=user_dict['dob'], bg=background, fg=txt,
                                         font=label_txt)
        self.date_of_birth_value.grid(row=4, column=3, sticky='w')

        # Gender
        self.gender_label = Label(self.profile_frame, text="Gender: ", bg=background, fg=txt, font=label_txt)
        self.gender_label.grid(row=5, column=1, sticky='w')

        self.gender_value = Label(self.profile_frame, text=user_dict['gender'], bg=background, fg=txt, font=label_txt)
        self.gender_value.grid(row=5, column=3, sticky='w')

        # Email id
        self.email_label = Label(self.profile_frame, text="Email ID: ", bg=background, fg=txt, font=label_txt)
        self.email_label.grid(row=6, column=1, sticky='w')

        self.email_value = Label(self.profile_frame, text=user_dict['email'], bg=background, fg=txt, font=label_txt)
        self.email_value.grid(row=6, column=3, sticky='w')

        # phone number
        self.phone_number_label = Label(self.profile_frame, text="Phone number: ", bg=background, fg=txt,
                                        font=label_txt)
        self.phone_number_label.grid(row=7, column=1, sticky='w')

        self.phone_number_value = Label(self.profile_frame, text=user_dict['phone_number'], bg=background, fg=txt,
                                        font=label_txt)
        self.phone_number_value.grid(row=7, column=3, sticky='w')

        if user_dict['user_id'][0] == 's':
            # Adding Stream_name
            self.stream_name_label = Label(self.profile_frame, text="Stream: ", bg=background, fg=txt, font=label_txt)
            self.stream_name_label.grid(row=8, column=1, sticky='w')

            self.stream_name_value = Label(self.profile_frame, text=user_dict['stream_name'], bg=background, fg=txt,
                                           font=label_txt)
            self.stream_name_value.grid(row=8, column=3, sticky='w')

            # Adding  Standard
            self.standard_label = Label(self.profile_frame, text="Standard: ", bg=background, fg=txt, font=label_txt)
            self.standard_label.grid(row=9, column=1, sticky='w')

            self.standard_value = Label(self.profile_frame, text=user_dict['standard'], bg=background, fg=txt,
                                        font=label_txt)
            self.standard_value.grid(row=9, column=3, sticky='w')

            # Adding result
            self.result_label = Label(self.profile_frame, text="Status: ", bg=background, fg=txt, font=label_txt)
            self.result_label.grid(row=10, column=1, sticky='w')

            self.result_value = Label(self.profile_frame, text=user_dict['result'], bg=background, fg=txt,
                                      font=label_txt)
            self.result_value.grid(row=10, column=3, sticky='w')

            # Adding Points
            self.result_label = Label(self.profile_frame, text="Points: ", bg=background, fg=txt, font=label_txt)
            self.result_label.grid(row=11, column=1, sticky='w')

            self.result_value = Label(self.profile_frame, text=user_dict['points'], bg=background, fg=txt,
                                      font=label_txt)
            self.result_value.grid(row=11, column=3, sticky='w')

        elif user_dict['user_id'][0] == 'f':
            cursor.execute('SELECT name FROM subject WHERE subject_id = %s', (user_dict['subject_id'],))
            subject = cursor.fetchone()

            # Adding Subject name
            self.subject_label = Label(self.profile_frame, text="Subject: ", bg=background, fg=txt, font=label_txt)
            self.subject_label.grid(row=9, column=1, sticky='w')

            self.subject_value = Label(self.profile_frame, text=subject[0], bg=background, fg=txt, font=label_txt)
            self.subject_value.grid(row=9, column=3, sticky='w')

        elif user_dict['user_id'][0] == 'm':
            # Adding post
            self.post_label = Label(self.profile_frame, text="Post: ", bg=background, fg=txt, font=label_txt)
            self.post_label.grid(row=8, column=1, sticky='w')

            self.post_value = Label(self.profile_frame, text=user_dict['post'], bg=background, fg=txt, font=label_txt)
            self.post_value.grid(row=8, column=3, sticky='w')

        self.profile_frame.place(relx=0.34, rely=0.24)

    # Creating functions for left frame
    def home(self, user_id):
        self.destroy_all()
        self.home_frame = Frame(self.right_frame, bg=background)
        # Configuring the buttons in home frame
        Grid.columnconfigure(self.home_frame, 0, weight=1)
        Grid.columnconfigure(self.home_frame, 1, weight=2)
        Grid.columnconfigure(self.home_frame, 2, weight=2)
        Grid.columnconfigure(self.home_frame, 3, weight=1)
        Grid.rowconfigure(self.home_frame, 0, weight=1)
        Grid.rowconfigure(self.home_frame, 1, weight=2)
        Grid.rowconfigure(self.home_frame, 2, weight=2)
        Grid.rowconfigure(self.home_frame, 3, weight=1)
        # Adding a To_do button
        self.todo_button = Button(self.home_frame, text="ToDo list", command=lambda: self.open_todo(user_id), height=12,
                                  width=40, relief="groove", bg=btns, fg=background, font=label_txt,
                                  activebackground=panels, activeforeground=txt)
        self.todo_button.grid(row=1, column=1, sticky='se')

        # Creating Notepad Button
        self.notepad_button = Button(self.home_frame, text="Notepad", command=self.open_notepad, height=12, width=40,
                                     relief="groove", bg=btns, fg=background, font=label_txt,
                                     activebackground=panels, activeforeground=txt)
        self.notepad_button.grid(row=1, column=2, sticky='sw')

        # Creating Paint Button
        self.paint_button = Button(self.home_frame, text="Paint", command=self.open_paint, height=12, width=40,
                                   relief="groove", bg=btns, fg=background, font=label_txt,
                                   activebackground=panels, activeforeground=txt)
        self.paint_button.grid(row=2, column=1, sticky='ne')

        # Creating Calculator Button
        self.calculator_button = Button(self.home_frame, text="Calculator", command=self.open_calculator, height=12,
                                        width=40, relief="groove", bg=btns, fg=background, font=label_txt,
                                        activebackground=panels, activeforeground=txt)
        self.calculator_button.grid(row=2, column=2, sticky='nw')

        self.home_frame.pack(fill=BOTH, expand=1)

    def open_todo(self, user_id):
        self.destroy_all()
        Todo(self.right_frame, user_id)

    def open_notepad(self):
        os.system(r"C:\Windows\system32\notepad.exe")

    def open_paint(self):
        os.system(r"C:\Windows\system32\mspaint.exe")

    def open_calculator(self):
        os.system(r"C:\Windows\System32\calc.exe")

    # Creating supportive functions
    def destroy_all(self,):
        for widgets in self.right_frame.winfo_children():
            widgets.destroy()
        self.right_frame.pack_forget()


# Creating a students interface
class Student(Main):
    def __init__(self, root, user_dict):
        super().__init__(root, user_dict['user_id'])

        # Configuring buttons according to student use
        self.profile_button.config(text=user_dict["f_name"] + " " + user_dict["l_name"],
                                   command=lambda: self.profile(user_dict))

        # A Menu button
        self.menu_btn = Menubutton(self.top_frame, text=u"\u2261", height=2, width=6, justify="center",
                                   bg=panels, fg=txt, activebackground=btns, activeforeground=background)
        self.menu_btn.place(relx=1, rely=0.5, anchor='e')
        self.menu_btn.menu = Menu(self.menu_btn, tearoff=0, bg=background, fg=txt,
                                  activebackground=btns, activeforeground=background)
        self.menu_btn["menu"] = self.menu_btn.menu
        self.menu_btn.menu.add_command(label="My Profile", command=lambda: self.profile(user_dict))
        self.menu_btn.menu.add_command(label="Change Password", command=lambda: self.change_passwd(user_dict))
        self.menu_btn.menu.add_separator()
        self.menu_btn.menu.add_command(label="Log out and Exit", command=root.destroy)

        # self.change_passwd_button.config(command=lambda:self.verify_change(user_dict))
        self.assignment_button.config(command=lambda: self.assignment(user_dict))
        self.syllabus_button.config(command=lambda: self.syllabus(user_dict))

    def change_passwd(self, user_dict):
        self.destroy_all()
        self.change_passwd_frame = Frame(self.right_frame, bg=background)

        # Title
        self.change_passwd_title = Label(self.change_passwd_frame, text='Change Password', bg=background, fg=btns,
                                         font=page_txt)
        self.change_passwd_title.grid(row=0, column=0, columnspan=5)

        # Old password
        self.old_passwd_label = Label(self.change_passwd_frame, text='Current Password: ', bg=background, fg=txt,
                                      font=label_txt)
        self.old_passwd_label.grid(row=1, column=1, sticky='w')

        self.old_passwd_value = Entry(self.change_passwd_frame, show='*', bg=txt, fg=background,
                                      font=entry_txt)
        self.old_passwd_value.grid(row=1, column=3)

        # New password
        self.new_passwd_label = Label(self.change_passwd_frame, text='New Password: ', bg=background, fg=txt,
                                      font=label_txt)
        self.new_passwd_label.grid(row=2, column=1, sticky='w')

        self.new_passwd_value = Entry(self.change_passwd_frame, show='*', bg=txt, fg=background,
                                      font=entry_txt)
        self.new_passwd_value.grid(row=2, column=3)

        # Confirm password
        self.confirm_passwd_label = Label(self.change_passwd_frame, text='Confirm new Password: ', bg=background,
                                          fg=txt, font=label_txt)
        self.confirm_passwd_label.grid(row=3, column=1, sticky='w')

        self.confirm_passwd_value = Entry(self.change_passwd_frame, show='*', bg=txt, fg=background, font=entry_txt)
        self.confirm_passwd_value.grid(row=3, column=3)

        # Change password
        self.change_passwd_button = Button(self.change_passwd_frame, text='Change Password',
                                           bg=btns, fg=background, font=label_txt, activebackground=panels,
                                           activeforeground=txt,
                                           command=lambda: self.verify_change(user_dict))
        self.change_passwd_button.grid(row=4, column=2, sticky='w')

        if self.passwd_changed:
            self.change_passwd_button.config(state=DISABLED)

        self.change_passwd_frame.place(relx=0.25, rely=0.35)

    def verify_change(self, user_dict):
        enc_pass = Encoder(self.old_passwd_value.get(), user_dict['key'])
        if enc_pass.encoded_passwd == user_dict['passwd']:
            if self.new_passwd_value.get() == self.confirm_passwd_value.get():
                enc_new_pass = Encoder(self.new_passwd_value.get())
                # updating database
                cursor.execute("UPDATE student SET passwd = %s, key_val = %s WHERE user_id = %s",
                               (enc_new_pass.encoded_passwd, enc_new_pass.key, user_dict['user_id']))
                jr_college_db.commit()
                self.passwd_changed = True
                self.change_passwd_button.config(state=DISABLED)
                messagebox.showinfo('SUCCESS!!', '''Password has been changed successfully.
                \nNote: You cannot change password again until you login again.''')

            else:
                messagebox.showerror('OOPs...', 'New and Confirm password did not match!!')
        else:
            messagebox.showerror('ERROR', "The entered Current Password is wrong!!!")

    def assignment(self, user_dict):
        self.destroy_all()
        self.assignment_frame = Frame(self.right_frame, bg=background, height=50)
        self.assignment_frame.grid(row=0, column=0, sticky=NSEW)

        Grid.columnconfigure(self.assignment_frame, 0, weight=1)
        Grid.rowconfigure(self.assignment_frame, 0, weight=1)

        Grid.columnconfigure(self.right_frame, 0, weight=1)

        # Declaring the dictionary
        stream_dict = {"Science": 1,
                       "Commerce": 2,
                       "Arts": 3,
                       "Voc. Science": 4}
        assign_code = str(stream_dict[user_dict['stream_name']])+user_dict['standard']
        # Extracting assignments from database
        cursor.execute('SELECT * FROM assignment WHERE assignment_code = %s', (assign_code,))
        assignments = cursor.fetchall()

        self.ass_frame = []
        self.row_num = 0
        for i in range(len(assignments)):
            if not assignments[i][12]:
                cursor.execute('SELECT turned_in FROM submission WHERE student_id = %s AND assignment_id = %s',
                               (user_dict['user_id'], assignments[i][9]))
                turned_in = cursor.fetchone()
                if turned_in is None:
                    self.show_assignment(user_dict, assignments[i], self.row_num)
                    self.row_num += 1

        if not self.row_num:
            self.no_assign = Label(self.assignment_frame, text='Yayy...NO assignments to do!!',
                                   bg=background, fg=btns, font=college_txt)
            self.no_assign.pack(fill=BOTH, expand=1)

    def show_assignment(self, user_dict, assignment, row_num):
        self.ass_frame.append(Frame(self.assignment_frame, bg=background))
        self.ass_frame[row_num].grid(row=row_num, column=0)
        self.ass_frame.append(
            Frame(self.assignment_frame, bg=background, highlightbackground=txt, highlightthickness=1))
        self.ass_frame[row_num].grid(row=row_num, column=0, sticky=NSEW)
        Grid.columnconfigure(self.ass_frame[row_num], 0, weight=1)
        Grid.columnconfigure(self.ass_frame[row_num], 1, weight=5)
        Grid.columnconfigure(self.ass_frame[row_num], 2, weight=1)
        Grid.columnconfigure(self.ass_frame[row_num], 3, weight=1)
        Grid.rowconfigure(self.ass_frame[row_num], 0, weight=1)
        Grid.rowconfigure(self.ass_frame[row_num], 1, weight=2)
        Grid.rowconfigure(self.ass_frame[row_num], 2, weight=1)

        self.assignment_topic = Label(self.ass_frame[row_num], text=assignment[10].strip(), bg=background, fg=btns,
                                      font=page_txt)
        self.assignment_topic.grid(row=0, column=0, columnspan=2, sticky=W)

        self.assignment_sub = Label(self.ass_frame[row_num], text='Subject: ' + str(assignment[4]), bg=background,
                                    fg=btns, font=label_txt)
        self.assignment_sub.grid(row=2, column=0, sticky=W)

        self.assignment_des = Label(self.ass_frame[row_num], text=assignment[11], bg=background, fg=txt,
                                    font=label_txt)
        self.assignment_des.grid(row=1, column=1, sticky=W)

        self.submit_at = Label(self.ass_frame[row_num], text='Submit at: ' + assignment[7], bg=background, fg=btns,
                               font=label_txt)
        self.submit_at.grid(row=2, column=2, rowspan=3, sticky=W)

        self.turn_in_btn = Button(self.ass_frame[row_num], text='Turn in', bg=btns, fg=background,
                                  font=label_txt, activebackground=panels, activeforeground=txt,
                                  command=lambda: self.turn_in(user_dict, assignment[9], row_num))
        self.turn_in_btn.grid(row=1, column=3, sticky=NSEW)

    def turn_in(self, user_dict, assign_id, row_num):
        cursor.execute('''INSERT INTO submission(
                            assignment_id,
                            student_id,
                            submission_id,
                            student_f_name,
                            student_l_name,
                            turned_in)
                          VALUES(%s, %s, %s, %s, %s, %s)''',
                       (assign_id, user_dict['user_id'],
                        assign_id+user_dict['user_id'], user_dict['f_name'], user_dict['l_name'], 1))
        jr_college_db.commit()
        messagebox.showinfo('Turned in', 'Assignment submitted successfully.')
        self.ass_frame[row_num].destroy()

    def syllabus(self, user_dict):
        self.destroy_all()
        self.syllabus_frame = Frame(self.right_frame, bg=background)
        self.syllabus_frame.pack(fill="both", expand=1)

        # Extracting data from database
        cursor.execute("SELECT stream.id FROM stream WHERE stream.name = %s", (user_dict['stream_name'],))
        stream_id = cursor.fetchone()
        cursor.execute("SELECT subject.code, subject.name FROM subject WHERE stream_id = %s", (stream_id[0],))
        subject_details = cursor.fetchall()

        # Extracting Subject Names
        self.sub_names = []
        for sub_name in subject_details:
            self.sub_names.append(sub_name[1])

        # Extracting Subject Codes
        self.sub_codes = []
        for sub_code in subject_details:
            self.sub_codes.append(sub_code[0])
        # configuring columns and rows
        Grid.columnconfigure(self.syllabus_frame, 0, weight=1)
        Grid.columnconfigure(self.syllabus_frame, 1, weight=3)
        Grid.columnconfigure(self.syllabus_frame, 2, weight=1)
        Grid.rowconfigure(self.syllabus_frame, 0, weight=1)
        Grid.rowconfigure(self.syllabus_frame, 1, weight=1)
        Grid.rowconfigure(self.syllabus_frame, 2, weight=1)
        Grid.rowconfigure(self.syllabus_frame, 3, weight=1)
        Grid.rowconfigure(self.syllabus_frame, 4, weight=1)
        Grid.rowconfigure(self.syllabus_frame, 5, weight=1)
        Grid.rowconfigure(self.syllabus_frame, 6, weight=1)
        # Creating Buttons For Each Subject
        self.buttons = []
        for i in range(len(self.sub_names)):
            self.add_button(self.sub_codes[i], user_dict, self.sub_names[i], i)

    def add_button(self, sub_code, user_dict, sub_name, row_num):
        self.buttons.append(Button(self.syllabus_frame, text=str(sub_name).title(),
                                   command=lambda: self.show_syllabus(sub_code, user_dict, sub_name),
                                   bg=btns, fg=background, activebackground=panels, activeforeground=txt))
        self.buttons[row_num].grid(row=row_num, column=1, sticky=NSEW)

    def show_syllabus(self, sub_code, user_dict, sub_name):
        # Extracting Data from Database
        syl_code = str(sub_code) + str(user_dict["standard"])
        cursor.execute("SELECT chapter FROM syllabus WHERE syllabus.code = %s", (syl_code,))
        chapters = cursor.fetchall()

        # Creating frame to show syllabus
        self.destroy_all()
        self.chapter_frame = Frame(self.right_frame, bg=background)
        self.chapter_frame.pack(fill=BOTH, expand=1)
        Grid.columnconfigure(self.chapter_frame, 0, weight=1)

        for i in range(50):
            Grid.rowconfigure(self.chapter_frame, i, weight=1)

        # Subject title
        self.subject_title = Label(self.chapter_frame, text=str(sub_name).title(), bg=background, fg=btns,
                                   font=page_txt)
        self.subject_title.grid(row=0, column=0, sticky=W)

        # Extracting all chapters
        self.list_of_chaps = []
        for chapter in chapters:
            self.list_of_chaps.append(chapter[0])
        # Displaying all the chapters
        for i in range(len(self.list_of_chaps)):
            self.chapter_label = Label(self.chapter_frame, text=f"{i + 1}. {self.list_of_chaps[i]}", bg=background,
                                       fg=txt, font=label_txt)
            self.chapter_label.grid(row=i + 1, column=0, sticky=W, padx=30)


# Creating a faculty interface
class Faculty(Main):
    def __init__(self, root, user_dict):
        super().__init__(root, user_dict['user_id'])
        # Configure buttons according to faculty use
        self.profile_button.config(text=user_dict["f_name"] + " " + user_dict["l_name"],
                                   command=lambda: self.profile(user_dict))
        self.assignment_button.config(command=lambda: self.assignment(user_dict))
        self.syllabus_button.config(command=lambda: self.syllabus(user_dict))

        # A Menu button
        self.menu_btn = Menubutton(self.top_frame, text=u"\u2261", height=2, width=6, justify="center",
                                   bg=panels, fg=txt, activebackground=btns, activeforeground=background)
        self.menu_btn.place(relx=1, rely=0.5, anchor='e')
        self.menu_btn.menu = Menu(self.menu_btn, tearoff=0, bg=background, fg=txt,
                                  activebackground=btns, activeforeground=background)
        self.menu_btn["menu"] = self.menu_btn.menu
        self.menu_btn.menu.add_command(label="My Profile", command=lambda: self.profile(user_dict))
        self.menu_btn.menu.add_command(label="Change Password",
                                       command=lambda: self.change_passwd(user_dict))
        self.menu_btn.menu.add_separator()
        self.menu_btn.menu.add_command(label="Log out and Exit", command=root.destroy)

        # Adding features for HOD
        if user_dict['is_hod'] == "Yes":
            self.edit_btn = Button(self.left_frame, text="Edit", justify='center',
                                   bg=panels, fg=txt, font=label_txt,
                                   activebackground=btns, activeforeground=txt,
                                   command=lambda: self.edit(user_dict))
            self.edit_btn.grid(row=3, column=0, sticky=NSEW)

    def change_passwd(self, user_dict):
        self.destroy_all()
        self.change_passwd_frame = Frame(self.right_frame, bg=background)

        # Title
        self.change_passwd_title = Label(self.change_passwd_frame, text='Change Password', bg=background, fg=btns,
                                         font=page_txt)
        self.change_passwd_title.grid(row=0, column=0, columnspan=5)

        # Old password
        self.old_passwd_label = Label(self.change_passwd_frame, text='Current Password: ', bg=background, fg=txt,
                                      font=label_txt)
        self.old_passwd_label.grid(row=1, column=1, sticky='w')

        self.old_passwd_value = Entry(self.change_passwd_frame, show='*', bg=txt, fg=background,
                                      font=entry_txt)
        self.old_passwd_value.grid(row=1, column=3)

        # New password
        self.new_passwd_label = Label(self.change_passwd_frame, text='New Password: ', bg=background, fg=txt,
                                      font=label_txt)
        self.new_passwd_label.grid(row=2, column=1, sticky='w')

        self.new_passwd_value = Entry(self.change_passwd_frame, show='*', bg=txt, fg=background,
                                      font=entry_txt)
        self.new_passwd_value.grid(row=2, column=3)

        # Confirm password
        self.confirm_passwd_label = Label(self.change_passwd_frame, text='Confirm new Password: ', bg=background,
                                          fg=txt, font=label_txt)
        self.confirm_passwd_label.grid(row=3, column=1, sticky='w')

        self.confirm_passwd_value = Entry(self.change_passwd_frame, show='*', bg=txt, fg=background,
                                          font=entry_txt)
        self.confirm_passwd_value.grid(row=3, column=3)

        # Change password
        self.change_passwd_button = Button(self.change_passwd_frame, text='Change Password',
                                           bg=btns, fg=background, font=label_txt, activebackground=panels,
                                           activeforeground=txt,
                                           command=lambda: self.verify_change(user_dict))
        self.change_passwd_button.grid(row=4, column=2, sticky='w')

        if self.passwd_changed:
            self.change_passwd_button.config(state=DISABLED)

        self.change_passwd_frame.place(relx=0.25, rely=0.35)

    def verify_change(self, user_dict):
        enc_pass = Encoder(self.old_passwd_value.get(), user_dict['key'])
        if enc_pass.encoded_passwd == user_dict['passwd']:
            if self.new_passwd_value.get() == self.confirm_passwd_value.get():
                enc_new_pass = Encoder(self.new_passwd_value.get())
                # updating database
                cursor.execute("UPDATE faculty SET passwd = %s, key_val = %s WHERE user_id = %s",
                               (enc_new_pass.encoded_passwd, enc_new_pass.key, user_dict['user_id']))
                jr_college_db.commit()
                self.passwd_changed = True
                self.change_passwd_button.config(state=DISABLED)
                messagebox.showinfo('SUCCESS!!', '''Password has been changed successfully.
                \nNote: You cannot change password again until you login again.''')

            else:
                messagebox.showerror('OOPs...', 'New and Confirm password did not match!!')
        else:
            messagebox.showerror('ERROR', "The entered Current Password is wrong!!!")

    def assignment(self, user_dict):
        self.destroy_all()
        self.assignment_frame = Frame(self.right_frame, bg=background)
        self.assignment_frame.pack(fill=BOTH, expand=1)

        # add assignment button
        self.add_assignment_btn = Button(self.assignment_frame, text='Add assignment',
                                         bg=btns, fg=background, activebackground=panels,
                                         activeforeground=txt,
                                         command=lambda: self.add_assignment(user_dict))
        self.add_assignment_btn.grid(row=0, column=0)

        # Extracting the assignments given by the faculty
        cursor.execute('SELECT * FROM assignment WHERE faculty_id = %s', (user_dict['user_id'], ))
        assignments = cursor.fetchall()

        # Configuring the columns in assignment frame
        Grid.columnconfigure(self.assignment_frame, 0, weight=1)

        self.ass_frame = []
        self.row_num = 0
        for i in range(len(assignments)):
            if not assignments[i][12]:
                self.show_assignments(assignments[i], self.row_num)
                self.row_num += 1

    def show_assignments(self, assignment, row_num):
        self.ass_frame.append(Frame(self.assignment_frame, bg=background))
        self.ass_frame[row_num].grid(row=row_num+1, column=0, sticky=NSEW)

        # Configuring the rows and columns
        Grid.rowconfigure(self.ass_frame[row_num], 0, weight=2)
        Grid.rowconfigure(self.ass_frame[row_num], 1, weight=2)
        Grid.rowconfigure(self.ass_frame[row_num], 2, weight=1)
        Grid.columnconfigure(self.ass_frame[row_num], 0, weight=1)
        Grid.columnconfigure(self.ass_frame[row_num], 1, weight=1)
        Grid.columnconfigure(self.ass_frame[row_num], 2, weight=1)

        self.assignment_topic = Label(self.ass_frame[row_num], text=assignment[10], bg=background, fg=btns,
                                      font=page_txt)
        self.assignment_topic.grid(row=0, column=0, sticky=W)

        # Extracting stream name from stream_id
        cursor.execute('SELECT name FROM stream WHERE id = %s', (assignment[2],))
        stream_name = cursor.fetchone()
        self.assignment_stream = Label(self.ass_frame[row_num], text="Stream: "+stream_name[0], bg=background, fg=btns,
                                       font=label_txt)
        self.assignment_stream.grid(row=2, column=0, sticky=W)

        self.assignment_des = Label(self.ass_frame[row_num], text=assignment[11], bg=background, fg=txt, font=label_txt)
        self.assignment_des.grid(row=1, column=0, columnspan=2)

        self.mail_at = Label(self.ass_frame[row_num], text="Mail at: "+assignment[7], bg=background, fg=btns,
                             font=label_txt)
        self.mail_at.grid(row=2, column=1, sticky=W)

        self.view_result_btn = Button(self.ass_frame[row_num], text='View result', bg=btns, fg=background,
                                      font=label_txt, activebackground=panels, activeforeground=txt,
                                      command=lambda: self.view_result(assignment[9], row_num))
        self.view_result_btn.grid(row=0, column=2, rowspan=3, sticky=E)

    def view_result(self, assign_id, row_num):
        self.view_result_window = Toplevel()
        self.view_result_window.title('View Result')
        self.view_result_window.geometry('700x500')
        self.view_result_window.config(bg=background)

        # title of window
        self.view_result_title = Label(self.view_result_window, text='List of submitted students', bg=background,
                                       fg=btns, font=page_txt)
        self.view_result_title.grid(row=0, column=0, columnspan=3)

        # Title for columns
        self.stud_id_title = Label(self.view_result_window, text='Student id', bg=background, fg=btns,
                                   font=label_txt)
        self.stud_id_title.grid(row=1, column=0)

        self.stud_name_title = Label(self.view_result_window, text='Student name', bg=background, fg=btns,
                                     font=label_txt)
        self.stud_name_title.grid(row=1, column=1)

        self.marks_title = Label(self.view_result_window, text='Marks', bg=background, fg=btns,
                                 font=label_txt)
        self.marks_title.grid(row=1, column=2)

        cursor.execute("SELECT * FROM submission WHERE assignment_id = %s", (assign_id,))
        submitted_results = cursor.fetchall()

        self.stud_id = []
        self.stud_name = []
        self.marks = []
        for i in range(len(submitted_results)):
            self.show_student(submitted_results[i], i+3)

        # buttons
        self.done_btn = Button(self.view_result_window, text='Done', bg=btns, fg=background,
                               font=label_txt, activebackground=panels, activeforeground=txt,
                               command=lambda: self.done(submitted_results))
        self.done_btn.grid(row=0, column=3)

        self.submit_btn = Button(self.view_result_window, text='Submit', bg=btns, fg=background,
                                 font=label_txt, activebackground=panels, activeforeground=txt,
                                 command=lambda: self.submit(submitted_results, row_num, assign_id))
        self.submit_btn.grid(row=0, column=4)

    def show_student(self, student, row_num):
        self.stud_id.append(Label(self.view_result_window, text=student[1], bg=background, fg=txt, font=label_txt))
        self.stud_id[row_num-3].grid(row=row_num, column=0)

        self.stud_name.append(Label(self.view_result_window, text=f'{student[3]} {student[4]}', bg=background,
                                    fg=txt, font=label_txt))
        self.stud_name[row_num-3].grid(row=row_num, column=1)

        self.marks.append(Entry(self.view_result_window, bg=txt, fg=background, font=entry_txt))
        self.marks[row_num-3].insert(0, student[5])
        self.marks[row_num-3].grid(row=row_num, column=2)

    def done(self, submitted_results):
        done = True
        for i in range(len(submitted_results)):
            mark = int(self.marks[i].get())
            submission_id = submitted_results[i][2]
            # storing data in data_base
            if mark > 100 or mark < 0:
                messagebox.showerror("Invalid Input", "The Entered marks cannot be negative or greater than 100")
                done = False
                break
            else:
                cursor.execute("UPDATE submission SET marks = %s WHERE submission_id = %s", (mark, submission_id))
                jr_college_db.commit()
                done = True
        if done:
            messagebox.showinfo("Marks Saved", "Entered marks were saved")
            self.view_result_window.destroy()

    def submit(self, submitted_results, row_num, assign_id):
        choice = messagebox.askyesno("Are You Sure You Want To Continue?",
                                     "Assignment will be saved\nAnd you will no longer be able to edit any info of this"
                                     " Assignment")
        if choice == 1:
            done = True
            for i in range(len(submitted_results)):
                mark = int(self.marks[i].get())
                submission_id = submitted_results[i][2]
                # storing data in data_base
                if mark > 100 or mark < 0:
                    messagebox.showerror("Invalid Input", "The Entered marks cannot be negative or greater than 100")
                    done = False
                    break
                else:
                    cursor.execute("UPDATE submission SET marks = %s WHERE submission_id = %s", (mark, submission_id))
                    jr_college_db.commit()
                    done = True
                    cursor.execute('SELECT points FROM student WHERE user_id = %s', (submitted_results[i][1],))
                    points = cursor.fetchone()
                    mark += points[0]
                    cursor.execute("UPDATE student SET points = %s WHERE user_id = %s", (mark, submitted_results[i][1]))
                    jr_college_db.commit()

            if done:
                cursor.execute('DELETE FROM submission WHERE assignment_id = %s', (assign_id,))
                jr_college_db.commit()
                cursor.execute('UPDATE assignment SET submitted = %s WHERE assignment_id = %s',
                               (1, assign_id))
                jr_college_db.commit()
                messagebox.showinfo("Assignment data Saved", "All changes were saved.")
                self.ass_frame[row_num].destroy()
                self.view_result_window.destroy()

    def add_assignment(self, user_dict):
        self.new_ass_window = Toplevel()
        self.new_ass_window.title('Add a new assignment')
        self.new_ass_window.geometry('800x400')
        self.new_ass_window.config(bg=background)

        # a topic for the window
        self.new_ass_title = Label(self.new_ass_window, text='New assignment', bg=background, fg=btns, font=page_txt)
        self.new_ass_title.grid(row=0, column=0, columnspan=5)

        # assignment topic
        self.new_ass_topic = Label(self.new_ass_window, text='Assignment topic: ', bg=background, fg=txt,
                                   font=label_txt)
        self.new_ass_topic.grid(row=1, column=1, sticky=W)

        self.new_ass_topic_val = Entry(self.new_ass_window, bg=txt, fg=background, font=entry_txt)
        self.new_ass_topic_val.grid(row=1, column=3, sticky=W)

        # assignment description
        self.new_ass_des = Label(self.new_ass_window, text='Assignment Description: ', bg=background, fg=txt,
                                 font=label_txt)
        self.new_ass_des.grid(row=2, column=1, sticky=W)

        self.new_ass_des_val = Text(self.new_ass_window, height=5, width=50, bg=txt, fg=background, font=text_txt)
        self.new_ass_des_val.grid(row=2, column=3, sticky=W)

        # Extracting data from database
        cursor.execute("SELECT stream_id, subject.code FROM subject WHERE faculty_id = %s", (user_dict["user_id"],))
        faculty_sub_detail = cursor.fetchall()

        # Extracting stream_names
        self.stream_names = []
        for stream_id in faculty_sub_detail:
            cursor.execute("SELECT stream.name FROM stream WHERE stream.id = %s", (stream_id[0],))
            stream = cursor.fetchall()
            self.stream_names.append(stream[0][0])
        # standard
        self.new_ass_std = Label(self.new_ass_window, text='Standard: ', bg=background, fg=txt,
                                 font=label_txt)
        self.new_ass_std.grid(row=3, column=1, sticky=W)

        self.new_ass_std_selector = ttk.Combobox(self.new_ass_window, values=("XI", "XII"), state='readonly')
        self.new_ass_std_selector.config(background=txt, foreground=background, font=entry_txt)
        self.new_ass_std_selector.current(0)
        self.new_ass_std_selector.grid(row=3, column=3, sticky=W)

        # stream
        self.new_ass_stream = Label(self.new_ass_window, text='Stream: ', bg=background, fg=txt,
                                    font=label_txt)
        self.new_ass_stream.grid(row=4, column=1, sticky=W)

        self.new_ass_stream_selector = ttk.Combobox(self.new_ass_window, state='readonly')
        self.new_ass_stream_selector['values'] = self.stream_names
        self.new_ass_stream_selector.config(background=txt, foreground=background, font=entry_txt)
        self.new_ass_stream_selector.current(0)
        self.new_ass_stream_selector.grid(row=4, column=3, sticky=W)
        stream_dict = {"Science": 1,
                       "Commerce": 2,
                       "Arts": 3,
                       "Voc. Science": 4}

        # Email at
        self.new_ass_email = Label(self.new_ass_window, text='Email at: ', bg=background, fg=txt,
                                   font=label_txt)
        self.new_ass_email.grid(row=5, column=1, sticky=W)

        self.new_ass_email_val = Entry(self.new_ass_window, bg=txt, fg=background, font=entry_txt)
        self.new_ass_email_val.insert(0, user_dict['email'])
        self.new_ass_email_val.grid(row=5, column=3, sticky=W)

        # save button
        self.save_ass_btn = Button(self.new_ass_window, text='Save', bg=btns, fg=background, font=label_txt,
                                   activebackground=panels, activeforeground=txt,
                                   command=lambda:
                                   self.save_assignment(user_dict,
                                                        stream_dict[self.new_ass_stream_selector.get().title()],
                                                        self.new_ass_std_selector.get(),
                                                        self.new_ass_topic_val.get(),
                                                        self.new_ass_des_val.get(1.0, END)))
        self.save_ass_btn.grid(row=6, column=2, sticky=W)

    def save_assignment(self, user_dict, stream_id, std, topic, descrptn):
        # Extracting subject name
        cursor.execute('SELECT name FROM subject WHERE subject_id = %s', (user_dict['subject_id'],))
        sub = cursor.fetchone()
        # creating subject_code
        sub_code = int(str(stream_id) + str(user_dict['subject_id']))
        # Creating assignment code
        assign_code = str(stream_id)+std
        try:
            # Entering data in database
            cursor.execute('''INSERT INTO assignment(
                                    faculty_id,
                                    stream_id,
                                    subject_id,
                                    subject_name,
                                    standard,
                                    subject_code,
                                    email,
                                    assignment_code,
                                    assignment_topic,
                                    assignment_description)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                           (user_dict['user_id'],
                            stream_id,
                            user_dict['subject_id'],
                            sub[0],
                            std,
                            sub_code,
                            user_dict['email'],
                            assign_code,
                            topic,
                            descrptn))
            jr_college_db.commit()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror('Oops...', 'The entered assignment is already given!!!')
            return

        # Extracting id
        cursor.execute('SELECT id FROM assignment WHERE assignment_description = %s', (descrptn,))
        id = cursor.fetchone()
        # creating assignment id
        assign_id = str(sub_code)+std+str(id[0])
        # adding Assignment id to the database
        cursor.execute('UPDATE assignment SET assignment_id = %s WHERE assignment_description = %s',
                       (assign_id, descrptn))
        jr_college_db.commit()

        # Adding a widget of the currently added assignment
        row_num = len(self.ass_frame)
        self.ass_frame.append(Frame(self.assignment_frame, bg=background))
        self.ass_frame[row_num].grid(row=row_num + 1, column=0, sticky=NSEW)

        # Configuring the rows and columns
        Grid.rowconfigure(self.ass_frame[row_num], 0, weight=2)
        Grid.rowconfigure(self.ass_frame[row_num], 1, weight=2)
        Grid.rowconfigure(self.ass_frame[row_num], 2, weight=1)
        Grid.columnconfigure(self.ass_frame[row_num], 0, weight=1)
        Grid.columnconfigure(self.ass_frame[row_num], 1, weight=1)
        Grid.columnconfigure(self.ass_frame[row_num], 2, weight=1)

        self.assignment_topic = Label(self.ass_frame[row_num], text=topic, bg=background, fg=btns, font=page_txt)
        self.assignment_topic.grid(row=0, column=0, sticky=W)

        # Extracting stream name from stream_id
        cursor.execute('SELECT name FROM stream WHERE id = %s', (stream_id,))
        stream_name = cursor.fetchone()
        self.assignment_stream = Label(self.ass_frame[row_num], text="Stream: "+stream_name[0], bg=background, fg=btns,
                                       font=label_txt)
        self.assignment_stream.grid(row=2, column=0, sticky=W)

        self.assignment_des = Label(self.ass_frame[row_num], text=descrptn, bg=background, fg=txt, font=label_txt)
        self.assignment_des.grid(row=1, column=0, columnspan=2)

        self.mail_at = Label(self.ass_frame[row_num], text="Mail at: "+user_dict['email'], bg=background, fg=btns,
                             font=label_txt)
        self.mail_at.grid(row=2, column=1, sticky=W)

        self.view_result_btn = Button(self.ass_frame[row_num], text='View result', font=label_txt,
                                      bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                      command=lambda: self.view_result(assign_id, row_num))
        self.view_result_btn.grid(row=0, column=2, rowspan=2, sticky=E)
        # showing success
        messagebox.showinfo('SUCCESS', f'Assignment {topic} added')

        self.new_ass_window.destroy()

    def syllabus(self, user_dict):
        self.destroy_all()
        self.syllabus_frame = Frame(self.right_frame, bg=background)
        self.syllabus_frame.pack(fill="both", expand=1)
        # Extracting data from database
        cursor.execute("SELECT stream_id, subject.code FROM subject WHERE faculty_id = %s", (user_dict["user_id"],))
        faculty_sub_detail = cursor.fetchall()

        # Extracting stream_names
        self.stream_names = []
        for stream_id in faculty_sub_detail:
            cursor.execute("SELECT stream.name FROM stream WHERE stream.id = %s", (stream_id[0],))
            stream = cursor.fetchall()
            self.stream_names.append(stream[0][0])

        # Extracting subject code
        self.sub_codes = []
        for sub_code in faculty_sub_detail:
            self.sub_codes.append(sub_code[1])

        # Subject title
        self.select_standard_lbl = Label(self.syllabus_frame, text="Select Standard: ", bg=background, fg=txt,
                                         font=label_txt)
        self.select_standard_lbl.grid(row=0, column=0)
        self.standard_selector = ttk.Combobox(self.syllabus_frame, values=("XI", "XII"), state='readonly')
        self.standard_selector.config(background=txt, foreground=background, font=entry_txt)
        self.standard_selector.current(0)
        self.standard_selector.grid(row=0, column=1)

        # adding buttons
        self.buttons = []
        for i in range(len(self.stream_names)):
            self.add_button(self.stream_names[i], self.sub_codes[i], i + 3)

    def add_button(self, stream_name, sub_code, row_num):
        self.buttons.append(Button(self.syllabus_frame, text=str(stream_name).title(),
                                   bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                   command=lambda: self.show_syllabus(sub_code, self.standard_selector.get())))
        self.buttons[row_num-3].grid(row=row_num, column=0)

    def show_syllabus(self, sub_code, standard):
        syl_code = str(sub_code)+str(standard)
        cursor.execute("SELECT syllabus.chapter FROM syllabus WHERE syllabus.code = %s", (syl_code,))
        chapters = cursor.fetchall()

        # Creating frame to show syllabus
        self.destroy_all()
        self.chapter_frame = Frame(self.right_frame, bg=background)
        self.chapter_frame.pack(fill=BOTH, expand=1)

        # Extracting all chapters
        self.list_of_chaps = []
        for chapter in chapters:
            self.list_of_chaps.append(chapter[0])
        # Displaying all the chapters
        for i in range(len(self.list_of_chaps)):
            self.chapter_label = Label(self.chapter_frame, text=str(i+1)+"."+self.list_of_chaps[i],
                                       bg=background, fg=txt, font=label_txt)
            self.chapter_label.grid(row=i + 1, column=2)

    # Creating Hod Related Functions
    def edit(self, user_dict):
        self.destroy_all()
        self.edit_frame = Frame(self.right_frame, bg=background)
        self.edit_frame.pack(fill="both", expand=1)

        # Select Standard
        self.select_standard_lbl = Label(self.edit_frame, text="Select Standard: ", bg=background, fg=txt,
                                         font=label_txt)
        self.select_standard_lbl.grid(row=0, column=0)
        self.standard_selector = ttk.Combobox(self.edit_frame, values=("XI", "XII"), state='readonly', background=txt,
                                              foreground=background, font=entry_txt)
        self.standard_selector.current(0)
        self.standard_selector.grid(row=0, column=1)

        # Select Stream
        self.select_stream_lbl = Label(self.edit_frame, text="Select Stream: ", bg=background, fg=txt,
                                       font=label_txt)
        self.select_stream_lbl.grid(row=2, column=0)
        self.stream_selector = ttk.Combobox(self.edit_frame, values=("Science", "Commerce", "Arts", "Voc. Science"),
                                            state='readonly', background=txt, foreground=background, font=entry_txt)
        self.stream_selector.current(0)
        self.stream_selector.grid(row=2, column=1)

        stream_dict = {"Science": 1,
                       "Commerce": 2,
                       "Arts": 3,
                       "Voc. Science": 4}

        # creating a frame to edit syllabus
        self.edit_syl_frame = Frame(self.edit_frame, bg=background)
        self.edit_syl_frame.grid(row=3, column=0, columnspan=10)

        # Button for editing
        self.edit_syl_button = Button(self.edit_frame, text="Edit Syllabus", font=label_txt,
                                      bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                      command=lambda:
                                      self.edit_syllabus(stream_dict[self.stream_selector.get()],
                                                         user_dict['subject_id'],
                                                         self.standard_selector.get()))
        self.edit_syl_button.grid(row=0, column=3)

    def edit_syllabus(self, stream_id, sub_id, standard):
        # clearing the search results
        self.edit_syl_frame.destroy()
        # generating the syllabus code for extraction of syllabus
        subject_code = str(stream_id) + str(sub_id)
        syl_code = subject_code + standard
        # Extracting the syllabus
        cursor.execute("SELECT * FROM syllabus WHERE code = %s", (syl_code,))
        syllabus = cursor.fetchall()

        # creating a frame to edit syllabus
        self.edit_syl_frame = Frame(self.edit_frame, bg=background)
        self.edit_syl_frame.grid(row=3, column=0, columnspan=10)

        # title of the frame
        self.title = Label(self.edit_syl_frame, text='The chapters in the syllabus are: ', bg=background, fg=txt,
                           font=label_txt)
        self.title.grid(row=0, column=0, columnspan=4)

        # a button to add a new chapter
        self.add_chapter_btn = Button(self.edit_syl_frame, text='Add chapter', font=label_txt,
                                      bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                      command=lambda:
                                      self.add_chapter(syl_code,
                                                       self.standard_selector.get(),
                                                       subject_code))
        self.add_chapter_btn.grid(row=0, column=5)

        # Creating titles for fields
        self.subject_code_title = Label(self.edit_syl_frame, text='Subject code', bg=background, fg=btns,
                                        font=label_txt)
        self.subject_code_title.grid(row=1, column=0)

        self.standard_title = Label(self.edit_syl_frame, text='Standard', bg=background, fg=btns, font=label_txt)
        self.standard_title.grid(row=1, column=1)

        self.syllabus_code_title = Label(self.edit_syl_frame, text='Syllabus code', bg=background, fg=btns,
                                         font=label_txt)
        self.syllabus_code_title.grid(row=1, column=2)

        self.chapter_name_title = Label(self.edit_syl_frame, text='Chapter', bg=background, fg=btns, font=label_txt)
        self.chapter_name_title.grid(row=1, column=3)

        self.subject_code = []
        self.standard = []
        self.syllabus_code = []
        self.chapter_name = []
        self.delete_buttons = []
        for i in range(len(syllabus)):
            self.show_chapter(syllabus[i], 2+i)

    def show_chapter(self, syllabus, row_num):
        self.subject_code.append(Label(self.edit_syl_frame, text=syllabus[1], bg=background, fg=txt, font=label_txt))
        self.subject_code[row_num-2].grid(row=row_num, column=0)

        self.standard.append(Label(self.edit_syl_frame, text=syllabus[2], bg=background, fg=txt, font=label_txt))
        self.standard[row_num-2].grid(row=row_num, column=1)

        self.syllabus_code.append(Label(self.edit_syl_frame, text=syllabus[3], bg=background, fg=txt, font=label_txt))
        self.syllabus_code[row_num-2].grid(row=row_num, column=2)

        self.chapter_name.append(Label(self.edit_syl_frame, text=syllabus[4], bg=background, fg=txt, font=label_txt))
        self.chapter_name[row_num-2].grid(row=row_num, column=3)

        self.delete_buttons.append(Button(self.edit_syl_frame, text='Delete', font=label_txt,
                                          bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                          command=lambda: self.delete_chapter(row_num, syllabus)))
        self.delete_buttons[row_num-2].grid(row=row_num, column=4)

    def add_chapter(self, syl_code, std, sub_code):
        self.add_chapter_window = Toplevel()
        self.add_chapter_window.title('New chapter')
        self.add_chapter_window.geometry('300x300')
        self.add_chapter_window.config(bg=background)

        # Title
        self.new_chapter_title = Label(self.add_chapter_window, text='New Chapter', bg=background, fg=btns,
                                       font=page_txt)
        self.new_chapter_title.grid(row=0, column=0, columnspan=5)

        # Add Chapter
        self.new_chapter_label = Label(self.add_chapter_window, text="Add New Chapter: ", bg=background, fg=txt,
                                       font=label_txt)
        self.new_chapter_label.grid(row=1, column=0)
        self.new_chapter_entry = Entry(self.add_chapter_window, bg=txt, fg=background, font=entry_txt)
        self.new_chapter_entry.grid(row=1, column=1)

        # Save Chapter
        self.save_chapter_btn = Button(self.add_chapter_window, text="Save", font=label_txt,
                                       bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                       command=lambda: self.save_chapter(self.new_chapter_entry.get(), syl_code, std,
                                                                         sub_code))
        self.save_chapter_btn.grid(row=2, column=0)

    def save_chapter(self, new_chapter, syl_code, std, sub_code):
        cursor.execute("INSERT INTO syllabus (chapter, code, standard, subject_code) VALUES (%s, %s, %s, %s)",
                       (new_chapter, syl_code, std, sub_code))
        jr_college_db.commit()
        self.new_chapter_entry.delete(0, END)
        messagebox.showinfo("Chapter Added Succesfully", f"{new_chapter} was added in {sub_code} for standard {std}")

    def delete_chapter(self, row_num, syllabus):
        choice = messagebox.askquestion('Are you sure?', 'You are about to delete a subject.\nDo you want to continue?')
        if choice == 'yes':
            cursor.execute('DELETE FROM subject WHERE id = %s', (syllabus[0],))
            self.subject_code[row_num].destroy()
            self.standard[row_num].destroy()
            self.syllabus_code[row_num].destroy()
            self.chapter_name[row_num].destroy()
            messagebox.showinfo('SUCCESS', 'The subject has been deleted successfully.')
            jr_college_db.commit()
        else:
            return


# Creating a management interface
class Management(Main):
    def __init__(self, root, user_dict):
        super().__init__(root, user_dict['user_id'])
        # Creating frames for further use
        self.edit_teachers_frame = Frame(self.right_frame, bg=background)
        self.edit_students_frame = Frame(self.right_frame, bg=background)
        self.edit_management_frame = Frame(self.right_frame, bg=background)
        self.search_query_frame = Frame(self.right_frame, bg=background)
        # Configuring buttons according to user
        self.profile_button.config(text=user_dict["f_name"] + " " + user_dict["l_name"],
                                   command=lambda: self.profile(user_dict))
        self.assignment_button.destroy()
        self.syllabus_button.destroy()
        # A Menu button
        self.menu_btn = Menubutton(self.top_frame, text=u"\u2261", height=2, width=6, justify="center",
                                   bg=panels, fg=txt, activebackground=btns, activeforeground=background)
        self.menu_btn.place(relx=1, rely=0.5, anchor='e')
        self.menu_btn.menu = Menu(self.menu_btn, tearoff=0, bg=background, fg=txt,
                                  activebackground=btns, activeforeground=background)
        self.menu_btn["menu"] = self.menu_btn.menu
        self.menu_btn.menu.add_command(label="My Profile", command=lambda: self.profile(user_dict))
        self.menu_btn.menu.add_command(label="Change Password",
                                       command=lambda: self.change_passwd(user_dict))
        self.menu_btn.menu.add_separator()
        self.menu_btn.menu.add_command(label="Log out and Exit", command=root.destroy)

        # Configuring the rows and columns
        Grid.columnconfigure(self.left_frame, 0, weight=1)
        Grid.rowconfigure(self.left_frame, 0, weight=1)

        # Adding Features for Management group
        # Features for Science Stream Manager
        if user_dict["post"] == "Head of Science" or user_dict["post"] == "Principal" or \
                user_dict["post"] == "Vice Principal":
            self.science_management_button = Button(self.left_frame, text="Edit Science Stream Info", font=label_txt,
                                                    bg=panels, fg=txt, activebackground=btns,
                                                    activeforeground=background, justify="center",
                                                    command=self.edit_science_stream)
            self.science_management_button.grid(row=4, column=0, sticky=NSEW)
            Grid.rowconfigure(self.left_frame, 4, weight=1)

        # Features for Commerce Stream Manager
        if user_dict["post"] == "Head of Commerce" or user_dict["post"] == "Principal" or \
                user_dict["post"] == "Vice Principal":
            self.commerce_management_button = Button(self.left_frame, text="Edit Commerce Stream Info", font=label_txt,
                                                     bg=panels, fg=txt, activebackground=btns,
                                                     activeforeground=background, justify="center",
                                                     command=self.edit_commerce_stream)
            self.commerce_management_button.grid(row=5, column=0, sticky=NSEW)
            Grid.rowconfigure(self.left_frame, 5, weight=1)

        # Features for Arts Stream Manager
        if user_dict["post"] == "Head of Arts" or user_dict["post"] == "Principal" or \
                user_dict["post"] == "Vice Principal":
            self.arts_management_button = Button(self.left_frame, text="Edit Arts Stream Info", font=label_txt,
                                                 bg=panels, fg=txt, activebackground=btns,
                                                 activeforeground=background, justify="center",
                                                 command=self.edit_arts_stream)
            self.arts_management_button.grid(row=6, column=0, sticky=NSEW)
            Grid.rowconfigure(self.left_frame, 6, weight=1)


        # Features for Voc.Science Stream Manager
        if user_dict["post"] == "Head of Voc. Science" or user_dict["post"] == "Principal" or \
                user_dict["post"] == "Vice Principal":
            self.voc_sci_management_button = Button(self.left_frame, text="Edit Voc. Science Stream Info",
                                                    font=label_txt, bg=panels, fg=txt, activebackground=btns,
                                                    activeforeground=background, justify="center",
                                                    command=self.edit_voc_sci_stream)
            self.voc_sci_management_button.grid(row=7, column=0, sticky=NSEW)
            Grid.rowconfigure(self.left_frame, 7, weight=1)

        # Features for Vice Principal
        if user_dict["post"] == "Vice Principal" or user_dict["post"] == "Principal":
            # Edit Faculty Info
            self.edit_teachers_button = Button(self.left_frame, text="Edit Faculty Info", font=label_txt,
                                               bg=panels, fg=txt, activebackground=btns,
                                               activeforeground=background,
                                               justify="center", command=self.edit_teachers)
            self.edit_teachers_button.grid(row=2, column=0, sticky=NSEW)

            # Edit Student Info
            self.edit_students_button = Button(self.left_frame, text="Edit Student Info", font=label_txt,
                                               bg=panels, fg=txt, activebackground=btns,
                                               activeforeground=background,
                                               justify="center", command=self.edit_students)
            self.edit_students_button.grid(row=3, column=0, sticky=NSEW)
            Grid.rowconfigure(self.left_frame, 1, weight=0)
            Grid.rowconfigure(self.left_frame, 2, weight=1)
            Grid.rowconfigure(self.left_frame, 3, weight=1)

        # Features for Principal
        if user_dict["post"] == "Principal":
            self.edit_management_button = Button(self.left_frame, text="Edit Management Info", font=label_txt,
                                                 bg=panels, fg=txt, activebackground=btns,
                                                 activeforeground=background,
                                                 justify="center", command=self.edit_management)
            self.edit_management_button.grid(row=1, column=0, sticky=NSEW)
            Grid.rowconfigure(self.left_frame, 1, weight=1)

        # Realigning the buttons
        if user_dict["post"] == "Head of Science":
            self.science_management_button.grid_forget()
            self.science_management_button.grid(row=1, column=0, sticky=NSEW)
        if user_dict["post"] == "Head of Commerce":
            self.commerce_management_button.grid_forget()
            self.commerce_management_button.grid(row=1, column=0, sticky=NSEW)
        if user_dict["post"] == "Head of Arts":
            self.arts_management_button.grid_forget()
            self.arts_management_button.grid(row=1, column=0, sticky=NSEW)
        if user_dict["post"] == "Head of Voc. Science":
            self.voc_sci_management_button.grid_forget()
            self.voc_sci_management_button.grid(row=1, column=0, sticky=NSEW)



    def change_passwd(self, user_dict):
        self.destroy_all()
        self.change_passwd_frame = Frame(self.right_frame, bg=background)

        # Title
        self.change_passwd_title = Label(self.change_passwd_frame, text='Change Password', bg=background, fg=btns,
                                         font=page_txt)
        self.change_passwd_title.grid(row=0, column=0, columnspan=5)

        # Old password
        self.old_passwd_label = Label(self.change_passwd_frame, text='Current Password: ', bg=background, fg=txt,
                                      font=label_txt)
        self.old_passwd_label.grid(row=1, column=1, sticky='w')

        self.old_passwd_value = Entry(self.change_passwd_frame, show='*', bg=txt, fg=background, font=entry_txt)
        self.old_passwd_value.grid(row=1, column=3)

        # New password
        self.new_passwd_label = Label(self.change_passwd_frame, text='New Password: ', bg=background, fg=txt,
                                      font=label_txt)
        self.new_passwd_label.grid(row=2, column=1, sticky='w')

        self.new_passwd_value = Entry(self.change_passwd_frame, show='*', bg=txt, fg=background, font=entry_txt)
        self.new_passwd_value.grid(row=2, column=3)

        # Confirm password
        self.confirm_passwd_label = Label(self.change_passwd_frame, text='Confirm new Password: ', bg=background,
                                          fg=txt, font=label_txt)
        self.confirm_passwd_label.grid(row=3, column=1, sticky='w')

        self.confirm_passwd_value = Entry(self.change_passwd_frame, show='*', bg=txt, fg=background, font=entry_txt)
        self.confirm_passwd_value.grid(row=3, column=3)

        # Change password
        self.change_passwd_button = Button(self.change_passwd_frame, text='Change Password', font=label_txt,
                                           bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                           command=lambda: self.verify_change(user_dict))
        self.change_passwd_button.grid(row=4, column=2, sticky='w')

        if self.passwd_changed:
            self.change_passwd_button.config(state=DISABLED)

        self.change_passwd_frame.place(relx=0.25, rely=0.35)

    # Creating Management Related Function
    def edit_teachers(self):
        self.destroy_all()
        self.edit_teachers_frame = Frame(self.right_frame, bg=background)
        # adding a title to the frame
        self.edit_teachers_title = Label(self.edit_teachers_frame, text="Teachers Info", bg=background, fg=btns,
                                         font=page_txt)
        self.edit_teachers_title.grid(row=0, column=0, columnspan=15, sticky=NSEW)
        self.search_ui(self.edit_teachers_frame)
        self.edit_teachers_frame.pack(fill=BOTH, expand=1)

    def edit_students(self):
        self.destroy_all()
        self.edit_students_frame = Frame(self.right_frame, bg=background)
        # adding a title to the frame
        self.edit_students_title = Label(self.edit_students_frame, text="Students Info", bg=background, fg=btns,
                                         font=page_txt)
        self.edit_students_title.grid(row=0, column=0, columnspan=15, sticky=NSEW)
        self.search_ui(self.edit_students_frame)
        self.edit_students_frame.pack(fill=BOTH, expand=1)

    def edit_management(self):
        self.destroy_all()
        self.edit_management_frame = Frame(self.right_frame, bg=background)
        # adding a title to the frame
        self.edit_management_title = Label(self.edit_management_frame, text="Management Info", bg=background, fg=btns,
                                           font=page_txt)
        self.edit_management_title.grid(row=0, column=0, columnspan=15, sticky=NSEW)
        self.search_ui(self.edit_management_frame)
        self.edit_management_frame.pack(fill=BOTH, expand=1)

    def edit_science_stream(self):
        self.destroy_all()
        self.edit_science_stream_frame = Frame(self.right_frame, bg=background)
        # Title
        self.science_title = Label(self.edit_science_stream_frame, text='Subjects in science stream: ', bg=background,
                                   fg=btns, font=page_txt)
        self.science_title.grid(row=0, column=0, columnspan=6)
        self.edit_stream_ui(self.edit_science_stream_frame, 'Science')

        self.edit_science_stream_frame.pack(fill=BOTH, expand=1)

    def edit_commerce_stream(self):
        self.destroy_all()
        self.edit_commerce_stream_frame = Frame(self.right_frame, bg=background)
        # Title
        self.commerce_title = Label(self.edit_commerce_stream_frame, text='Subjects in commerce stream: ',
                                    bg=background, fg=btns, font=page_txt)
        self.commerce_title.grid(row=0, column=0, columnspan=6)
        self.edit_stream_ui(self.edit_commerce_stream_frame, 'Commerce')
        self.edit_commerce_stream_frame.pack(fill=BOTH, expand=1)

    def edit_arts_stream(self):
        self.destroy_all()
        self.edit_arts_stream_frame = Frame(self.right_frame, bg=background)
        # Title
        self.arts_title = Label(self.edit_arts_stream_frame, text='Subjects in arts stream: ', bg=background,
                                fg=btns, font=page_txt)
        self.arts_title.grid(row=0, column=0, columnspan=6)
        self.edit_stream_ui(self.edit_arts_stream_frame, 'Arts')
        self.edit_arts_stream_frame.pack(fill=BOTH, expand=1)

    def edit_voc_sci_stream(self):
        self.destroy_all()
        self.edit_voc_sci_stream_frame = Frame(self.right_frame, bg=background)
        # Title
        self.voc_sci_title = Label(self.edit_voc_sci_stream_frame, text='Subjects in vocational science stream: ',
                                   bg=background, fg=btns, font=page_txt)
        self.voc_sci_title.grid(row=0, column=0, columnspan=6)
        self.edit_stream_ui(self.edit_voc_sci_stream_frame, 'Voc. Science')
        self.edit_voc_sci_stream_frame.pack(fill=BOTH, expand=1)

    # supportive functions
    def edit_stream_ui(self, master_frame, stream):
        # Extracting the stream id for the respective stream
        cursor.execute('SELECT id FROM stream WHERE name = %s', (stream,))
        stream_id = cursor.fetchone()

        # Extracting subjects for the stream
        cursor.execute('SELECT * FROM subject WHERE stream_id = %s', (stream_id[0], ))
        subjects = cursor.fetchall()

        # Configuring the rows and columns
        Grid.columnconfigure(master_frame, 0, weight=1)
        Grid.columnconfigure(master_frame, 1, weight=1)
        Grid.columnconfigure(master_frame, 2, weight=1)
        Grid.columnconfigure(master_frame, 3, weight=1)
        # Grid.columnconfigure(master_frame, 4, weight=1)
        # Grid.columnconfigure(master_frame, 5, weight=1)
        Grid.columnconfigure(master_frame, 6, weight=1)

        # Creating add new subject button
        self.new_sub_btn = Button(master_frame, text='New subject', font=label_txt,
                                  bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                  command=lambda: self.new_sub(stream_id[0]))
        self.new_sub_btn.grid(row=0, column=6, sticky='e')
        # making titles for the attributes of the subjects
        self.sub_id_title = Label(master_frame, text='Subject ID', bg=background, fg=btns, font=label_txt)
        self.sub_id_title.grid(row=1, column=0)

        self.sub_name_title = Label(master_frame, text='Subject name', bg=background, fg=btns, font=label_txt)
        self.sub_name_title.grid(row=1, column=1)

        self.sub_code_title = Label(master_frame, text='Subject code', bg=background, fg=btns, font=label_txt)
        self.sub_code_title.grid(row=1, column=2)

        self.sub_id = []
        self.sub_name = []
        self.sub_code = []
        self.delete_sub = []

        for i in range(len(subjects)):
            self.add_sub(master_frame, subjects[i], 2+i)

    def add_sub(self, master_frame, sub, row):
        # creating
        self.sub_id.append(Label(master_frame, text=sub[2], bg=background, fg=txt, font=label_txt))
        self.sub_id[row-2].grid(row=row, column=0)

        self.sub_name.append(Label(master_frame, text=sub[3], bg=background, fg=txt, font=label_txt))
        self.sub_name[row-2].grid(row=row, column=1)

        self.sub_code.append(Label(master_frame, text=sub[6], bg=background, fg=txt, font=label_txt))
        self.sub_code[row-2].grid(row=row, column=2)

        self.delete_sub.append(Button(master_frame, text='Delete', font=label_txt,
                                      bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                      command=lambda: self.del_sub(row-2, sub[6], sub[4])))
        self.delete_sub[row-2].grid(row=row, column=3)

    def del_sub(self, index, code, faculty_id):
        choice = messagebox.askquestion('Are you sure?',
                                        "You are about to delete a subject and the associated teacher's data."
                                        "\nDo you want to continue?")
        if choice == 'yes':
            cursor.execute('DELETE FROM subject WHERE code = %s', (code,))
            cursor.execute('DELETE FROM syllabus WHERE subject_code = %s', (code,))
            cursor.execute('DELETE FROM faculty WHERE user_id = %s', (faculty_id,))
            self.sub_id[index].destroy()
            self.sub_name[index].destroy()
            self.sub_code[index].destroy()
            self.delete_sub[index].destroy()
            messagebox.showinfo('SUCCESS', 'The subject has been deleted successfully')
            jr_college_db.commit()
        else:
            return

    def new_sub(self, stream_id):
        self.new_sub_window = Toplevel()
        self.new_sub_window.title('Add new subject')
        self.new_sub_window.geometry('400x200')
        self.new_sub_window.config(bg=background)

        # title
        self.new_sub_title = Label(self.new_sub_window, text='New subject: ', bg=background, fg=btns, font=page_txt)
        self.new_sub_title.grid(row=0, column=0, columnspan=5)

        self.name = Label(self.new_sub_window, text='Subject name: ', bg=background, fg=txt, font=label_txt)
        self.name.grid(row=1, column=1)

        self.name_entry = Entry(self.new_sub_window, bg=txt, fg=background, font=entry_txt)
        self.name_entry.grid(row=1, column=3)

        self.add_new_sub_btn = Button(self.new_sub_window, text='Add', font=label_txt,
                                      bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                      command=lambda: self.add_new_subject(self.name_entry.get(), stream_id))
        self.add_new_sub_btn.grid(row=2, column=2)

    def add_new_subject(self, name, stream_id):
        # Checking if the subject already exists in the current stream
        cursor.execute('SELECT * FROM subject WHERE name = %s AND stream_id = %s', (name, stream_id))
        sub = cursor.fetchall()
        if len(sub) == 0:
            # Checking if the subject exists in other streams
            hod_id = str()
            sub_id = int()
            cursor.execute('SELECT * FROM subject WHERE name = %s', (name,))
            sub = cursor.fetchall()
            if len(sub) == 0:
                cursor.execute('SELECT MAX(subject_id) FROM subject')
                max_ui = cursor.fetchone()
                sub_id = int(max_ui[0])+1
                hod_id = 'TBD'
            else:
                sub_id = sub[0][2]
                hod_id = sub[0][5]
            # adding subject to the current stream
            cursor.execute('''INSERT INTO subject(
                                        stream_id,
                                        subject_id,
                                        name,
                                        faculty_id,
                                        hod_id,
                                        code)
                              VALUES(%s, %s, %s ,%s, %s, %s)''',
                           (stream_id, sub_id, name, 'TBD', hod_id, int(str(stream_id) + str(sub_id))))
            jr_college_db.commit()
            self.new_sub_window.destroy()
            messagebox.showinfo('SUCCESS', 'The subject has been successfully added to the stream')
        else:
            messagebox.showerror('Error', 'This subject already exists in the current stream!!')

    def verify_change(self, user_dict):
        enc_pass = Encoder(self.old_passwd_value.get(), user_dict['key'])
        if enc_pass.encoded_passwd == user_dict['passwd']:
            if self.new_passwd_value.get() == self.confirm_passwd_value.get():
                enc_new_pass = Encoder(self.new_passwd_value.get())
                # updating database
                cursor.execute("UPDATE management SET passwd = %s, key_val = %s WHERE user_id = %s",
                               (enc_new_pass.encoded_passwd, enc_new_pass.key, user_dict['user_id']))
                jr_college_db.commit()
                self.passwd_changed = True
                self.change_passwd_button.config(state=DISABLED)
                messagebox.showinfo('SUCCESS!!', '''Password has been changed successfully.
                \nNote: You cannot change password again until you login again.''')

            else:
                messagebox.showerror('OOPs...', 'New and Confirm password did not match!!')
        else:
            messagebox.showerror('ERROR', "The entered Current Password is wrong!!!")

    def search_ui(self, master_frame):
        # Search label
        self.search_label = Label(master_frame, text='Search : ', bg=background, fg=txt, font=label_txt)
        self.search_label.grid(row=1, column=0, sticky='w')

        # search entry
        self.search_entry = Entry(master_frame, bg=txt, fg=background, font=entry_txt)
        self.search_entry.grid(row=1, column=1, sticky='w')

        # 'search_by' box
        self.search_by_box = ttk.Combobox(master_frame, state='readonly')
        self.search_by_box['values'] = ('first_name', 'last_name', 'user_id')
        self.search_by_box.config(background=txt, foreground=background, font=entry_txt)
        self.search_by_box.grid(row=1, column=2, sticky='w')
        self.search_by_box.current(0)

        # search button
        self.search_button = Button(master_frame, text='Search', font=label_txt,
                                    bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                    command=lambda: self.search_result(self.search_by_box.get(),
                                                                       self.search_entry.get(),
                                                                       master_frame))
        self.search_button.grid(row=2, column=0, sticky='w')
        if master_frame != self.edit_management_frame:
            # add new button
            self.add_new_button = Button(master_frame, text='Add new', font=label_txt,
                                         bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                         command=lambda: self.add_new(master_frame))
            self.add_new_button.grid(row=1, column=3, sticky='w')

    def search_result(self, column, value, master_frame):
        self.search_query_frame.destroy()
        if master_frame == self.edit_students_frame:
            # Dynamically changing query based on selected column
            if column == 'first_name':
                cursor.execute("SELECT * FROM student WHERE first_name LIKE %s", (value,))
            elif column == 'last_name':
                cursor.execute("SELECT * FROM student WHERE last_name = %s", (value,))
            elif column == 'user_id':
                cursor.execute("SELECT * FROM student WHERE user_id = %s", (value,))
        elif master_frame == self.edit_teachers_frame:
            if column == 'first_name':
                cursor.execute("SELECT * FROM faculty WHERE first_name = %s", (value,))
            elif column == 'last_name':
                cursor.execute("SELECT * FROM faculty WHERE last_name = %s", (value,))
            elif column == 'user_id':
                cursor.execute("SELECT * FROM faculty WHERE user_id = %s", (value,))
        elif master_frame == self.edit_management_frame:
            if column == 'first_name':
                cursor.execute("SELECT * FROM management WHERE first_name = %s", (value,))
            elif column == 'last_name':
                cursor.execute("SELECT * FROM management WHERE last_name = %s", (value,))
            elif column == 'user_id':
                cursor.execute("SELECT * FROM management WHERE user_id = %s", (value,))
        # Fetching the search results
        search_results = cursor.fetchall()
        # Handling if no results are found
        if len(search_results) == 0:
            messagebox.showinfo('No results found', f'No one with {column} = {value}')
        else:
            # a frame to show search queries
            self.search_query_frame = Frame(master_frame, bg=background)
            self.search_query_frame.grid(row=3, columnspan=5)

            # Showing the results of current query
            for i in range(len(search_results)):
                self.add_query_result(search_results[i], i+1, master_frame)

    def add_query_result(self, result, row_num, master_frame):
        # Creating title labels
        self.title = Label(self.search_query_frame, text='Edit', bg=background, fg=btns, font=label_txt)
        self.title.grid(row=0, column=0)
        self.name_title = Label(self.search_query_frame, text='Name', bg=background, fg=btns, font=label_txt)
        self.name_title.grid(row=0, column=1, columnspan=2)
        self.dob_title = Label(self.search_query_frame, text='DOB', bg=background, fg=btns, font=label_txt)
        self.dob_title.grid(row=0, column=3)
        self.gender_title = Label(self.search_query_frame, text='Gender', bg=background, fg=btns, font=label_txt)
        self.gender_title.grid(row=0, column=4)
        self.email_title = Label(self.search_query_frame, text='Email', bg=background, fg=btns, font=label_txt)
        self.email_title.grid(row=0, column=5)
        self.phone_number_title = Label(self.search_query_frame, text='Phone NO.', bg=background, fg=btns,
                                        font=label_txt)
        self.phone_number_title.grid(row=0, column=6)
        self.address_title = Label(self.search_query_frame, text='Address', bg=background, fg=btns, font=label_txt)
        self.address_title.grid(row=0, column=7)
        self.pincode_title = Label(self.search_query_frame, text='pincode', bg=background, fg=btns, font=label_txt)
        self.pincode_title.grid(row=0, column=8)
        # Edit button
        self.edit_query_button = Button(self.search_query_frame, text='Edit', font=label_txt,
                                        bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                        command=lambda: self.edit_query(result, master_frame))
        self.edit_query_button.grid(row=row_num, column=0)

        # First name
        self.f_name = Label(self.search_query_frame, text=result[1], bg=background, fg=txt, font=label_txt)
        self.f_name.grid(row=row_num, column=1, sticky='w')

        # Last name
        self.l_name = Label(self.search_query_frame, text=result[2], bg=background, fg=txt, font=label_txt)
        self.l_name.grid(row=row_num, column=2, sticky='w')

        # Date of Birth
        self.dob = Label(self.search_query_frame, text=result[3], bg=background, fg=txt, font=label_txt)
        self.dob.grid(row=row_num, column=3, sticky='w')

        # Gender
        self.gender = Label(self.search_query_frame, text=result[4], bg=background, fg=txt, font=label_txt)
        self.gender.grid(row=row_num, column=4, sticky='w')

        # Email id
        self.email = Label(self.search_query_frame, text=result[5], bg=background, fg=txt, font=label_txt)
        self.email.grid(row=row_num, column=5, sticky='w')

        # phone number
        self.phone_no = Label(self.search_query_frame, text=result[6], bg=background, fg=txt, font=label_txt)
        self.phone_no.grid(row=row_num, column=6, sticky='w')

        # address
        self.address = Label(self.search_query_frame, text=result[7], bg=background, fg=txt, font=label_txt)
        self.address.grid(row=row_num, column=7, sticky='w')

        # pincode
        self.pincode = Label(self.search_query_frame, text=result[8], bg=background, fg=txt, font=label_txt)
        self.pincode.grid(row=row_num, column=8, sticky='w')

        if master_frame == self.edit_students_frame:
            # Creating title labels for students
            self.stream_title = Label(self.search_query_frame, text='Stream', bg=background, fg=btns, font=label_txt)
            self.stream_title.grid(row=0, column=9)
            self.user_id_title = Label(self.search_query_frame, text='User ID', bg=background, fg=btns, font=label_txt)
            self.user_id_title.grid(row=0, column=10)
            self.standard_title = Label(self.search_query_frame, text='Standard', bg=background, fg=btns,
                                        font=label_txt)
            self.standard_title.grid(row=0, column=11)
            self.status_title = Label(self.search_query_frame, text='Status', bg=background, fg=btns, font=label_txt)
            self.status_title.grid(row=0, column=12)
            self.doa_title = Label(self.search_query_frame, text='Date of admission', bg=background, fg=btns,
                                   font=label_txt)
            self.doa_title.grid(row=0, column=13)
            self.points_title = Label(self.search_query_frame, text='Points', bg=background, fg=btns, font=label_txt)
            self.points_title.grid(row=0, column=14)
            # creating labels to show data
            self.stream_name = Label(self.search_query_frame, text=result[9], bg=background, fg=txt, font=label_txt)
            self.stream_name.grid(row=row_num, column=9, sticky='w')

            self.user_id = Label(self.search_query_frame, text=result[10], bg=background, fg=txt, font=label_txt)
            self.user_id.grid(row=row_num, column=10, sticky='w')

            self.standard = Label(self.search_query_frame, text=result[12], bg=background, fg=txt, font=label_txt)
            self.standard.grid(row=row_num, column=11, sticky='w')

            self.status = Label(self.search_query_frame, text=result[13], bg=background, fg=txt, font=label_txt)
            self.status.grid(row=row_num, column=12, sticky='w')

            self.doa = Label(self.search_query_frame, text=result[14], bg=background, fg=txt, font=label_txt)
            self.doa.grid(row=row_num, column=13, sticky='w')

            self.points = Label(self.search_query_frame, text=result[15], bg=background, fg=txt, font=label_txt)
            self.points.grid(row=row_num, column=14, sticky='w')
        elif master_frame == self.edit_teachers_frame:
            # is_hod
            self.is_hod_title = Label(self.search_query_frame, text='Is Hod', bg=background, fg=btns, font=label_txt)
            self.is_hod_title.grid(row=0, column=9)
            self.is_hod = Label(self.search_query_frame, text=result[10], bg=background, fg=txt, font=label_txt)
            self.is_hod.grid(row=row_num, column=9, sticky='w')

            # Subject
            self.subject_title = Label(self.search_query_frame, text='Subject', bg=background, fg=btns, font=label_txt)
            self.subject_title.grid(row=0, column=10)
            self.subject = Label(self.search_query_frame, text=result[9], bg=background, fg=txt, font=label_txt)
            self.subject.grid(row=row_num, column=10, sticky='w')

            # user_id
            self.user_id_title = Label(self.search_query_frame, text='User Id', bg=background, fg=btns, font=label_txt)
            self.user_id_title.grid(row=0, column=11)
            self.user_id = Label(self.search_query_frame, text=result[11], bg=background, fg=txt, font=label_txt)
            self.user_id.grid(row=row_num, column=11, sticky='w')
        elif master_frame == self.edit_management_frame:
            # Post
            self.post_title = Label(self.search_query_frame, text='Post', bg=background, fg=btns, font=label_txt)
            self.post_title.grid(row=0, column=9)
            self.post = Label(self.search_query_frame, text=result[9], bg=background, fg=txt, font=label_txt)
            self.post.grid(row=row_num, column=9, sticky='w')

            # user_id
            self.user_id_title = Label(self.search_query_frame, text='User Id', bg=background, fg=btns, font=label_txt)
            self.user_id_title.grid(row=0, column=10)
            self.user_id = Label(self.search_query_frame, text=result[10], bg=background, fg=txt, font=label_txt)
            self.user_id.grid(row=row_num, column=10, sticky='w')

    def edit_query(self, user_info, master_frame):
        self.edit_window = Toplevel()
        self.edit_window.title('Edit info')
        self.edit_window.geometry('750x600')
        self.edit_window.config(bg=background)

        def save_changes(master_frame):
            if master_frame == self.edit_students_frame:
                cursor.execute('''UPDATE student SET first_name = %s, 
                                                     last_name = %s, 
                                                     dob = %s, 
                                                     gender = %s,
                                                     email = %s,
                                                     phone_number = %s, 
                                                     address = %s, 
                                                     pincode = %s, 
                                                     stream_name = %s, 
                                                     standard = %s
                                  WHERE id = %s''',
                               (self.first_name_entry.get(),
                                self.last_name_entry.get(),
                                self.date_of_birth_entry.get(),
                                self.gender_picker.get(),
                                self.email_entry.get(),
                                self.phone_number_entry.get(),
                                self.address_text.get(1.0, END).strip(),
                                self.pincode_entry.get(),
                                self.stream_name_picker.get(),
                                self.standard_picker.get(),
                                user_info[0]))
            elif master_frame == self.edit_teachers_frame:
                if self.is_hod_entry.get().title() == 'Yes':
                    cursor.execute("UPDATE faculty SET is_hod = 'No' WHERE subject_id = %s", (user_info[9],))
                    cursor.execute("UPDATE faculty SET is_hod = 'Yes' WHERE user_id = %s", (user_info[11],))
                    cursor.execute("UPDATE subject SET hod_id = %s WHERE subject_id = %s",
                                   (user_info[11], user_info[9]))
                    jr_college_db.commit()
                cursor.execute('''UPDATE faculty SET first_name = %s, 
                                                     last_name = %s, 
                                                     dob = %s, 
                                                     gender = %s,
                                                     email = %s,
                                                     phone_number = %s, 
                                                     address = %s, 
                                                     pincode = %s
                                                  WHERE id = %s''',
                               (self.first_name_entry.get(),
                                self.last_name_entry.get(),
                                self.date_of_birth_entry.get(),
                                self.gender_picker.get(),
                                self.email_entry.get(),
                                self.phone_number_entry.get(),
                                self.address_text.get(1.0, END).strip(),
                                self.pincode_entry.get(),
                                user_info[0]))
            elif master_frame == self.edit_management_frame:
                cursor.execute('''UPDATE management SET first_name = %s, 
                                                     last_name = %s, 
                                                     dob = %s, 
                                                     gender = %s,
                                                     email = %s,
                                                     phone_number = %s, 
                                                     address = %s, 
                                                     pincode = %s
                                  WHERE id = %s''',
                               (self.first_name_entry.get(),
                                self.last_name_entry.get(),
                                self.date_of_birth_entry.get(),
                                self.gender_picker.get(),
                                self.email_entry.get(),
                                self.phone_number_entry.get(),
                                self.address_text.get(1.0, END).strip(),
                                self.pincode_entry.get(),
                                user_info[0]))
            jr_college_db.commit()
            messagebox.showinfo('SUCCESS', 'All changes have been saved.')
            self.edit_window.destroy()

        def delete_record(master_frame):
            choice = messagebox.askquestion('Warning',
                                            f"You're about to delete {user_info[1]}'s record.\nDo you want to proceed?")
            if choice == 'yes':
                if master_frame == self.edit_students_frame:
                    cursor.execute('DELETE FROM student WHERE id = %s', (user_info[0],))
                elif master_frame == self.edit_teachers_frame:
                    cursor.execute('DELETE FROM faculty WHERE id = %s', (user_info[0],))
                jr_college_db.commit()
                self.edit_window.destroy()
            else:
                return

        # Title
        self.new_student_title = Label(self.edit_window, text="Edit Info", bg=background, fg=btns, font=page_txt)
        self.new_student_title.grid(row=0, column=0, columnspan=5)

        # First name
        self.first_name_label = Label(self.edit_window, text="First name: ", bg=background, fg=txt, font=label_txt)
        self.first_name_label.grid(row=1, column=1, sticky='w')

        self.first_name_entry = Entry(self.edit_window, bg=txt, fg=background, font=entry_txt)
        self.first_name_entry.insert(0, user_info[1])
        self.first_name_entry.grid(row=1, column=3, sticky='w')

        # Last name
        self.last_name_label = Label(self.edit_window, text="Last name: ", bg=background, fg=txt, font=label_txt)
        self.last_name_label.grid(row=2, column=1, sticky='w')

        self.last_name_entry = Entry(self.edit_window, bg=txt, fg=background, font=entry_txt)
        self.last_name_entry.insert(0, user_info[2])
        self.last_name_entry.grid(row=2, column=3, sticky='w')

        # Date of Birth
        self.date_of_birth = Label(self.edit_window, text="Date of Birth", bg=background, fg=txt, font=label_txt)
        self.date_of_birth.grid(row=3, column=1, sticky='w')
        self.date_of_birth_entry = Entry(self.edit_window, bg=txt, fg=background, font=entry_txt)
        self.date_of_birth_entry.insert(0, user_info[3])
        self.date_of_birth_entry.grid(row=3, column=3, sticky='w')
        self.dob_selector_button = Button(self.edit_window, text="Select Birth Date", font=label_txt,
                                          bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                          command=self.birth_date_picker)
        self.dob_selector_button.grid(row=3, column=4, sticky='w')

        # Gender
        self.gender_label = Label(self.edit_window, text="Gender: ", bg=background, fg=txt, font=label_txt)
        self.gender_label.grid(row=4, column=1, sticky='w')

        self.gender_picker = ttk.Combobox(self.edit_window)
        self.gender_picker['values'] = ("Non-binary", "Female", "Male")
        self.gender_picker.config(background=txt, foreground=background, font=entry_txt)
        self.gender_picker.grid(row=4, column=3, sticky='w')
        i = int()
        for i in range(len(self.gender_picker['values'])):
            if self.gender_picker['values'][i] == user_info[4]:
                break
        self.gender_picker.current(i)

        # Email id
        self.email_label = Label(self.edit_window, text="Email ID: ", bg=background, fg=txt, font=label_txt)
        self.email_label.grid(row=5, column=1, sticky='w')

        self.email_entry = Entry(self.edit_window, bg=txt, fg=background, font=entry_txt)
        self.email_entry.insert(0, user_info[5])
        self.email_entry.grid(row=5, column=3, sticky='w')

        # phone number
        self.phone_number_label = Label(self.edit_window, text="Phone number: ", bg=background, fg=txt, font=label_txt)
        self.phone_number_label.grid(row=6, column=1, sticky='w')

        self.phone_number_entry = Entry(self.edit_window, bg=txt, fg=background, font=entry_txt)
        self.phone_number_entry.insert(0, user_info[6])
        self.phone_number_entry.grid(row=6, column=3, sticky='w')

        # Address
        self.address_label = Label(self.edit_window, text="Address :", bg=background, fg=txt, font=label_txt)
        self.address_label.grid(row=7, column=1, sticky='w')

        self.address_text_scroll = Scrollbar(self.edit_window)
        self.address_text_scroll.grid(row=7, column=4, sticky='w')
        self.address_text = Text(self.edit_window, height=2, width=20, bg=txt, fg=background, font=text_txt)
        self.address_text.insert(1.0, user_info[7])
        self.address_text.grid(row=7, column=3, sticky='w')
        self.address_text_scroll.config(command=self.address_text.yview)
        self.address_text.config(yscrollcommand=self.address_text_scroll.set)

        # Pincode
        self.pincode_label = Label(self.edit_window, text="Pincode :", bg=background, fg=txt, font=label_txt)
        self.pincode_label.grid(row=8, column=1, sticky='w')

        self.pincode_entry = Entry(self.edit_window, bg=txt, fg=background, font=entry_txt)
        self.pincode_entry.insert(0, user_info[8])
        self.pincode_entry.grid(row=8, column=3, sticky='w')

        if master_frame == self.edit_students_frame:
            # stream
            self.stream_name = Label(self.edit_window, text="Stream: ", bg=background, fg=txt, font=label_txt)
            self.stream_name.grid(row=9, column=1, sticky='w')

            self.stream_name_picker = ttk.Combobox(self.edit_window)
            self.stream_name_picker['values'] = ("Science", "Commerce", "Arts", "Voc. Science")
            self.stream_name_picker.config(background=txt, foreground=background, font=entry_txt)
            self.stream_name_picker.grid(row=9, column=3, sticky='w')
            for i in range(len(self.stream_name_picker['values'])):
                if self.stream_name_picker['values'][i] == user_info[9]:
                    break
            self.stream_name_picker.current(i)

            # Standard
            self.standard = Label(self.edit_window, text="Standard: ", bg=background, fg=txt, font=label_txt)
            self.standard.grid(row=10, column=1, sticky='w')

            self.standard_picker = ttk.Combobox(self.edit_window)
            self.standard_picker['values'] = ('XI', 'XII')
            self.standard_picker.config(background=txt, foreground=background, font=entry_txt)
            self.standard_picker.grid(row=10, column=3, sticky='w')
            for i in range(len(self.standard_picker['values'])):
                if self.standard_picker['values'][i] == user_info[12]:
                    break
            self.standard_picker.current(i)

            # Status
            self.result_lbl = Label(self.edit_window, text='Status', bg=background, fg=txt, font=label_txt)
            self.result_lbl.grid(row=11, column=1, sticky='w')
            self.result = Label(self.edit_window, text=user_info[13], bg=background, fg=txt, font=label_txt)
            self.result.grid(row=11, column=3, sticky='w')

            # Date of admission
            self.doa_lbl = Label(self.edit_window, text='Date of admission :', bg=background, fg=txt, font=label_txt)
            self.doa_lbl.grid(row=12, column=1, sticky='w')

            self.doa = Label(self.edit_window, text=user_info[14], bg=background, fg=txt, font=label_txt)
            self.doa.grid(row=12, column=3, sticky='w')

            # Points
            self.points_label = Label(self.edit_window, text='Points: ', bg=background, fg=txt, font=label_txt)
            self.points_label.grid(row=13, column=1, sticky='w')

            self.points = Label(self.edit_window, text=user_info[15], bg=background, fg=txt, font=label_txt)
            self.points.grid(row=13, column=3, sticky='w')

            # userId
            self.id_label = Label(self.edit_window, text='User_id: ', bg=background, fg=txt, font=label_txt)
            self.id_label.grid(row=14, column=1, sticky='w')

            self.id = Label(self.edit_window, text=user_info[10], bg=background, fg=txt, font=label_txt)
            self.id.grid(row=14, column=3, sticky='w')

            # password
            self.forgot_passwd = Label(self.edit_window, text='Forgot Password?', bg=background, fg=txt, font=label_txt)
            self.forgot_passwd.grid(row=15, column=1, sticky='w')

            self.restore_passwd_btn = Button(self.edit_window, text='Restore system password.', font=label_txt,
                                             bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                             command=lambda: self.restore_passwd(user_info, master_frame))
            self.restore_passwd_btn.grid(row=15, column=3, sticky='w')
            # delete record button
            self.delete_record = Button(self.edit_window, text='Delete record', font=label_txt,
                                        bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                        command=lambda: delete_record(master_frame))
            self.delete_record.grid(row=0, column=5, sticky='w')
        elif master_frame == self.edit_teachers_frame:
            # is_hod
            self.is_hod_label = Label(self.edit_window, text="is_hod: ", bg=background, fg=txt, font=label_txt)
            self.is_hod_label.grid(row=9, column=1, sticky='w')
            cursor.execute("SELECT is_hod FROM faculty WHERE user_id = %s", (user_info[11],))
            current_post = cursor.fetchone()
            self.is_hod_entry = Entry(self.edit_window, bg=txt, fg=background, font=entry_txt)
            self.is_hod_entry.insert(0, current_post[0])
            self.is_hod_entry.grid(row=9, column=3, sticky='w')

            # subject
            cursor.execute("SELECT name FROM subject WHERE subject_id = %s", (user_info[9],))
            subject = cursor.fetchone()
            self.subject_label = Label(self.edit_window, text="Subject: ", bg=background, fg=txt, font=label_txt)
            self.subject_label.grid(row=10, column=1, sticky='w')
            self.subject_value = Label(self.edit_window, text=subject[0], bg=background, fg=txt, font=label_txt)
            self.subject_value.grid(row=10, column=3, sticky='w')
            # userId
            self.id_label = Label(self.edit_window, text='User_id: ', bg=background, fg=txt, font=label_txt)
            self.id_label.grid(row=11, column=1, sticky='w')

            self.id = Label(self.edit_window, text=user_info[11], bg=background, fg=txt, font=label_txt)
            self.id.grid(row=11, column=3, sticky='w')
            # password
            self.forgot_passwd = Label(self.edit_window, text='Forgot Password?', bg=background, fg=txt, font=label_txt)
            self.forgot_passwd.grid(row=12, column=1, sticky='w')

            self.restore_passwd_btn = Button(self.edit_window, text='Restore system password.', font=label_txt,
                                             bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                             command=lambda: self.restore_passwd(user_info, master_frame))
            self.restore_passwd_btn.grid(row=12, column=3, sticky='w')
            # delete record button
            self.delete_record = Button(self.edit_window, text='Delete record', font=label_txt,
                                        bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                        command=lambda: delete_record(master_frame))
            self.delete_record.grid(row=0, column=5, sticky='w')
        elif master_frame == self.edit_management_frame:
            # post
            self.post_lbl = Label(self.edit_window, text='Post:', bg=background, fg=txt, font=label_txt)
            self.post_lbl.grid(row=9, column=1, sticky='w')
            self.post_val = Label(self.edit_window, text=user_info[9], bg=background, fg=txt, font=label_txt)
            self.post_val.grid(row=9, column=3, sticky='w')
            # user_id
            self.id_label = Label(self.edit_window, text='User_id: ', bg=background, fg=txt, font=label_txt)
            self.id_label.grid(row=10, column=1, sticky='w')
            self.id = Label(self.edit_window, text=user_info[10], bg=background, fg=txt, font=label_txt)
            self.id.grid(row=10, column=3, sticky='w')
            # password
            self.forgot_passwd = Label(self.edit_window, text='Forgot Password?', bg=background, fg=txt, font=label_txt)
            self.forgot_passwd.grid(row=11, column=1, sticky='w')

            self.restore_passwd_btn = Button(self.edit_window, text='Restore system password.', font=label_txt,
                                             bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                             command=lambda: self.restore_passwd(user_info, master_frame))
            self.restore_passwd_btn.grid(row=11, column=3, sticky='w')

        self.save_changes_btn = Button(self.edit_window, text='Save changes', font=label_txt,
                                       bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                       command=lambda: save_changes(master_frame))
        self.save_changes_btn.grid(row=16, column=2)

    def restore_passwd(self, user_info, master_frame):
        self.gen_passwd = user_info[1] + str(user_info[0])
        enc = Encoder(self.gen_passwd)
        if master_frame == self.edit_students_frame:
            cursor.execute('UPDATE student SET passwd = %s, key_val = %s WHERE id = %s',
                           (enc.encoded_passwd, enc.key, user_info[0]))
        elif master_frame == self.edit_teachers_frame:
            cursor.execute('UPDATE faculty SET passwd = %s, key_val = %s WHERE id = %s',
                           (enc.encoded_passwd, enc.key, user_info[0]))
        elif master_frame == self.edit_management_frame:
            cursor.execute('UPDATE management SET passwd = %s, key_val = %s WHERE id = %s',
                           (enc.encoded_passwd, enc.key, user_info[0]))

        jr_college_db.commit()
        messagebox.showinfo('Reset successful', f'Your password has been successfully reset to: {self.gen_passwd}')

    def add_new(self, master_frame):
        add_window = Toplevel()
        add_window.geometry('570x400')
        add_window.config(bg=background)
        if master_frame == self.edit_students_frame:
            add_window.title('Add new student')
            New_student(add_window)
        elif master_frame == self.edit_teachers_frame:
            add_window.title('Add new faculty')
            New_faculty(add_window)

    def birth_date_picker(self):
        global date_picker
        date_picker = Toplevel()
        date_picker.title("Birth Date Picker")
        date_picker.geometry("300x250")
        date_picker.config(bg=background)
        global cal
        cal = Calendar(date_picker, selectmode="day", date_pattern='y-mm-dd', font=label_txt,
                       background=panels, foreground=txt)
        cal.pack()

        grab_date_button = Button(date_picker, text="Pick Date", font=label_txt,
                                  bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                  command=self.grab_date)
        grab_date_button.pack()

    def grab_date(self):
        self.date_of_birth_entry.delete(0, END)
        self.date_of_birth_entry.insert(0, cal.get_date())
        date_picker.destroy()


# A page to add new student
class New_student:

    def __init__(self, root):
        # Add a new student page
        self.new_student_frame = Frame(root, bg=background)
        self.new_student_frame.pack(anchor="center", fill=BOTH, expand=1)

        # Title
        self.new_student_title = Label(self.new_student_frame, text="New Student", bg=background, fg=btns,
                                       font=page_txt)
        self.new_student_title.grid(row=0, column=0, columnspan=5)

        # First name
        self.first_name_label = Label(self.new_student_frame, text="First name: ", bg=background, fg=txt,
                                      font=label_txt)
        self.first_name_label.grid(row=1, column=1, sticky='w')

        self.first_name_entry = Entry(self.new_student_frame, bg=txt, fg=background, font=entry_txt)
        self.first_name_entry.grid(row=1, column=3, sticky='w')

        # Last name
        self.last_name_label = Label(self.new_student_frame, text="Last name: ", bg=background, fg=txt, font=label_txt)
        self.last_name_label.grid(row=2, column=1, sticky='w')

        self.last_name_entry = Entry(self.new_student_frame, bg=txt, fg=background, font=entry_txt)
        self.last_name_entry.grid(row=2, column=3, sticky='w')

        # Date of Birth
        self.date_of_birth = Label(self.new_student_frame, text="Date of Birth", bg=background, fg=txt, font=label_txt)
        self.date_of_birth.grid(row=3, column=1, sticky='w')
        self.date_of_birth_entry = Entry(self.new_student_frame, bg=txt, fg=background, font=entry_txt)
        self.date_of_birth_entry.insert(0, "(yyyy-mm-dd)")
        self.date_of_birth_entry.grid(row=3, column=3, sticky='w')
        self.dob_selector_button = Button(self.new_student_frame, text="Select Birth Date", font=label_txt,
                                          bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                          command=self.birth_date_picker)
        self.dob_selector_button.grid(row=3, column=4, sticky='w')

        # Gender
        self.gender_label = Label(self.new_student_frame, text="Gender: ", bg=background, fg=txt, font=label_txt)
        self.gender_label.grid(row=4, column=1, sticky='w')

        self.gender_picker = ttk.Combobox(self.new_student_frame)
        self.gender_picker['values'] = ("Non-binary", "Female", "Male")
        self.gender_picker.config(background=txt, foreground=background, font=entry_txt)
        self.gender_picker.grid(row=4, column=3, sticky='w')
        self.gender_picker.current(0)

        # Email id
        self.email_label = Label(self.new_student_frame, text="Email ID: ", bg=background, fg=txt, font=label_txt)
        self.email_label.grid(row=5, column=1, sticky='w')

        self.email_entry = Entry(self.new_student_frame, bg=txt, fg=background, font=entry_txt)
        self.email_entry.grid(row=5, column=3, sticky='w')

        # phone number
        self.phone_number_label = Label(self.new_student_frame, text="Phone number: ", bg=background, fg=txt,
                                        font=label_txt)
        self.phone_number_label.grid(row=6, column=1, sticky='w')

        self.phone_number_entry = Entry(self.new_student_frame, bg=txt, fg=background, font=entry_txt)
        self.phone_number_entry.grid(row=6, column=3, sticky='w')

        # Address
        self.address_label = Label(self.new_student_frame, text="Address :", bg=background, fg=txt, font=label_txt)
        self.address_label.grid(row=7, column=1, sticky='w')

        self.address_text_scroll = Scrollbar(self.new_student_frame)
        self.address_text_scroll.grid(row=7, column=4, sticky='w')
        self.address_text = Text(self.new_student_frame, height=2, width=20, bg=txt, fg=background, font=text_txt)
        self.address_text.grid(row=7, column=3, sticky='w')
        self.address_text_scroll.config(command=self.address_text.yview)
        self.address_text.config(yscrollcommand=self.address_text_scroll.set)

        # Pincode
        self.pincode_label = Label(self.new_student_frame, text="Pincode :", bg=background, fg=txt, font=label_txt)
        self.pincode_label.grid(row=8, column=1, sticky='w')

        self.pincode_entry = Entry(self.new_student_frame, bg=txt, fg=background, font=entry_txt)
        self.pincode_entry.grid(row=8, column=3, sticky='w')

        # Standard
        self.standard = Label(self.new_student_frame, text="Standard: ", bg=background, fg=txt, font=label_txt)
        self.standard.grid(row=9, column=1, sticky='w')

        self.standard_picker = ttk.Combobox(self.new_student_frame)
        self.standard_picker['values'] = ('XI', 'XII')
        self.standard_picker.config(background=txt, foreground=background, font=entry_txt)
        self.standard_picker.grid(row=9, column=3, sticky='w')
        self.standard_picker.current(0)

        # stream
        self.stream_name = Label(self.new_student_frame, text="Stream: ", bg=background, fg=txt, font=label_txt)
        self.stream_name.grid(row=10, column=1, sticky='w')

        self.stream_name_picker = ttk.Combobox(self.new_student_frame)
        self.stream_name_picker['values'] = ("Science", "Commerce", "Arts", "Voc. Science")
        self.stream_name_picker.config(background=txt, foreground=background, font=entry_txt)
        self.stream_name_picker.grid(row=10, column=3, sticky='w')
        self.stream_name_picker.current(0)

        # Submit button
        self.enter_data_btn = Button(self.new_student_frame, text="Enter data", font=label_txt,
                                     bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                     command=self.enter_data)
        self.enter_data_btn.grid(row=12, column=2, sticky='w')

    def birth_date_picker(self):
        global date_picker
        date_picker = Toplevel()
        date_picker.title("Birth Date Picker")
        date_picker.geometry("300x250")
        global cal
        cal = Calendar(date_picker, selectmode="day", date_pattern='y-mm-dd')
        cal.pack()

        grab_date_button = Button(date_picker, text="Pick Date", command=self.grab_date)
        grab_date_button.pack()

    def grab_date(self):
        self.date_of_birth_entry.delete(0, END)
        self.date_of_birth_entry.insert(0, cal.get_date())
        date_picker.destroy()

    def enter_data(self):
        # variables to hold userid and password
        self.gen_id = StringVar()
        self.gen_passwd = StringVar()
        admission_date = date.today().strftime('%Y-%m-%d')
        batch = admission_date[:4]
        error_generated = False

        try:
            # Entering the data in database
            sql_command = '''INSERT INTO student(first_name, 
                                                 last_name, 
                                                 dob, 
                                                 gender,
                                                 email,
                                                 phone_number, 
                                                 address, 
                                                 pincode, 
                                                 stream_name, 
                                                 user_id,
                                                 passwd, 
                                                 standard, 
                                                 date_of_admission) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            values = (self.first_name_entry.get(),
                      self.last_name_entry.get(),
                      self.date_of_birth_entry.get(),
                      self.gender_picker.get(),
                      self.email_entry.get(),
                      self.phone_number_entry.get(),
                      self.address_text.get(1.0, END).strip(),
                      self.pincode_entry.get(),
                      self.stream_name_picker.get(),
                      self.gen_id.get(),
                      self.gen_passwd.get(),
                      self.standard_picker.get(),
                      admission_date)
            cursor.execute(sql_command, values)
        except mysql.connector.errors.IntegrityError:
            error_generated = True
            messagebox.showerror('Error', 'The entered Email address is already registered for another student!')

        except mysql.connector.errors.DataError:
            error_generated = True
            messagebox.showerror('Error', 'The data in Date of birth field is incorrect!!')

        if not error_generated:
            # Committing changes
            jr_college_db.commit()

            # Generating userID and password
            cursor.execute("SELECT `id` from `student` WHERE email = %s ", (self.email_entry.get(),))
            primary_id = cursor.fetchone()
            self.gen_id.set('s' + str(primary_id[0]) + batch)
            self.gen_passwd.set(self.first_name_entry.get() + str(primary_id[0]))
            enc = Encoder(self.gen_passwd.get())

            # updating database
            cursor.execute("UPDATE student SET user_id = %s, passwd = %s, key_val = %s WHERE id = %s",
                           (self.gen_id.get(), enc.encoded_passwd, enc.key, primary_id[0]))
            jr_college_db.commit()

            # Clearing screen
            self.first_name_entry.delete(0, END)
            self.last_name_entry.delete(0, END)
            self.date_of_birth_entry.delete(0, END)
            self.date_of_birth_entry.insert(0, 'yyyy-mm-dd')
            self.gender_picker.current(0)
            self.email_entry.delete(0, END)
            self.phone_number_entry.delete(0, END)
            self.address_text.delete(1.0, END)
            self.pincode_entry.delete(0, END)
            self.stream_name_picker.current(0)
            self.standard_picker.current(0)

            # A window to show user_id and password
            self.new_stud_gen = Toplevel()
            self.new_stud_gen.geometry("300x200")
            self.new_stud_gen.title("Data entered successfully!")

            # Prompt
            self.prompt = Label(self.new_stud_gen,
                                text='Data entered successfully.\nPlease note down the userID and password.')
            self.prompt.grid(row=0, column=0, columnspan=5)

            # UserID
            self.student_user_id = Label(self.new_stud_gen, text='User ID: ')
            self.student_user_id.grid(row=1, column=1, sticky='w')

            self.student_user_id_value = Label(self.new_stud_gen, text=self.gen_id.get())
            self.student_user_id_value.grid(row=1, column=3)

            # Password
            self.passwd = Label(self.new_stud_gen, text="Password: ")
            self.passwd.grid(row=2, column=1, sticky='w')

            self.passwd_value = Label(self.new_stud_gen, text=self.gen_passwd.get())
            self.passwd_value.grid(row=2, column=3)

            # Done button
            self.done_btn = Button(self.new_stud_gen, text='Done', command=self.new_stud_gen.destroy)
            self.done_btn.grid(row=3, column=2)


# A page to add new faculty
class New_faculty:

    def __init__(self, root):
        # Add a new student page
        self.new_faculty_frame = Frame(root, bg=background)
        self.new_faculty_frame.pack(anchor="center")

        # Title
        self.new_faculty_title = Label(self.new_faculty_frame, text="New Faculty", bg=background, fg=btns,
                                       font=page_txt)
        self.new_faculty_title.grid(row=0, column=0, columnspan=5)

        # First name
        self.first_name_label = Label(self.new_faculty_frame, text="First name: ", bg=background, fg=txt,
                                      font=label_txt)
        self.first_name_label.grid(row=1, column=1, sticky='w')

        self.first_name_entry = Entry(self.new_faculty_frame, bg=txt, fg=background, font=entry_txt)
        self.first_name_entry.grid(row=1, column=3, sticky='w')

        # Last name
        self.last_name_label = Label(self.new_faculty_frame, text="Last name: ", bg=background, fg=txt, font=label_txt)
        self.last_name_label.grid(row=2, column=1, sticky='w')

        self.last_name_entry = Entry(self.new_faculty_frame, bg=txt, fg=background, font=entry_txt)
        self.last_name_entry.grid(row=2, column=3, sticky='w')

        # Date of Birth
        self.date_of_birth = Label(self.new_faculty_frame, text="Date of Birth", bg=background, fg=txt, font=label_txt)
        self.date_of_birth.grid(row=3, column=1, sticky='w')
        self.date_of_birth_entry = Entry(self.new_faculty_frame, bg=txt, fg=background, font=entry_txt)
        self.date_of_birth_entry.insert(0, "(yyyy-mm-dd)")
        self.date_of_birth_entry.grid(row=3, column=3, sticky='w')
        self.dob_selector_button = Button(self.new_faculty_frame, text="Select Birth Date", font=label_txt,
                                          bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                          command=self.birth_date_picker)
        self.dob_selector_button.grid(row=3, column=4, sticky='w')

        # Gender
        self.gender_label = Label(self.new_faculty_frame, text="Gender: ", bg=background, fg=txt, font=label_txt)
        self.gender_label.grid(row=4, column=1, sticky='w')

        self.gender_picker = ttk.Combobox(self.new_faculty_frame)
        self.gender_picker['values'] = ("Non-binary", "Female", "Male")
        self.gender_picker.config(background=txt, foreground=background, font=entry_txt)
        self.gender_picker.grid(row=4, column=3, sticky='w')
        self.gender_picker.current(0)

        # Email id
        self.email_label = Label(self.new_faculty_frame, text="Email ID: ", bg=background, fg=txt, font=label_txt)
        self.email_label.grid(row=5, column=1, sticky='w')

        self.email_entry = Entry(self.new_faculty_frame, bg=txt, fg=background, font=entry_txt)
        self.email_entry.grid(row=5, column=3, sticky='w')

        # phone number
        self.phone_number_label = Label(self.new_faculty_frame, text="Phone number: ", bg=background, fg=txt,
                                        font=label_txt)
        self.phone_number_label.grid(row=6, column=1, sticky='w')

        self.phone_number_entry = Entry(self.new_faculty_frame, bg=txt, fg=background, font=entry_txt)
        self.phone_number_entry.grid(row=6, column=3, sticky='w')

        # Address
        self.address_label = Label(self.new_faculty_frame, text="Address :", bg=background, fg=txt, font=label_txt)
        self.address_label.grid(row=7, column=1, sticky='w')

        self.address_text_scroll = Scrollbar(self.new_faculty_frame)
        self.address_text_scroll.grid(row=7, column=4, sticky='w')
        self.address_text = Text(self.new_faculty_frame, height=2, width=20, bg=txt, fg=background, font=text_txt)
        self.address_text.grid(row=7, column=3, sticky='w')
        self.address_text_scroll.config(command=self.address_text.yview)
        self.address_text.config(yscrollcommand=self.address_text_scroll.set)

        # Pincode
        self.pincode_label = Label(self.new_faculty_frame, text="Pincode :", bg=background, fg=txt, font=label_txt)
        self.pincode_label.grid(row=8, column=1, sticky='w')

        self.pincode_entry = Entry(self.new_faculty_frame, bg=txt, fg=background, font=entry_txt)
        self.pincode_entry.grid(row=8, column=3, sticky='w')

        # Subject
        self.subject = Label(self.new_faculty_frame, text='Subject', bg=background, fg=txt, font=label_txt)
        self.subject.grid(row=9, column=1, sticky='w')

        cursor.execute('SELECT DISTINCT name FROM subject')
        subjects = cursor.fetchall()
        list_of_sub = []
        for sub in subjects:
            list_of_sub.append(sub[0])
        self.subject_picker = ttk.Combobox(self.new_faculty_frame)
        self.subject_picker['values'] = tuple(list_of_sub)
        self.subject_picker.config(background=txt, foreground=background, font=entry_txt)
        self.subject_picker.grid(row=9, column=3, sticky='w')
        self.subject_picker.current(0)

        # Submit button
        self.enter_data_btn = Button(self.new_faculty_frame, text="Enter data", font=label_txt,
                                     bg=btns, fg=background, activebackground=panels, activeforeground=txt,
                                     command=self.enter_data)
        self.enter_data_btn.grid(row=10, column=2, sticky='w')

    def birth_date_picker(self):
        global date_picker
        date_picker = Toplevel()
        date_picker.title("Birth Date Picker")
        date_picker.geometry("300x250")
        global cal
        cal = Calendar(date_picker, selectmode="day", date_pattern='y-mm-dd')
        cal.pack()

        grab_date_button = Button(date_picker, text="Pick Date", command=self.grab_date)
        grab_date_button.pack()

    def grab_date(self):
        self.date_of_birth_entry.delete(0, END)
        self.date_of_birth_entry.insert(0, cal.get_date())
        date_picker.destroy()

    def enter_data(self):
        # variables to hold userid and password
        self.gen_id = StringVar()
        self.gen_passwd = StringVar()
        birth_year = str(self.date_of_birth_entry.get())[:4]
        error_generated = False
        # extracting subject id to store in database
        cursor.execute('SELECT subject_id FROM subject WHERE name = %s', (self.subject_picker.get(),))
        sub_id = cursor.fetchone()
        try:
            # Entering the data in database
            sql_command = '''INSERT INTO faculty(first_name, 
                                                 last_name, 
                                                 dob, 
                                                 gender,
                                                 email,
                                                 phone_number, 
                                                 address, 
                                                 pincode, 
                                                 subject_id, 
                                                 user_id,
                                                 passwd) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            values = (self.first_name_entry.get(),
                      self.last_name_entry.get(),
                      self.date_of_birth_entry.get(),
                      self.gender_picker.get(),
                      self.email_entry.get(),
                      self.phone_number_entry.get(),
                      self.address_text.get(1.0, END).strip(),
                      self.pincode_entry.get(),
                      sub_id[0],
                      self.gen_id.get(),
                      self.gen_passwd.get())
            cursor.execute(sql_command, values)
        except mysql.connector.errors.IntegrityError:
            error_generated = True
            messagebox.showerror('Error', 'The entered Email address is already registered for another faculty!')

        except mysql.connector.errors.DataError:
            error_generated = True
            messagebox.showerror('Error', 'The data in Date of birth field is incorrect!!')

        if not error_generated:
            # Committing changes
            jr_college_db.commit()

            # Generating userID and password
            cursor.execute("SELECT `id` from `faculty` WHERE email = %s ", (self.email_entry.get(),))
            primary_id = cursor.fetchone()
            self.gen_id.set('f' + str(primary_id[0]) + birth_year)
            self.gen_passwd.set(self.first_name_entry.get() + str(primary_id[0]))
            enc = Encoder(self.gen_passwd.get())

            # updating database
            cursor.execute("UPDATE faculty SET user_id = %s, passwd = %s, key_val = %s WHERE id = %s",
                           (self.gen_id.get(), enc.encoded_passwd, enc.key, primary_id[0]))
            jr_college_db.commit()

            # Clearing screen
            self.first_name_entry.delete(0, END)
            self.last_name_entry.delete(0, END)
            self.date_of_birth_entry.delete(0, END)
            self.date_of_birth_entry.insert(0, 'yyyy-mm-dd')
            self.gender_picker.current(0)
            self.email_entry.delete(0, END)
            self.phone_number_entry.delete(0, END)
            self.address_text.delete(1.0, END)
            self.pincode_entry.delete(0, END)
            self.subject_picker.current(0)

            # A window to show user_id and password
            self.new_faculty_gen = Toplevel()
            self.new_faculty_gen.geometry("300x200")
            self.new_faculty_gen.title("Data entered successfully!")

            # Prompt
            self.prompt = Label(self.new_faculty_gen,
                                text='Data entered successfully.\nPlease note down the userID and password.')
            self.prompt.grid(row=0, column=0, columnspan=5)

            # UserID
            self.user_id = Label(self.new_faculty_gen, text='User ID: ')
            self.user_id.grid(row=1, column=1, sticky='w')

            self.user_id_value = Label(self.new_faculty_gen, text=self.gen_id.get())
            self.user_id_value.grid(row=1, column=3)

            # Password
            self.passwd = Label(self.new_faculty_gen, text="Password: ")
            self.passwd.grid(row=2, column=1, sticky='w')

            self.passwd_value = Label(self.new_faculty_gen, text=self.gen_passwd.get())
            self.passwd_value.grid(row=2, column=3)

            # Done button
            self.done_btn = Button(self.new_faculty_gen, text='Done', command=self.new_faculty_gen.destroy)
            self.done_btn.grid(row=3, column=2)


if __name__ == '__main__':
    # Creating main window
    root_window = Tk()
    root_window.title("Junior college")
    root_window.geometry("500x300")
    root_window.configure(bg=background)
    change_theme_btn = Button(root_window, text="Change Theme", bg=panels, fg=txt, font=label_txt,
                              activebackground=btns,
                              activeforeground=txt, command=change_theme)
    change_theme_btn.pack(anchor=NE)

    login = Log_in(root_window)
    root_window.mainloop()

# Closing database connections
cursor.close()
jr_college_db.close()
jr_college_db.disconnect()
