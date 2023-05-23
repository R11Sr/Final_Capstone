import pandas as pd
import random
import numpy as np
import csv

fileName = 'CurrentRegistration.csv'
df = pd.read_csv('Mock_Data_Updated.csv')
# define capacity dictionaries
classroom_capacity = {
    "CompCLR": 40,
    "CompLab": 45,
    "GEOG Lab 2": 20,
    "GEOG Lecture RM 1": 40,
    "GEOG Lecture RM 2": 40,
    "GEOG Lab 3": 20,
    "Physics Lab": 20,
    "SLT1": 170,
    "SLT2": 160,
    "SLT3": 155,
    "ENG Comp Lab": 28,
    "Math Room 1": 30,
    "Math Room 2": 30,
    "C2": 80,
    "C3": 60,
    "C5": 200
}

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
    "Travis Campbell" : [11, 12, 13,14,15, 16, 17]
}

# specify the name of the column to count unique values in
count_column1 = 'CoreCourses_Sem1'
count_column2 = 'CoreCourses_Sem2'
count_column3 = 'Electivesminor_Sem1'
count_column4 = 'Electivesminor_Sem2'
count_column5 = 'CoreCourses_Summer'

# create a dictionary to store the counts of each unique value
coreSem1Value_counts_dict = {}

# create a dictionary to store the counts of how many times each value in the search list is found in the same row as a unique value
coreSem1Search_counts_dict = {}

# specify the name of the other column to search for values in
search_column = 'major'

# create a set of values to search for in the search column
search_values = {'COMP', 'INFO', 'SWEN'}


