from connect import MotionSystem
from parameters import AlignmentParameter
from stagecontrol import AlignmentController
import time
import winsound

ms = MotionSystem("5.153.34.236.1.1")
ms.connect()
    # initial position
    # ms.show_positions()

controller = AlignmentController(ms, 1310)


# command line control
def LaserBeamAlign(controller):
    controller.find_beam()

    CachePower = [-60, -60, -60]
    CachePower_mean = sum(CachePower) / len(CachePower)
    while CachePower_mean < -15:
        last_CachePower_mean = CachePower_mean
        while CachePower_mean <= -40:
            for i in range(3):
                CachePower[i] = controller.read_power()
                print(i, ":", CachePower[i])
                time.sleep(2)
            last_CachePower_mean = CachePower_mean
            CachePower_mean = sum(CachePower) / len(CachePower)
            time.sleep(3)
            print(CachePower_mean)
        
        if abs(last_CachePower_mean - CachePower_mean) < 2:
            if controller.read_power() > -20:
                print("Great, first search is done!")
                print(controller.read_power())
                break

            while controller.read_power() < -10.0:
                print("Oops, hit local minimum...")
                controller.skip_local_min_ytx()

                if controller.read_power() < -15.0:
                    controller.skip_local_min_xty()
                    
            print("Finally, get rid of local minimum")
            break

    print("Final: four axis alignment ")
    repeatTimes = 3
    while repeatTimes > 0:
        print("Try: ", repeatTimes)
        try:
            print("Turning ...")
            controller.four_axis_alignment()
            repeatTimes -= 1
        except:
            continue
    print("First Alignment Done!")

def moveDistanceChose():
    dist_chosen = input("""Please choose moving distance:
          1. 100 um
          2. 500 um,
          3. 2000 um
          4. 5000 um
          5. Custom distance
          """)
    
    match dist_chosen:
        case "1":
            distance = 100
        case "2":
            distance = 500 
        case "3":
            distance = 2000 
        case "4":
            distance = 5000
        case "5":
            distance = int(input("Please input moving distance (um): "))
        case _:
            print("Please choose the number between 1-5")
            distance = moveDistanceChose()

    return distance

isSystemOn = True

while isSystemOn and ms.firstTimeConnected:
    print("""
        1. Initial Alginment
        2. Z-Moving Forward
        3. Z-Moving Backward
        4. Fine Alignment
        5. Find Best Center
        6. Epoyx Moving out and Moving Back
        7. Exit
          """)
    
    chosen = input("Step Choice: ")
    match chosen:
        case "1":
            LaserBeamAlign(controller)

        case "2":
            
            moving_dist = moveDistanceChose()
            ms.ZMove(int(moving_dist)*(-1))
            # ms.stop()
            time.sleep(5)

        case "3":
            moving_dist = moveDistanceChose()
            ms.ZMove(int(moving_dist))
            # ms.stop()
            time.sleep(5)

        case "4":
            controller.four_axis_fineAlignment()

        case "5":
            points = 4
            for point in range(points):
                controller.four_axis_fineAlignment()
                ms.show_positions()
                time.sleep(1)
                ms.save_current_positions(point)
                input("Press Enter to continue...")
            
            best_position = ms.center_position()
            ms.restore_position(best_position)
            ms.show_positions()

        case "6":
            ms.ZMove(10000)
            input("Add Epoxy, If it is done, Press Enter to Move back...")
            ms.ZMove(-10000)
            ms.stop()
            time.sleep(5)

        case "7":
            ms.stop()
            isSystemOn = False
            ms.disconnect()
            break
        
        case _:
            print("Please chose the number between 1-7")

    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

