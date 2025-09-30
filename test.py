#%%
import pythonnet 
pythonnet.load("coreclr")

import clr
clr.AddReference("srgmc")
import SurugaSeiki.Motion
import time

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
def SetXYAlignmentParameter(FlatAlignmentParameter):
    FlatAlignmentParameter.mainStageNumberX = 1
    FlatAlignmentParameter.mainStageNumberY = 2
    FlatAlignmentParameter.subStageNumberXY = 0
    FlatAlignmentParameter.subAngleX = 0
    FlatAlignmentParameter.subAngleY = 0
    FlatAlignmentParameter.pmCh = 1
    FlatAlignmentParameter.analogCh = 1
    FlatAlignmentParameter.pmAutoRangeUpOn = True
    FlatAlignmentParameter.pmInitRangeSettingOn = True
    FlatAlignmentParameter.pmInitRange = -40
    FlatAlignmentParameter.fieldSearchThreshold = 0.1
    FlatAlignmentParameter.peakSearchThreshold = 20
    FlatAlignmentParameter.searchRangeX = 50000
    FlatAlignmentParameter.searchRangeY = 50000
    FlatAlignmentParameter.fieldSearchPitchX = 100
    FlatAlignmentParameter.fieldSearchPitchY = 100
    FlatAlignmentParameter.fieldSearchFirstPitchX = 0
    FlatAlignmentParameter.fieldSearchSpeedX = 500
    FlatAlignmentParameter.fieldSearchSpeedY = 500
    FlatAlignmentParameter.peakSearchSpeedX = 10
    FlatAlignmentParameter.peakSearchSpeedY = 10
    FlatAlignmentParameter.smoothingRangeX = 30
    FlatAlignmentParameter.smoothingRangeY = 30
    FlatAlignmentParameter.centroidThresholdX = 5
    FlatAlignmentParameter.centroidThresholdY = 5
    FlatAlignmentParameter.convergentRangeX = 0.5
    FlatAlignmentParameter.convergentRangeY = 0.5
    FlatAlignmentParameter.comparisonCount = 2
    FlatAlignmentParameter.maxRepeatCount = 5

def SetXTyAlignmentParameter(FlatAlignmentParameter):
    FlatAlignmentParameter.mainStageNumberX = 1
    FlatAlignmentParameter.mainStageNumberY = 5
    FlatAlignmentParameter.subStageNumberXY = 0
    FlatAlignmentParameter.subAngleX = 0
    FlatAlignmentParameter.subAngleY = 0
    FlatAlignmentParameter.pmCh = 1
    FlatAlignmentParameter.analogCh = 1
    FlatAlignmentParameter.pmAutoRangeUpOn = True
    FlatAlignmentParameter.pmInitRangeSettingOn = False
    FlatAlignmentParameter.pmInitRange = -40
    FlatAlignmentParameter.fieldSearchThreshold = 0.1
    FlatAlignmentParameter.peakSearchThreshold = 20
    FlatAlignmentParameter.searchRangeX = 50000
    FlatAlignmentParameter.searchRangeY = 40
    FlatAlignmentParameter.fieldSearchPitchX = 100
    FlatAlignmentParameter.fieldSearchPitchY = 0.1
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

def SetXTyAlignmentParameter_SkipMin(FlatAlignmentParameter, FieldSearchVolt):
    FlatAlignmentParameter.mainStageNumberX = 1
    FlatAlignmentParameter.mainStageNumberY = 5
    FlatAlignmentParameter.subStageNumberXY = 0
    FlatAlignmentParameter.subAngleX = 0
    FlatAlignmentParameter.subAngleY = 0
    FlatAlignmentParameter.pmCh = 1
    FlatAlignmentParameter.analogCh = 1
    FlatAlignmentParameter.pmAutoRangeUpOn = True
    FlatAlignmentParameter.pmInitRangeSettingOn = False
    FlatAlignmentParameter.pmInitRange = -30
    FlatAlignmentParameter.fieldSearchThreshold = FieldSearchVolt
    FlatAlignmentParameter.peakSearchThreshold = 20
    FlatAlignmentParameter.searchRangeX = 50000
    FlatAlignmentParameter.searchRangeY = 40
    FlatAlignmentParameter.fieldSearchPitchX = 100
    FlatAlignmentParameter.fieldSearchPitchY = 0.1
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

