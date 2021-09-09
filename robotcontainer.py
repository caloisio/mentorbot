import wpilib
from wpilib.interfaces import GenericHID

import commands2
import commands2.button

import constants

from commands.complexauto import ComplexAuto
from commands.drivedistance import DriveDistance
from commands.defaultdrive import DefaultDrive

from subsystems.drivesubsystem import DriveSubsystem

from units import units


class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:

        # The driver's controller
        # self.driverController = wpilib.XboxController(constants.kDriverControllerPort)
        self.translationController = wpilib.Joystick(
            constants.kTranslationControllerPort
        )
        self.rotationController = wpilib.Joystick(constants.kRotationControllerPort)

        # The robot's subsystems
        self.drive = DriveSubsystem()

        # Autonomous routines

        # A simple auto routine that drives forward a specified distance, and then stops.
        self.simpleAuto = DriveDistance(
            constants.kAutoDriveDistance.to(units.meters),
            constants.kAutoDriveSpeedFactor,
            DriveDistance.Axis.X,
            self.drive,
        )

        # A complex auto routine that drives forward, right, back, left
        self.complexAuto = ComplexAuto(self.drive)

        # Chooser
        self.chooser = wpilib.SendableChooser()

        # Add commands to the autonomous command chooser
        self.chooser.setDefaultOption("Simple Auto", self.simpleAuto)
        self.chooser.addOption("Complex Auto", self.complexAuto)

        # Put the chooser on the dashboard
        wpilib.SmartDashboard.putData("Autonomous", self.chooser)

        self.configureButtonBindings()

        # set up default drive command
        self.drive.setDefaultCommand(
            DefaultDrive(
                self.drive,
                lambda: -1 * self.translationController.getY(GenericHID.Hand.kLeftHand),
                lambda: -1 * self.translationController.getX(GenericHID.Hand.kLeftHand),
                lambda: -1 * self.rotationController.getX(GenericHID.Hand.kRightHand),
            )
        )

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """

    def getAutonomousCommand(self) -> commands2.Command:
        return self.chooser.getSelected()