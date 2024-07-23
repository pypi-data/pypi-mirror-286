def hidden(obj):
    obj.__ishidden__ = True
    return obj


class HiddenMeta(type):
    def __new__(metacls, name, bases, namespace):
        cls = super().__new__(metacls, name, bases, namespace)
        hidden_names = []
        for name, obj in namespace.items():
            if getattr(obj, '__ishidden__', False):
                hidden_names.append(name)
        original_getattribute = cls.__getattribute__
        def __getattribute__(self, name: str):
            if name in hidden_names:
                self_dict: dict = original_getattribute(self, '__dict__')
                item = self_dict.get(name)
                if item:
                    return item
                else:
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
            else:
                return original_getattribute(self, name)
        cls.__getattribute__ = __getattribute__
        return cls