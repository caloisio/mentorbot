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


class OperatorInterface:
    """
    The controls that the operator(s)/driver(s) interact with
    """

    def __init__(self) -> None:
        self.xboxController = XboxController(constants.kXboxControllerPort)
        self.translationController = Joystick(constants.kTranslationControllerPort)
        self.rotationController = Joystick(constants.kRotationControllerPort)

        self.coordinateModeControl = (
            self.xboxController,
            XboxController.Button.kRightBumper,
        )

        self.resetSwerveControl = (
            self.xboxController,
            XboxController.Button.kX,
        )

        # self.chassisControls = HolonomicInput(
        #     Invert(
        #         Deadband(
        #             lambda: self.translationController.getLeftY(GenericHID.Hand.kLeftHand),
        #             constants.kKeyboardJoystickDeadband,
        #         )
        #     ),
        #     Invert(
        #         Deadband(
        #             lambda: self.translationController.getLeftX(GenericHID.Hand.kLeftHand),
        #             constants.kKeyboardJoystickDeadband,
        #         )
        #     ),
        #     Invert(
        #         Deadband(
        #             lambda: self.rotationController.getLeftX(GenericHID.Hand.kRightHand),
        #             constants.kKeyboardJoystickDeadband,
        #         )
        #     ),
        # )

        self.chassisControls = HolonomicInput(
            Invert(
                Deadband(
                    lambda: self.xboxController.getLeftY(),
                    constants.kXboxJoystickDeadband,
                )
            ),
            Invert(
                Deadband(
                    lambda: self.xboxController.getLeftX(),
                    constants.kXboxJoystickDeadband,
                )
            ),
            Invert(
                Deadband(
                    lambda: self.xboxController.getRightX(),
                    constants.kXboxJoystickDeadband,
                )
            ),
        )
