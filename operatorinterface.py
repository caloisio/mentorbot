from os import path
from wpilib import Joystick, XboxController, RobotBase
from wpilib.interfaces import GenericHID

import typing
import json

import constants

AnalogInput = typing.Callable[[], float]


def Deadband(input: AnalogInput, deadband: float) -> AnalogInput:
    """take a function and reture a function which if below a threshold returns 0"""
    def withDeadband() -> float:
        value = input()
        if abs(value) <= deadband:
            return 0
        else:
            return value

    return withDeadband


def Abs(input: AnalogInput) -> AnalogInput:
    """takes a function and returns the absolute value of that function"""
    def absolute() -> float:
        inp = input()
        return -1 * inp if inp < 0 else inp

    return absolute


def Invert(input: AnalogInput) -> AnalogInput:
    """inverts the output of a function"""
    def invert() -> float:
        return -1 * input()

    return invert


class CameraControl:
    """class to contain the data related to controlling a camera"""
    def __init__(self, leftRight: AnalogInput, upDown: AnalogInput):
        self.leftRight = leftRight
        self.upDown = upDown


class HolonomicInput:
    """class containing 3 axis of motion that make a system holonomic
    all values are functions"""
    def __init__(
        self,
        forwardsBackwards: AnalogInput,
        sideToSide: AnalogInput,
        rotation: AnalogInput,
    ) -> None:
        self.forwardsBackwards = forwardsBackwards
        self.sideToSide = sideToSide
        self.rotation = rotation


class OperatorInterface:
    """
    The controls that the operator(s)/driver(s) interact with
    """
    def __init__(self) -> None:

        with open(
                path.join(path.dirname(path.realpath(__file__)),
                          'controlInterface.json'), 'r') as file:
            controlScheme = json.load(
                file
            )  # get the generau control scheme defined in controlInterface.json

        defaultControls = controlScheme[controlScheme["default"] + (
            "_SIM" if not RobotBase.isReal() else "_DRIVERSTATION"
        )]  # get controls, accounting for the difference in the simulator and the actual driverstation

        self.driveController = Joystick(
            constants.kXboxControllerPort)  # main drive controller
        self.cameraController = XboxController(
            constants.kCameraControllerPort)  # camera controller

        self.scaler = lambda: (
            self.driveController.getRawAxis(defaultControls["scaler"]) - 1
        ) * -0.5  # motor scaler, used to decrease the velocity through a single control

        self.returnPositionInput = (
            self.driveController, defaultControls["setWaypoint"], 0
        )  # D Pad / POV button to set a waypoint to return to later

        self.returnModeControl = (
            self.driveController, defaultControls["goToWaypoint"], 0
        )  # D Pad / POV button to return to the waypoint defined above

        self.fillCannon = (self.driveController, defaultControls["fillCannon"]
                           )  # button to fill the cannon for firing
        self.launchCannon = (self.driveController,
                             defaultControls["launchCannon"])  #FIRE!

        self.coordinateModeControl = (
            self.driveController, defaultControls["fieldRelative"]
        )  # switch from robot centric and field centric

        self.resetSwerveControl = (
            self.driveController, defaultControls["resetSwerveControl"]
        )  # reset swerve drive orientation and motors

        self.cameraControls = CameraControl(  # camera related axis control
            Invert(  # left/right
                Deadband(
                    lambda: self.cameraController.getX(GenericHID.Hand.
                                                       kLeftHand),
                    constants.kXboxJoystickDeadband,
                )),
            Invert(  # up/down
                Deadband(
                    lambda: self.cameraController.getY(GenericHID.Hand.
                                                       kLeftHand),
                    constants.kXboxJoystickDeadband,
                )))

        self.lightControl = Abs(lambda: self.driveController.getRawAxis(
            defaultControls["lightControl"]
        ))  # control for the lights (trigger axis by default)

        self.chassisControls = HolonomicInput(  # drive controls, allows for any directional movement and rotation
            Invert(  # forwards / backwards
                Deadband(
                    lambda: self.driveController.getRawAxis(defaultControls[
                        "forwardsBackwards"]) * self.scaler(),
                    constants.kXboxJoystickDeadband,
                )),
            Invert(  # left / right
                Deadband(
                    lambda: self.driveController.getRawAxis(defaultControls[
                        "sideToSide"]) * self.scaler(),
                    constants.kXboxJoystickDeadband,
                )),
            Invert(
                Deadband(  # rotational movement
                    lambda: self.driveController.getRawAxis(defaultControls[
                        "rotation"]) * self.scaler(),
                    constants.kXboxJoystickDeadband,
                )),
        )
