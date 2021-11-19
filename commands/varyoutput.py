import typing
from commands2 import CommandBase
from ctre import ControlMode, WPI_TalonSRX


class RelayControl(CommandBase):
    def __init__(self, controller: WPI_TalonSRX,
                 controlPercent: typing.Callable[[], float]) -> None:
        CommandBase.__init__(self)
        self.control = controller
        self.controlPercentCommand = controlPercent

        self.setOutputPercent = lambda percent: self.control.set(
            ControlMode.PercentOutput, percent)

    def execute(self) -> None:
        self.setOutputPercent(self.controlPercentCommand())

    def end(self, interrupted: bool) -> None:
        self.setOutputPercent(0.0)
