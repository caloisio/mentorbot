from commands2 import SubsystemBase
from wpilib import Solenoid
import constants


class CannonSubsystem(SubsystemBase):
    def __init__(self) -> None:
        SubsystemBase.__init__(self)
        self.launchSolonoid = Solenoid(constants.kPCMCannonCanID,
                                       constants.kCannonLaunchPCMID)
        self.fillSolonoid = Solenoid(constants.kPCMCannonCanID,
                                     constants.kCannonFillPCMID)

        self.fillSolonoid.set(False)
        self.launchSolonoid.set(True)

    def close(self) -> None:
        """close all the solonoids"""
        self.fillSolonoid.set(False)
        self.launchSolonoid.set(True)
        # print("CLOSING")

    def fill(self) -> None:
        """begins filling staging tank"""
        # self.launchSolonoid.set(
        #     False
        # )  #ensure air doesnt just flow out the end without being stored
        self.fillSolonoid.toggle()
        print(self.fillSolonoid.get())
        print("FILLING")

    def launch(self) -> None:
        self.launchSolonoid.toggle()
        print(self.launchSolonoid.get())

