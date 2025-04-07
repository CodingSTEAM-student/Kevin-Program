with open("day2/inputs.txt","r") as file: 
    contents = file.read()
 

reports = [ ]
for line in contents.splitlines():
    report = [int(n) for n in line.split()]
    reports.append(report)

def validation(report:list):
    if report[0] > report[1]:
        increasing = False 
    else: 
        increasing =True
    for i in range(0, len(report)-1):
        distance = abs(report[i+1] - report[i])
        if distance > 3 or distance == 0: 
            return False
        if increasing and report[i+1] - report[i] < 0: 
            return False
        if not increasing and  report[i+1] - report[i] > 0: 
            return False
    return True
# print(*reports)
validcount = 0
for report in reports:
    print(report)
    if validation(report):
        validcount += 1

print(validcount)

 

