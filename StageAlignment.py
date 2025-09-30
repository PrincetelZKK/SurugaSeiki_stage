# command line 
from utils.AlignmentParameters import SetXYAlignmentParameter, SetXTyAlignmentParameter, SetYTxAlignmentParameter, SingleAlignmentParameter
import sys

class StageAlignments:
    def __init__(self):
        self.choices = {
            '1': self.XYAlignment,
            '2': self.XTyAlignment,
            '3': self.YTxAlignment,
            '4': self.TzAlignment,
            '5': self.quit
        }


    # display menu
    def display(self):
        print(
            """
            Run Alignment:
            1. X & Y-Alignment
            2. X & Ty-Alignment
            3. Y & Tz-Alignment
            4. Tz-Alignment
            5. Quit
            """
        )

    def XYAlignment(self, FlatParameters):
        SetXYAlignmentParameter(FlatParameters)
    
    def XTyAlignment(self, FlatParameters):
        SetXTyAlignmentParameter(FlatParameters)
    
    def YTxAlignment(self, FlatParameters):
        SetYTxAlignmentParameter(FlatParameters)
    
    def TzAlignment(self, SingleParameters):
        SingleAlignmentParameter(SingleParameters)
    
    def quit(self):
        print("Thank you for using")
        sys.exit(0)
    
    def RunAlign(self):
        '''Display menu and run alignment'''
        while True:
            self.display()
            choice = input("Enter an option: ")
            # flat or single alignment

            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("Not the right input, range 1-5")