with open(fileName,mode= 'w',newline='') as file_write:
    writer = csv.writer(file_write)
        
    # iterate over each row in the dataframe and update the coreSem1Value_counts_dict and coreSem1Search_counts_dict dictionaries
    for i, row in df.iterrows():
        values = row[count_column1].split(',')
        for value in values:
            if value in coreSem1Value_counts_dict:
                coreSem1Value_counts_dict[value] += 1
            else:
                coreSem1Value_counts_dict[value] = 1
            if row[search_column] in search_values:
                if value in coreSem1Search_counts_dict:
                    coreSem1Search_counts_dict[value][row[search_column]] += 1
                else:
                    coreSem1Search_counts_dict[value] = {}
                    for search_value in search_values:
                        coreSem1Search_counts_dict[value][search_value] = 0
                    coreSem1Search_counts_dict[value][row[search_column]] = 1

    # Add Lecture, Tutorial, Seminar, and Lab random whole numbers

    # get the first key-value pair from coreSem1Value_counts_dict
    max_count = list(coreSem1Value_counts_dict.values())[0]

    for value, count in coreSem1Value_counts_dict.items():
        lecture_count = random.randint(1, 3)
        tutorial_max = max_count - lecture_count
        tutorial_count = random.randint(1, min(9, tutorial_max))
        tutorial_sum = 0
        tutorial_numbers = []
        while tutorial_sum < count and len(tutorial_numbers) < tutorial_count:
            num = random.randint(0, min(40, tutorial_max))
            if tutorial_sum + num <= count:
                tutorial_sum += num
                tutorial_numbers.append(num)
        lecture_sum = 0
        lecture_numbers = []
        while lecture_sum < count and len(lecture_numbers) < lecture_count:
            num = random.randint(0, min(50, count - lecture_sum))
            lecture_sum += num
            lecture_numbers.append(num)
        if count > 1:
            add_seminar_or_lab = random.choice(["Seminar", "Lab"])
            if add_seminar_or_lab == "Seminar":
                seminar_max = max_count - lecture_count - tutorial_count
                seminar_count = random.randint(1, min(2, seminar_max))
                seminar_sum = 0
                seminar_numbers = []
                while seminar_sum < count and len(seminar_numbers) < seminar_count:
                    num = random.randint(0, min(40, seminar_max))
                    if seminar_sum + num <= count:
                        seminar_sum += num
                        seminar_numbers.append(num)
                while lecture_count + tutorial_count + seminar_count > max_count or seminar_sum > count:
                    if seminar_count > 1:
                        seminar_count -= 1
                        seminar_numbers = seminar_numbers[:-1]
                        seminar_sum = sum(seminar_numbers)
                    elif tutorial_count > 1:
                        tutorial_count -= 1
                    elif lecture_count > 1:
                        lecture_count -= 1
                coreSem1Value_counts_dict[value] = {
                    'count': count,
                    'Lecture': lecture_numbers,
                    'Tutorial': tutorial_numbers,
                    'Seminar': list(seminar_numbers),
                }
            else:
                lab_max = min(max_count - lecture_count - tutorial_count, 100)
                lab_count = random.randint(1, min(2, lab_max))
                lab_sum = 0
                lab_numbers = []
                while lab_sum < count and len(lab_numbers) < lab_count:
                    num = random.randint(0, min(40, lab_max))
                    if lab_sum + num <= count:
                        lab_sum += num
                        lab_numbers.append(num)
                while lecture_count + tutorial_count + lab_count > max_count or lab_sum > count:
                    if lab_count > 1:
                        lab_count -= 1
                        lab_numbers = lab_numbers[:-1]
                        lab_sum = sum(lab_numbers)
                    elif tutorial_count > 1:
                        tutorial_count -= 1
                    elif lecture_count > 1:
                        lecture_count -= 1
                coreSem1Value_counts_dict[value] = {
                    'count': count,
                    'Lecture': lecture_numbers,
                    'Tutorial': tutorial_numbers,
                    'Lab': list(lab_numbers),
                }
        else:
            lecture_numbers = list(np.random.randint(0, min(50, lecture_count), size=lecture_count)) if lecture_count > 2 else list(np.random.randint(0, 100, size=lecture_count))
            while sum(lecture_numbers) > count:
                lecture_numbers.pop()
            coreSem1Value_counts_dict[value] = {
                'count': count,
                'Lecture': lecture_numbers,
                'Tutorial': tutorial_numbers,
            }


    for value, data in coreSem1Value_counts_dict.items():

        writer.writerows([
                [f"{value} : {data}"]
                ])
            
    # create a dictionary to store the counts of each unique value
    coreSem2Value_counts_dict = {}

    # create a dictionary to store the counts of how many times each value in the search list is found in the same row as a unique value
    coreSem2Search_counts_dict = {}

    # specify the name of the other column to search for values in
    search_column = 'major'

    # create a set of values to search for in the search column
    search_values = {'COMP', 'INFO', 'SWEN'}



    # iterate over each row in the dataframe and update the coreSem2Value_counts_dict and coreSem2Search_counts_dict dictionaries
    for i, row in df.iterrows():
        values = row[count_column2].split(',')
        for value in values:
            if value in coreSem2Value_counts_dict:
                coreSem2Value_counts_dict[value] += 1
            else:
                coreSem2Value_counts_dict[value] = 1
            if row[search_column] in search_values:
                if value in coreSem2Search_counts_dict:
                    coreSem2Search_counts_dict[value][row[search_column]] += 1
                else:
                    coreSem2Search_counts_dict[value] = {}
                    for search_value in search_values:
                        coreSem2Search_counts_dict[value][search_value] = 0
                    coreSem2Search_counts_dict[value][row[search_column]] = 1

    # Add Lecture, Tutorial, Seminar, and Lab random whole numbers

    # get the first key-value pair from coreSem2Value_counts_dict
    max_count = list(coreSem2Value_counts_dict.values())[0]

    for value, count in coreSem2Value_counts_dict.items():
        lecture_count = random.randint(1, 3)
        tutorial_max = max_count - lecture_count
        tutorial_count = random.randint(1, min(9, tutorial_max))
        tutorial_sum = 0
        tutorial_numbers = []
        while tutorial_sum < count and len(tutorial_numbers) < tutorial_count:
            num = random.randint(0, min(40, tutorial_max))
            if tutorial_sum + num <= count:
                tutorial_sum += num
                tutorial_numbers.append(num)
        lecture_sum = 0
        lecture_numbers = []
        while lecture_sum < count and len(lecture_numbers) < lecture_count:
            num = random.randint(0, min(50, count - lecture_sum))
            lecture_sum += num
            lecture_numbers.append(num)
        if count > 1:
            add_seminar_or_lab = random.choice(["Seminar", "Lab"])
            if add_seminar_or_lab == "Seminar":
                seminar_max = max_count - lecture_count - tutorial_count
                seminar_count = random.randint(1, min(2, seminar_max))
                seminar_sum = 0
                seminar_numbers = []
                while seminar_sum < count and len(seminar_numbers) < seminar_count:
                    num = random.randint(0, min(40, seminar_max))
                    if seminar_sum + num <= count:
                        seminar_sum += num
                        seminar_numbers.append(num)
                while lecture_count + tutorial_count + seminar_count > max_count or seminar_sum > count:
                    if seminar_count > 1:
                        seminar_count -= 1
                        seminar_numbers = seminar_numbers[:-1]
                        seminar_sum = sum(seminar_numbers)
                    elif tutorial_count > 1:
                        tutorial_count -= 1
                    elif lecture_count > 1:
                        lecture_count -= 1
                coreSem2Value_counts_dict[value] = {
                    'count': count,
                    'Lecture': lecture_numbers,
                    'Tutorial': tutorial_numbers,
                    'Seminar': list(seminar_numbers),
                }
            else:
                lab_max = min(max_count - lecture_count - tutorial_count, 100)
                lab_count = random.randint(1, min(2, lab_max))
                lab_sum = 0
                lab_numbers = []
                while lab_sum < count and len(lab_numbers) < lab_count:
                    num = random.randint(0, min(40, lab_max))
                    if lab_sum + num <= count:
                        lab_sum += num
                        lab_numbers.append(num)
                while lecture_count + tutorial_count + lab_count > max_count or lab_sum > count:
                    if lab_count > 1:
                        lab_count -= 1
                        lab_numbers = lab_numbers[:-1]
                        lab_sum = sum(lab_numbers)
                    elif tutorial_count > 1:
                        tutorial_count -= 1
                    elif lecture_count > 1:
                        lecture_count -= 1
                coreSem2Value_counts_dict[value] = {
                    'count': count,
                    'Lecture': lecture_numbers,
                    'Tutorial': tutorial_numbers,
                    'Lab': list(lab_numbers),
                }
        else:
            lecture_numbers = list(np.random.randint(0, min(50, lecture_count), size=lecture_count)) if lecture_count > 2 else list(np.random.randint(0, 100, size=lecture_count))
            while sum(lecture_numbers) > count:
                lecture_numbers.pop()
            coreSem2Value_counts_dict[value] = {
                'count': count,
                'Lecture': lecture_numbers,
                'Tutorial': tutorial_numbers,
            }

    for value, data in coreSem2Value_counts_dict.items():
        writer.writerows([
                [f"{value} : {data}"]
                ])
        

    # create a dictionary to store the counts of each unique value
    electSem1Value_counts_dict = {}

    # create a dictionary to store the counts of how many times each value in the search list is found in the same row as a unique value
    electSem1Search_counts_dict = {}

    # specify the name of the other column to search for values in
    search_column = 'major'

    # create a set of values to search for in the search column
    search_values = {'COMP', 'INFO', 'SWEN'}



    # iterate over each row in the dataframe and update the electSem1Value_counts_dict and electSem1Search_counts_dict dictionaries
    for i, row in df.iterrows():
        values = row[count_column3].split(',')
        for value in values:
            if value in electSem1Value_counts_dict:
                electSem1Value_counts_dict[value] += 1
            else:
                electSem1Value_counts_dict[value] = 1
            if row[search_column] in search_values:
                if value in electSem1Search_counts_dict:
                    electSem1Search_counts_dict[value][row[search_column]] += 1
                else:
                    electSem1Search_counts_dict[value] = {}
                    for search_value in search_values:
                        electSem1Search_counts_dict[value][search_value] = 0
                    electSem1Search_counts_dict[value][row[search_column]] = 1

    # Add Lecture, Tutorial, Seminar, and Lab random whole numbers

    # get the first key-value pair from electSem1Value_counts_dict
    max_count = list(electSem1Value_counts_dict.values())[0]

    for value, count in electSem1Value_counts_dict.items():
        lecture_count = random.randint(1, 3)
        tutorial_max = max_count - lecture_count
        tutorial_count = random.randint(1, min(9, tutorial_max))
        tutorial_sum = 0
        tutorial_numbers = []
        while tutorial_sum < count and len(tutorial_numbers) < tutorial_count:
            num = random.randint(0, min(40, tutorial_max))
            if tutorial_sum + num <= count:
                tutorial_sum += num
                tutorial_numbers.append(num)
        lecture_sum = 0
        lecture_numbers = []
        while lecture_sum < count and len(lecture_numbers) < lecture_count:
            num = random.randint(0, min(50, count - lecture_sum))
            lecture_sum += num
            lecture_numbers.append(num)
        if count > 1:
            add_seminar_or_lab = random.choice(["Seminar", "Lab"])
            if add_seminar_or_lab == "Seminar":
                seminar_max = max_count - lecture_count - tutorial_count
                seminar_count = random.randint(1, min(2, seminar_max))
                seminar_sum = 0
                seminar_numbers = []
                while seminar_sum < count and len(seminar_numbers) < seminar_count:
                    num = random.randint(0, min(40, seminar_max))
                    if seminar_sum + num <= count:
                        seminar_sum += num
                        seminar_numbers.append(num)
                while lecture_count + tutorial_count + seminar_count > max_count or seminar_sum > count:
                    if seminar_count > 1:
                        seminar_count -= 1
                        seminar_numbers = seminar_numbers[:-1]
                        seminar_sum = sum(seminar_numbers)
                    elif tutorial_count > 1:
                        tutorial_count -= 1
                    elif lecture_count > 1:
                        lecture_count -= 1
                electSem1Value_counts_dict[value] = {
                    'count': count,
                    'Lecture': lecture_numbers,
                    'Tutorial': tutorial_numbers,
                    'Seminar': list(seminar_numbers),
                }
            else:
                lab_max = min(max_count - lecture_count - tutorial_count, 100)
                lab_count = random.randint(1, min(2, lab_max))
                lab_sum = 0
                lab_numbers = []
                while lab_sum < count and len(lab_numbers) < lab_count:
                    num = random.randint(0, min(40, lab_max))
                    if lab_sum + num <= count:
                        lab_sum += num
                        lab_numbers.append(num)
                while lecture_count + tutorial_count + lab_count > max_count or lab_sum > count:
                    if lab_count > 1:
                        lab_count -= 1
                        lab_numbers = lab_numbers[:-1]
                        lab_sum = sum(lab_numbers)
                    elif tutorial_count > 1:
                        tutorial_count -= 1
                    elif lecture_count > 1:
                        lecture_count -= 1
                electSem1Value_counts_dict[value] = {
                    'count': count,
                    'Lecture': lecture_numbers,
                    'Tutorial': tutorial_numbers,
                    'Lab': list(lab_numbers),
                }
        else:
            lecture_numbers = list(np.random.randint(0, min(50, lecture_count), size=lecture_count)) if lecture_count > 2 else list(np.random.randint(0, 100, size=lecture_count))
            while sum(lecture_numbers) > count:
                lecture_numbers.pop()
            electSem1Value_counts_dict[value] = {
                'count': count,
                'Lecture': lecture_numbers,
                'Tutorial': tutorial_numbers,
            }


    for value, data in electSem1Value_counts_dict.items():
        writer.writerows([
                [f"{value} : {data}"]
                ])
            

    # create a dictionary to store the counts of each unique value
    electSem2Value_counts_dict = {}

    # create a dictionary to store the counts of how many times each value in the search list is found in the same row as a unique value
    electSem2Search_counts_dict = {}

    # specify the name of the other column to search for values in
    search_column = 'major'

    # create a set of values to search for in the search column
    search_values = {'COMP', 'INFO', 'SWEN'}



    # iterate over each row in the dataframe and update the electSem2Value_counts_dict and electSem2Search_counts_dict dictionaries
    for i, row in df.iterrows():
        values = row[count_column4].split(',')
        for value in values:
            if value in electSem2Value_counts_dict:
                electSem2Value_counts_dict[value] += 1
            else:
                electSem2Value_counts_dict[value] = 1
            if row[search_column] in search_values:
                if value in electSem2Search_counts_dict:
                    electSem2Search_counts_dict[value][row[search_column]] += 1
                else:
                    electSem2Search_counts_dict[value] = {}
                    for search_value in search_values:
                        electSem2Search_counts_dict[value][search_value] = 0
                    electSem2Search_counts_dict[value][row[search_column]] = 1

    # Add Lecture, Tutorial, Seminar, and Lab random whole numbers

    # get the first key-value pair from electSem2Value_counts_dict
    max_count = list(electSem2Value_counts_dict.values())[0]

    for value, count in electSem2Value_counts_dict.items():
        lecture_count = random.randint(1, 3)
        tutorial_max = max_count - lecture_count
        tutorial_count = random.randint(1, min(9, tutorial_max))
        tutorial_sum = 0
        tutorial_numbers = []
        while tutorial_sum < count and len(tutorial_numbers) < tutorial_count:
            num = random.randint(0, min(40, tutorial_max))
            if tutorial_sum + num <= count:
                tutorial_sum += num
                tutorial_numbers.append(num)
        lecture_sum = 0
        lecture_numbers = []
        while lecture_sum < count and len(lecture_numbers) < lecture_count:
            num = random.randint(0, min(50, count - lecture_sum))
            lecture_sum += num
            lecture_numbers.append(num)
        if count > 1:
            add_seminar_or_lab = random.choice(["Seminar", "Lab"])
            if add_seminar_or_lab == "Seminar":
                seminar_max = max_count - lecture_count - tutorial_count
                seminar_count = random.randint(1, min(2, seminar_max))
                seminar_sum = 0
                seminar_numbers = []
                while seminar_sum < count and len(seminar_numbers) < seminar_count:
                    num = random.randint(0, min(40, seminar_max))
                    if seminar_sum + num <= count:
                        seminar_sum += num
                        seminar_numbers.append(num)
                while lecture_count + tutorial_count + seminar_count > max_count or seminar_sum > count:
                    if seminar_count > 1:
                        seminar_count -= 1
                        seminar_numbers = seminar_numbers[:-1]
                        seminar_sum = sum(seminar_numbers)
                    elif tutorial_count > 1:
                        tutorial_count -= 1
                    elif lecture_count > 1:
                        lecture_count -= 1
                electSem2Value_counts_dict[value] = {
                    'count': count,
                    'Lecture': lecture_numbers,
                    'Tutorial': tutorial_numbers,
                    'Seminar': list(seminar_numbers),
                }
            else:
                lab_max = min(max_count - lecture_count - tutorial_count, 100)
                lab_count = random.randint(1, min(2, lab_max))
                lab_sum = 0
                lab_numbers = []
                while lab_sum < count and len(lab_numbers) < lab_count:
                    num = random.randint(0, min(40, lab_max))
                    if lab_sum + num <= count:
                        lab_sum += num
                        lab_numbers.append(num)
                while lecture_count + tutorial_count + lab_count > max_count or lab_sum > count:
                    if lab_count > 1:
                        lab_count -= 1
                        lab_numbers = lab_numbers[:-1]
                        lab_sum = sum(lab_numbers)
                    elif tutorial_count > 1:
                        tutorial_count -= 1
                    elif lecture_count > 1:
                        lecture_count -= 1
                electSem2Value_counts_dict[value] = {
                    'count': count,
                    'Lecture': lecture_numbers,
                    'Tutorial': tutorial_numbers,
                    'Lab': list(lab_numbers),
                }
        else:
            lecture_numbers = list(np.random.randint(0, min(50, lecture_count), size=lecture_count)) if lecture_count > 2 else list(np.random.randint(0, 100, size=lecture_count))
            while sum(lecture_numbers) > count:
                lecture_numbers.pop()
            electSem2Value_counts_dict[value] = {
                'count': count,
                'Lecture': lecture_numbers,
                'Tutorial': tutorial_numbers,
            }


    for value, data in electSem2Value_counts_dict.items():
        writer.writerows([
                [f"{value} : {data}"]
                ])
            

    # create a dictionary to store the counts of each unique value
    coreSummerValue_counts_dict = {}

    # create a dictionary to store the counts of how many times each value in the search list is found in the same row as a unique value
    coreSummerSearch_counts_dict = {}

    # specify the name of the other column to search for values in
    search_column = 'major'

    # create a set of values to search for in the search column
    search_values = {'COMP', 'INFO', 'SWEN'}



    # iterate over each row in the dataframe and update the coreSummerValue_counts_dict and coreSummerSearch_counts_dict dictionaries
    for i, row in df.iterrows():
        if not pd.isna(row[count_column5]):
            values = row[count_column5].split(',')
            for value in values:
                if value in coreSummerValue_counts_dict:
                    coreSummerValue_counts_dict[value] += 1
                else:
                    coreSummerValue_counts_dict[value] = 1
                if row[search_column] in search_values:
                    if value in coreSummerSearch_counts_dict:
                        coreSummerSearch_counts_dict[value][row[search_column]] += 1
                    else:
                        coreSummerSearch_counts_dict[value] = {}
                        for search_value in search_values:
                            coreSummerSearch_counts_dict[value][search_value] = 0
                        coreSummerSearch_counts_dict[value][row[search_column]] = 1

    # Add Lecture, Tutorial, Seminar, and Lab random whole numbers

    # get the first key-value pair from coreSummerValue_counts_dict
    max_count = list(coreSummerValue_counts_dict.values())[0]

    for value, count in coreSummerValue_counts_dict.items():
        lecture_count = random.randint(1, 3)
        tutorial_max = max_count - lecture_count
        tutorial_count = random.randint(1, min(9, tutorial_max))
        tutorial_sum = 0
        tutorial_numbers = []
        while tutorial_sum < count and len(tutorial_numbers) < tutorial_count:
            num = random.randint(0, min(40, tutorial_max))
            if tutorial_sum + num <= count:
                tutorial_sum += num
                tutorial_numbers.append(num)
        lecture_sum = 0
        lecture_numbers = []
        while lecture_sum < count and len(lecture_numbers) < lecture_count:
            num = random.randint(0, min(50, count - lecture_sum))
            lecture_sum += num
            lecture_numbers.append(num)
        if count > 1:
            add_seminar_or_lab = random.choice(["Seminar", "Lab"])
            if add_seminar_or_lab == "Seminar":
                seminar_max = max_count - lecture_count - tutorial_count
                seminar_count = random.randint(1, min(2, seminar_max))
                seminar_sum = 0
                seminar_numbers = []
                while seminar_sum < count and len(seminar_numbers) < seminar_count:
                    num = random.randint(0, min(40, seminar_max))
                    if seminar_sum + num <= count:
                        seminar_sum += num
                        seminar_numbers.append(num)
                while lecture_count + tutorial_count + seminar_count > max_count or seminar_sum > count:
                    if seminar_count > 1:
                        seminar_count -= 1
                        seminar_numbers = seminar_numbers[:-1]
                        seminar_sum = sum(seminar_numbers)
                    elif tutorial_count > 1:
                        tutorial_count -= 1
                    elif lecture_count > 1:
                        lecture_count -= 1
                coreSummerValue_counts_dict[value] = {
                    'count': count,
                    'Lecture': lecture_numbers,
                    'Tutorial': tutorial_numbers,
                    'Seminar': list(seminar_numbers),
                }
            else:
                lab_max = min(max_count - lecture_count - tutorial_count, 100)
                lab_count = random.randint(1, min(2, lab_max))
                lab_sum = 0
                lab_numbers = []
                while lab_sum < count and len(lab_numbers) < lab_count:
                    num = random.randint(0, min(40, lab_max))
                    if lab_sum + num <= count:
                        lab_sum += num
                        lab_numbers.append(num)
                while lecture_count + tutorial_count + lab_count > max_count or lab_sum > count:
                    if lab_count > 1:
                        lab_count -= 1
                        lab_numbers = lab_numbers[:-1]
                        lab_sum = sum(lab_numbers)
                    elif tutorial_count > 1:
                        tutorial_count -= 1
                    elif lecture_count > 1:
                        lecture_count -= 1
                coreSummerValue_counts_dict[value] = {
                    'count': count,
                    'Lecture': lecture_numbers,
                    'Tutorial': tutorial_numbers,
                    'Lab': list(lab_numbers),
                }
        else:
            lecture_numbers = list(np.random.randint(0, min(50, lecture_count), size=lecture_count)) if lecture_count > 2 else list(np.random.randint(0, 100, size=lecture_count))
            while sum(lecture_numbers) > count:
                lecture_numbers.pop()
            coreSummerValue_counts_dict[value] = {
                'count': count,
                'Lecture': lecture_numbers,
                'Tutorial': tutorial_numbers,
            }


    for value, data in coreSummerValue_counts_dict.items():
        writer.writerows([
                [f"{value} : {data}"]
                ])
            
