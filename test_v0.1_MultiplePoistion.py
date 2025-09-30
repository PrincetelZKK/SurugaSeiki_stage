#%%
import pythonnet 
pythonnet.load("coreclr")

import clr
clr.AddReference("srgmc")
import SurugaSeiki.Motion
import time

start_time = time.time()
    # Your code here

# print(dir(SurugaSeiki.Motion))

alignmentSystem = SurugaSeiki.Motion.System.Instance
# Showing DLL version and starting ADS communication to a target controller
# Change the following ADS address according to an actual target controller.
print(alignmentSystem.DllVersion)

alignmentSystem.SetAddress("5.153.34.236.1.1")
print(alignmentSystem.Connected)

#%%
AxisComponents = {}
for axisNumber in range(1,7):
    AxisComponents[axisNumber] = SurugaSeiki.Motion.AxisComponents(axisNumber)
XTargetPosition: float
YTargetPosition: float

# AxisComponents[1].TurnOffServo()

# Creating an Axis2D class instance for axis 7 and 8.
Axis2D = SurugaSeiki.Motion.Axis2D(1,2)

# Creating an Alignment class instance
Alignment = SurugaSeiki.Motion.Alignment()
FlatAlignmentParameter = SurugaSeiki.Motion.Alignment.FlatParameter()
SingleAlignmentParameter = SurugaSeiki.Motion.Alignment.SingleParameter()
# FocusAlignmentParameter = SurugaSeiki.Motion.Alignment.FocusParameter()

#%% test different algorithms
# Set flat alignment parameters
def SetXTyAlignmentParameterFine(FlatAlignmentParameter):
    FlatAlignmentParameter.mainStageNumberX = 1
    FlatAlignmentParameter.mainStageNumberY = 5
    FlatAlignmentParameter.subStageNumberXY = 0
    FlatAlignmentParameter.subAngleX = 0
    FlatAlignmentParameter.subAngleY = 0
    FlatAlignmentParameter.pmCh = 1
    FlatAlignmentParameter.analogCh = 1
    FlatAlignmentParameter.pmAutoRangeUpOn = True
    FlatAlignmentParameter.pmInitRangeSettingOn = True
    FlatAlignmentParameter.pmInitRange = -10
    FlatAlignmentParameter.fieldSearchThreshold = 0.1
    FlatAlignmentParameter.peakSearchThreshold = 5
    FlatAlignmentParameter.searchRangeX = 1000
    FlatAlignmentParameter.searchRangeY = 10
    FlatAlignmentParameter.fieldSearchPitchX = 10
    FlatAlignmentParameter.fieldSearchPitchY = 0.01
    FlatAlignmentParameter.fieldSearchFirstPitchX = 0
    FlatAlignmentParameter.fieldSearchSpeedX = 500
    FlatAlignmentParameter.fieldSearchSpeedY = 1
    FlatAlignmentParameter.peakSearchSpeedX = 10
    FlatAlignmentParameter.peakSearchSpeedY = 0.5
    FlatAlignmentParameter.smoothingRangeX = 30
    FlatAlignmentParameter.smoothingRangeY = 30
    FlatAlignmentParameter.centroidThresholdX = 5
    FlatAlignmentParameter.centroidThresholdY = 5
    FlatAlignmentParameter.convergentRangeX = 0.5
    FlatAlignmentParameter.convergentRangeY = 0.1
    FlatAlignmentParameter.comparisonCount = 1
    FlatAlignmentParameter.maxRepeatCount = 5


def SetYTxAlignmentParameterFine(FlatAlignmentParameter):
    FlatAlignmentParameter.mainStageNumberX = 2
    FlatAlignmentParameter.mainStageNumberY = 4
    FlatAlignmentParameter.subStageNumberXY = 0
    FlatAlignmentParameter.subAngleX = 0
    FlatAlignmentParameter.subAngleY = 0
    FlatAlignmentParameter.pmCh = 1
    FlatAlignmentParameter.analogCh = 1
    FlatAlignmentParameter.pmAutoRangeUpOn = True
    FlatAlignmentParameter.pmInitRangeSettingOn = True
    FlatAlignmentParameter.pmInitRange = -10
    FlatAlignmentParameter.fieldSearchThreshold = 0.1
    FlatAlignmentParameter.peakSearchThreshold = 1
    FlatAlignmentParameter.searchRangeX = 200
    FlatAlignmentParameter.searchRangeY = 1
    FlatAlignmentParameter.fieldSearchPitchX = 1
    FlatAlignmentParameter.fieldSearchPitchY = 0.01
    FlatAlignmentParameter.fieldSearchFirstPitchX = 0
    FlatAlignmentParameter.fieldSearchSpeedX = 5
    FlatAlignmentParameter.fieldSearchSpeedY = 0.1
    FlatAlignmentParameter.peakSearchSpeedX = 10
    FlatAlignmentParameter.peakSearchSpeedY = 0.01
    FlatAlignmentParameter.smoothingRangeX = 30
    FlatAlignmentParameter.smoothingRangeY = 30
    FlatAlignmentParameter.centroidThresholdX = 5
    FlatAlignmentParameter.centroidThresholdY = 5
    FlatAlignmentParameter.convergentRangeX = 0.5
    FlatAlignmentParameter.convergentRangeY = 0.1
    FlatAlignmentParameter.comparisonCount = 1
    FlatAlignmentParameter.maxRepeatCount = 5




