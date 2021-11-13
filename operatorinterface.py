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
        with open('controlInterface.yml', 'r') as file:
            controlScheme = yaml.safe_load(file)

        defaultControls = controlScheme[controlScheme["default"]]

        self.xboxController = Joystick(constants.kXboxControllerPort)
        self.translationController = Joystick(
            constants.kTranslationControllerPort)
        self.rotationController = Joystick(constants.kRotationControllerPort)

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

        self.chassisControls = HolonomicInput(
            Invert(
                Deadband(
                    lambda: self.xboxController.getRawAxis(defaultControls[
                        "forwardsBackwards"]),
                    constants.kXboxJoystickDeadband,
                )),
            Invert(
                Deadband(
                    lambda: self.xboxController.getRawAxis(defaultControls[
                        "sideToSide"]),
                    constants.kXboxJoystickDeadband,
                )),
            Invert(
                Deadband(
                    lambda: self.xboxController.getRawAxis(defaultControls[
                        "rotation"]),
                    constants.kXboxJoystickDeadband,
                )),
        )
