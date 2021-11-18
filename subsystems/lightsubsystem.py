from commands2._impl import SubsystemBase
from ctre._ctre import WPI_TalonSRX
import constants


class LightSubsystem(SubsystemBase):
    def __init__(self) -> None:
        SubsystemBase.__init__(self)

        self.light = WPI_TalonSRX(constants.kBackLightControllerDeviceID)
