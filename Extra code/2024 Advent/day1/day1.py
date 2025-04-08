# with open("day1/inputs.txt","r") as file:
#     content = file.read()  


# print(content)

# ids1 = []
# ids2 = []
# total = 0
# lines = content.splitlines()

# for line in lines:
#     num1, num2 = line.split("   ")
#     # print(line, "/", num1,"/", num2)
#     ids1.append(num1)
#     ids2.append(num2)

# ids1.sort()
# ids2.sort()

# for i in range(len(ids1)):
#     difference = abs(int(ids1[i])-int(ids2[i]))
#     total += difference

# print(total)
# part 2 
from collections import Counter
with open("day1/inputs.txt","r") as file:
    content = file.read()  


print(content)

ids1 = []
ids2 = []
total = 0
lines = content.splitlines()

for line in lines:
    num1, num2 = line.split("   ")
    # print(line, "/", num1,"/", num2)
    ids1.append(num1)
    ids2.append(num2)

totalSimilarity = 0
for i in ids1:
    count = ids2.count(i)
    score = count * int(i)
    totalSimilarity += score

print(totalSimilarity)