import os

def parseCSV(filePath):
    # check if the file exists
    if filePath == "q":
        print("Goodbye!")
        exit()
    elif not os.path.isfile(filePath):
        print(f"Error: The file '{filePath}' does not exist.")
        exit()

    # read the file and strip whitespace from each line
    with open(filePath, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    
    # parse the machine name and states
    machineName = lines[0]
    startState = lines[4]
    acceptState = lines[5]
    rejectState = lines[6]
    
    # parse the transitions
    transitions = [tuple(line.split(',')) for line in lines[7:]]
    
    return machineName, startState, acceptState, rejectState, transitions

def nextConfig(config, transitions):
    left, state, right = config
    head = right[0] if right else "_"
    nextConfigs = []
    
    # iterate through transitions to find applicable ones
    for (currState, inputChar, nextState, writeChar, moveDir) in transitions:
        if currState == state and inputChar == head:
            newLeft = left
            newRight = right[1:] if len(right) > 1 else ""
            
            # update the tape based on the move direction
            if moveDir == "R":
                newLeft += writeChar
            elif moveDir == "L":
                if newLeft:
                    newRight = newLeft[-1] + writeChar + newRight
                    newLeft = newLeft[:-1]
                else:
                    newRight = writeChar + newRight
            
            nextConfigs.append((newLeft, nextState, newRight))
    return nextConfigs

def ntm(acceptState, rejectState, transitions, config, maxDepth):
    tree = [[config]]
    depth = 0

    while depth < maxDepth:
        currLevel = tree[-1]
        nextLevel = []

        if depth == 0:
            print("Initial Configuration:")
        else:
            print(f"Depth {depth}:")
        for config in currLevel:
            left, state, right = config
            head = right[0] if right else "_"
            left_display = left if left else "_"
            print(f"  {left_display}, {state}, {head}, {right[1:] if len(right) > 1 else '_'}")
            
            # check if the current state is the accept state
            if state == acceptState:
                print(f"String accepted in {depth} steps!")
                return
            # check if the current state is not the reject state
            elif state != rejectState:
                nextLevel.extend(nextConfig(config, transitions))
        
        # if no next level configurations, reject the string
        if not nextLevel:
            print()
            print(f"String rejected in {depth} steps!")
            return

        tree.append(nextLevel)
        depth += 1
    
    print(f"Execution stopped after max depth of {maxDepth}.")

def main():
    # loop while user wants to test more files
    while True:
        # get the file path from the user
        filePath = input("Enter the NTM CSV filename or q to quit: ")
        machineName, startState, acceptState, rejectState, transitions = parseCSV(filePath)
        
        print()
        print(f"Machine Name: {machineName}")
        print("=====================================")
        
        # loop ntm while user input is not empty
        while True:
            print("(press Enter to use a different test file or q to quit)")
            inputString = input("Enter the input string: ")
            if not inputString: 
                break
            elif inputString == "q":
                print("Goodbye!")
                exit()
            
            print()
            ntm(acceptState, rejectState, transitions, ("", startState, inputString), 100) # max depth of 100
            print("=====================================")
            print()

if __name__ == '__main__':
    main()