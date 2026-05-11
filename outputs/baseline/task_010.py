class BigNumCalculator:
    """
    This is a class that implements big number calculations, including adding, subtracting and multiplying.
    """

    @staticmethod
    def add(num1, num2):
        """
        Adds two big numbers.
        """
        return str(int(num1) + int(num2))

    @staticmethod
    def subtract(num1, num2):
        """
        Subtracts two big numbers.
        """
        return str(int(num1) - int(num2))

    @staticmethod
    def multiply(num1, num2):
        """
        Multiplies two big numbers.
        """
        return str(int(num1) * int(num2))