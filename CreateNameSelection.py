class NameSelection:
    def __init__(self, delete, name, a, r, g, b):
        self.name = name
        self.color = Color.FromArgb(a,r,g,b)
        self.first = True
        self.delete = delete

NameSelectionList = []
DeletedFaceList = []


##list of name selections
lower = NameSelection(False,"lower",255, 143, 175, 151)
upper = NameSelection(False,"upper",255, 175, 175, 143)
chassis_upper = NameSelection(False,"chassis_upper",255, 143, 143, 175)
edges = NameSelection(False,"edges",255, 143, 175, 143)
rw_plates = NameSelection(False,"rw_plates",255, 175, 174, 143)
front_wheel = NameSelection(False,"front_wheel",255, 169, 143, 175)
rear_wheel = NameSelection(False,"rear_wheel",255, 175, 161, 143)
motors = NameSelection(False,"motors",255, 30, 30, 30)
rods = NameSelection(False, "rods",255, 143, 171, 175)
#delete = NameSelection(True, "del",255, 175, 161, 143)
##### unused face ARGB 255, 175, 143, 143


NameSelectionList.append(lower)
NameSelectionList.append(upper)
NameSelectionList.append(chassis_upper)
NameSelectionList.append(edges)
NameSelectionList.append(rw_plates)
NameSelectionList.append(front_wheel)
NameSelectionList.append(rear_wheel)
NameSelectionList.append(motors)
NameSelectionList.append(rods)
#NameSelectionList.append(delete)


for nameSelection in NameSelectionList:
    componentsLength = GetRootPart().Components.Count
    for i in range(componentsLength):
        bodyList = GetRootPart().Components[i].GetAllBodies() # az i edik componensben minden body-t begyujtunk
        bodylistCount = bodyList.Count
        for j in range(bodylistCount):
            faceLength = bodyList[j].Faces.Count
            for k in range(faceLength):
                selection = FaceSelection.Create(bodyList[j].Faces[k])
                secondary = Selection.Empty()
                if ColorHelper.GetColor(selection) == nameSelection.color:          
                    if nameSelection.delete:
                       DeletedFaceList.append(selection)
                    elif nameSelection.first:
                        nameSelection.first = False
                        result = NamedSelection.Create(selection, secondary, nameSelection.name)
                    else:
                        result = NamedSelection.Create(selection, secondary, "group")
                        result = NamedSelection.Merge(nameSelection.name, "group")    
                        
for item in DeletedFaceList:
    try:
        Delete.Execute(item)
    except:
        print("")
    

print("Generating NameSelections terminated")    