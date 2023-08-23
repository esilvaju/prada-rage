from typing import Literal, Optional, TypeVar


class BaseViewModel:
    """
    A base type for view models.
    @property status A string that indicates the status of the view model. Can be either `'success'` or `'error'`.
    @property message An optional string that provides additional information about the view model.
    """
    def __init__(
            self,
            status: Literal['success'] | Literal['error'] | Literal['pending'],
            message: Optional[str] = None
            ):

        self.status = status
        self.message = message

TViewModel = TypeVar('TViewModel', bound=BaseViewModel)