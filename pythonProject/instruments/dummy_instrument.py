

class DummyIntrument:
    def __init__(self, intrument_label):
        self.intrument_label = intrument_label
        self.parent_sattelite = None

    def assign_sattelite(self, sattelite_pointer):
        self.parent_sattelite = sattelite_pointer

    def measure(self, data_from_objects):
        pass




