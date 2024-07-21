class Model:
    @property
    def _key(self):
        return f"__{self.__class__.__name__}__"

    @classmethod
    def _keyname(cls):
        return f"__{cls.__name__}__"
    
    def __new__(cls, **kwargs):
        instance = super(Model, cls).__new__(cls)
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance

    def _to_dict(self):
        return {
            self._key: self.__dict__.copy()
        }

    def _from_dict(self, data):
        if self._key in data:
            self.__dict__.update(data[self._key])

        return self

    @classmethod
    def _deserialize(cls, data):
        return cls._from_dict(data)