#%% 
# from AlignmentParameters import SetXYAlignmentParameter

firstTimeConnected = False
isAlignment = False
# alignmentSystem.SetAddress("169.254.118.27")
DOF = 6

TxZeroPosition = 0.0

position_label = ("X", 'Y', "Z", "Tx", "Ty", "Tz")


def ShowPosition(position_label, AxisComponents, DOF=6):
    for n in range(DOF):
        print(f'{position_label[n]} position: {AxisComponents[n+1].GetActualPosition()}')
    print("=====================================")

def MoveToPositionBefore(AxisComponents, PositionsBefore):
    for i in range(DOF):
        AxisComponents[i+1].MoveAbsolute(PositionsBefore[i])
        time.sleep(0.5)
        while AxisComponents[i+1].IsMoving():
            time.sleep(0.5)
    print("Move back to Old Position")

def ReturnCurrentPosition(AxisCompoments):
    CurrentPosition = []
    for i in range(DOF):
        CurrentPosition.append(AxisComponents[i+1].GetActualPosition())
    return CurrentPosition

def FourAxisAlignment(FlatAlignmentParameter, Alignment):
    print("Tune Y and Tx")
    # Y and Tx angle 
    SetYTxAlignmentParameter(FlatAlignmentParameter)
    Alignment.SetMeasurementWaveLength(FlatAlignmentParameter.pmCh, 1310)
    Alignment.SetFlat(FlatAlignmentParameter)
    Alignment.StartFlat()
    time.sleep(1)
    while str(Alignment.GetStatus()) != "Success":
        time.sleep(3)

    # X and Ty angle 
    print("Tune X and Ty")
    SetXTyAlignmentParameter(FlatAlignmentParameter)
    Alignment.SetMeasurementWaveLength(FlatAlignmentParameter.pmCh, 1310)
    Alignment.SetFlat(FlatAlignmentParameter)
    Alignment.StartFlat()
    time.sleep(1)
    while str(Alignment.GetStatus()) != "Success":
        time.sleep(3)

def FourAxisAlignmentFine(FlatAlignmentParameter, Alignment):
    print("Tune Y and Tx")
    # Y and Tx angle 
    SetYTxAlignmentParameterFine(FlatAlignmentParameter)
    Alignment.SetMeasurementWaveLength(FlatAlignmentParameter.pmCh, 1310)
    Alignment.SetFlat(FlatAlignmentParameter)
    Alignment.StartFlat()
    time.sleep(1)
    while str(Alignment.GetStatus()) != "Success":
        time.sleep(3)

    # X and Ty angle 
    print("Tune X and Ty")
    SetXTyAlignmentParameterFine(FlatAlignmentParameter)
    Alignment.SetMeasurementWaveLength(FlatAlignmentParameter.pmCh, 1310)
    Alignment.SetFlat(FlatAlignmentParameter)
    Alignment.StartFlat()
    time.sleep(1)
    while str(Alignment.GetStatus()) != "Success":
        time.sleep(3)

def SavePosition(CurrentPosition):


# print(Alignment.GetStatus())

while True:
        if alignmentSystem.Connected == True:
            if firstTimeConnected == False:
                firstTimeConnected = True
                # Showing the system version of the target controller once after connection success
                print(alignmentSystem.SystemVersion)
                
                # initial position
                print("Initial Posion and Power meter numbers: ")
                ShowPosition(position_label, AxisComponents)

                for axisComponent in AxisComponents.items():
                # Turning on servo controls if servo controls are off for each axes
                    if axisComponent[1].IsServoOn() == False:
                        axisComponent[1].TurnOnServo()
                        # print(AxisComponents[1].IsServoOn())
                
                # start position
                # CurrentPosition = ReturnCurrentPosition(AxisComponents)

                #  #### flat alignment 
                # # set
                while firstTimeConnected :
                    print("Rotate Rotor Side, ")
                    FourAxisAlignmentFine(FlatAlignmentParameter, Alignment)
                    print(Alignment.GetPower(FlatAlignmentParameter.pmCh))


                    CurrentPosition = ReturnCurrentPosition(AxisComponents)
                    

                    print(Alignment.GetPower(FlatAlignmentParameter.pmCh))
                    ShowPosition(position_label, AxisComponents)
                    break
                break
        else:
            print("Ads not connected")
            time.sleep(1)

print("Well done")
print("Laser Power:", Alignment.GetPower(FlatAlignmentParameter.pmCh))

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Running Time: {elapsed_time / 60} minutes")