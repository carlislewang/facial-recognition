"""
Reads in a csv file
Takes three parameters: 
1. The name of the file
2. An empty list to hold the header attributes
3. An empty list to hold the values of the instances

When done:
- attributes will be a 1-D array, each instance is the name of an attribute
- instances will be a list of lists (2-D array):
  - each row is one instance (instances[0])
  - each column is the value of the nth attribute in that instance (instance[0][2])

Some complications:
Excel exports the files with a "\r" rather than a "\n" as the end of line symbol
"""
def parseCSV(filename, attributes, instances):
    # We need to open in binary because Excel exports a csv with "\r" newlines
    infile = open(filename, "rU")
    header = ""
    linenum = 0
    current_minute = 0
    for line in infile:
        if linenum < 8:  # still in the header
            line = line.strip()  # strip off whitespace
            header += line + " "
            if linenum == 7:  # end of header
                # build up the attributes array.
                features = header.split(",")
                attributes.append(features[0])
                attributes.append(features[1])
                attributes.append(features[2]+features[3])
        else:
            instances.append([]) # new row
            features = line.split(",")
            minute = 0
            if features[0] != "": # minute column
                minute = int(features[0])
            # Make sure that the minute column is updated
            if (minute > current_minute):
                current_minute = minute
            else:
                minute = current_minute
            seconds = int(features[1])
            frame = (minute*60+seconds)*30  # 30 fps
            #print "%d"%(int(frame))
            instances[len(instances)-1].append(frame)
            instances[len(instances)-1].append(minute)
            instances[len(instances)-1].append(int(features[1])) # seconds
            instances[len(instances)-1].append(features[2]) # affect
        linenum += 1
    infile.close()
            
"""
Prints out the attribute values for one given instance.
Just as a demo to show how the instances work
"""
def printInstance(attributes, instances, instance_num):
    # if instance_num > len(instances):
    #     print "No such instance!"
    #     return
    # print attributes
    # print "%d, %d"%(len(attributes), len(instances[instance_num]))
    # if len(attributes) != len(instances[instance_num]):
    #     print "Wrong number of attributes!"
    #     return

    # for i in range(len(attributes)):
    #     print "%s. %s: %s"%(str(i), attributes[i], str(instances[instance_num][i]))
    print instances[1]

def main():
    filename = "./data/Alpaca/realtime.csv"
    attributes = []  # empty array
    instances = []
    parseCSV(filename, attributes, instances)
    # print one out just to check
    printInstance(attributes, instances, 0)

# Put this in so that we can use it as a module
if __name__ == "__main__":
    main()
