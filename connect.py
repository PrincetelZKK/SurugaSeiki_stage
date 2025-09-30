import pythonnet
pythonnet.load("coreclr")
from collections import namedtuple
import time

import clr
clr.AddReference("srgmc")
import SurugaSeiki.Motion as Motion

class MotionSystem:
    PositionRecord = namedtuple("PositionRecord", ["index", "X", "Y", "Z", "Tx", "Ty", "Tz"])

    def __init__(self, ads_address: str, dof: int = 6):
        self.system = Motion.System.Instance
        self.system.SetAddress(ads_address)
        self.dof = dof
        self.labels = ("X", "Y", "Z", "Tx", "Ty", "Tz")
        self.firstTimeConnected = False
        self.axes = {i: Motion.AxisComponents(i) for i in range(1, dof + 1)}
        self.axis2d = Motion.Axis2D(1, 2)
        self.alignment = Motion.Alignment()
        self.flat_params = Motion.Alignment.FlatParameter()
        self.single_params = Motion.Alignment.SingleParameter()
        self.position_history = []      # store saved postions in memory
    
    def connect(self):
        while True:
            if self.system.Connected:
                if self.firstTimeConnected == False:
                    self.firstTimeConnected = True
                    print(f"DLL Version: {self.system.DllVersion}")
                    print(f"System Version: {self.system.SystemVersion}")

                    #  Turn on the servo
                    for axisComponent in self.axes.items():
                        if axisComponent[1].IsServoOn() == False:
                            axisComponent[1].TurnOnServo()
                    break
        print("Servo is On! Stage is Connected!")

    def show_positions(self):
        for i in range(self.dof):
            pos = self.axes[i + 1].GetActualPosition()
            print(f"{self.labels[i]} position: {pos}")
        print("=" * 40)

    def get_current_positions(self):
        return [self.axes[i + 1].GetActualPosition() for i in range(self.dof)]

    def save_current_positions(self, index):
        positions = self.get_current_positions()
        record = MotionSystem.PositionRecord(
            index if index is not None else len(self.position_history) + 1, 
            *positions)
        self.position_history.append(record)
        return record

    def get_position_by_index(self, idx: int):
        """Return the PositionRecord with matching index field (not list index)."""
        for rec in self.position_history:
            if rec.index == idx:
                return rec
        raise ValueError(f"No saved position with index {idx}")

    def restore_position(self, record):
        """Move the system to a saved PositionRecord."""
        self.MoveToPosition([record.X, record.Y, record.Z, record.Tx, record.Ty, record.Tz])
    
    def stop(self):
        self.alignment.Stop()
        print("Stage Stopped.")

    def center_position(self):
        n = len(self.position_history)
        if n == 0:
            return None
        
        sumX = sum(rec.X for rec in self.position_history)
        sumY = sum(rec.Y for rec in self.position_history)
        sumZ = sum(rec.Z for rec in self.position_history)
        sumTx = sum(rec.Tx for rec in self.position_history)
        sumTy = sum(rec.Ty for rec in self.position_history)
        sumTz = sum(rec.Tz for rec in self.position_history)

        return MotionSystem.PositionRecord(
            index="center",  # label for clarity
            X=sumX/n, Y=sumY/n, Z=sumZ/n,
            Tx=sumTx/n, Ty=sumTy/n, Tz=sumTz/n
        )

    def disconnect(self):
        if self.system.Connected:
            for axisComponent in self.axes.values():
                axisComponent.TurnOffServo()
        print("Stage Disconnected")

    def MoveToPosition(self, Positions):
        # Move to absolute position
        for i in range(self.dof):
            self.axes[i+1].MoveAbsolute(Positions[i])
            time.sleep(0.1)
            while self.axes[i+1].IsMoving():
                time.sleep(0.1)
        print("Move to position done.")
    
    def ZMove(self, RelativeDist):
        # RelativeDist is in um
        self.axes[3].MoveRelative(RelativeDist)
        while self.axes[3].IsMoving():
            time.sleep(0.1)
        print("Z direction move done.")
                    
if __name__ == "__main__":
    ms= MotionSystem("5.153.34.236.1.1")
    ms.connect()
    ms.show_positions()

    print("*" * 40)
    time.sleep(1)
    ms.ZMove(-500)

    time.sleep(1)
    ms.show_positions()

    ms.stop()
    # ms.disconnect()             # disconnect