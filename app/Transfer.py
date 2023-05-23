import json
import queue
import scipy.stats as stats
import statistics
from dataclasses import dataclass, field
from typing import Any
from .Course import *
from collections import deque

from .courseListCreator import *
from .sessionListCreator import *
from .SessionAssign import classroom_capacity

# import pdb; pdb.set_trace()


"""
Arbirary choices:
    self.CLASH_PERCENT_INDEX = 0.025 #arbitrary

"""


class Transfer():
    def __init__(self,geneotype:str) -> None:
        self.fifoqueue = None
        self.deque = None
        self.priorityqueue = None
        self.geneotype = geneotype
        self.timeTable = None
        self.lecturePrefGeneome = None
        self.clashGenome = None
        self.roomProximityGenome = None
        self.CAIgenome = None
        self.CAIdecimal = None
        self.ClashConstraintPercentage = None
        self.placementUrgency = None # eager or lazy placement
        self.MAXIMUM_REQUEUE_ATTEMPTS = None
        self.CLASH_PERCENT_INDEX = 0.25 #arbitrary
        self.LECTURER_PREF_INDEX = None
        self.allSessions = None
        self.AllsessionRegistration = None
        self.placeDict = None
        self.ListingofRooms = None
        self.costOfAllPlacements ={}
        """
        All courses is a dictionary of all Course objects
        output like: {'SWEN3145': <name:SWEN3145, registrationData: 
        {'2019': [348, ['INFO', 'SWEN', 'COMP']], '2020': [414, ['SWEN', 'COMP', 'INFO']],
          '2021': [321, ['INFO', 'SWEN', 'COMP']], '2022': [342, ['COMP', 'INFO', 'SWEN']]}>,.....
        """
        self.AllCourses= None
        

        




    def setAttibutes(self):
        self.lecturePrefGeneome = self.geneotype[:3]
        self.setLectureFactor()
        self.clashGenome = self.geneotype[3:11] 
        self.roomProximityGenome = self.geneotype[11:16]
        #CAI,16 bit gene sequence interpreted as  sign(0)0.0000 0000 0000 00
 
        self.CAIgenome = self.geneotype[16:32]
        self.CAIconstraintDecimal = None
        self.setDecimalCAI()
        self.placementPlan=self.geneotype[32:35]
        # [37:40]
        self.placementUrgency= self.geneotype[35:]
        self.setMaxRequeueAttempts()
        self.ClashConstraintRange = self.setClashConstraintPercentage()
        
    def setClashConstraintPercentage(self):
        clashbits = self.clashGenome
        self.ClashConstraintPercentage = int(clashbits.lstrip('0'), 2)

    def setLectureFactor(self):
        lectbits = self.lecturePrefGeneome
        self.LECTURER_PREF_INDEX = int(str(lectbits), 2)/10

    def getPlacement(self)-> str:
        return self.placementPlan


    def makeplacementPlans(self):
        self.placeDict  ={}
        self.placeDict['000'] = 'PriorityQNonLimitingConstraints'
        self.placeDict['001'] = 'FIFOQNonLimitingConstraints'
        self.placeDict['010'] = 'DequeQNonLimitingConstraints'   #tentative
        self.placeDict['011'] = 'PriorityQLimiting'
        self.placeDict['100'] = 'FIFOQLimiting'
        self.placeDict['101'] = 'DequeQLimiting'  #tentative
        self.placeDict['110']  = 'PriorityQLimiting'
        self.placeDict['111'] = 'FIFOQLimiting'

        
    """_summary_
        Responsible for setting the total number of attempts that can be made to requeue a session
        if conditions are unfavorable for its placement.
        it calculates the number by converted the placement urgency bit string to its decimal 
        value and then to increase the number of attempts its is arbitrarily multiplied by 5.
    """
    def setMaxRequeueAttempts(self) ->None:
            totalReQattempts =  int(self.placementUrgency,2) * 5 
            self.MAXIMUM_REQUEUE_ATTEMPTS = totalReQattempts
    

    def getMaxRequeueAttempts(self) -> int:
        return self.MAXIMUM_REQUEUE_ATTEMPTS


    # This also normalises the data. In that it changes the values from the range of -1 to 1, to 0 to 2.
    # makes it easier when running a minimising GA
    def setDecimalCAI(self):
        gene = self.CAIgenome

        def parse_bin(s):
            return int(s[1:], 2) / 2.**(len(s) - 1)
        
        fraction = '.' + gene[2:]

        if gene[0]:
            _ =  float(f'{gene[1]}') + parse_bin(fraction)
            self.CAIconstraintDecimal = 1 + _ 

        else:
            self.CAIconstraintDecimal = - float(f'{gene[1]}') - parse_bin(fraction)
        
    
    def isFIFOQueueAvailable(self)-> bool:
        if self.fifoqueue:
            return True
        return False
    
    def isDequeAvailable(self) -> bool:
        if self.deque:
            return True
        return False
    
    def isPriorityQueueAvailable(self) -> bool:
        if self.priorityqueue:
            return True
        return False


        

    def buildPriorityQueue(self) ->None:
        self.priorityqueue = queue.PriorityQueue()

    def buildFIFOQueue(self) ->None:
        self.fifoqueue = queue.Queue()

    def buildDeque(self) -> None:
        self.deque  = deque()

    
    # This method may not be needed. But just in case. It is there as a wrapper class
    def enqueuePriority(self,priority: int, session: Session) ->None:
        if self.isPriorityQueueAvailable():
            self.priorityqueue.put((priority,session))
        else:
            raise Exception("The Queue must exist before elements can be added to it.")

    def enqueueFIFO(self,session: Session) -> None:
        if self.isFIFOQueueAvailable():
            self.fifoqueue.put(session)
        else:
            raise Exception("The Queue must exist before elements can be added to it.")


    def FIFOrequeue(self,session: Session) ->None:
        if self.FIFOQueueAvailable():
            self.fifoqueue.put(session)
    
    def isDequeEmpty(self) -> bool:
        if not bool(self.deque):
            return True
        return False
 
    def RequeueDequeLeft(self,session: Session) -> None:
        if self.isDequeAvailable():
            self.deque.appendleft(session)

    def RequeueDequeRight(self,session: Session) -> None:
        if self.isDequeAvailable():
            self.deque.append(session)

    def priorityRequeue(self,session: Session) ->None:
        self.priorityqueue.put((session.getPriority(),session))


    def getTimeTable(self) ->list:
        return self.timeTable
    
    def setTimeTable(self,tt: list)-> None:
        self.timeTable = tt

    """
        Session Position In Time Table
        [
                M   T   W   Th  F           
        8       [1],[2],[3],[4],[5],
        9       [6],[7],[8],[9],[10],
        10    [11],[12],[13],[14],[15],
        11    [16],[17],[18],[19],[20],
        12    [21],[22],[23],[24],[25],
        13    [26],[27],[28],[29],[30],
        14    [31],[32],[33],[34],[35],
        15    [36],[37],[38],[39],[40],
        16    [41],[42],[43],[44],[45],
        17    [46],[47],[48],[49],[50],
        18    [51],[52],[53],[54],[55],
        19    [56],[57],[58],[59],[60],
        20    [61],[62],[63],[64],[65],
        ]
    
    """

    def generateTimetable(self) ->None:
        
        timeTable = [
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
        ]
        #block out club time

        self.setTimeTable(timeTable)
    
    def inCAI(self,s1: Session,location: int)-> bool:
        if self.CAI(s1,location) <= self.CAIconstraintDecimal:
            return True
        return False
    
    def inLecturerPref(self,session: Session, location: int)-> bool:
        pass

    def inClashConstraint(self,session: Session, location: int)-> bool:
        if self.ClashConstraint(session,location)[1] <= self.ClashConstraintPercentage:
            return True
        return False
        
    def inRoomProximity(self, session: Session, location: int) -> bool:
        pass

    def CAI(self,s1: Session, location: int)-> float:
        
        #if there is one or more courses in the spot
        if self.timeTable[location]:
            list_of_cai =[]
            for existingSession in self.timeTable[location]:
                #get all the majors for a selected course

                """
                CC          Majors
                INFO2180    Computer Science, Actorial Science, Marketing
                COMP1161    Information technology,Computer Science
                .......     ........
                """
                existingSessionMajor = self.AllCourses[f'{existingSession.getcourseCode()}'].getMajors()
                s1Mojor = self.AllCourses[f'{s1.getcourseCode()}'].getMajors()

                # if there exists majors between the current courses(likely students did both) run the kendal Tau
                if any(element in existingSessionMajor for element in s1Mojor):
                        # print(key, "exists in both dictionaries")
                        """
                        RegistrationAmount():
                        list of amount order by year [155,145,185]
                        YEAR    AMOUNT ENROLLED
                        2016        155
                        2015        145
                        2017        185
                        """
                        c1Data = self.AllCourses[f'{s1.getcourseCode()}'].getRegistrationAmount()
                        c2Data = self.AllCourses[f'{existingSession.getcourseCode()}'].getRegistrationAmount()
                        

                        cai = self.kendalTau(c1Data,c2Data)
                        """Transform the data from the range -1 to 1, to 0 to 2.
                        Makes it easier when running a minimizing algorithm"""

                        if cai > 0:
                            cai +=1
                        elif cai < 0:
                            cai = abs(cai)
                        else:
                            cai = 1
                        list_of_cai.append(cai)
                else:
                    cai = 0
                    list_of_cai.append(0)
                    
            return statistics.mean(list_of_cai)
        else:
            return 0

    def kendalTau(self,c1Data: list,c2Data: list) ->float:
        tau, p_value = stats.kendalltau(c1Data,c2Data)
        return tau
    
    """Weighting table
        Hrs outside     weight
        1               0.1
        2               0.2
        3               0.3
        4               0.4
        5               0.5
        6               0.6
       
        implemented by using self.LECTURER_PREF_INDEX
    """
    def LecturerPref(self,session: Session, location: list)-> float:
        lectPrefTimes = x[f'{session.facilitator}']
        lectPrefTimes.sort()
        timeDiff = 0

        timedict = self.makeTimedictionary()
        timesOfSesison = []
        if type(location) == list:
            for t in location:
                for key, val in timedict.items():
                    if val == location:
                        timesOfSesison.append(timedict[key])
        else:
            for key, val in timedict.items():
                    if val == location:
                        timesOfSesison.append(timedict[key])

        timesOfSesison.sort()


        if all(item in lectPrefTimes for item in timesOfSesison):
            timeDiff = 0
        else:
            diff = list(set(lectPrefTimes) - set(timesOfSesison))

            #if session is ahead of lect pref
            if timesOfSesison[:1] > lectPrefTimes[-1:]:
                
                timeDiff = [x - y for x, y in zip(timesOfSesison[:1], lectPrefTimes[-1:])][0]
            else:
                # session behind lectPref
                # timeDiff = lectPrefTimes[:1] - timesOfSesison[-1:]
                timeDiff = [x - y for x, y in zip(lectPrefTimes[:1], timesOfSesison[-1:])][0]

                
        return timeDiff * self.LECTURER_PREF_INDEX
        



    def makeTimedictionary(self) ->dict:
        timedict = {}
        timedict['8'] = 1
        timedict['8'] = 2
        timedict['8'] = 3
        timedict['8'] = 4
        timedict['8'] = 5
        timedict['9'] = 6
        timedict['9'] = 7
        timedict['9'] = 8
        timedict['9'] = 9
        timedict['9'] = 10
        timedict['10'] = 11
        timedict['10'] = 12
        timedict['10'] = 13
        timedict['10'] = 14
        timedict['10'] = 15
        timedict['11'] = 16
        timedict['11'] = 17
        timedict['11'] = 18
        timedict['11'] = 19
        timedict['11'] = 20
        timedict['12'] = 21
        timedict['12'] = 22
        timedict['12'] = 23
        timedict['12'] = 24
        timedict['12'] = 25
        timedict['13'] = 26
        timedict['13'] = 27
        timedict['13'] = 28
        timedict['13'] = 29
        timedict['13'] = 30
        timedict['14'] = 31
        timedict['14'] = 32
        timedict['14'] = 33
        timedict['14'] = 34
        timedict['14'] = 35
        timedict['15'] = 36
        timedict['15'] = 37
        timedict['15'] = 38
        timedict['15'] = 39
        timedict['15'] = 40
        timedict['16'] = 41
        timedict['16'] = 42
        timedict['16'] = 43
        timedict['16'] = 44
        timedict['16'] = 45
        timedict['17'] = 46
        timedict['17'] = 47
        timedict['17'] = 48
        timedict['17'] = 49
        timedict['17'] = 50
        timedict['18'] = 51
        timedict['18'] = 52
        timedict['18'] = 53
        timedict['18'] = 54
        timedict['18'] = 55
        timedict['19'] = 56
        timedict['19'] = 57
        timedict['19'] = 58
        timedict['19'] = 59
        timedict['19'] = 60
        timedict['20'] = 61
        timedict['20'] = 62
        timedict['20'] = 63
        timedict['20'] = 64
        timedict['20'] = 65

        return timedict

    def makeRoomListing(self)  ->list:
        rooms =[]
        for k,v in classroom_capacity.items():
            rooms.append(Room(k,int(v)))
        return rooms

    """
    What percentage of students of that slot hav clashes 
    e.g. 3 sessions in slot totaling 150 students 50 have clash with 2 or more sessions in slot
    30% clash weighting

    WEIGHTING TABLE FOR % OF STUDENT CLASH
      %             weighting
    0  - 5          0 -1.25
    6  - 10         1.50 - 2.50
    11 - 15         2.75 - 3.75
    16 - 20         4.00 - 5.00
    21 - 25         5.25 - 6.25
    26 - 30         6.50 - 7.50
    31 - 35         7.75 - 8.75
    36 - 40         9.00 - 10.00
    > 40            20.00
    
    implemented with CLASH_PERCENT_INDEX
    percentage bit reprentation 0000000, 2^6
    can do int(bitrepresentation,2) to get decimal
    
    -------For Future Implementation -----------
    Weighting           Clash Meaning
    100.00              Lecturer or room having Simultaneous classes
    0.90                Lab to Lecture
    0.80                Lab to Lab
    0.70                Tutorial to Lecture
    0.60                Lab to Tutorial
    0.50                Seminar to Lecture
    0.40                Seminar to Lab
    0.30                Seminar to Tutorial
    0.20                Tutorial to Tutorial
    0.00                No Clashes
    -------------------------------------------

    Used 'Mock data updated' to enroll students in sessions
    """
    def ClashConstraint(self,session: Session, location: int)-> tuple:
        clashSet = set() # number of students with the clashes
        total = 0
        listFacilitators =[]
        clashPercentScore = 0.00
        # print(self.AllsessionRegistration[f'{session.name}'])
        # print('passed')
        sessionEnrolled = set(self.AllsessionRegistration[f'{session.name}'])


        for existingSession in self.timeTable[location]:
            total += len(sessionEnrolled)

            existingSessionEnrolled = set(self.AllsessionRegistration[f'{existingSession.name}'])
            listFacilitators.append(existingSession.facilitator)
            total += len(existingSessionEnrolled)

            clashSet = clashSet | sessionEnrolled | existingSessionEnrolled
            
        # calculates the percentage
        if total != 0:
            clashPercentage = (float(len(clashSet)) / float(total)) * 100
        else:
            clashPercentage = 0
        
        clashPercentScore = round(clashPercentage) * self.CLASH_PERCENT_INDEX # in accord with clash weighting table above

        # to adhere to weighting table above
        if clashPercentage > 40:
            clashPercentScore = 20.0

        #check if a facilitator will have more than 1 session in that slot
        if session.facilitator in listFacilitators:
            clashPercentScore = 20000.00 

        # also check if sessions clash in rooms
        """Rooms with special requirements are not taking into consideration at this time"""
        # breakpoint()
        """Select Room for Session"""
        for room in self.ListingofRooms:

                #ensure room is not in use before assigning it
                # if len(self.timeTable[location]) == 0:
                #     pass
                # else:
                #     print(location)
                #     print(self.timeTable[location])


                 #if the there is no sessions at that time, all rooms are emplty   
                if len(self.timeTable[location]) == 0:
                    # print('no classes, room available')
                    session.tentativeRoom = room.title
                    # print(f'assinged {room.title} to {session}')
                else:
                    roomsInUse = [s.approvedRoom for s in self.timeTable[location]]
                    # print(roomsInUse,room.title)
                    if room.title in roomsInUse:
                        pass
                    else:
                        session.tentativeRoom = room.title
                        # print(f'assinged {room.title} to {session}')
                # breakpoint()
                    # for existingSession in self.timeTable[location]:
                    #     if existingSession.approvedRoom == room.title:
                    #         flag.append(True)
                    #     else:
                    #         flag.append(False)
                    # if not all(flag):
                    #     session.tentativeRoom = room.title

        return clashPercentScore,clashPercentage
        
             
    """---------To be Implemented------"""       
    def RoomProximity(self, session: Session, location: int) -> float:
        return 0
    """------------------------------------"""
    def filter(self,session: Session) -> list:

        placementPoints=[]
        for spot in range(0,len(self.timeTable)):
            '''available location should be a list [(score: float,location: list)]
                eg. for a session [(5.322,6),(7.456,8)]'''
            
            if self.isValid(session.getTimeSpan(),spot):
                total = self.getCost(session,spot)
                placementPoints.append((total,spot))      

        return placementPoints

    def getCost(self,session: Session, spot: int) -> float:
        cai = self.CAI(session,spot)
        LecturerPref = self.LecturerPref(session,spot)
        clash = self.ClashConstraint(session,spot)[0]
        RoomProximity = self.RoomProximity(session,spot)
        return  cai + LecturerPref + clash + RoomProximity




    def placeSession(self,session: Session,location: int,cost: float) -> bool:
        length = session.getTimeSpan()
        
        if self.isValid(length,location):
            session.useEnergy()
            session.approvedRoom =  session.tentativeRoom

            for time in range(0,length): 
                '''Add the price paid in this session'''  
                self.timeTable[location + 5* time].append(session)
                if location in self.costOfAllPlacements:
                    self.costOfAllPlacements[location].append(cost)
                    return True
                else:
                    self.costOfAllPlacements[location] = []
                    self.costOfAllPlacements[location].append(cost)
                    return True
        else:
            session.useEnergy()
            return False
            

    def isValid(self,length: int,location: int) -> bool:
        flag = []
        for time in range(0,length):
            try:
                #if the location is in club time
                if location in [39,44,49,54,59,64]:
                    flag.append(False)

                self.timeTable[location + 5* time]
                flag.append(True)
            except IndexError:
                flag.append(False)
                
        return all(flag)
            
    def makeTTtoString(self) ->list:
        tt =[]
        for loc in range(0,len(self.timeTable)):
            l = []
            for sess in self.timeTable[loc]:
                l.append(sess.toString())
            tt.append(l)
        return tt



    def checkAllHardConstraint(self,session: Session, spot: int) -> list:
            cai = self.inCAI(session,spot)
            clash = self.inClashConstraint(session,spot)

            return [cai,clash]
            
        
    def PriorityQLimiting(self) -> None:
        print("Excuting PriorityQLimiting")
        self.buildPriorityQueue()

        if self.isPriorityQueueAvailable():
            for k, sessionList in self.allSessions.items():
                for session in sessionList:
                    self.enqueuePriority(session.getPriority(),session)
        
        while not self.priorityqueue.empty():
            # breakpoint()
            pri,session = self.priorityqueue.get()

            '''available location should be a list [(score: int,location: list)]
                eg. for 2 hr session [(5,[6,11]),(7,[8,13])]'''
            allLocations = self.filter(session)
            val = lambda tup: tup[0]
            allLocations.sort(key=val)

            if len(allLocations) >0:
                cost,location = allLocations.pop(0)
                if all(self.checkAllHardConstraint(session,location)): 
                    self.placeSession(session,location,cost)
                elif session.getAttempts() >= self.getMaxRequeueAttempts():
                    self.placeSession(session,location,cost)
                else:
                    session.useAttempt()
                    self.enqueuePriority(session.getPriority(),session)

        
      

            
    def PriorityQNonLimitingConstraints(self) -> None:

        print('executing PriorityQNonLimitingConstraints')
        self.buildPriorityQueue()

        if self.isPriorityQueueAvailable():
            for k, sessionList in self.allSessions.items(): 
                for session in sessionList:
                    self.enqueuePriority(session.getPriority(),session)
        # while not self.priorityqueue.empty():
        #     pri,sess = self.priorityqueue.get()
        #     print(sess)
        while not self.priorityqueue.empty():

            pri, session = self.priorityqueue.get()

            '''available location should be a list [(score: int,location: list)]
                eg. for 2 hr session [(5,[6,11]),(7,[8,13])]'''
            allLocations = self.filter(session)
            val = lambda tup: tup[0]
            allLocations.sort(key=val)

            if allLocations:
                cost,location = allLocations.pop(0)
                self.placeSession(session,location,cost)


        return self.priorityqueue


        
    def FIFOQLimiting(self )-> None:
        print("Executing FIFOQLimiting")
        self.buildFIFOQueue()

        if self.isFIFOQueueAvailable():
            for k, sessionList in self.allSessions.items(): 
                for session in sessionList:
                    self.enqueueFIFO(session)
        
        while not self.fifoqueue.empty():
            session = self.fifoqueue.get()
            
            '''available location should be a list [(score: int,location: list)]
                eg. for 2 hr session [(5,[6,11]),(7,[8,13])]'''
            allLocations = self.filter(session)
            val = lambda tup: tup[0]
            allLocations.sort(key=val)

            if allLocations:
                cost,location = allLocations.pop(0)
                if all(self.checkAllHardConstraint(session,location)): 
                    self.placeSession(session,location,cost)
                elif session.getAttempts() >= self.getMaxRequeueAttempts():
                    self.placeSession(session,location,cost)
                else:
                    session.useAttempt()
                    self.enqueueFIFO(session)


    def FIFOQNonLimitingConstraints(self) -> None:
        print('Executing FIFOQNonLimitingConstraints')

        self.buildFIFOQueue()
        
        if self.isFIFOQueueAvailable():
            for k, sessionList in self.allSessions.items(): 
                for session in sessionList:
                    self.enqueueFIFO(session)

        while not self.fifoqueue.empty():
            session = self.fifoqueue.get()
            
            '''available location should be a list [(score: int,location: list)]
                eg. for 2 hr session [(5,[6,11]),(7,[8,13])]'''
            allLocations = self.filter(session)
            val = lambda tup: tup[0]
            allLocations.sort(key=val)

            if allLocations:
                cost,location = allLocations.pop(0)
                self.placeSession(session,location,cost)

    """
    https://docs.python.org/3/library/collections.html#deque-objects

    This manner of generating the time table places the lectures to a separate portion of the queue the left
    all other sessions are placed to the right.

    """
    def DequeQLimiting(self) -> None:
        # print('executing DequeQLimiting')
        self.buildDeque()
        counter = 0
        #Populate the Queue
        for k, sessionList in self.allSessions.items():

            for session in sessionList:
                if session.getType() == 'Lecture':
                    self.deque.appendleft(session)
                else:
                    self.deque.append(session)


        # breakpoint()  
        while not self.isDequeEmpty():

            #This is to simulate taking 1 from the left(lecturer) and in the next iteration
            #take 1 session from the right(tut,seminar or lab)

            #from Left
            if counter % 2 == 0:
                session = self.deque.popleft()
                
                '''available location should be a list [(score: int,location: list)]
                    eg. for 2 hr session [(5,[6,11]),(7,[8,13])]'''
                allLocations = self.filter(session)
                val = lambda tup: tup[0]
                allLocations.sort(key=val)

                if allLocations:
                    cost,location = allLocations.pop(0)

                    if all(self.checkAllHardConstraint(session,location)): 
                        self.placeSession(session,location,cost)
                    elif session.getAttempts() >= self.getMaxRequeueAttempts():
                        self.placeSession(session,location,cost)
                    else:
                        session.useAttempt()
                        self.RequeueDequeLeft(session)
            #from Right
            else:
                session = self.deque.pop()
                
                '''available location should be a list [(score: int,location: list)]
                    eg. for 2 hr session [(5,[6,11]),(7,[8,13])]'''
                allLocations = self.filter(session)
                val = lambda tup: tup[0]
                allLocations.sort(key=val)

                if allLocations:
                    cost,location = allLocations.pop(0)

                    if all(self.checkAllHardConstraint(session,location)): 
                        self.placeSession(session,location,cost)
                    elif session.getAttempts() >= self.getMaxRequeueAttempts():
                        self.placeSession(session,location,cost)
                    else:
                        session.useAttempt()
                        self.RequeueDequeRight(session)

            
            counter+=1


    def DequeQNonLimitingConstraints(self) -> None :
        # print('executing DequeQNonLimitingConstraints')

        self.buildDeque()
        counter = 0

        #Populate the Queue
        for k,sessionList in self.allSessions.items():
            for session in sessionList:
                if session.getType() == 'Lecture':
                    self.deque.appendleft(session)

                else:
                    self.deque.append(session)
                    

            
        while not self.isDequeEmpty():
            # breakpoint()
            #This is to simulate taking 1 from the left(lecturer) and in the next iteration
            #take 1 session from the right(tut,seminar or lab)

            #from Left
            if counter % 2 == 0:
                session = self.deque.popleft()
                # print(session)
                for location in range(0,len(self.timeTable)):
                    occupiedRooms = []
                    busyLects = []
                    ccOfExistingSessions = []

                    #check all Attr of placed Session at location
                    for existingSes in self.timeTable[location]:
                        occupiedRooms.append(existingSes.approvedRoom)
                        busyLects.append(existingSes.facilitator)
                        ccOfExistingSessions.append(existingSes.getcourseCode())

                    #if a room is available and the ffacilitator is not busy and another session
                    #of the same course is not at that location, place this session
                    freeRooms = list(set(self.ListingofRooms) - set(occupiedRooms))
                    if session.facilitator not in busyLects and len(freeRooms) != 0 and session.getcourseCode() not in ccOfExistingSessions:
                        session.approvedRoom = freeRooms[random.randint(0,len(freeRooms)) - 1].title
                        cost = self.getCost(session,location)
                        self.placeSession(session,location,cost)
                        break

                counter+=1

                # allLocations = self.filter(session)
                # val = lambda tup: tup[0]
                # allLocations.sort(key=val)
                
                # """Since without constraint
                #     Just ensure that no lect 2 class at a time
                #     1 room 2 classes at a time
                # """
                # if allLocations:
                #     cost,location = allLocations.pop(0)
                #     self.placeSession(session,location,cost)
            #from Right
            else:
                session = self.deque.pop()
                # print(session)
                for location in range(0,len(self.timeTable)):
                    occupiedRooms = []
                    busyLects = []
                    ccOfExistingSessions = []

                    #check all Attr of placed Session at location
                    for existingSes in self.timeTable[location]:
                        occupiedRooms.append(existingSes.approvedRoom)
                        busyLects.append(existingSes.facilitator)
                        ccOfExistingSessions.append(existingSes.getcourseCode())

                    #if a room is available and the ffacilitator is not busy and another session
                    #of the same course is not at that location, place this session
                    freeRooms = list(set(self.ListingofRooms) - set(occupiedRooms))
                    if session.facilitator not in busyLects and len(freeRooms) != 0 and session.getcourseCode() not in ccOfExistingSessions:
                        session.approvedRoom = freeRooms[random.randint(0,len(freeRooms)) - 1].title
                        cost = self.getCost(session,location)
                        self.placeSession(session,location,cost)
                        break
                '''available location should be a list [(score: int,location: list)]
                    eg. for 2 hr session [(5,[6,11]),(7,[8,13])]'''
                # allLocations = self.filter(session)
                # val = lambda tup: tup[0]
                # allLocations.sort(key=val)

                # if allLocations:
                #     cost,location = allLocations.pop(0)
                #     self.placeSession(session,location,cost)
                counter+=1

        
                    

