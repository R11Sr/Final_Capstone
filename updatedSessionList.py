import csv
from Course import Session
import random
import ast

lecturer_preferences = {
    "John Dellinger" : [8, 9, 10, 11],
    "Pamella Anderson" : [9, 10, 11, 12, 13],
    "Jeremy Jackson" : [11, 12, 13, 14, 15],
    "Sister Francis" : [14, 15, 16, 17, 18],
    "Marlon Eccleston" : [8, 9, 10, 11, 12],
    "Simeon Bride" : [12, 13, 14, 15, 16],
    "Mary McCarthy" : [10, 11, 12, 13],
    "Billy Baxton" : [15, 16, 17, 18],
    "Winnifred Morgan" : [13, 14, 15, 16, 17, 18],
    "Christina Jones" : [13, 14, 15, 16],
    "Shawn Senior" : [9, 10, 11, 12, 13],
    "Jack Spicer" : [10, 11, 12, 13],
    "Peter Earlington" : [12, 13, 14, 15],
    "Joseph Aaronson" : [14, 15, 16,17,18],
    "Ramone Jones" : [9, 10, 11, 12, 13],
    "Persephone Riles" : [12, 13, 14, 15],
    "Martha Brae Johnson" : [16, 17, 18,19,20],
    "Jillian Wilson-Clarke" : [11, 12, 13, 14],
    "Jordan Daniels" : [12,13, 14, 15,16, 17, 18, 19],
    "Preacher Lawson" : [10, 11, 12, 13, 14],
    "Samuel Orton" : [13, 14, 14, 16,17],
    "Kimberlay Otter" : [8, 9,10, 11, 12, 13, 14, 15], 
    "Pebbles Montana" : [11, 12, 13, 14, 15, 16],
    "Larry Underhill" : [9, 10, 11, 12, 13, 14,15, 16],
    "Shanks Longville" : [14, 15,16,17, 18, 19],
    "Melissa Henry" : [8,9, 10, 11,12,13,14,15],
    "Carrie Manchester" : [14,15, 16, 17,18, 19],
    "Matthew Turner" : [12,13,14,15,16,17, 18, 19,20],
    "Dane Wheezer" : [15, 16, 17, 18, 19],
    "Maxwell Ryan" : [8, 9, 10,11,12, 13, 14, 15],
    "Travis Campbell" : [11, 12, 13,14,15, 16, 17],
    "Jerome Houston" : [10, 11, 12, 13],
    "Dalton Chandler" : [13, 14, 15, 16, 17],
    "Denzel Owens" : [8, 9, 10, 11, 12, 13],
    "Carley Mendez" : [11, 12, 13, 14, 15],
    "Kelly Chapman" : [14, 15, 16, 17],
    "Leon Rivera" : [17, 18, 19, 20],
    "Raquel Hammond" : [12, 13, 14, 15, 16],
    "Malaki Hart" : [9, 10, 11],
    "Katie Dominguez" : [11, 12, 13, 14],
    "Sariah Shepard" : [17, 18, 19],
    "Allie Potter" : [10, 11, 12, 13, 14, 15, 16],
    "Zaire Grant" : [8, 9, 10, 11, 12],
    "Gavin Baxter" : [10, 11, 12, 13, 14, 15],
    "Myah Mcgrath" : [12, 13, 14, 15],
    "Patience Barber" : [8, 9, 10, 11],
    "Emely Robles" : [14, 15, 16, 17, 18],
    "Shyann Obrien" : [16, 17, 18, 19, 20],
    "Alisa Lindsey" : [9, 10, 12, 13, 14],
    "Rihanna Guerrero" : [18, 19, 20],
    "Jeramiah Reilly" : [15, 16, 17, 18, 19, 20],
    "Skyler Snow" : [10, 11, 12, 13, 14, 15],
    "Kate Bowman" : [9, 10, 11, 12, 13],
    "Elian Andrade" : [11, 12, 13, 14, 15],
    "Peyton Zimmerman" : [14, 15, 16, 17, 18],
    "Camilla Christensen" : [12, 13, 14, 15, 16],
    "Brock Baird" : [10, 11, 12, 13],
    "Laila Murphy" : [8, 9, 10],
    "Tamara Phillips" : [15, 16, 17, 18],
    "Dakota Wheeler" : [10, 11, 12, 13, 14, 15, 16],
    "Denzel Lee" : [14, 15, 16, 17],
    "Stacy McIntosh" : [10, 11, 12, 13],
    "Irvin Huynh" : [17, 18, 19, 20],
    "Sabrina Valencia" : [14, 15, 16, 17],
    "Alfredo Burnett" : [9, 10, 11, 12, 13, 14],
    "Hassan Gibbs" : [12, 13, 14, 15, 16],
    "Annalise Wise" : [10, 11, 12, 13, 14, 15, 16],
    "Libby Barnes" : [9, 10, 11],
    "Donald Hatfield" : [15, 16, 17, 18],
    "Samuel Saunders" : [12, 13, 14, 15, 16],
    "Maritza Bray" : [14, 15, 16, 17, 18],
    "Charity Willis" : [17, 18, 19],
    "Jamar Curry" : [11, 12, 13, 14],
    "Eduardo Payne" : [15, 16, 17],
    "Camilla Atkins" : [10, 11, 12, 13],
    "Tomas Kirk" : [16, 17, 18, 19, 20],
    "Bridger Frank" : [9, 10, 11, 12, 13, 14],
    "Timothy Dalton" : [13, 14, 15, 16, 17, 18, 19, 20],
    "Frida Arias" : [16, 17, 18, 19],
    "Liberty Walls" : [8, 9, 10, 11, 12],
    "Matias Young" : [15, 16, 17, 18, 19],
    "Orion Jefferson" : [14, 15, 16, 17],
    "Lailah Williams" : [12, 13, 14, 15, 16, 17],
    "Julien Valenzuela" : [9, 10, 11, 12, 13, 14, 15, 16],
    "Charlie Cole" : [14, 15, 16, 17, 18],
    "Johanna Cooley" : [10, 11, 12, 13],
    "Jared Stanton" : [15, 16, 17, 18, 19, 20],
    "Gilbert Mckinney" : [17, 18, 19],
    "Kade Johnson" : [13, 14, 15, 16, 17],
    "Alyssa Levine" : [11, 12, 13, 14, 15, 16],
    "Anderson Forbes" : [16, 17, 18, 19]
    
}

