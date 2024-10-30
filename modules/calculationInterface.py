from abc import abstractmethod
from PySide6.QtCore import QObject, Signal, QThread


# Abstract class with calculate method for all calculation methods of WTA
class CalculationInterface(QObject):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def calculate(self, data_path):
        pass
