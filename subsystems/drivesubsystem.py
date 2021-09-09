import commands2
import wpilib
import wpilib.drive
from wpimath.geometry import Rotation2d
from wpimath.kinematics import (
    ChassisSpeeds,
    SwerveModuleState,
    SwerveDrive4Kinematics,
    SwerveDrive4Odometry,
)

import constants

from units import units


class SwerveModule:
    def __init__(
        self,
        driveMotor: wpilib.PWMVictorSPX,
        steerMotor: wpilib.PWMVictorSPX,
        driveEncoder: wpilib.Encoder,
        steerEncoder: wpilib.Encoder,
    ) -> None:
        self.driveMotor = driveMotor
        self.steerMotor = steerMotor
        self.driveEncoder = driveEncoder
        self.steerEncoder = steerEncoder

        self.driveEncoder.setDistancePerPulse(
            constants.kWheelEncoderDistancePerPulse.to(
                units.meters / units.count
            ).magnitude
        )
        self.steerEncoder.setDistancePerPulse(
            constants.kSwerveEncoderAnglePerPulse.to(
                units.radians / units.count
            ).magnitude
        )

    def getState(self) -> SwerveModuleState:
        return SwerveModuleState(
            self.driveEncoder.getRate(),
            Rotation2d(self.steerEncoder.getDistance()),
        )

    def applyState(self, state: SwerveModuleState) -> None:
        optimizedState = SwerveModuleState.optimize(
            state, Rotation2d(self.steerEncoder.getDistance())
        )
        speedFactor = (
            optimizedState.speed
            / constants.kMaxWheelSpeed.to(units.meters / units.second).magnitude
        )
        speedFactorClamped = min(max(speedFactor, -1), 1)
        self.driveMotor.setSpeed(speedFactorClamped)
        steerError = optimizedState.angle.radians() - self.steerEncoder.getDistance()
        steerErrorClamped = min(max(steerError, -1), 1)
        self.steerMotor.setSpeed(steerErrorClamped)


class DriveSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        self.frontLeftModule = SwerveModule(
            wpilib.PWMVictorSPX(constants.kFrontLeftDriveMotorPort),
            wpilib.PWMVictorSPX(constants.kFrontLeftSteerMotorPort),
            wpilib.Encoder(*constants.kFrontLeftDriveEncoderPorts),
            wpilib.Encoder(*constants.kFrontLeftSteerEncoderPorts),
        )
        self.frontRightModule = SwerveModule(
            wpilib.PWMVictorSPX(constants.kFrontRightDriveMotorPort),
            wpilib.PWMVictorSPX(constants.kFrontRightSteerMotorPort),
            wpilib.Encoder(*constants.kFrontRightDriveEncoderPorts),
            wpilib.Encoder(*constants.kFrontRightSteerEncoderPorts),
        )
        self.backLeftModule = SwerveModule(
            wpilib.PWMVictorSPX(constants.kBackLeftDriveMotorPort),
            wpilib.PWMVictorSPX(constants.kBackLeftSteerMotorPort),
            wpilib.Encoder(*constants.kBackLeftDriveEncoderPorts),
            wpilib.Encoder(*constants.kBackLeftSteerEncoderPorts),
        )
        self.backRightModule = SwerveModule(
            wpilib.PWMVictorSPX(constants.kBackRightDriveMotorPort),
            wpilib.PWMVictorSPX(constants.kBackRightSteerMotorPort),
            wpilib.Encoder(*constants.kBackRightDriveEncoderPorts),
            wpilib.Encoder(*constants.kBackRightSteerEncoderPorts),
        )

        self.kinematics = SwerveDrive4Kinematics(
            constants.kFrontLeftWheelPosition,
            constants.kFrontRightWheelPosition,
            constants.kBackLeftWheelPosition,
            constants.kBackRightWheelPosition,
        )

        # Create the gyro, a sensor which can indicate the heading of the robot relative
        # to a customizable position.
        self.gyro = wpilib.ADXRS450_Gyro()

        # Create the an object for our odometry, which will utilize sensor data to
        # keep a record of our position on the field.
        self.odometry = SwerveDrive4Odometry(self.kinematics, self.gyro.getRotation2d())

    def periodic(self):
        """
        Called periodically when it can be called. Updates the robot's
        odometry with sensor data.
        """
        self.odometry.update(
            self.gyro.getRotation2d(),
            self.frontLeftModule.getState(),
            self.frontRightModule.getState(),
            self.backLeftModule.getState(),
            self.backRightModule.getState(),
        )

        rX = self.odometry.getPose().translation().X()
        rY = self.odometry.getPose().translation().Y()
        rAngle = int(self.odometry.getPose().rotation().degrees())

        flAngle = int(
            (self.frontLeftModule.steerEncoder.getDistance() * units.radians)
            .to(units.degrees)
            .magnitude
        )
        frAngle = int(
            (self.frontRightModule.steerEncoder.getDistance() * units.radians)
            .to(units.degrees)
            .magnitude
        )
        blAngle = int(
            (self.backLeftModule.steerEncoder.getDistance() * units.radians)
            .to(units.degrees)
            .magnitude
        )
        brAngle = int(
            (self.backRightModule.steerEncoder.getDistance() * units.radians)
            .to(units.degrees)
            .magnitude
        )

        flSpeed = self.frontLeftModule.driveMotor.getSpeed()
        frSpeed = self.frontRightModule.driveMotor.getSpeed()
        blSpeed = self.backLeftModule.driveMotor.getSpeed()
        brSpeed = self.backRightModule.driveMotor.getSpeed()

        print(
            "r: {:.1f}, {:.1f}, {}* fl: {}* {:.1f} fr: {}* {:.1f} bl: {}* {:.1f} br: {}* {:.1f}".format(
                rX,
                rY,
                rAngle,
                flAngle,
                flSpeed,
                frAngle,
                frSpeed,
                blAngle,
                blSpeed,
                brAngle,
                brSpeed,
            )
        )

    def arcadeDriveWithFactors(
        self,
        forwardSpeedFactor: float,
        sidewaysSpeedFactor: float,
        rotationSpeedFactor: float,
    ) -> None:
        """
        Drives the robot using arcade controls.

        :param forwardSpeedFactor: the commanded forward movement
        :param sidewaysSpeedFactor: the commanded sideways movement
        :param rotationSpeedFactor: the commanded rotation
        """
        # print(
        #     "inputs: x: {:.2f} y: {:.2f} *: {:.2f}".format(
        #         forwardSpeedFactor, sidewaysSpeedFactor, rotationSpeedFactor
        #     )
        # )
        chassisSpeeds = ChassisSpeeds(
            (forwardSpeedFactor * constants.kMaxForwardSpeed)
            .to(units.meters / units.second)
            .magnitude,
            (sidewaysSpeedFactor * constants.kMaxSidewaysSpeed)
            .to(units.meters / units.second)
            .magnitude,
            (rotationSpeedFactor * constants.kMaxRotationAngularSpeed)
            .to(units.radians / units.second)
            .magnitude,
        )

        self.arcadeDriveWithSpeeds(chassisSpeeds)

    def arcadeDriveWithSpeeds(self, chassisSpeeds: ChassisSpeeds) -> None:
        moduleStates = self.kinematics.toSwerveModuleStates(chassisSpeeds)
        (
            frontLeftState,
            frontRightState,
            backLeftState,
            backRightState,
        ) = SwerveDrive4Kinematics.normalizeWheelSpeeds(
            moduleStates,
            constants.kMaxWheelSpeed.to(units.meters / units.second).magnitude,
        )
        self.frontLeftModule.applyState(frontLeftState)
        self.frontRightModule.applyState(frontRightState)
        self.backLeftModule.applyState(backLeftState)
        self.backRightModule.applyState(backRightState)