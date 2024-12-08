# Prase config.json file and check if the values can be used in the index file
#imports
import json
import re

# Regular Expression patterns
PatternRGB = r"^\(\d{1,3},\s*\d{1,3},\s*\d{1,3}\)$"

# Variables
Invalid = 0

# open the file
with open("config.json") as jsonFile:
    Configuration = json.load(jsonFile)

# Sort the data
WindowConf = Configuration["Window"]
Colors = Configuration["Colors"]

BoardSize = WindowConf["BoardSize"]
WinSize = WindowConf["WinSize"]
WindowScale = WindowConf["Scale"]

BackgroundColor = eval(Colors["Background"])
LineColor = eval(Colors["Lines"])
CircleColor = eval(Colors["Circle"])
XColor = eval(Colors["X"])

# Make sure the Data is Valid
def ValidateColor(ValueRGB, Name):
    ValueRGB = str(ValueRGB)
    # Validate if there are 3 numbers between 0-999 seperated by a comma
    if re.match(PatternRGB, ValueRGB):
        # Validate if the 3 numbers are between 0 and 255
        ValueRGB = ValueRGB[1:-1]
        Values = [int(x.strip()) for x in ValueRGB.split(',')]
        Check = all(0 <= Value <= 255 for Value in Values)
        if Check:
            print("✓", Name)
            return True
    print("x", Name, "is not a valid RGB pattern")
    return False

def ValidateInt(Value, Name):
    if type(Value) == int:
        print("✓", Name)
        return True
    print("x", Name, "is not an Integer")
    return False

def ValidateFloatAndInt(Value, Name):
    if type(Value) == float or type(Value) == int:
        print("✓", Name)
        return True
    print("x", Name, "is not a Float or Integer")
    return False
    
# Validate all values
print("Making sure all Values in 'config.json' are valid..")
if not ValidateInt(BoardSize, Name = "BoardSize"): Invalid += 1
if not ValidateInt(WinSize, Name = "WinSize"): Invalid += 1
if not ValidateFloatAndInt(WindowScale, Name = "Scale"): Invalid += 1

if WinSize <= BoardSize: print("✓", "Game is possible")
else: 
    print("x", "Game is impossible") 
    Invalid += 1

if not ValidateColor(BackgroundColor, Name = "Background"): Invalid += 1
if not ValidateColor(LineColor, Name = "Lines"): Invalid += 1
if not ValidateColor(CircleColor, Name = "Circle"): Invalid += 1
if not ValidateColor(XColor, Name = "X"): Invalid += 1

#Scale the size Variables
SquareSize = int(200 * WindowScale)
CircleRadius = int(60 * WindowScale)
LineWidth = int(20 * WindowScale)
ScreenSize = int(BoardSize * SquareSize)
offset = int(55 * WindowScale)

# Conclusion
print(f"Found {Invalid} invalid values in 'config.json'.")
if Invalid > 0:
    print("Quitting..")
    quit()