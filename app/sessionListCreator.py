import csv
from .Course import Session
import random
import ast



lecturer_preferences = {}
Lect_file = 'lecturer_preference.csv'
def create_lect_pref_dict():
    with open(Lect_file, mode='r', newline='') as file:
                # Create a CSV writer object
                reader = csv.reader(file)

                rows = [row for row in reader]

                for row in rows:
                    
                    lecturer_preferences[row[0]] = [int(x) for x in row[1:]] 
create_lect_pref_dict()


def getAllSessions():
    def sessFinder(sessName: str, sessList: list) -> bool:
        sNameList = [s.name for s in sessList]
        if sessName in sNameList:
            return True
        return False  
    
    allSessions = {}
 
    fileName = 'CurrentRegistration.csv'

    sessionCounter = 0 
    MAX_SESSIONS = 305 # Used to limit the amount of sess generated
    with open(fileName, mode='r', newline='') as file:
            # Create a CSV writer object
            reader = csv.reader(file)

            rows = [row for row in reader]

            for row in rows:

                row = row[0]
                cCode = row.split('{')[0][:-3].strip()
                data =  ast.literal_eval("{" + row.split('{')[1])

                """Limit amount of sessions"""
                if sessionCounter >= MAX_SESSIONS:
                    break

                #remove Duplicate courses
                if cCode in allSessions.keys():
                    continue

                #select a Lecturer
                random_key = random.choice(list(lecturer_preferences.keys()))

                """ Randomly assign Lecturers
                    All students attend the lecture and seminars
                    Simulate even distribution of other sessions
                """

                if 'Lecture' in data:
                    count = 1
                    for ea in data['Lecture']:
                        random_key = random.choice(list(lecturer_preferences.keys()))
                        
                        sess = Session(random_key,'Lecture',cCode,data['count'],count)
                        sess.setPriority(4)
                        sess.setTimeSpan(1)
                        if cCode in allSessions:
                            if not sessFinder(sess.name,allSessions[cCode]):
                                allSessions[cCode].append(sess)
                                sessionCounter +=1
                        else:
                            allSessions[cCode] = []
                            allSessions[cCode].append(sess)
                            sessionCounter +=1

                        count +=1
                if 'Lab' in data:
                    count = 1
                    for ea in data['Lab']:
                        random_key = random.choice(list(lecturer_preferences.keys()))
                        sess = Session(random_key,'Lab',cCode,round((int(data['count']) / len(data['Tutorial'])* 1.3)),count)
                        sess.setPriority(2)
                        sess.setTimeSpan(1)
                        if cCode in allSessions:
                            if not sessFinder(sess.name,allSessions[cCode]):
                                allSessions[cCode].append(sess)
                                sessionCounter +=1

                        else:
                            allSessions[cCode] = []
                            allSessions[cCode].append(sess)
                            sessionCounter +=1

                        count +=1

                if 'Tutorial' in data:
                    count = 1
                    for ea in data['Tutorial']:
                        random_key = random.choice(list(lecturer_preferences.keys()))
                        sess = Session(random_key,'Tutorial',cCode,round((int(data['count']) / len(data['Tutorial'])* 1.3)),count)
                        sess.setPriority(1)
                        sess.setTimeSpan(1)
                        if cCode in allSessions:
                            if not sessFinder(sess.name,allSessions[cCode]):
                                allSessions[cCode].append(sess)
                                sessionCounter +=1

                        else:
                            allSessions[cCode] = []
                            allSessions[cCode].append(sess)
                            sessionCounter +=1

                        count +=1
                if 'Seminar' in data:
                    count = 1
                    for ea in data['Seminar']:
                        random_key = random.choice(list(lecturer_preferences.keys()))
                        sess = Session(random_key,'Seminar',cCode,data['count'],count)
                        sess.setPriority(3)
                        sess.setTimeSpan(1)
                        if cCode in allSessions:
                            if not sessFinder(sess.name,allSessions[cCode]):
                                allSessions[cCode].append(sess)
                                sessionCounter +=1

                        else:
                            allSessions[cCode] = []
                            allSessions[cCode].append(sess)
                            sessionCounter +=1

                        count +=1


      
         
    return  allSessions

# print(d)
# count = 0
# for k,v in d.items():
#     count+= len(v)

# print(count)


def makeRegistrationData(all_sessions):
    regis ={}
    file_name = 'Student_Registration_files\student_data.csv'
    allsess = list(all_sessions.values())

    ListAllSessions = []
    for ele in allsess:
        for ea in ele:
           if ea.name in ListAllSessions:
               pass
           else:
               ListAllSessions.append(ea.name)
                
    list_length = len(ListAllSessions)
    print(list_length)

    with open(file_name, mode='r', newline='') as file:
    #    Create a CSV reader object
        reader = csv.reader(file)

        # Read the header row
        header = next(reader)

        rows = [row for row in reader]
        counter = 0
        for row in rows:
            index = counter % list_length
            if counter > 3000:
                break
            id = int(row[0].strip())
            sessName = ListAllSessions[index]
            if sessName in regis:
                regis[sessName].append(id)
            else:
                l = []
                l.append(id)
                regis[sessName] = l
            counter +=1
    return regis

def allData():
    d = getAllSessions()
    r = makeRegistrationData(d)

    return d,r


    


