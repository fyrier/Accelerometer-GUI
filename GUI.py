from Tkinter import *
import os.path
from chronoslib import *
import time
import threading
import ctypes
import os
import operator

addUser = None
recognizeUser = None
global_frame = None
common_box = None
v0 = Tk()


class User(object):
    """A user from the user recognition system. Users have the
        following properties:

        Attributes:
            ID: A string representing the user's identification.
            age: A integer with the user's age.
            gender: A string with the user's gender.
            fitness: An integer with the user fitness (values from 1 to 5).
        """

    def __init__(self, ID):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        self.ID = ID
        self.age = 0
        self.gender = 'none'
        self.fitness = 1

    def getID(self):
        return self.ID

    def getAge(self):
        return self.age

    def getGender(self):
        return self.gender

    def getFitness(self):
        return self.fitness

    def setID(self, ID):
        self.ID = ID

    def setAge(self, age):
        self.age = age

    def setGender(self, gender):
        self.gender = gender

    def setFitness(self, fitness):
        self.fitness = fitness

    def addUser(self, ID, age, gender, fitness):
        self.ID = ID
        self.age = age
        self.gender = gender
        self.fitness = fitness


class Activity(object):
    """Activities that are recognised by the system. Activities have the
                following properties:

                Attributes:
                    ID: An int indicating the algorithm name.
                    name: A string indicating the activity name.
                    train_time: an int indicating the needed training time for the activity.
                """

    def __init__(self, ID, name, train_time):
        self.ID = ID
        self.name = name
        self.train_time = train_time

    def setID(self, ID):
        self.ID = ID

    def setName(self, name):
        self.name = name

    def setTrain_time(self, train_time):
        self.train_time = train_time

    def getID(self):
        return self.ID

    def getName(self):
        return self.name

    def getTrain_time(self):
        return self.train_time


class Model(object):
    """Machine learning model to recognize users. Models have the
            following properties:

            Attributes:
                algorithm: A string indicating the algorithm name.
                parameters: A integer vector with the algorithm parameters.
                users: An User vector with the users that the model can recognize.
                activities: An Activity vector with the activities that the model can recognize.
            """

    def __init__(self, algorithm, parameters):
        self.algorithm = algorithm
        self.parameters = parameters
        self.users = []
        self.activities = []

    def setAlgorithm(self, algorithm):
        self.algorithm = algorithm

    def setParameters(self, parameters):
        self.parameters = parameters

    def setUsers(self, users):
        self.users = users

    def setActivities(self, activities):
        self.activities = activities

    def addUser(self, user):
        self.users.append(user)

    def addActivity(self, activity):
        self.activities.append(activity)

    def getAlgorithm(self):
        return self.algorithm

    def getParameters(self):
        return self.parameters

    def getUsers(self):
        return self.users

    def getActivities(self):
        return self.activities


class ACCData(object):
    """ACC information from the smartwatch. ACCData has the
                following properties:

                Attributes:
                    x: A string indicating the algorithm name.
                    y: A integer vector with the algorithm parameters.
                    z: An User vector with the users that the model can recognize.
                """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z


def terminate_thread(thread):
    """Terminates a python thread from another thread.

    :param thread: a threading.Thread instance
    """
    if thread is None or not thread.isAlive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def keep_flat(event):       # on click,
    if event.widget is addUser or event.widget is recognizeUser:  # if the click came from the button
        event.widget.config(relief=FLAT)  # enforce an option


def train(information, but):
    global common_box
    global model
    global global_frame
    global v0

    user = User(len(model.getUsers()))
    model.addUser(user)

    # Check if there is a data file to create the classifier
    with open('data.arff', 'r') as input_file, open('data.csv', 'a+') as output_file:
        users = '{'

        for x in range(0, len(model.getUsers())):
            users += str(x) + ','

        users = users[:-1]
        old_users = users[:-2]
        old_users += '}'
        users += '}'

        if os.stat(input_file.name).st_size == 0:
            activities = '{'
            for x in range(0, len(model.getActivities())):
                activities += str(x) + ','

            activities = activities[:-1]
            activities += '}'
            output_file.write(
               '@relation \'Accelerometer: -C 2\'\n\n@attribute activity- ' + activities + '\n@attribute user- ' + users + '\n@attribute x numeric\n@attribute y numeric\n@attribute z numeric\n\n@data\n')
        else:
            for line in input_file:
                if line == ('@attribute user- ' + old_users + '\n'):
                    output_file.write('@attribute user- ' + users + '\n')
                else:
                    output_file.write(line)

        # Start to record data for each activity
        fd = port_open()
        start_ap(fd)

        ide = user.getID()
        for x in model.getActivities():
            # Get activity x data
            info = "Training period for activity " + str(x.getID()) + " (" + x.getName() + ") started. \nPlease, perform this action for " + str(x.getTrain_time()) + " seconds."
            information.config(text=info)
            t_end = time.time() + x.getTrain_time()
            while time.time() < t_end:
                r = get_acc_data(fd)
                if r:
                    output_file.write(str(x.getID()) + ',' + str(ide) + ',' + str(r[0]) + ',' + str(r[1]) + ',' + str(r[2]) + '\n')

        stop_ap(fd)

    info = "Training process completed. Please wait until the model is updated."
    information.config(text=info)

    # Train the system
    if os.path.isfile('./data.arff'):
        os.remove('./data.arff')

    os.rename('./data.csv', './data.arff')

    with open('./data.arff', 'a+') as f:
        os.system(
            'java -cp ".\meka-release-1.9.1\lib\*" meka.classifiers.multitarget.BCC -t ' + f.name +
            ' -X Ibf -S 0 -d BccJ48.model -R -W weka.classifiers.trees.J48 -- -C 0.1 -M 10')

    # Inform the user that the model has been updated to include them

    information.config(text='User added to the system.')
    but.config(text='Return')