allSessions = {}
fileName = 'CurrentRegistration.csv'
with open(fileName, mode='r', newline='') as file:
        # Create a CSV writer object
        reader = csv.reader(file)

        rows = [row for row in reader]

        for row in rows:
            row = row[0]
            cCode = row.split('{')[0][:-3]
            data =  ast.literal_eval("{" + row.split('{')[1])

            #select a Lecturer

            random_key = random.choice(list(lecturer_preferences.keys()))

            """ Randomly assign Lecturers
                All students attend the lecture and seminars
                Simulate even distribution of other sessions
            """

            if 'Lecture' in data:
                for ea in data['Lecture']:
                    random_key = random.choice(list(lecturer_preferences.keys()))
                    sess = Session(lecturer_preferences[random_key],'Lecture',cCode,data['count'])
                    sess.setPriority(4)
                    sess.setTimeSpan(random.randint(1, 2))
                    allSessions[cCode] = sess

            if 'Lab' in data:
                for ea in data['Lab']:
                    random_key = random.choice(list(lecturer_preferences.keys()))
                    sess = Session(lecturer_preferences[random_key],'Lab',cCode,round(int(data['count']) / len(data['Lab'])))
                    sess.setPriority(2)
                    sess.setTimeSpan(random.randint(1, 2))
                    allSessions[cCode] = sess

            if 'Tutorial' in data:
                for ea in data['Tutorial']:
                    random_key = random.choice(list(lecturer_preferences.keys()))
                    sess = Session(lecturer_preferences[random_key],'Tutorial',cCode,round(int(data['count']) / len(data['Tutorial'])))
                    sess.setPriority(1)
                    sess.setTimeSpan(1)
                    allSessions[cCode] = sess

            if 'Seminar' in data:
                for ea in data['Seminar']:
                    random_key = random.choice(list(lecturer_preferences.keys()))
                    sess = Session(lecturer_preferences[random_key],'Seminar',cCode,data['count'])
                    sess.setPriority(3)
                    sess.setTimeSpan(1)
                    allSessions[cCode] = sess


            

print(len(allSessions))
