import pandas as pd 
import csv



###Attempt 1
#usecols=['CoreCourses_Sem1']

#df= pd.read_csv('MockData.csv')

#sepList=[]

#sepList = df['CoreCourses_Sem1'].str.split(',')

#print(sepList.unique())
#print(df.CoreCourses_Sem1.unique())
#print(df.CoreCourses_Sem2.unique())
#print(df.Electivesminor_Sem1.unique())
#print(pd.unique(df['Electivesminor_Sem1']))
#print(df.Electivesminor_Sem2.unique())
#print(df.CoreCourses_Summer.unique())


### Attempt 2
#csv_path = "MockData.csv"
#column_name = "CoreCourses_Sem1"

#df = pd.read_csv(csv_path)

#new_df = df[column_name].str.split(',', expand=True).stack().reset_index(level=1, drop=True).to_frame('value')

#unique_count = new_df['value'].nunique()

#print(new_df)

#print(f"There are {unique_count} unique values in the {column_name} column.")


###Attempt 3

#df = pd.read_csv("MockData.csv")
#column_name = "CoreCourses_Sem1"
#major = "major"
#search_values = ['COMP', 'INFO', 'SWEN']

# create an empty dictionary to store the counts of each unique value
#value_counts = {}

# iterate over each row in the specified column and update the value_counts dictionary
#for row in df[column_name]:
    #values = row.split(',')
    #for value in values:
        #if value.strip() in value_counts:
            #value_counts[value.strip()] += 1
        #else:
            #value_counts[value.strip()] = 1
            

# print out the counts of each unique value
#for value, count in value_counts.items():
    #print(value, count)
    

###Attempt 4
#df = pd.read_csv("MockData.csv")

# specify the name of the column to count unique values in
#count_column = 'CoreCourses_Sem1'

# create a dictionary to store the counts of each unique value
#value_counts = {}

# iterate over each row in the dataframe and update the value_counts dictionary
#for i, row in df.iterrows():
    #values = row[count_column].split(',')
    #for value in values:
        #if value in value_counts:
            #value_counts[value] += 1
        #else:
            #value_counts[value] = 1

# create a list of values to search for in the other column
#search_values = ['COMP', 'INFO', 'SWEN']

# specify the name of the other column to search for values in
#search_column2 = 'major'

# iterate over each row in the dataframe and check if any of the search values are in the search column for each unique value
#for value in value_counts.keys():
    #for i, row in df.iterrows():
        #if value in row[count_column]:
            #if row[search_column2] in search_values:
                #print(value, "found in", count_column, "and", row[search_column2], "found in", search_column2, "for row", i)

# print out the unique values and their counts in the count column
#print("Unique values and counts in", count_column, ":")
#for value, count in value_counts.items():
    #print(value, ":", count)  
    
    
###Attempt 5
    
#df = pd.read_csv('MockData.csv')

# specify the name of the column to count unique values in
#count_column = 'CoreCourses_Sem1'

# create a dictionary to store the counts of each unique value
#value_counts = {}

# create a dictionary to store the counts of how many times each value in the search list is found in the same row as a unique value
#search_counts = {}

# specify the name of the other column to search for values in
#search_column = 'major'

# create a set of values to search for in the search column
#search_values = {'COMP', 'INFO', 'SWEN'}

# iterate over each row in the dataframe and update the value_counts and search_counts dictionaries
#for i, row in df.iterrows():
    #values = row[count_column].split(',')
    #for value in values:
        #if value in value_counts:
            #value_counts[value] += 1
        #else:
            #value_counts[value] = 1
        #if row[search_column] in search_values:
            #if value in search_counts:
                #search_counts[value] += 1
            #else:
                #search_counts[value] = 1

# print out the unique values and their counts in the count column, as well as how many times each value in the search list was found in the same row as each unique value
#print("Unique values and counts in", count_column, ":")
#for value, count in value_counts.items():
    #search_value_counts = {}
    #for search_value in search_values:
        #search_value_counts[search_value] = 0
    #if value in search_counts:
        #search_value_counts[row[search_column]] = search_counts[value]
    #print(value, ":", count, "(", search_value_counts, "with a value in", search_column, ")")



###Attempt 6
###CoreCoursesSem1
sourceFile = '2022.csv'
df = pd.read_csv(f'{sourceFile}')

# specify the name of the column to count unique values in
count_column1 = 'CoreCourses_Sem1'
count_column2 = 'CoreCourses_Sem2'
count_column3 = 'Electivesminor_Sem1'
count_column4 = 'Electivesminor_Sem2'
count_column5 = 'CoreCourses_Summer'

# create a dictionary to store the counts of each unique value
value_counts = {}

# create a dictionary to store the counts of how many times each value in the search list is found in the same row as a unique value
search_counts = {}

# specify the name of the other column to search for values in
search_column = 'major'

# create a set of values to search for in the search column
search_values = {'COMP', 'INFO', 'SWEN'}

