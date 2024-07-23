from .inspection import self_from_frame
import inspect

class typeattr:
    def __init__(self, *args):
        length = len(args)
        if length == 0:
            last_self = self_from_frame(inspect.currentframe().f_back)
        elif length == 1:
            if isinstance(args[0], type):
                last_self = None
                self.__type = args[0]
            else:
                last_self = args[0]
        else:
            raise TypeError("`typeattr.__init__` takes up to 1 argument.")
        if last_self:
            self.__type = type(last_self)
        elif not self.__type:
            raise TypeError("the class `typeattr` without a type argument should be used in a class.")
    
    def __getitem__(self, key):
        current_type = self.__type
        item = current_type.__dict__.get(key)
        while not item:
            current_type = current_type.__base__
            item = current_type.__dict__.get(key)
        return item
    
    def __getattr__(self, name):
        return self[name]
    
    def __repr__(self) -> str:
        main_str = str(self.__type)
        splitted = main_str.split("'")
        if len(splitted) > 2:
            return f"<'{splitted[1]}': {self.__type.__dict__}>"
        else:
            return main_str
    
    @property
    def __base__(self):
        instance = super().__new__(typeattr)
        instance.__type = self.__type.__base__
        return instance