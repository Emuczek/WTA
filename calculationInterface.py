from abc import abstractmethod


class CalculationInterface:

    @abstractmethod
    def calculate(self, data_path):
        pass