class AlignmentParameter:
    """Centralized factory for all alignment parameter presets."""

    @staticmethod
    def xy(params):
        params.mainStageNumberX = 1
        params.mainStageNumberY = 2
        params.subStageNumberXY = 0
        params.subAngleX = 0
        params.subAngleY = 0
        params.pmCh = 1
        params.analogCh = 1
        params.pmAutoRangeUpOn = True
        params.pmInitRangeSettingOn = True
        params.pmInitRange = -40
        params.fieldSearchThreshold = 0.1
        params.peakSearchThreshold = 5
        params.searchRangeX = 10000
        params.searchRangeY = 10000
        params.fieldSearchPitchX = 100
        params.fieldSearchPitchY = 100
        params.fieldSearchFirstPitchX = 0
        params.fieldSearchSpeedX = 200
        params.fieldSearchSpeedY = 200
        params.peakSearchSpeedX = 10
        params.peakSearchSpeedY = 10
        params.smoothingRangeX = 30
        params.smoothingRangeY = 30
        params.centroidThresholdX = 5
        params.centroidThresholdY = 5
        params.convergentRangeX = 0.5
        params.convergentRangeY = 0.5
        params.comparisonCount = 2
        params.maxRepeatCount = 5

    @staticmethod
    def xy_fine(params):
        params.mainStageNumberX = 1
        params.mainStageNumberY = 2
        params.subStageNumberXY = 0
        params.subAngleX = 0
        params.subAngleY = 0
        params.pmCh = 1
        params.analogCh = 1
        params.pmAutoRangeUpOn = True
        params.pmInitRangeSettingOn = False
        params.pmInitRange = -30
        params.fieldSearchThreshold = 0.1
        params.peakSearchThreshold = 20
        params.searchRangeX = 2500
        params.searchRangeY = 2500
        params.fieldSearchPitchX = 50
        params.fieldSearchPitchY = 50
        params.fieldSearchFirstPitchX = 0
        params.fieldSearchSpeedX = 500
        params.fieldSearchSpeedY = 500
        params.peakSearchSpeedX = 2
        params.peakSearchSpeedY = 2
        params.smoothingRangeX = 30
        params.smoothingRangeY = 30
        params.centroidThresholdX = 5
        params.centroidThresholdY = 5
        params.convergentRangeX = 0.5
        params.convergentRangeY = 0.5
        params.comparisonCount = 2
        params.maxRepeatCount = 2

    @staticmethod
    def xty(params):
        params.mainStageNumberX = 1
        params.mainStageNumberY = 5
        params.subStageNumberXY = 0
        params.subAngleX = 0
        params.subAngleY = 0
        params.pmCh = 1
        params.analogCh = 1
        params.pmAutoRangeUpOn = True
        params.pmInitRangeSettingOn = False
        params.pmInitRange = -40
        params.fieldSearchThreshold = 0.1
        params.peakSearchThreshold = 5
        params.searchRangeX = 10000
        params.searchRangeY = 40
        params.fieldSearchPitchX = 100
        params.fieldSearchPitchY = 0.1
        params.fieldSearchFirstPitchX = 0
        params.fieldSearchSpeedX = 500
        params.fieldSearchSpeedY = 1
        params.peakSearchSpeedX = 10
        params.peakSearchSpeedY = 0.5
        params.smoothingRangeX = 30
        params.smoothingRangeY = 30
        params.centroidThresholdX = 5
        params.centroidThresholdY = 5
        params.convergentRangeX = 0.5
        params.convergentRangeY = 0.1
        params.comparisonCount = 1
        params.maxRepeatCount = 5

    @staticmethod
    def xty_fine(params):
        params.mainStageNumberX = 1
        params.mainStageNumberY = 5
        params.subStageNumberXY = 0
        params.subAngleX = 0
        params.subAngleY = 0
        params.pmCh = 1
        params.analogCh = 1
        params.pmAutoRangeUpOn = True
        params.pmInitRangeSettingOn = True
        params.pmInitRange = -10
        params.fieldSearchThreshold = 0.05
        params.peakSearchThreshold = 1
        params.searchRangeX = 200
        params.searchRangeY = 1
        params.fieldSearchPitchX = 1
        params.fieldSearchPitchY = 0.01
        params.fieldSearchFirstPitchX = 0
        params.fieldSearchSpeedX = 5
        params.fieldSearchSpeedY = 0.1
        params.peakSearchSpeedX = 10
        params.peakSearchSpeedY = 0.01
        params.smoothingRangeX = 30
        params.smoothingRangeY = 30
        params.centroidThresholdX = 5
        params.centroidThresholdY = 5
        params.convergentRangeX = 0.5
        params.convergentRangeY = 0.1
        params.comparisonCount = 1
        params.maxRepeatCount = 2

    @staticmethod
    def xty_skip_min(params, field_search_volt):
        params.mainStageNumberX = 1
        params.mainStageNumberY = 5
        params.subStageNumberXY = 0
        params.subAngleX = 0
        params.subAngleY = 0
        params.pmCh = 1
        params.analogCh = 1
        params.pmAutoRangeUpOn = True
        params.pmInitRangeSettingOn = False
        params.pmInitRange = -30
        params.fieldSearchThreshold = field_search_volt
        params.peakSearchThreshold = 20
        params.searchRangeX = 10000
        params.searchRangeY = 40
        params.fieldSearchPitchX = 100
        params.fieldSearchPitchY = 0.1
        params.fieldSearchFirstPitchX = 0
        params.fieldSearchSpeedX = 500
        params.fieldSearchSpeedY = 1
        params.peakSearchSpeedX = 10
        params.peakSearchSpeedY = 0.5
        params.smoothingRangeX = 30
        params.smoothingRangeY = 30
        params.centroidThresholdX = 5
        params.centroidThresholdY = 5
        params.convergentRangeX = 0.5
        params.convergentRangeY = 0.1
        params.comparisonCount = 1
        params.maxRepeatCount = 5

    @staticmethod
    def ytx(params):
        params.mainStageNumberX = 2
        params.mainStageNumberY = 4
        params.subStageNumberXY = 0
        params.subAngleX = 0
        params.subAngleY = 0
        params.pmCh = 1
        params.analogCh = 1
        params.pmAutoRangeUpOn = True
        params.pmInitRangeSettingOn = False
        params.pmInitRange = -40
        params.fieldSearchThreshold = 0.1
        params.peakSearchThreshold = 20
        params.searchRangeX = 10000
        params.searchRangeY = 16
        params.fieldSearchPitchX = 100
        params.fieldSearchPitchY = 0.1
        params.fieldSearchFirstPitchX = 0
        params.fieldSearchSpeedX = 500
        params.fieldSearchSpeedY = 1
        params.peakSearchSpeedX = 10
        params.peakSearchSpeedY = 0.5
        params.smoothingRangeX = 30
        params.smoothingRangeY = 30
        params.centroidThresholdX = 5
        params.centroidThresholdY = 5
        params.convergentRangeX = 0.5
        params.convergentRangeY = 0.1
        params.comparisonCount = 1
        params.maxRepeatCount = 5
    
    @staticmethod
    def ytx_fine(params):
        params.mainStageNumberX = 2
        params.mainStageNumberY = 4
        params.subStageNumberXY = 0
        params.subAngleX = 0
        params.subAngleY = 0
        params.pmCh = 1
        params.analogCh = 1
        params.pmAutoRangeUpOn = True
        params.pmInitRangeSettingOn = True
        params.pmInitRange = -10
        params.fieldSearchThreshold = 0.05
        params.peakSearchThreshold = 1
        params.searchRangeX = 200
        params.searchRangeY = 1
        params.fieldSearchPitchX = 1
        params.fieldSearchPitchY = 0.01
        params.fieldSearchFirstPitchX = 0
        params.fieldSearchSpeedX = 5
        params.fieldSearchSpeedY = 0.1
        params.peakSearchSpeedX = 10
        params.peakSearchSpeedY = 0.01
        params.smoothingRangeX = 30
        params.smoothingRangeY = 30
        params.centroidThresholdX = 5
        params.centroidThresholdY = 5
        params.convergentRangeX = 0.5
        params.convergentRangeY = 0.1
        params.comparisonCount = 1
        params.maxRepeatCount = 5

    @staticmethod
    def ytx_skip_min(params, field_search_volt):
        params.mainStageNumberX = 2
        params.mainStageNumberY = 4
        params.subStageNumberXY = 0
        params.subAngleX = 0
        params.subAngleY = 0
        params.pmCh = 1
        params.analogCh = 1
        params.pmAutoRangeUpOn = True
        params.pmInitRangeSettingOn = False
        params.pmInitRange = -30
        params.fieldSearchThreshold = field_search_volt
        params.peakSearchThreshold = 10
        params.searchRangeX = 10000
        params.searchRangeY = 16
        params.fieldSearchPitchX = 100
        params.fieldSearchPitchY = 0.1
        params.fieldSearchFirstPitchX = 0
        params.fieldSearchSpeedX = 500
        params.fieldSearchSpeedY = 1
        params.peakSearchSpeedX = 10
        params.peakSearchSpeedY = 0.5
        params.smoothingRangeX = 30
        params.smoothingRangeY = 30
        params.centroidThresholdX = 5
        params.centroidThresholdY = 5
        params.convergentRangeX = 0.5
        params.convergentRangeY = 0.1
        params.comparisonCount = 1
        params.maxRepeatCount = 5

    


    @staticmethod
    def tz(params):
        params.mainStageNumberX = 6
        params.subStageNumberXY = 0
        params.subAngleX = 0
        params.pmCh = 1
        params.analogCh = 1
        params.pmAutoRangeUpOn = True
        params.pmInitRangeSettingOn = True
        params.pmInitRange = -30
        params.fieldSearchThreshold = 0.1
        params.peakSearchThreshold = 10
        params.searchRangeX = 16
        params.fieldSearchSpeedX = 3
        params.peakSearchSpeedX = 0.5
        params.smoothingRangeX = 30
        params.centroidThresholdX = 0
        params.convergentRangeX = 0.1
        params.comparisonCount = 1
        params.maxRepeatCount = 5