# iterate over each row in the dataframe and update the value_counts and search_counts dictionaries
for i, row in df.iterrows():
    values = row[count_column1].split(',')
    for value in values:
        if value in value_counts:
            value_counts[value] += 1
        else:
            value_counts[value] = 1
        if row[search_column] in search_values:
            if value in search_counts:
                search_counts[value][row[search_column]] += 1
            else:
                search_counts[value] = {}
                for search_value in search_values:
                    search_counts[value][search_value] = 0
                search_counts[value][row[search_column]] = 1

file_name = f'courseData-{sourceFile}'
with open(file_name, mode='w', newline='') as file:
    # Create a CSV writer object
    writer = csv.writer(file)

    # print out the unique values and their counts in the count column, as well as how many times each value in the search list was found in the same row as each unique value
    print("Unique values and counts in", count_column1, ":")
    for value, count in value_counts.items():
        search_value_counts = search_counts[value]
        print(value, ":", count, "(", search_value_counts, "with a value in", search_column, "in this semester", count_column1, ")")
        
        writer.writerows([
            [value,count,search_value_counts]
            ])



    ####Core Courses Sem 2

    # iterate over each row in the dataframe and update the value_counts and search_counts dictionaries
    for i, row in df.iterrows():
        values = row[count_column2].split(',')
        for value in values:
            if value in value_counts:
                value_counts[value] += 1
            else:
                value_counts[value] = 1
            if row[search_column] in search_values:
                if value in search_counts:
                    search_counts[value][row[search_column]] += 1
                else:
                    search_counts[value] = {}
                    for search_value in search_values:
                        search_counts[value][search_value] = 0
                    search_counts[value][row[search_column]] = 1

    # print out the unique values and their counts in the count column, as well as how many times each value in the search list was found in the same row as each unique value
    print("Unique values and counts in", count_column2, ":")
    for value, count in value_counts.items():
        search_value_counts = search_counts[value]
        print(value, ":", count, "(", search_value_counts, "with a value in", search_column, "in this semester", count_column2, ")")
        
        writer.writerows([
            [value,count,search_value_counts]
            ])




    ####Electives Minor Sem 1
    # iterate over each row in the dataframe and update the value_counts and search_counts dictionaries
    for i, row in df.iterrows():
        values = row[count_column3].split(',')
        for value in values:
            if value in value_counts:
                value_counts[value] += 1
            else:
                value_counts[value] = 1
            if row[search_column] in search_values:
                if value in search_counts:
                    search_counts[value][row[search_column]] += 1
                else:
                    search_counts[value] = {}
                    for search_value in search_values:
                        search_counts[value][search_value] = 0
                    search_counts[value][row[search_column]] = 1

    # print out the unique values and their counts in the count column, as well as how many times each value in the search list was found in the same row as each unique value
    print("Unique values and counts in", count_column3, ":")
    for value, count in value_counts.items():
        search_value_counts = search_counts[value]
        print(value, ":", count, "(", search_value_counts, "with a value in", search_column, "in this semester", count_column3, ")")
        
        writer.writerows([
            [value,count,search_value_counts]
            ])


    ####Electives Minor Sem 2
    # iterate over each row in the dataframe and update the value_counts and search_counts dictionaries
    for i, row in df.iterrows():
        values = row[count_column4].split(',')
        for value in values:
            if value in value_counts:
                value_counts[value] += 1
            else:
                value_counts[value] = 1
            if row[search_column] in search_values:
                if value in search_counts:
                    search_counts[value][row[search_column]] += 1
                else:
                    search_counts[value] = {}
                    for search_value in search_values:
                        search_counts[value][search_value] = 0
                    search_counts[value][row[search_column]] = 1

    # print out the unique values and their counts in the count column, as well as how many times each value in the search list was found in the same row as each unique value
    print("Unique values and counts in", count_column4, ":")
    for value, count in value_counts.items():
        search_value_counts = search_counts[value]
        print(value, ":", count, "(", search_value_counts, "with a value in", search_column, "in this semester", count_column4, ")")
        
        writer.writerows([
            [value,count,search_value_counts]
            ])


        
        
    ####Electives Summer Courses
    # iterate over each row in the dataframe and update the value_counts and search_counts dictionaries
    for i, row in df.iterrows():
        if not pd.isna(row[count_column5]):
            values = row[count_column5].split(',')
        if row[search_column] in search_values:
            for value in values:
                if value in value_counts:
                    value_counts[value] += 1
                else:
                    value_counts[value] = 1
                if value:
                    if value in search_counts:
                        search_counts[value][row[search_column]] += 1
                    else:
                        search_counts[value] = {search_value: 0 for search_value in search_values}
                        search_counts[value][row[search_column]] = 1


    # print out the unique values and their counts in the count column, as well as how many times each value in the search list was found in the same row as each unique value
    print("Unique values and counts in", count_column5, ":")
    for value, count in value_counts.items():
        search_value_counts = {}
        for search_value in search_values:
            search_value_counts[search_value] = 0
        if value in search_counts:
            for search_value, search_count in search_counts[value].items(): # iterate over the items of the dictionary
                search_value_counts[search_value] = search_count
        print(value, ":", count, "(", search_value_counts, "with a value in", search_column, "in this semester", count_column5, ")")

        writer.writerows([
            [value,count,search_value_counts]
            ])


    