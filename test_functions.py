# relative move
# AxisComponents[1].MoveRelative(0.1)
# time.sleep(0.5)

# MovingAxis = 6
# MovingTo = 0

# # response time is needed to check movign status of a axis
# AxisComponents[MovingAxis].MoveAbsolute(MovingTo)
# # set moving speed
# # AxisComponents[MovingAxis].SetMaxSpeed(0.5)
# time.sleep(0.5)
# MovingAxisStatus = AxisComponents[MovingAxis].IsMoving()

# # print(MovingAxisStatus)
# while MovingAxisStatus:
#     time.sleep(2)
#     MovingAxisStatus = AxisComponents[MovingAxis].IsMoving()
#     # print(MovingAxisStatus)
# # while AxisComponents[MovingAxis].IsMoving():
# #     time.sleep(0.5)


# for n in range(DOF):
#     print(f'{position_label[n]} position: {AxisComponents[n+1].GetActualPosition()}')
# print("=====================================")
