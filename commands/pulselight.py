from commands2 import CommandBase
from ctre import WPI_TalonSRX


class PulseLight(CommandBase):
    def __init__(self, light: WPI_TalonSRX, pulseInterval: int,
                 squareOutput: bool) -> None:
        CommandBase.__init__(self)
        self.light = light
        self.pulseInterval = pulseInterval  # interval between each pulse

        self.setBrightness = lambda x: self.light.set(
            x**x if squareOutput else x)  # yay inline functions

        self.rising = True

    def execute(self) -> None:
        self.setBrightness(bright := (  # set and reture for future use
            self.light.get() +
            (self.rising * 2 - 1) *  # convert bool (0 or 1) to range of -1,1
            (self.pulseInterval / 40)))  # 40 because 1 pulse = 1 up and 1 down

        if bright <= 0 or bright >= 1:
            self.rising = not self.rising

    def end(self) -> None:
        self.light.set(0.0)  # turn off when done
