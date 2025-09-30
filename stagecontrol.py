from parameters import AlignmentParameter
from connect import MotionSystem
import time

class AlignmentController:
    def __init__(self, motion_system, wavelength):
        self.ms = motion_system
        self.wavelength = wavelength

    def read_power(self):
        # self.ms.alignment.SetMeasurementWaveLength(params.pmCh, self.wavelength)
        return self.ms.alignment.GetPower(1)
    
    def read_voltage(self):
        return self.ms.alignment.GetVoltage(1)
    
    def run_flat(self, params):
        self.ms.alignment.SetMeasurementWaveLength(params.pmCh, self.wavelength)
        self.ms.alignment.SetFlat(params)
        self.ms.alignment.StartFlat()
        time.sleep(1)
        while str(self.ms.alignment.GetStatus()) != "Success":
            time.sleep(5)
            # print(self.ms.alignment.GetStatus())7
            if str(self.ms.alignment.GetStatus()) == "PeakSearchRangeOver" or str(self.ms.alignment.GetStatus()) == "PeakSearchCountOver":
                print("Stop...")
                break

    def run_single(self, params):
        self.ms.alignment.SetMeasurementWaveLength(params.pmCh, self.wavelength)
        self.ms.alignment.SetSingle(params)
        self.ms.alignment.StartSingle()
        time.sleep(1)
        while str(self.ms.alignment.GetStatus()) != "Success":
            time.sleep(5)

    def find_beam(self):
        print("Step 1: Find Laser Beam")
        AlignmentParameter.xy(self.ms.flat_params)
        # self.run_flat(self.ms.flat_params)
        # print("Beam found at power:", self.ms.alignment.GetPower(self.ms.flat_params.pmCh))
        self.ms.alignment.SetMeasurementWaveLength(self.ms.flat_params.pmCh, 1310)
        self.ms.alignment.SetFlat(self.ms.flat_params)
        self.ms.alignment.StartFlat()
        while str(self.ms.alignment.GetStatus()) != "Success":
            time.sleep(5)
            # print(self.ms.alignment.GetStatus())
            if str(self.ms.alignment.GetStatus()) == "PeakSearchRangeOver" or str(self.ms.alignment.GetStatus()) == "PeakSearchCountOver":
                # print("Stop...")
                self.four_axis_alignment()
                break
        

    def four_axis_alignment(self):
        """Tuning Y and Tx pair, and then tuning X and Ty"""
        try:
            print("Tune Y and Tx")
            AlignmentParameter.ytx(self.ms.flat_params)
            self.run_flat(self.ms.flat_params)

            print("Tune X and Ty")
            AlignmentParameter.xty(self.ms.flat_params)
            self.run_flat(self.ms.flat_params)
        except:
            self.ms.stop()
            print("Error, stop alignment")

    def four_axis_fineAlignment(self):
        """Tuning Y and Tx pair, and then tuning X and Ty"""
        try:
            print("Tune Y and Tx")
            AlignmentParameter.ytx_fine(self.ms.flat_params)
            self.run_flat(self.ms.flat_params)

            print("Tune X and Ty")
            AlignmentParameter.xty_fine(self.ms.flat_params)
            self.run_flat(self.ms.flat_params)
        except:
            self.ms.stop()
            print("Error, stop alignment")

    def skip_local_min_ytx(self):
        FieldSearchVolt = float(self.read_voltage())
        AlignmentParameter.ytx_skip_min(self.ms.flat_params, FieldSearchVolt+0.02)
        self.run_flat(self.ms.flat_params)

    def skip_local_min_xty(self):
        FieldSearchVolt = float(self.read_voltage())
        AlignmentParameter.xty_skip_min(self.ms.flat_params, FieldSearchVolt+0.02)
        self.run_flat(self.ms.flat_params)


if __name__ == "__main__":
    ms = MotionSystem("5.153.34.236.1.1")
    ms.connect()
    # initial position
    # ms.show_positions()

    controller = AlignmentController(ms, 1310)
    # while ms.firstTimeConnected:
    #     print("Step 1: Find Laser Beam")
    #     controller.find_beam()

    #     CachePower = [-60, -60, -60]
    #     CachePower_mean = sum(CachePower) / len(CachePower)
    #     while CachePower_mean < -15:
    #         last_CachePower_mean = CachePower_mean
    #         while CachePower_mean <= -40:
    #             for i in range(3):
    #                 CachePower[i] = controller.read_power()
    #                 print(i, ":", CachePower[i])
    #                 time.sleep(2)
    #             last_CachePower_mean = CachePower_mean
    #             CachePower_mean = sum(CachePower) / len(CachePower)
    #             time.sleep(3)
    #             print(CachePower_mean)
            
    #         if abs(last_CachePower_mean - CachePower_mean) < 2:
    #             if controller.read_power() > -20:
    #                 print("Great, first search is done!")
    #                 print(controller.read_power())
    #                 break

    #             while controller.read_power() < -10.0:
    #                 print("Oops, hit local minimum...")
    #                 controller.skip_local_min_ytx()

    #                 if controller.read_power() < -15.0:
    #                     controller.skip_local_min_xty()
                        
    #             print("Finally, get rid of local minimum")
    #             break
        
    #     print("Final: four axis alignment ")
    #     repeatTimes = 3
    #     while repeatTimes > 0:
    #         print("Try: ", repeatTimes)
    #         try:
    #             print("Turning ...")
    #             controller.four_axis_alignment()
    #             repeatTimes -= 1
    #         except:
    #             continue
        
    # CurrentPosition = ms.show_positions()

    # print(controller.read_power())
    # print(controller.read_voltage())

    #### z-axis moving and final alignment
    


    #  step 2: z moving in and fine tune at the same time
    # -100 means, moving close to rotor


    # step 3: 4 rotational position check
    # step 4: z-moving out, add epoxy and moving back

    points = 4
    while ms.firstTimeConnected:
        ms.firstTimeConnected = True
        # moving max distance is 7.9 mm
        ms.show_positions()
        time.sleep(1)

        # for _ in range(5):
        #     ms.ZMove(-500)

        #     time.sleep(1)
        #     ms.show_positions()

        #     controller.four_axis_fineAlignment()

        #     time.sleep(1)
        #     ms.show_positions()

        #     print(controller.read_power())

        # ms.ZMove(-1000)

        # time.sleep(5)
        # ms.show_positions()

        # controller.four_axis_fineAlignment()

        # time.sleep(1)
        # ms.show_positions()

        # break
    #     # ms.show_positions()

    #     # print("*" * 40)
    #     # ms.ZMove(-500)

    #     # time.sleep(5)

    #     # rotation postion record
    #     # 1st 
    #     controller.four_axis_fineAlignment()
    #     ms.show_positions()
    #     time.sleep(1)
    #     ms.save_current_positioins(1)
    #     input("Press Enter to continue...")


    #     # maually rotate 
    #     # 2nd
    #     controller.four_axis_fineAlignment()
    #     ms.show_positions()
    #     time.sleep(1)
    #     ms.save_current_positioins(2)
    #     input("Press Enter to continue...")
    #     break

        for point in range(points):
            controller.four_axis_fineAlignment()
            ms.show_positions()
            time.sleep(1)
            ms.save_current_positioins(point)
            input("Press Enter to continue...")
        
        break


    ms.stop()
    # # ms.save_current_positioins(5)
    print(len(ms.position_history))
    print(ms.center_position())

    # # move it to the center position
    best_position = ms.center_position()
    ms.restore_position(best_position)
    ms.show_positions()