def SetYTxAlignmentParameter(FlatAlignmentParameter):
    FlatAlignmentParameter.mainStageNumberX = 2
    FlatAlignmentParameter.mainStageNumberY = 4
    FlatAlignmentParameter.subStageNumberXY = 0
    FlatAlignmentParameter.subAngleX = 0
    FlatAlignmentParameter.subAngleY = 0
    FlatAlignmentParameter.pmCh = 1
    FlatAlignmentParameter.analogCh = 1
    FlatAlignmentParameter.pmAutoRangeUpOn = True
    FlatAlignmentParameter.pmInitRangeSettingOn = False
    FlatAlignmentParameter.pmInitRange = -40
    FlatAlignmentParameter.fieldSearchThreshold = 0.1
    FlatAlignmentParameter.peakSearchThreshold = 20
    FlatAlignmentParameter.searchRangeX = 50000
    FlatAlignmentParameter.searchRangeY = 16
    FlatAlignmentParameter.fieldSearchPitchX = 100
    FlatAlignmentParameter.fieldSearchPitchY = 0.1
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

def SetYTxAlignmentParameter_SkipMin(FlatAlignmentParameter, FieldSearchVolt):
    FlatAlignmentParameter.mainStageNumberX = 2
    FlatAlignmentParameter.mainStageNumberY = 4
    FlatAlignmentParameter.subStageNumberXY = 0
    FlatAlignmentParameter.subAngleX = 0
    FlatAlignmentParameter.subAngleY = 0
    FlatAlignmentParameter.pmCh = 1
    FlatAlignmentParameter.analogCh = 1
    FlatAlignmentParameter.pmAutoRangeUpOn = True
    FlatAlignmentParameter.pmInitRangeSettingOn = False
    FlatAlignmentParameter.pmInitRange = -30
    FlatAlignmentParameter.fieldSearchThreshold = FieldSearchVolt
    FlatAlignmentParameter.peakSearchThreshold = 20
    FlatAlignmentParameter.searchRangeX = 50000
    FlatAlignmentParameter.searchRangeY = 16
    FlatAlignmentParameter.fieldSearchPitchX = 100
    FlatAlignmentParameter.fieldSearchPitchY = 0.1
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

def SetTzAlignmentParameter(SingleAlignmentParameter):
    SingleAlignmentParameter.mainStageNumberX = 6
    SingleAlignmentParameter.subStageNumberXY = 0
    SingleAlignmentParameter.subAngleX = 0
    SingleAlignmentParameter.pmCh = 1
    SingleAlignmentParameter.analogCh = 1
    SingleAlignmentParameter.pmAutoRangeUpOn = True
    SingleAlignmentParameter.pmInitRangeSettingOn = True
    SingleAlignmentParameter.pmInitRange = -30
    SingleAlignmentParameter.fieldSearchThreshold = 0.1
    SingleAlignmentParameter.peakSearchThreshold = 10
    SingleAlignmentParameter.searchRangeX = 16
    SingleAlignmentParameter.fieldSearchSpeedX = 3
    SingleAlignmentParameter.peakSearchSpeedX = 0.5
    SingleAlignmentParameter.smoothingRangeX = 30
    SingleAlignmentParameter.centroidThresholdX = 0
    SingleAlignmentParameter.convergentRangeX = 0.1
    SingleAlignmentParameter.comparisonCount = 1
    SingleAlignmentParameter.maxRepeatCount = 5

