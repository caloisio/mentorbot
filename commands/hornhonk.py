from subsystems.hornsubsystem import HornSubsystem
from commands2 import CommandBase


class HornHonk(CommandBase):
    def __init__(self, horn: HornSubsystem) -> None:  #amount: int
        CommandBase.__init__(self)
        #self.repeatAmount = amount
        self.horn = horn

        self.setName(__class__.__name__)
        self.addRequirements([self.horn])

    def execute(self) -> None:

        self.horn.horn.set(1.0)

    def end(self, interrupted: bool) -> None:
        self.horn.horn.set(0.0)
