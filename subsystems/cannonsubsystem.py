from commands2._impl import SubsystemBase
from wpilib._wpilib import Solenoid
import constants


class CannonSubsystem(SubsystemBase):
    def __init__(self) -> None:
        SubsystemBase.__init__(self)
        self.launchSolonoid = Solenoid(constants.kPCMCannonCanID,
                                       constants.kCannonLaunchPCMID)
        self.fillSolonoid = Solenoid(constants.kPCMCannonCanID,
                                     constants.kCannonFillPCMID)

    def close(self) -> None:
        """close all the solonoids"""
        self.launchSolonoid.set(False)
        self.fillSolonoid.set(False)

    def fill(self) -> None:
        """begins filling staging tank"""
        self.launchSolonoid.set(
            False
        )  #ensure air doesnt just flow out the end without being stored
        self.fillSolonoid.set(True)

    def fire(self) -> None:
        """the part where you yell "fire" and make people happy"""
        self.launchSolonoid.set(True)
        self.fillSolonoid.set(False)
