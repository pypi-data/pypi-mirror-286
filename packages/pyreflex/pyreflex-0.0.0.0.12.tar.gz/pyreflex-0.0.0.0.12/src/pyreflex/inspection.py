from typing import Sequence, Optional, Any
import inspect
import sys
from types import FrameType


def stack(context = 1, *, depth = 0) -> Sequence[inspect.FrameInfo]:
    '''
    Return a list of records for the stack above the indicated depth caller's frame.
    '''
    return inspect.getouterframes(sys._getframe(depth + 1), context)


def get_frame_at(depth = 0) -> Optional[FrameType]:
    '''
    Return the frame at the given depth if accessible, otherwise return `None`.
    '''
    try:
        return sys._getframe(depth + 1)
    except ValueError:
        return None


def get_frameinfo_at(depth = 0, context = 1) -> Optional[inspect.FrameInfo]:
    '''
    Return the `FrameInfo` instance at the given depth if accessible, otherwise return `None`.
    '''
    frame = get_frame_at(depth)
    if frame:
        frameinfo = (frame,) + inspect.getframeinfo(frame, context)
        return inspect.FrameInfo(*frameinfo)


def self_from_frame(frame: FrameType) -> Any:
    '''
    Get the `self` instance of the frame if the frame is a called method, otherwise `None` will be returned.
    '''
    co_varnames = frame.f_code.co_varnames
    if len(co_varnames) > 0:
        module_self = co_varnames[0]
        module_self = frame.f_locals[module_self]
        func_name = frame.f_code.co_name
        from .mirror import get_instruction_at
        from dis import opmap
        # if not (func_name in frame.f_back.f_locals):
        back_frame = frame.f_back
        instruction = get_instruction_at(back_frame.f_code, back_frame.f_lasti)
        if hasattr(object, func_name) or instruction.opcode == opmap['CALL_METHOD']:
            return module_self
        elif instruction.opcode == opmap['CALL_FUNCTION']:
            return None
        else:
        # if instruction.opcode == opmap['CALL_FUNCTION_KW'] or instruction.opcode == opmap['CALL_FUNCTION_EX']:
            for i in range(back_frame.f_lasti - 2, -1, -2):
                instruction = get_instruction_at(back_frame.f_code, back_frame.f_lasti - i)
                if instruction.argval == func_name:
                    if instruction.opcode == opmap['LOAD_ATTR']:
                        return module_self
                    else:
                        return None


def overriding_depth() -> int:
    '''
    Used in the function that has been overriden by subclasses, with the current called overriding depth returned.
    '''
    frame = inspect.currentframe().f_back
    if frame:
        method_name = frame.f_code.co_name
        self = self_from_frame(frame)
        if self:
            frame = frame.f_back
            i = 1
            while frame and (frame.f_code.co_name == method_name and self_from_frame(frame) is self):
                i += 1
                frame = frame.f_back
            return i
    return 0