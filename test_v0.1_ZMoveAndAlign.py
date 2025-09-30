import time

DOF = 6

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

def MoveToTargetPosition(AxisComponents, TargetPosition):
    for i in range(DOF):
        AxisComponents[i+1].MoveAbsolute(TargetPosition[i])
        time.sleep(0.5)
        while AxisComponents[i+1].IsMoving():
            time.sleep(0.5)
    print("Move to target Position")

def ZAxisMove(AxisComponents, RelativeDist):
    '''
    Relative Move in Z Axis
    '''
    AxisComponents[3].MoveRelative(RelativeDist)
    time.sleep(0.1)

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