def test(information, but):
    global common_box
    global model
    global global_frame
    global v0

    # Start data collection
    with open('./user_data.arff', 'w') as f:
        # Get the activities
        activities = '{'
        for x in range(0, len(model.getActivities())):
            activities += str(x) + ','

        activities = activities[:-1]
        activities += '}'

        # Get the users
        users = '{'

        for x in range(0, len(model.getUsers())):
            users += str(x) + ','

        users = users[:-1]
        users += '}'

        f.write('@relation \'Accelerometer: -C 2\'\n\n@attribute activity- ' + activities + '\n@attribute user- ' + users + '\n@attribute x numeric\n@attribute y numeric\n@attribute z numeric\n\n@data\n')

        # Get user data
        fd = port_open()
        start_ap(fd)
        t_end = time.time() + 30
        while time.time() < t_end:
            r = get_acc_data(fd)
            if r:
                f.write('?,?,' + str(r[0]) + ',' + str(r[1]) + ',' + str(r[2]) + '\n')

        stop_ap(fd)

    # Start user recognition
    with open('./user_data.arff', 'a+') as f:
        if os.stat(f.name).st_size != 0:
            os.system(
                'java -cp ".\meka-release-1.9.1\lib\*" meka.classifiers.multitarget.BCC -l BccJ48.model -t ' + f.name + ' -T ' + f.name + ' -predictions ./results.csv -no-eval')

    # Structure for act_res and us_res: [class, number of times class appears]
    act_res = {}
    us_res = {}
    total = 0
    # Calculate user results
    with open('./results.csv', 'r') as f:
        for line in f:
            if 'activity' in line:
                continue
            else:
                # activity-,user-,x,y,z: we use activity and user
                res = line.split(',')
                total += 1
                act = res[0]
                us = res[1]
                if not act_res:
                    act_res[act] = 1
                else:
                    if act in act_res:
                        act_res[act] = act_res.get(act) + 1
                    else:
                        act_res[act] = 1
                if not us_res:
                    us_res[us] = 1
                else:
                    if us in us_res:
                        us_res[us] = us_res.get(us) + 1
                    else:
                        us_res[us] = 1

    # Calculate the accuracy of the result
    # Activity:
    act = max(act_res.iteritems(), key=operator.itemgetter(1))[0]

    # User:
    us = max(us_res.iteritems(), key=operator.itemgetter(1))[0]

    act_stat = (act_res.get(act)*100) / total
    us_stat = (us_res.get(us)*100) / total

    act_name = ''

    for x in model.getActivities():
        if x.getID() == act:
            act_name = x.getName()

    information.config(text='culo')

    # Inform the user of the results
    info = 'Data belongs to user ' + str(us) + ' with a probability of ' + str(us_stat) + '%\n while ' + act_name + ' with a probability of ' + str(act_stat) + '%.'
    information.config(text=info)
    but.config(text='Return')


model = Model('J48', None)
train_thread = None
recognize_thread = None


def add():
    global global_frame
    global model
    global common_box
    global train_thread

    v0.configure(background='white')

    global_frame.destroy()
    global_frame = Frame(v0)
    global_frame.configure(background='white')

    text_frame = Frame(global_frame)

    text = Text(text_frame, bg="black", height=1.4, width=58, relief=FLAT)
    text.insert(INSERT, "User recognition > ")
    text.insert(END, "Add user")
    text.pack()
    text.tag_add("first", "1.0", "1.18")
    text.tag_add("second", "1.18", "1.28")
    text.tag_config("first", foreground="#8A8A8A")
    text.tag_config("second", foreground="white")
    text.configure(pady=8, padx=15)

    text_frame.pack(side=TOP, expand=NO, fill=NONE)

    common_box = Frame(global_frame)
    common_box.configure(background='white')

    # info = StringVar()
    info = "Initiating training period. Please, wait..."
    information = Label(common_box, text=info, pady=30, padx=30)
    information.configure(background="white")
    # info.set("Training period for activity 1 (resting) started. Please, wait...")
    information.pack()

    but_frame = Frame(common_box)
    but = Button(but_frame, text="Cancel", bg='#8A8A8A', fg='white', command=mainScreen, relief=FLAT, padx=5, pady=4)
    but.pack(side=LEFT, padx=10, pady=5)

    but_frame.configure(background='white')
    but_frame.pack(side=BOTTOM)

    v0.bind('<Button-3>', keep_flat)
    common_box.pack()

    global_frame.pack()

    # MEKA events
    train_thread = threading.Thread(target=train, args=[information, but])
    train_thread.start()

    v0.mainloop()


