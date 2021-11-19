from commands2 import CommandBase
from ctre import WPI_TalonSRX


class BlinkLight(CommandBase):
    def __init__(self, light: WPI_TalonSRX, amount: int,
                 interval: int) -> None:
        CommandBase.__init__(self)
        self.repeatAmount = amount
        self.light = light
        self.interval = interval

        self.timer = 0  # track ms since start

        self.isFinished = lambda: self.repeatAmount <= 0  # consider finished when go through all blinks

    def execute(self) -> None:
        # ASSUME 20MS BETWEEN EACH ITERATION OF BEING CALLED
        # !!! DO NOT CHANDE INTERVAL OF ROBOT !!!
        self.timer += 20

        if self.timer > self.interval:
            if self.light.get() != 0:
                self.light.set(0.0)
                self.repeatAmount -= 1
            else:
                self.light.set(1.0)
            self.timer = self.timer % self.interval  # if go over take the remainder
