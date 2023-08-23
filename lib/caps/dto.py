from typing import Dict, Any, Optional, Literal
import json
from io import BytesIO


class BaseDTO:
    """
    A data transfer object (DTO) that can be used to represent the response of an API endpoint
    """

    def __init__(
            self, 
# A string literal type that indicates the status of the API response. It can be either 'success' or `error'
            status: Literal['success', 'error'],
# An optional number that indicates the error code. Usually contains an HTTP status code
            error_code: Optional[int] = None,
# An optional string that indicates the error message. Usually contains an error message
            error_message: Optional[str] = None,
# An optional string that provides the name of the error that occurred
            error_name: Optional[str] = None,
# An optional string that provides the type of the error that occurred. Usually contains the name and src of the error
            error_type: Optional[Literal['gateway_endpoint_error'] | str] = None
            ):
        """
        @property 
        """

        self.status = status
        self.error_code = error_code
        self.error_message = error_message
        self.error_name = error_name
        self.error_type = error_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            'status': self.status,
            'errorCode': self.error_code,
            'errorMessage': self.error_message,
            'errorName': self.error_name,
            'errorType': self.error_type
        }

class DTOEncoder:
    def encode(self, dto: BaseDTO) -> bytes:
        return BytesIO(json.dumps(dto.to_dict()).encode('utf-8')).getvalue()