def execute() ->None:

    """
        self.lecturePrefGeneome = self.geneotype[:3]
        self.setLectureFactor()
        self.clashGenome = self.geneotype[3:11] 
        self.roomProximityGenome = self.geneotype[11:16]
        #CAI,16 bit gene sequence interpreted as  sign(0)0.0000 0000 0000 00
        self.CAIgenome = self.geneotype[16:32]
        self.CAIconstraintDecimal = None
        self.setDecimalCAI()
        self.placementPlan=self.geneotype[32:35]
        # [37:40]
        self.placementUrgency= self.geneotype[35:]
    """

    counter = 0


# for iea in first_five_tt:
#     dicttopass[counter] = iea
#     counter +=1




#     # genome ='010 00010100 00000 0100000000000000 010 00000'
#     genomeList =['0100001010000000010000000000000001000000','0100001010000000010000000000000000000000',
#                  '0100001010000000010000000000000000100000','0100001010000000010000000000000001100000',
#                  '0100001010000000010000000000000010000000','0100001010000000010000000000000010100000']
#     dicttopass = {}
#     counter  = 0
#     for genome in genomeList:
#         print("===========================================================================================")
#     # genome = '0001101100111100110010110001010111010111'
#         AllSession,AllRegistration = allData()
#         t = Transfer(genome)
#         t.setAttibutes()
#         t.generateTimetable()
#         t.makeplacementPlans()
#         t.AllCourses = getAllcourses()
#         t.allSessions = AllSession
#         t.AllsessionRegistration = AllRegistration
        
#         t.ListingofRooms = t.makeRoomListing()
#         placementOperation = f"t.{t.placeDict[t.getPlacement()]}()"
#         eval(placementOperation)
#         print(f"++++++++++ {t.costOfAllPlacements} ++++++++++++++")
#         print(t.getTimeTable())
#         dicttopass[counter] = t.makeTTtoString() 
#         counter +=1

#     json_str = json.dumps(dicttopass)

#     # Open the file in write mode
#     file_name = 'mock_tables.txt'
#     with open(file_name, mode='w') as file:

#         # Write the data to the CSV file
#         file.write(json_str)

# execute()