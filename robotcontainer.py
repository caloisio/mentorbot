from ctre._ctre import WPI_TalonSRX
import wpilib

import commands2
import commands2.button
from commands.honk import RelayControl
from commands.rotatecamera import RotateCamera

import constants

from commands.complexauto import ComplexAuto
from commands.drivedistance import DriveDistance
from commands.defaultdrive import DefaultDrive
from commands.fieldrelativedrive import FieldRelativeDrive
from commands.resetdrive import ResetDrive
from subsystems.cameracontroller import CameraSubsystem

from subsystems.drivesubsystem import DriveSubsystem

from operatorinterface import OperatorInterface


class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:

        # The operator interface (driver controls)
        self.operatorInterface = OperatorInterface()

        # The robot's subsystems
        self.drive = DriveSubsystem()
        self.camera = CameraSubsystem()

        # horn
        # self.light = wpilib.(constants.kHornPWMPinLocation)
        # self.light2 = wpilib.Spark(constants.kHorn2PWMPinLocation)
        # self.light.setRaw(65535) #turn off horn by default
        # self.light2.setRaw(65535)

        self.light = WPI_TalonSRX(constants.kBackLightControllerDeviceID)

        # Autonomous routines

        # A simple auto routine that drives forward a specified distance, and then stops.
        self.simpleAuto = DriveDistance(
            constants.kAutoDriveDistance,
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

        self.drive.setDefaultCommand(
            DefaultDrive(
                self.drive,
                self.operatorInterface.chassisControls.forwardsBackwards,
                self.operatorInterface.chassisControls.sideToSide,
                self.operatorInterface.chassisControls.rotation,
            )
        )

        self.camera.setDefaultCommand(RotateCamera(
            self.camera, self.operatorInterface.cameraControls.leftRight, self.operatorInterface.cameraControls.upDown))

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """
        commands2.button.JoystickButton(
            *self.operatorInterface.coordinateModeControl
        ).whileHeld(
            FieldRelativeDrive(
                self.drive,
                self.operatorInterface.chassisControls.forwardsBackwards,
                self.operatorInterface.chassisControls.sideToSide,
                self.operatorInterface.chassisControls.rotation,
            )
        )

        commands2.button.JoystickButton(
            *self.operatorInterface.resetSwerveControl
        ).whenPressed(ResetDrive(self.drive))

        # commands2.button.JoystickButton(
        #     *self.operatorInterface.honkControl
        # ).whileHeld(HornHonk(self.light2))

        commands2.button.JoystickButton(
            *self.operatorInterface.honkControl2
        ).whileHeld(RelayControl(self.light, self.operatorInterface.backLightControl))

        

    def getAutonomousCommand(self) -> commands2.Command:
        return self.chooser.getSelected()
