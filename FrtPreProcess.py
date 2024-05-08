class FrtPreProcess:
    
    #inicializalas
    def __init__(self):
        self.partCount = GetRootPart().Components.Count - 1# components count
        self.bigFlowImported = False

    def ImportBigFlow(self):
        try:
            self.bigFlowImported = True
            selections = BodySelection.Create(GetRootPart().Components[self.partCount].Content.Bodies[0])
            component = PartSelection.Create(GetRootPart())
            result = ComponentHelper.MoveBodiesToComponent(selections, component, False, None)
            #cut out bois
            selection = BodySelection.Create([GetRootPart().Components[self.partCount].Content.Bodies[0],
            GetRootPart().Components[self.partCount].Content.Bodies[1],
            GetRootPart().Components[self.partCount].Content.Bodies[2]])
            result = Cut.ToClipboard(selection)        
        except:
            print("Missing big flow space file")
    #aramlaster meghatarozasa ha nincs big flow space
  
    #alap NameSelectionok meghatarozasa    
    def GenerateStandartNameSelections(self):
        body = GetRootPart().Bodies[0] # a hasab
        length = len(body.Faces) # hasab surfacek hossza
        firstSymetry = True
        for i in range(length):
            primarySelection = FaceSelection.Create(GetRootPart().Bodies[0].Faces[i])
            secondarySelection = Selection.Empty()
            if i == 2:      
                result = NamedSelection.Create(primarySelection, secondarySelection, "inlet")
            elif i == 0:
                result = NamedSelection.Create(primarySelection, secondarySelection, "outlet")
            elif i == 3:
                result = NamedSelection.Create(primarySelection, secondarySelection, "ground")
            else:
               if firstSymetry:
                   firstSymetry = False
                   result = NamedSelection.Create(primarySelection, secondarySelection, "symmetry")
               else:
                   result = NamedSelection.Create(primarySelection, secondarySelection, "group")
                   result = NamedSelection.Merge("symmetry","group")
                    

    # kivagja az autot az aramlasi terbol
    def CutOutGeometry(self):
        for i in range(self.partCount):
            passed = False
            targets = BodySelection.Create(GetRootPart().Bodies[0])
            numberOfBodies = GetRootPart().Components[i].Content.Bodies.Count
            j = 0
            while j < numberOfBodies and passed == False:
                try:
                    tools = BodySelection.Create(GetRootPart().Components[i].Content.Bodies[j])
                    options = MakeSolidsOptions()
                    result = Combine.Intersect(targets, tools, options)
                    passed = True
                except:
                    print("")
                j = j + 1
                

    #beallitja a supress for physicset
    def SupressForPhysics(self):
        face_list = [GetRootPart().Components[index] for index in range(self.partCount)]
        selection = ComponentSelection.Create(face_list)
        supress = True
        ViewHelper.SetSuppressForPhysics(selection,supress)
    
    #smallFaces,extraEdges,splitEdges
    def Repair(self):
        result = FixSmallFaces.FindAndFix()
        result = FixExtraEdges.FindAndFix()
        result = FixSplitEdges.FindAndFix()

    def InsertBois(self):
        result = Paste.FromClipboard()
        
    def DeleteReferenceFlowSpace(self):
        selection = ComponentSelection.Create(GetRootPart().Components[self.partCount])
        result = Delete.Execute(selection)
               
## main program
frt = FrtPreProcess() 
# use ImportBigFlow() or GenerateWaterTightGeometry()
frt.ImportBigFlow() 
#frt.GenerateWaterTightGeometry()

frt.GenerateStandartNameSelections()
#frt.CutOutGeometry()
frt.SupressForPhysics()
#frt.Repair()
if frt.bigFlowImported:
    frt.InsertBois()
    frt.DeleteReferenceFlowSpace()
print("Pre processing terminated")
