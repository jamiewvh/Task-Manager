#=====importing libraries===========
from datetime import date
from datetime import datetime
import os.path

# defining functions


# user register function
def reg_user():
    done = False
    while not done:
        same_name = False
        new_username = input("Please enter the new user's username:")
        with open("user.txt", "r") as f:
            for line in f:
                if new_username == line.split(", ")[0]:
                    same_name = True
                    print("User already exists. Please try again.")
        if same_name:
            continue
        new_user_pass = input("Please enter the new user's password:")
        new_pass_check = input("Please confirm the new user's password:")
        if new_user_pass == new_pass_check:
            with open("user.txt","a") as f:
                f.write("\n" + new_username + ", " + new_user_pass)
            done = True
        else:
            print(
"The entered passwords do not match. Please try again.")


# task adding function
def add_task():
    task_user = input("Please enter the username of the task assignee:")
    task_title = input("Please enter the title of the task:")
    task_desc = input("Please enter a description of the task:")
    task_date = input('''Please enter the due date of the task
in the format DD Mon YYYY, e.g. 03 Feb 2025:''')
    today_date = date.today().strftime("%d %b %Y")
    with open("tasks.txt", "a") as f:
        f.write(
f"\n{task_user}, {task_title}, {task_desc}, {today_date}, {task_date}, No")


# task viewing function
def view_all():
    with open("tasks.txt","r") as f:
        for line in f:
            print(f'''
_______________________________________________________________________________

Task:                   {line.split(", ")[1]}
Assigned to:            {line.split(", ")[0]}
Date assigned:          {line.split(", ")[3]}
Due date:               {line.split(", ")[4]}
Task complete?          {line.split(", ")[5]}
Task description:       
    {line.split(", ")[2]}
_______________________________________________________________________________
''')


# personal task viewing function
def view_mine():
    i = 0
    with open("tasks.txt","r") as f:
        for line in f:
            if line.split(", ")[0] == username:
                i += 1
                print(f'''
_______________________________________________________________________________

Task:                   {line.split(", ")[1]}
Task No.:               {i}
Assigned to:            {line.split(", ")[0]}
Date assigned:          {line.split(", ")[3]}
Due date:               {line.split(", ")[4]}
Task complete?          {line.split(", ")[5]}
Task description:       
    {line.split(", ")[2]}
_______________________________________________________________________________
''')
# task selection
    task_menu = int(input('''
Select a specific task by entering its number,
or select -1 to return to main menu.
: '''))
    if task_menu == -1:
        return

# mark as complete or edit
    else:
        sub_menu = input(
f'''You have selected task {task_menu}.
c - mark this task as complete
e - edit this task
''').lower()

# read file
    contents = []
    with open("tasks.txt", "r") as f:
        for line in f:
            contents.append(line)
# change no to yes
    if sub_menu == "c":
        for line in contents:
            if contents[task_menu-1] == line:
                new_line = line.replace("No", "Yes")
                contents[task_menu-1] = new_line
        with open("tasks.txt", "w") as f:
            for line in contents:
                f.write(line)
        print(f"Task {task_menu} marked complete.")
# editing menu
    elif sub_menu == "e":
        edit_menu = input('''
Would you like to edit the username or the due date?
u - edit username
d - edit due date
''')
# change username
        if edit_menu == "u":
            replacement_u = input("Enter a new user for the task:")
            for line in contents:
                if contents[task_menu-1] == line:
                    new_line = line.replace(line.split(", ")[0], replacement_u)
                    contents[task_menu-1] = new_line
            with open("tasks.txt", "w") as f:
                for line in contents:
                    f.write(line)
            print("Username changed.")
# change due date
        elif edit_menu == "d":
            i = 0
            replacement_d = input('''Enter a new due date for the task
in the format DD Mon YYYY, e.g. 03 Feb 2025::''')
            for line in contents:
                if contents[task_menu-1] == line:
                    new_line = line.replace(line.split(", ")[4], replacement_d)
                    contents[task_menu-1] = new_line
            with open("tasks.txt", "w") as f:
                for line in contents:
                    f.write(line)
            print("Due date changed.")


