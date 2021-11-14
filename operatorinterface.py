from wpilib import Joystick, XboxController
from wpilib.interfaces import GenericHID

import typing
import yaml

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

class CameraControl:
    def __init__(self, leftRight: AnalogInput, upDown: AnalogInput):
        self.leftRight = leftRight
        self.upDown = upDown

class OperatorInterface:
    """
    The controls that the operator(s)/driver(s) interact with
    """
    def __init__(self) -> None:        

        with open('controlInterface.yml', 'r') as file:
            controlScheme = yaml.safe_load(file)

        defaultControls = controlScheme[controlScheme["default"]]

        self.xboxController = Joystick(constants.kXboxControllerPort)
        self.cameraController = XboxController(constants.kCameraControllerPort)
        self.translationController = Joystick(
            constants.kTranslationControllerPort)
        self.rotationController = Joystick(constants.kRotationControllerPort)
        
        self.scaler = lambda: (self.xboxController.getTriggerAxis(GenericHID.Hand.kRightHand) -1 ) * -1
        self.rotation = lambda: self.xboxController.getX(GenericHID.Hand.kRightHand)

        self.returnPositionInput = (
            self.xboxController,
            180,
            0 
        )

        self.returnModeControl = (
            self.xboxController,
            0, 
            0
        )

        self.honkControl = (
            self.xboxController,
            XboxController.Button.kB.value,
        )

        self.honkControl2 = (
            self.xboxController,
            XboxController.Button.kY.value
        )

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
                    lambda: self.cameraController.getX(GenericHID.Hand.kLeftHand), constants.kXboxJoystickDeadband,)), Invert(
                Deadband(lambda: self.cameraController.getY(GenericHID.Hand.kLeftHand), constants.kXboxJoystickDeadband,)))
        self.backLightControl = Abs(
            lambda: self.cameraController.getTriggerAxis(
                GenericHID.Hand.kLeftHand))
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