def SetXYAlignmentParameterFine(FlatAlignmentParameter):
    FlatAlignmentParameter.mainStageNumberX = 1
    FlatAlignmentParameter.mainStageNumberY = 2
    FlatAlignmentParameter.subStageNumberXY = 0
    FlatAlignmentParameter.subAngleX = 0
    FlatAlignmentParameter.subAngleY = 0
    FlatAlignmentParameter.pmCh = 1
    FlatAlignmentParameter.analogCh = 1
    FlatAlignmentParameter.pmAutoRangeUpOn = True
    FlatAlignmentParameter.pmInitRangeSettingOn = False
    FlatAlignmentParameter.pmInitRange = -30
    FlatAlignmentParameter.fieldSearchThreshold = 0.1
    FlatAlignmentParameter.peakSearchThreshold = 20
    FlatAlignmentParameter.searchRangeX = 2500
    FlatAlignmentParameter.searchRangeY = 2500
    FlatAlignmentParameter.fieldSearchPitchX = 50
    FlatAlignmentParameter.fieldSearchPitchY = 50
    FlatAlignmentParameter.fieldSearchFirstPitchX = 0
    FlatAlignmentParameter.fieldSearchSpeedX = 500
    FlatAlignmentParameter.fieldSearchSpeedY = 500
    FlatAlignmentParameter.peakSearchSpeedX = 2
    FlatAlignmentParameter.peakSearchSpeedY = 2
    FlatAlignmentParameter.smoothingRangeX = 30
    FlatAlignmentParameter.smoothingRangeY = 30
    FlatAlignmentParameter.centroidThresholdX = 5
    FlatAlignmentParameter.centroidThresholdY = 5
    FlatAlignmentParameter.convergentRangeX = 0.5
    FlatAlignmentParameter.convergentRangeY = 0.5
    FlatAlignmentParameter.comparisonCount = 2
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
    # X and Ty angle 
    print("Tune X and Ty")
    SetXTyAlignmentParameter(FlatAlignmentParameter)
    Alignment.SetMeasurementWaveLength(FlatAlignmentParameter.pmCh, 1310)
    Alignment.SetFlat(FlatAlignmentParameter)
    Alignment.StartFlat()
    time.sleep(1)

    while str(Alignment.GetStatus()) != "Success":
        time.sleep(5)

    print("Tune Y and Tx")
    # Y and Tx angle 
    SetYTxAlignmentParameter(FlatAlignmentParameter)
    Alignment.SetMeasurementWaveLength(FlatAlignmentParameter.pmCh, 1310)
    Alignment.SetFlat(FlatAlignmentParameter)
    Alignment.StartFlat()
    time.sleep(1)
    while str(Alignment.GetStatus()) != "Success":
        time.sleep(5)

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
                
                CurrentPosition = ReturnCurrentPosition(AxisComponents)
                # SetXYAlignmentParameter(FlatAlignmentParameter)
                # Alignment.SetMeasurementWaveLength(FlatAlignmentParameter.pmCh, 1310)
                # Alignment.SetFlat(FlatAlignmentParameter)

                # # # # # run
                # Alignment.StartFlat()
                # time.sleep(20)

                # # move all angles to zeros
                # MovingTo = 0.0
                # MovingAxis = 4
                # # for MovingAxis in range(4, 7):
                # AxisComponents[MovingAxis].MoveAbsolute(MovingTo)
                # time.sleep(5)
                
                # time.sleep(10)
                # ShowPosition(position_label, AxisComponents)

                # PositionsBefore = [-25377.3, 5153.31, -28714.4, 1.23376486, -1.56874208, -2.82]
                # MoveToPositionBefore(AxisComponents, PositionsBefore)
                # print(Alignment.GetPower(FlatAlignmentParameter.pmCh))

                #  #### flat alignment 
                # # set
                while firstTimeConnected:
                    print("Step 1: Find Laser Beam .....")
                    SetXYAlignmentParameter(FlatAlignmentParameter)
                    Alignment.SetMeasurementWaveLength(FlatAlignmentParameter.pmCh, 1310)
                    Alignment.SetFlat(FlatAlignmentParameter)

                    # # # # run
                    Alignment.StartFlat()
                    time.sleep(10)

                    # read the power, 3 times powermeter value average
                    CachePower = [-60, -60, -60]
                    CachePower_mean = sum(CachePower) / len(CachePower)
                    while CachePower_mean < -42 or CachePower_mean == -40.0:
                        for i in range(3):
                            CachePower[i] = Alignment.GetPower(FlatAlignmentParameter.pmCh)
                        CachePower_mean = sum(CachePower) / len(CachePower)
                        time.sleep(10)
                    
                    if Alignment.GetPower(FlatAlignmentParameter.pmCh) > -42:
                        Alignment.Stop()
                        print("Great, first search is done!")
                        print(Alignment.GetPower(FlatAlignmentParameter.pmCh))
                        ShowPosition(position_label, AxisComponents)
                        CurrentPosition = ReturnCurrentPosition(AxisComponents)
                    #     break

                    print("Step 2: four axis alignment .....")
                    # # repeat 3 times and check the power
                    repeatTimes = 2
                    while repeatTimes > 0:
                        try:
                            print("Turning ...")
                            FourAxisAlignment(FlatAlignmentParameter, Alignment)
                            repeatTimes -= 1
                            print(Alignment.GetPower(FlatAlignmentParameter.pmCh))
                        except:
                            # print()
                            continue
                        # print("Turning ...")
                        # FourAxisAlignment(FlatAlignmentParameter, Alignment)
                        # repeatTimes -= 1
                        # print(Alignment.GetPower(FlatAlignmentParameter.pmCh))
                    CurrentPosition = ReturnCurrentPosition(AxisComponents)
                    
                    # PositionsBefore = [-25354.69, 5324.085, -28588.3, 0.68438, -1.07752483, -2.82]
                    # MoveToPositionBefore(AxisComponents, CurrentPosition)
                    # print(Alignment.GetPower(FlatAlignmentParameter.pmCh))
                    import random
                    # if it is stack in minimum, try to
                    tryTimes = 3
                    while Alignment.GetPower(FlatAlignmentParameter.pmCh) < -30.0:
                        print("Oops, hit local minimum....")
                        choice = random.randint(1, 2)
                        # if choice == 1:
                        #     FieldSearchVolt = float(Alignment.GetVoltage(FlatAlignmentParameter.pmCh)) + 0.1
                        #     SetYTxAlignmentParameter_SkipMin(FlatAlignmentParameter, FieldSearchVolt)
                        #     Alignment.SetMeasurementWaveLength(FlatAlignmentParameter.pmCh, 1310)
                        #     Alignment.SetFlat(FlatAlignmentParameter)
                        #     Alignment.StartFlat()
                        #     time.sleep(10)

                        #     SkipTimes = 1000
                        #     while str(Alignment.GetStatus()) != "Success" or SkipTimes > 0:
                        #         time.sleep(10)
                        #         SkipTimes -= 1

                        # else:
                        FieldSearchVolt = float(Alignment.GetVoltage(FlatAlignmentParameter.pmCh)) + 0.1
                        SetXTyAlignmentParameter_SkipMin(FlatAlignmentParameter, FieldSearchVolt)
                        Alignment.SetMeasurementWaveLength(FlatAlignmentParameter.pmCh, 1310)
                        Alignment.SetFlat(FlatAlignmentParameter)
                        Alignment.StartFlat()
                        time.sleep(10)

                        while str(Alignment.GetStatus()) != "Success":
                            time.sleep(10)
                    
                    print("Step 3: Final fine tuning......")
                    repeatTimes = 2
                    while repeatTimes > 0:
                        FourAxisAlignment(FlatAlignmentParameter, Alignment)
                        repeatTimes -= 1
                        print(Alignment.GetPower(FlatAlignmentParameter.pmCh))

                    CurrentPosition = ReturnCurrentPosition(AxisComponents)

                    #
                    print("Step 4: final Step...")
                    SetTzAlignmentParameter(SingleAlignmentParameter)
                    Alignment.SetMeasurementWaveLength(SingleAlignmentParameter.pmCh, 1310)
                    Alignment.SetSingle(SingleAlignmentParameter)
                    Alignment.StartSingle()
                    time.sleep(10)

                    while str(Alignment.GetStatus()) != "Success":
                        time.sleep(10)

                    repeatTimes = 2
                    while repeatTimes > 0:
                        FourAxisAlignment(FlatAlignmentParameter, Alignment)
                        repeatTimes -= 1
                        print(Alignment.GetPower(FlatAlignmentParameter.pmCh))

                    print(Alignment.GetPower(FlatAlignmentParameter.pmCh))
                    ShowPosition(position_label, AxisComponents)
                    break
                break
        else:
            print("Ads not connected")
            time.sleep(1)

print("Well done")
print("Laser Power:", Alignment.GetPower(FlatAlignmentParameter.pmCh))
# %%