def recognize():
    global global_frame
    global model
    global recognize_thread

    v0.configure(background='white')

    global_frame.destroy()
    global_frame = Frame(v0)
    global_frame.configure(background='white')

    text_frame = Frame(global_frame)

    text = Text(text_frame, bg="black", height=1.4, width=58, relief=FLAT)
    text.insert(INSERT, "User recognition > ")
    text.insert(END, "Recognize user")
    text.pack()
    text.tag_add("first", "1.0", "1.18")
    text.tag_add("second", "1.18", "1.36")
    text.tag_config("first", foreground="#8A8A8A")
    text.tag_config("second", foreground="white")
    text.configure(pady=8, padx=15)

    text_frame.pack(side=TOP, expand=NO, fill=NONE)

    info = "Collecting user data. Please, stand by..."
    information = Label(global_frame, text=info, pady=30, padx=30)
    information.configure(background="white")
    information.pack()

    but_frame = Frame(global_frame)
    but = Button(but_frame, text="Cancel", bg='#8A8A8A', fg='white', command=mainScreen, relief=FLAT, padx=5,
                           pady=4)
    but.pack(side=LEFT, padx=10, pady=5)

    but_frame.configure(background='white')
    but_frame.pack(side=BOTTOM)

    v0.bind('<Button-4>', keep_flat)

    global_frame.pack()

    # MEKA events
    recognize_thread = threading.Thread(target=test, args=[information, but])
    recognize_thread.start()

    v0.mainloop()


def mainScreen():
    global addUser
    global recognizeUser
    global global_frame
    global v0
    global train_thread
    global recognize_thread

    terminate_thread(train_thread)
    terminate_thread(recognize_thread)

    v0.configure(background='white')
    v0.option_add("*Font", "TkDefaultFont")

    if global_frame is not None:
        global_frame.destroy()

    global_frame = Frame(v0)
    global_frame.configure(background='white')

    var = StringVar()
    label = Label(global_frame, textvariable=var, bg='black', fg='white', anchor="w", pady=8, padx=15)
    var.set("User recognition")
    label.pack(fill=BOTH, expand=1)

    info = StringVar()
    information = Label(global_frame, textvariable=info, pady=30, padx=30)
    information.configure(background="white")
    info.set("Choose \"Add user\" to incorporate a new user to the system. \n"
             "Choose \"Recognize user\" to identify a user that is already \nregistered on the system.")
    information.pack()

    but_frame = Frame(global_frame)

    addUser = Button(but_frame, text="Add user", command=add, bg='#8A8A8A', fg='white', relief=FLAT, padx=20, pady=4)
    addUser.pack(side=LEFT, padx=10, pady=5)

    recognizeUser = Button(but_frame, text="Recognize user", bg='white', command=recognize, relief=FLAT, padx=5, pady=4)
    recognizeUser.pack(side=LEFT, padx=10, pady=5)

    but_frame.configure(background='white')
    but_frame.pack(side=BOTTOM)

    v0.bind('<Button-1>', keep_flat)
    v0.bind('<Button-2>', keep_flat)

    global_frame.pack()

    v0.mainloop()


def main():

    global model

    rest = Activity('0', 'resting', 10)
    model.addActivity(rest)
    walk = Activity('1', 'walking', 10)
    model.addActivity(walk)
    run = Activity('2', 'running', 10)
    model.addActivity(run)
    jump = Activity('3', 'jumping', 10)
    model.addActivity(jump)

    with open('data.arff', 'a+') as input_file, open('data.csv', 'a+') as output_file:
        users = '{'

        for x in range(0, len(model.getUsers())):
            users += str(x) + ','

        users = users[:-1]
        users += '}'

        activities = '{'
        for x in range(0, len(model.getActivities())):
            activities += str(x) + ','

        activities = activities[:-1]
        activities += '}'

        if os.stat(input_file.name).st_size == 0:
            user = User('0')
            model.addUser(user)
            users = '{0}'
            output_file.write(
               '@relation \'Accelerometer: -C 2\'\n\n@attribute activity- ' + activities + '\n@attribute user- ' + users + '\n@attribute x numeric\n@attribute y numeric\n@attribute z numeric\n\n@data\n')
        else:
            for line in input_file:
                if '@attribute activity- ' in line:
                    output_file.write('@attribute activity- ' + activities + '\n')
                elif '@attribute user- ' in line:
                    output_file.write(line)
                    aux = line.split(' ')
                    aux[2] = aux[2][:-2]
                    aux[2] = aux[2][1:]
                    us = aux[2].split(',')
                    for x in us:
                        user = User(x)
                        model.addUser(user)
                else:
                    output_file.write(line)

    if os.path.isfile('./data.arff'):
        os.remove('./data.arff')

    os.rename('./data.csv', './data.arff')

    mainScreen()


if __name__ == '__main__':
    main()
