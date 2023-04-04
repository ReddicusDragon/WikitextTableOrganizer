import os,sys
def ascend_sort(data):
    return sorted(data)

def descend_sort(data):
    return sorted(data, reverse = True)

if not os.path.isfile(os.path.join(os.path.realpath(os.path.dirname(__file__)),"input.txt")):
    print("InputFile not exist. Exiting.")
    sys.exit()
print("A - sort ascending")
print("B - sort descending")
choice = input("Enter choice, or 'exit' to quit:")
while not choice in ("a","b","exit"):
    print("Invalid choice '{0}'".format(choice))
    choice = input("Enter choice, or 'exit' to quit:")

if choice == "exit":
    print("Abort")
    sys.exit()

#main logic
stringToSort = ""
with open("input.txt","r") as myfi:
    for line in myfi.readlines():
        stringToSort += line

stringToSort.replace("\r\n","\n")
#now we divide based on wikilang
tempstring = ""
tableContentStart = ""
unsortedTables = []
tableStart = False
tableDoStart = False
amSorting = False
for element in range(0, len(stringToSort)):
    try:
        if stringToSort[element] == "{":
            if stringToSort[element + 1] == "|":
                if stringToSort[element + 2:element + 20] == " class=\"wikitable\"":
                    print("Found start of table")
                    tableStart = True
    except IndexError:
        pass

    #handle the !
    if stringToSort[element] == "!":
        if amSorting == False:
            amSorting = True
    
    # Did we hit the tableDoStart? If not, add our chars to tableContentStart
    if tableStart == True and tableDoStart == False:
        tableContentStart += stringToSort[element]
    #if we did, then we add it to the tempstring as 
    if tableStart == True and tableDoStart == True:
        if amSorting == True: # if we're sorting here we add to our temp string
            tempstring += stringToSort[element]

    

    try:
        if stringToSort[element] == "|":
            if stringToSort[element + 1] == "-":
                # did we find a valid table start? If so, did we hit the first |-?
                if tableStart == True and tableDoStart == False:
                    tableDoStart = True
                    tableContentStart += "-"
                elif tableStart == True and tableDoStart == True:
                    #sanity check
                    print(stringToSort[element + 3])
                    if stringToSort[element + 2] == "\n":
                        if stringToSort[element + 3] == "!" or (stringToSort[element + 3] == "|" and stringToSort[element + 4] == "}"):
                            # now we handle if we did do it
                            tempstring += "-"
                            # append this to the unsorted tables
                            unsortedTables.append(tempstring)
                            tempstring = "" # now we clear for the next table
                            amSorting = False #clear the sorting flag bc we filled out this table
    except IndexError:
        print("Error occurred.")
        raise

# hacky hack
data_e = unsortedTables[0]
data_e = data_e.replace("-","",1)
data_e = data_e.replace("\n","",1)
unsortedTables.pop(0)
unsortedTables.insert(0,data_e)
print(unsortedTables)
myOutput = tableContentStart + "\n"
if choice == "a":
    sortedTables = ascend_sort(unsortedTables)
    for item in sortedTables:
        myOutput += item + "\n"

if choice == "b":
    sortedTables = descend_sort(unsortedTables)
    for item in sortedTables:
        myOutput += item + "\n"

myOutput += "|}"
# output
with open("output.wiki","w") as myfi:
    myfi.write(myOutput)
