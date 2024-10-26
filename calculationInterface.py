from abc import abstractmethod


class CalculationInterface:

    # should retur a tuple of main_image_path and list of images
    @abstractmethod
    def calculate(self, image_path):
        pass