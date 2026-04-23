class AttrDict(dict):
    """Dict subclass whose entries can be accessed as attributes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    @classmethod
    def from_nested_dicts(cls, data):
        if not isinstance(data, dict):
            return data
        return cls({key: cls.from_nested_dicts(value) for key, value in data.items()})
