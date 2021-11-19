from os import path
from wpilib import Joystick, XboxController, RobotBase
from wpilib.interfaces import GenericHID

import typing
import json

import constants

AnalogInput = typing.Callable[[], float]


def Deadband(input: AnalogInput, deadband: float) -> AnalogInput:
    def withDeadband() -> float:
        value = input()
        if abs(value) <= deadband:
            return 0
        else:
            return value

    return withDeadband


def Abs(input: AnalogInput) -> AnalogInput:
    def absolute() -> float:
        inp = input()
        return -1 * inp if inp < 0 else inp

    return absolute


def Invert(input: AnalogInput) -> AnalogInput:
    def invert() -> float:
        return -1 * input()

    return invert


class CameraControl:
    def __init__(self, leftRight: AnalogInput, upDown: AnalogInput):
        self.leftRight = leftRight
        self.upDown = upDown


class HolonomicInput:
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
            controlScheme = json.load(file)

        defaultControls = controlScheme[controlScheme["default"] + (
            "_SIM" if not RobotBase.isReal() else "_DRIVERSTATION")]

        self.xboxController = Joystick(constants.kXboxControllerPort)
        self.cameraController = XboxController(constants.kCameraControllerPort)
        self.translationController = Joystick(
            constants.kTranslationControllerPort)
        self.rotationController = Joystick(constants.kRotationControllerPort)

        self.scaler = lambda: (self.xboxController.getRawAxis(defaultControls[
            "scaler"]) - 1) * -0.5

        self.returnPositionInput = (self.xboxController, 180, 0)

        self.returnModeControl = (self.xboxController, 0, 0)

        self.honkControl = (
            self.xboxController,
            XboxController.Button.kB.value,
        )

        self.fillCannon = (self.xboxController, defaultControls["fillCannon"])
        self.launchCannon = (self.xboxController,
                             defaultControls["launchCannon"])

        self.honkControl2 = (self.xboxController,
                             XboxController.Button.kY.value)

        self.coordinateModeControl = (self.xboxController,
                                      defaultControls["fieldRelative"])

        self.resetSwerveControl = (self.xboxController,
                                   defaultControls["resetSwerveControl"])

        # self.chassisControls = HolonomicInput(
        #     Invert(
        #         Deadband(
        #             lambda: self.translationController.getY(GenericHID.Hand.kLeftHand),
        #             constants.kKeyboardJoystickDeadband,
        #         )
        #     ),
        #     Invert(
        #         Deadband(
        #             lambda: self.translationController.getX(GenericHID.Hand.kLeftHand),
        #             constants.kKeyboardJoystickDeadband,
        #         )
        #     ),
        #     Invert(
        #         Deadband(
        #             lambda: self.rotationController.getX(GenericHID.Hand.kRightHand),
        #             constants.kKeyboardJoystickDeadband,
        #         )
        #     ),
        # )

        self.cameraControls = CameraControl(
            Invert(
                Deadband(
                    lambda: self.cameraController.getX(GenericHID.Hand.
                                                       kLeftHand),
                    constants.kXboxJoystickDeadband,
                )),
            Invert(
                Deadband(
                    lambda: self.cameraController.getY(GenericHID.Hand.
                                                       kLeftHand),
                    constants.kXboxJoystickDeadband,
                )))
        self.backLightControl = Abs(lambda: self.cameraController.
                                    getTriggerAxis(GenericHID.Hand.kLeftHand))
        self.chassisControls = HolonomicInput(
            Invert(
                Deadband(
                    lambda: self.xboxController.getRawAxis(defaultControls[
                        "forwardsBackwards"]) * self.scaler(),
                    constants.kXboxJoystickDeadband,
                )),
            Invert(
                Deadband(
                    lambda: self.xboxController.getRawAxis(defaultControls[
                        "sideToSide"]) * self.scaler(),
                    constants.kXboxJoystickDeadband,
                )),
            Invert(
                Deadband(
                    lambda: self.xboxController.getRawAxis(defaultControls[
                        "rotation"]) * self.scaler(),
                    constants.kXboxJoystickDeadband,
                )),
        )
