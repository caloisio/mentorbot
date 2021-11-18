import typing
from commands2 import CommandBase
from ctre import ControlMode, WPI_TalonSRX


class RelayControl(CommandBase):
    def __init__(self, controller: WPI_TalonSRX,
                 controlPercent: typing.Callable[[], float]) -> None:
        CommandBase.__init__(self)
        self.horn = controller
        self.horn.set(ControlMode.PercentOutput, 0.0)
        self.controlPercent = controlPercent
        self.setOutputPercent = lambda percent: self.horn.set(
            ControlMode.PercentOutput, percent)

    def execute(self) -> None:
        self.setOutputPercent(self.controlPercent())

    def end(self, interrupted: bool) -> None:
        self.setOutputPercent(0.0)
