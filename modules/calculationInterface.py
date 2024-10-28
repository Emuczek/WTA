from abc import abstractmethod


# Abstract class with calculate method for all calculation methods of WTA
class CalculationInterface:

    @abstractmethod
    def calculate(self, data_path):
        pass
