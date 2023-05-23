import csv

sourceFile = '2021.csv'

csList =[]
file_name = f'courseData-{sourceFile}'
f_write = f'only_2_duplicate_{sourceFile}'

coursedict = {}
with open(file_name, mode='r', newline='') as file:
    # Create a CSV writer object
    reader = csv.reader(file)

    # Read the remaining rows
    rows = [row for row in reader]

with open(f_write,mode= 'w',newline='') as file_write:
    writer = csv.writer(file_write)
    for row in rows:
        row[0] = row[0].strip()

        if row[0] in coursedict:
            if coursedict[row[0]] >=2:
                pass
            else:
                coursedict[row[0]] +=1
                writer.writerows([
                [row[0],row[1],row[2]]
                ])
        else:
            coursedict[row[0]] = 1
            writer.writerows([
                [row[0],row[1],row[2]]
                ])




           
# print(header)
# print(rows)
