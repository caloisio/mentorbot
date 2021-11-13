from wpilib import Joystick, XboxController
from wpilib.interfaces import GenericHID

import typing

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
        self.xboxController = XboxController(constants.kXboxControllerPort)
        self.cameraController = XboxController(constants.kCameraControllerPort)
        self.translationController = Joystick(
            constants.kTranslationControllerPort)
        self.rotationController = Joystick(constants.kRotationControllerPort)

        self.coordinateModeControl = (
            self.xboxController,
            # XboxController.Button.kA.value,
            XboxController.Button.kBumperRight.value,
        )

        self.resetSwerveControl = (
            self.xboxController,
            XboxController.Button.kX.value,
        )

        self.honkControl = (
            self.xboxController,
            XboxController.Button.kB.value,
        )

        self.honkControl2 = (
            self.xboxController,
            XboxController.Button.kY.value
        )

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
                    lambda: self.xboxController.getY(GenericHID.Hand.kLeftHand) * (
                        self.xboxController.getTriggerAxis(GenericHID.Hand.kRightHand) - 1) * -0.5,
                    constants.kXboxJoystickDeadband,
                )
            ),
            Invert(
                Deadband(
                    lambda: self.xboxController.getX(GenericHID.Hand.kLeftHand) * (
                        self.xboxController.getTriggerAxis(GenericHID.Hand.kRightHand) - 1) * -0.5,
                    constants.kXboxJoystickDeadband,
                )
            ),
            Invert(
                Deadband(
                    #lambda: self.xboxController.getX(GenericHID.Hand.kRightHand),
                    lambda: self.xboxController.getTriggerAxis(GenericHID.Hand.kLeftHand) * (
                        self.xboxController.getTriggerAxis(GenericHID.Hand.kRightHand) - 1) * -0.5,
                    constants.kXboxJoystickDeadband,
                )
            ),
        )
