from commands2 import CommandBase

from subsystems.drivesubsystem import DriveSubsystem


class SetReturn(CommandBase):
    def __init__(self, drive: DriveSubsystem) -> None:
        CommandBase.__init__(self)

        self.drive = drive

    def initialize(self) -> None:
        currentPose = self.drive.odometry.getPose()
        self.drive.returnPos = currentPose

        currentX = currentPose.X()
        currentY = currentPose.Y()

        print("New Coordinates \nX: {0}, Y: {1}".format(currentX, currentY))
        

    def isFinished(self) -> bool:
        return True