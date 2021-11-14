from commands2._impl import SubsystemBase
from wpilib._wpilib import PWMSpeedController, RobotBase
import constants


class CameraSubsystem(SubsystemBase):
    def __init__(self) -> None:
        SubsystemBase.__init__(self)
        self.leftRight = PWMSpeedController(
            constants.kPWMCameraSwerveLeftRight if RobotBase.isReal(
            ) else constants.kPWMCameraSimSwerveLeftRight)
        self.upDown = PWMSpeedController(
            constants.kPWMCameraSwerveUpDown if RobotBase.isReal(
            ) else constants.kPWMCameraSimSwerveUpDown)

        self.leftRight.setInverted(constants.kPWMCameraLeftRightInverted)
        self.upDown.setInverted(constants.kPWMCameraUpDownInverted)

    def setCameraRotation(self, x: float, y: float):
        self.leftRight.set(x)
        self.upDown.set(y)
