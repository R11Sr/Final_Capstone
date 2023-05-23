import csv
from .Course import Course

import os
import fnmatch

import ast 

def getAllcourses():
        
    """List of Previous Registration Data FileNames"""
    registration_files_by_year = []

    """Registration in Course dictionary"""
    allCourses ={}
    # Get the current directory
    folder_path = os.getcwd()

    # Specify the file pattern
    file_pattern = 'only_2_duplicate_*'


    # Find all files that match the pattern
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if fnmatch.fnmatch(file, file_pattern):
                file_list.append(os.path.join(root, file))

    # Print the matched file names
    for file_path in file_list:
        registration_files_by_year.append(file_path.split("\\")[-1])

    for regPerYear in registration_files_by_year:
        year = regPerYear.split('.')[0][-4:]
        with open(regPerYear, mode='r', newline='') as file:
            # Create a CSV writer object
            reader = csv.reader(file)

            # Read the rows
            rows = [row for row in reader]
            
            for row in rows:
                courseCode = row[0].strip()
                my_dict = ast.literal_eval(row[2])
                
                if courseCode in allCourses:

                    if year in allCourses[courseCode].registrationData:
                        _ = allCourses[courseCode].registrationData[year]
                        for k in my_dict.keys():
                            try:
                                if k in _[1]:
                                    pass
                                else:
                                    _[1].append(k)
                            except Exception:
                                pass
                        allCourses[courseCode].registrationData[year] = [_[0] + int(row[1]),_[1]]
                        
                    else:
                        majorList = []
                        for k in my_dict.keys():
                            if k in majorList:
                                pass
                            else:
                                majorList.append(k)
                        allCourses[courseCode].registrationData[year] = [int(row[1]),majorList]           
                    
                else:
                    c= Course(courseCode,courseCode,"John J Public", ['Lecture','Lab','Tutorial'])
                    majorList = []
                    for k in my_dict.keys():
                        if k in majorList:
                            pass
                        else:
                            majorList.append(k)
                    c.registrationData[year] = [int(row[1]),majorList]
                    
                    allCourses[courseCode] = c

          



    return allCourses


