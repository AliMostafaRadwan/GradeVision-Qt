class Config:
    def __init__(self):
        self.dpi_scale = "Auto"
        self.language = "en"

    def get(self, key):
        return getattr(self, key)