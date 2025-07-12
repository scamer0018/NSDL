class DynamicConfig:
    def __init__(self, config):
        self.__dict__["_config"] = config
        for key, value in config.items():
            if isinstance(value, dict):
                value = DynamicConfig(value)
            setattr(self, key, value)

    def get(self, key, default=None):
        return getattr(self, key, default)