# statistics function
def show_stats():
    # check for files
    if (os.path.isfile("task_overview.txt") == False
    or os.path.isfile("user_overview.txt") == False):
        gen_reports()
    # read files
    t_over_cont = ''
    u_over_cont = ''
    with open("task_overview.txt", "r") as f:
        for line in f:
                t_over_cont += line
    with open("user_overview.txt","r") as f:
        for line in f:
                u_over_cont += line
    print(f'''
    Task Overview:
    {t_over_cont}
    
    User Overview:
    {u_over_cont}''')


# generate reports
def gen_reports():
    # read file data
    task_contents = []
    with open("tasks.txt","r") as f:
        for line in f:
            task_contents.append(line)
    user_contents = []
    with open("user.txt","r") as f:
        for line in f:
            user_contents.append(line)
    complete_tasks = 0
    overdue_tasks = 0
    for task in task_contents:
        if task.split(", ")[5] == "Yes\n":
            complete_tasks += 1    
    for task in task_contents:
        if task.split(", ")[5] == "No\n":
            if (
datetime.strptime(task.split(", ")[4], "%d %b %Y") < datetime.now()):
                overdue_tasks += 1
    # number of incomplete tasks
    incomplete_tasks = len(task_contents)-complete_tasks
    # write task info to file
    with open("task_overview.txt","w") as f:
        try:
            f.write(f'''
Total number of tasks: {len(task_contents)}
Complete tasks: {complete_tasks}
Incomplete tasks: {incomplete_tasks}
Overdue tasks: {overdue_tasks}
Percentage tasks incomplete: {(incomplete_tasks/len(task_contents))*100}%
Percentage tasks overdue: {(overdue_tasks/len(task_contents))*100}%
''')
        except ZeroDivisionError:
            print("You must add tasks before generating reports.")

    # write user info to file
    with open("user_overview.txt","w") as f:
        f.write(f'''
Number of registered users: {len(user_contents)}
Total number of tasks: {len(task_contents)}
''')
        for user in user_contents:
            num_tasks = 0
            comp_tasks = 0
            over_tasks = 0
            for task in task_contents:
                if task.split(", ")[0] == user.split(", ")[0]:
                    num_tasks += 1
                    if task.split(", ")[5] == "Yes\n":
                        comp_tasks += 1
                    if task.split(", ")[5] == "No\n":
                        if (
datetime.strptime(task.split(", ")[4], "%d %b %Y") < datetime.now()):
                            over_tasks += 1
            try:
                f.write(f'''
User: {user.split(", ")[0]}
Percentage of all tasks: {(num_tasks/len(task_contents))*100}%
Percentage of tasks completed: {(comp_tasks/num_tasks)*100}%
Percentage of tasks incomplete: {100-(comp_tasks/num_tasks)*100}%
Percentage of tasks overdue: {(over_tasks/num_tasks)*100}%

''')
            except ZeroDivisionError:
                print("You must add tasks before generating reports.")


# user login
authorised = False
while not authorised:
    username = input("Please enter your username:")
    password = input("Please enter your password:")
    with open("user.txt", "r") as f:
        for line in f:
            if (username == line.split(",")[0].strip()
            and password == line.split(",")[1].strip()):
                authorised = True
    if authorised == False:
        print('''
You have not entered an authorised username and password.
Please try again.
''')

while True:
    #presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    menu = input('''Select one of the following Options below:
r - registering a user
a - adding a task
va - View all tasks
vm - view my task
gr - generate reports
ds - display statistics
e - exit
: ''').lower()

    # registering a user
    if menu == 'r'and username == "admin":
        reg_user()

    elif menu == 'r':
        print("Only an administrator may register new users.")

    # adding a task
    elif menu == 'a':
        add_task()
        
    # displaying all tasks
    elif menu == 'va':
        view_all()

    # displaying user's tasks
    elif menu == 'vm':
        view_mine()
        
    # displaying statistics
    elif menu == 'ds' and username == "admin":
        show_stats()
        
    elif menu == 'ds':
        print("Only an administrator may view statistics.")
    
    # generating reports
    elif menu == 'gr':
        gen_reports()

    # exit
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    # error
    else:
        print("You have made a wrong choice, Please try again")