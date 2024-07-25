from .stream_exceptions import OpenOBDStreamException


class ResponseException(OpenOBDStreamException):
    """
    Base class for all exceptions that can be raised during vehicle communication.
    """

    def __init__(self, request="", response="", request_id=0, response_id=0, **kwargs):
        self.request = request
        self.response = response
        self.request_id = request_id
        self.response_id = response_id
        super().__init__(**kwargs)

    def __str__(self):
        exception_info = self.__class__.__name__

        if self.request_id:
            exception_info += f" ({self.request_id:03X}"
            if self.response_id:
                exception_info += f" -> {self.response_id:03X}"
            exception_info += ")"
        if self.request:
            exception_info += f" request: {self.request}"
        if self.response:
            exception_info += f" response: {self.response}"

        return exception_info


class NoResponseException(ResponseException):
    """
    Did not receive a response from the vehicle in the specified time.
    """
    pass


class InvalidResponseException(ResponseException):
    """
    The response received from the vehicle does not have the correct format.
    """
    pass


class NegativeResponseException(ResponseException):
    """
    Base class for all exceptions that are raised because of a negative response received from the vehicle.
    """
    pass


class GeneralRejectException(NegativeResponseException):
    pass


class ServiceNotSupportedException(NegativeResponseException):
    pass


class SubFunctionNotSupportedException(NegativeResponseException):
    pass


class IncorrectMessageLengthOrInvalidFormatException(NegativeResponseException):
    pass


class ResponseTooLongException(NegativeResponseException):
    pass


class BusyRepeatRequestException(NegativeResponseException):
    pass


class ConditionsNotCorrectException(NegativeResponseException):
    pass


class RequestSequenceErrorException(NegativeResponseException):
    pass


class NoResponseFromSubnetComponentException(NegativeResponseException):
    pass


class FailurePreventsExecutionOfRequestedActionException(NegativeResponseException):
    pass


class RequestOutOfRangeException(NegativeResponseException):
    pass


class SecurityAccessDeniedException(NegativeResponseException):
    pass


class InvalidKeyException(NegativeResponseException):
    pass


class ExceedNumberOfAttemptsException(NegativeResponseException):
    pass


class RequiredTimeDelayNotExpiredException(NegativeResponseException):
    pass


class UploadDownloadNotAcceptedException(NegativeResponseException):
    pass


class TransferDataSuspendedException(NegativeResponseException):
    pass


class GeneralProgrammingFailureException(NegativeResponseException):
    pass


class WrongBlockSequenceCounterException(NegativeResponseException):
    pass


class RequestCorrectlyReceivedResponsePendingException(NegativeResponseException):
    pass


class SubFunctionNotSupportedInActiveSessionException(NegativeResponseException):
    pass


class ServiceNotSupportedInActiveSessionException(NegativeResponseException):
    pass


class SpecificConditionNotCorrectException(NegativeResponseException):
    pass


class RpmTooHighException(SpecificConditionNotCorrectException):
    pass


class RpmTooLowException(SpecificConditionNotCorrectException):
    pass


class EngineIsRunningException(SpecificConditionNotCorrectException):
    pass


class EngineIsNotRunningException(SpecificConditionNotCorrectException):
    pass


class EngineRunTimeTooLowException(SpecificConditionNotCorrectException):
    pass


class TemperatureTooHighException(SpecificConditionNotCorrectException):
    pass


class TemperatureTooLowException(SpecificConditionNotCorrectException):
    pass


class VehicleSpeedTooHighException(SpecificConditionNotCorrectException):
    pass


class VehicleSpeedTooLowException(SpecificConditionNotCorrectException):
    pass


class ThrottlePedalTooHighException(SpecificConditionNotCorrectException):
    pass


class ThrottlePedalTooLowException(SpecificConditionNotCorrectException):
    pass


class TransmissionRangeNotInNeutralException(SpecificConditionNotCorrectException):
    pass


class TransmissionRangeNotInGearException(SpecificConditionNotCorrectException):
    pass


class BrakeSwitchesNotClosedException(SpecificConditionNotCorrectException):
    pass


class ShifterLeverNotInParkException(SpecificConditionNotCorrectException):
    pass


class TorqueConverterClutchLockedException(SpecificConditionNotCorrectException):
    pass


class VoltageTooHighException(SpecificConditionNotCorrectException):
    pass


class VoltageTooLowException(SpecificConditionNotCorrectException):
    pass


class UnknownNegativeResponseException(NegativeResponseException):
    pass


# Based on ISO 14229-1
negative_response_code_exceptions = {
    "10": GeneralRejectException,
    "11": ServiceNotSupportedException,
    "12": SubFunctionNotSupportedException,
    "13": IncorrectMessageLengthOrInvalidFormatException,
    "14": ResponseTooLongException,
    "21": BusyRepeatRequestException,
    "22": ConditionsNotCorrectException,
    "24": RequestSequenceErrorException,
    "25": NoResponseFromSubnetComponentException,
    "26": FailurePreventsExecutionOfRequestedActionException,
    "31": RequestOutOfRangeException,
    "33": SecurityAccessDeniedException,
    "35": InvalidKeyException,
    "36": ExceedNumberOfAttemptsException,
    "37": RequiredTimeDelayNotExpiredException,
    "70": UploadDownloadNotAcceptedException,
    "71": TransferDataSuspendedException,
    "72": GeneralProgrammingFailureException,
    "73": WrongBlockSequenceCounterException,
    "78": RequestCorrectlyReceivedResponsePendingException,
    "7E": SubFunctionNotSupportedInActiveSessionException,
    "7F": ServiceNotSupportedInActiveSessionException,
    "81": RpmTooHighException,
    "82": RpmTooLowException,
    "83": EngineIsRunningException,
    "84": EngineIsNotRunningException,
    "85": EngineRunTimeTooLowException,
    "86": TemperatureTooHighException,
    "87": TemperatureTooLowException,
    "88": VehicleSpeedTooHighException,
    "89": VehicleSpeedTooLowException,
    "8A": ThrottlePedalTooHighException,
    "8B": ThrottlePedalTooLowException,
    "8C": TransmissionRangeNotInNeutralException,
    "8D": TransmissionRangeNotInGearException,
    "8F": BrakeSwitchesNotClosedException,
    "90": ShifterLeverNotInParkException,
    "91": TorqueConverterClutchLockedException,
    "92": VoltageTooHighException,
    "93": VoltageTooLowException,
}
