from subsystems.hornsubsystem import HornSubsystem
from commands2 import CommandBase


class HornHonk(CommandBase):
    def __init__(self, horn: HornSubsystem) -> None: #amount: int
        CommandBase.__init__(self)
        #self.repeatAmount = amount
        self.horn = horn

        self.setName(__class__.__name__)
        self.addRequirements([self.horn])

        self.on = False

    def execute(self) -> None:

        self.horn.horn.set(1.0)
        self.on = not self.on

    def isFinished(self) -> bool:
        self.horn.horn.set(0.0)
        return (not self.on) #and (self.repeatAmount < 0)
