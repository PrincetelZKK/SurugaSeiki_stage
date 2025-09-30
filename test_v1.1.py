import time
import random
import pythonnet

pythonnet.load("coreclr")

import clr
clr.AddReference("srgmc")
import SurugaSeiki.Motion as Motion

from utils.AlignmentParameters import AlignmentParameterFactory

class MotionSystem:
    def __init__(self, ads_address: str, dof: int = 6):
        self.system = Motion.System.Instance
        self.system.SetAddress(ads_address)
        self.dof = dof
        self.axes = {i: Motion.AxisComponents(i) for i in range(1, dof + 1)}
        self.axis2d = Motion.Axis2D(1, 2)
        self.alignment = Motion.Alignment()
        self.flat_params = Motion.Alignment.FlatParameter()
        self.single_params = Motion.Alignment.SingleParameter()

    def connect(self):
        if not self.system.Connected:
            raise ConnectionError("ADS not connected.")
        print(f"DLL Version: {self.system.DllVersion}")
        print(f"System Version: {self.system.SystemVersion}")

    def show_positions(self):
        labels = ("X", "Y", "Z", "Tx", "Ty", "Tz")
        for i in range(self.dof):
            pos = self.axes[i + 1].GetActualPosition()
            print(f"{labels[i]} position: {pos}")
        print("=" * 40)

    def get_current_positions(self):
        return [self.axes[i + 1].GetActualPosition() for i in range(self.dof)]

    def move_to_positions(self, positions):
        for i in range(self.dof):
            self.axes[i + 1].MoveAbsolute(positions[i])
            while self.axes[i + 1].IsMoving():
                time.sleep(0.5)
        print("Move completed.")



class AlignmentController:
    def __init__(self, motion_system: MotionSystem):
        self.ms = motion_system

    def read_power(self):
        pass
    
    def run_flat(self, params):
        self.ms.alignment.SetMeasurementWaveLength(params.pmCh, 1310)
        self.ms.alignment.SetFlat(params)
        self.ms.alignment.StartFlat()
        while str(self.ms.alignment.GetStatus()) != "Success":
            time.sleep(5)

    def run_single(self, params):
        self.ms.alignment.SetMeasurementWaveLength(params.pmCh, 1310)
        self.ms.alignment.SetSingle(params)
        self.ms.alignment.StartSingle()
        while str(self.ms.alignment.GetStatus()) != "Success":
            time.sleep(5)

    def find_beam(self):
        print("Step 1: Find Laser Beam")
        AlignmentParameterFactory.xy(self.ms.flat_params)
        self.run_flat(self.ms.flat_params)
        print("Beam found at power:", self.ms.alignment.GetPower(self.ms.flat_params.pmCh))

    def four_axis_alignment(self):
        print("Step 2: Four-axis alignment")
        AlignmentParameterFactory.xty(self.ms.flat_params)
        self.run_flat(self.ms.flat_params)
        AlignmentParameterFactory.ytx(self.ms.flat_params)
        self.run_flat(self.ms.flat_params)

    def final_tuning(self):
        print("Step 3: Final tuning")
        self.four_axis_alignment()
        AlignmentParameterFactory.tz(self.ms.single_params)
        self.run_single(self.ms.single_params)


if __name__ == "__main__":
    ms = MotionSystem("5.153.34.236.1.1")
    ms.connect()
    ms.show_positions()

    controller = AlignmentController(ms)
    controller.find_beam()
    controller.four_axis_alignment()
    controller.final_tuning()

    ms.show_positions()
    print("Final Laser Power:", ms.alignment.GetPower(ms.flat_params.pmCh))
