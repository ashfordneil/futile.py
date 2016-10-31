#!/usr/bin/env python3
import math
import sys

class DecimalFloat:
    """
    Stores a floating point number with a mantissa and exponent, in base 10.

    Attributes:
        _mantissa: float -- Mantissa of the DecimalFloat
        _exponent: int -- Exponent of the DecimalFloat
    """

    def __init__(self, param):
        """
        Default constructor. Accepts a parameter that can be cast to a floating
        point number.
        """
        self._exponent = int(math.log10(float(param)))
        if (10 ** self._exponent > float(param)):
            self._exponent -= 1
        self._mantissa = float(param) / (10 ** self._exponent)

    def __float__(self):
        """
        Casts to a regular floating point number.
        """
        return (self._mantissa * 10 ** self._exponent)

    def __repr__(self):
        """
        For printing.
        """
        return "DecimalFloat: {0}".format(self)
    def __str__(self):
        """
        Casts to a string.
        """
        return "{0} * 10**{1}".format(self._mantissa, self._exponent)

    def __add__(self, param):
        """
        Floating point addition.
        """
        return DecimalFloat(float(self) + float(param))

    def __radd__(self, param):
        """
        Right floating point addition.
        """
        return DecimalFloat(float(param) + float(self))

    def __sub__(self, param):
        """
        Floating point subtraction.
        """
        return DecimalFloat(float(self) - float(param))

    def __rsub__(self, param):
        """
        Right floating point subtraction.
        """
        return DecimalFloat(float(param) - float(self))

    def __mul__(self, param):
        """
        Floating point multiplication.
        """
        return DecimalFloat(float(self) * float(param))

    def __rmul__(self, param):
        """
        Right floating point multiplication.
        """
        return DecimalFloat(float(param) * float(self))

    def __truediv__(self, param):
        """
        Floating point division.
        """
        return DecimalFloat(float(self) / float(param))

    def __rtruediv__(self, param):
        """
        Right floating point division.
        """
        return DecimalFloat(float(param) / float(self))

class Resistor:
    """
    Stores a single standardised resistor.

    Static Attributes:
        mantissas: list[float] -- Possible mantissas for standardised
            resistors.
        exponents: range -- Possible exponents for standardised resistors.

    Attributes:
        _value: DecimalFloat -- Value of the resistor.
    """
    mantissas = [
            1.0, 1.2, 1.5, 1.8, 2.2, 2.7,
            3.3, 3.9, 4.7, 5.6, 6.8, 8.2
            ]
    exponents = range(1, 9)

    def __init__(self, param):
        """
        Default constructor for a resistor. Accepts a parameter that can be
        cast to a floating point number, and stores it as a DecimalFloat that
        best approximates the given value with a standardised resistor size.
        """
        value = DecimalFloat(param)
        if value._mantissa > Resistor.mantissas[-1]:
            value._mantissa = Resistor.mantissas[0]
            value._exponent += 1
        if not value._exponent in Resistor.exponents:
            raise ValueError("Resistors must be between 10R and 820M")
        for mantissa in Resistor.mantissas:
            if mantissa >= value._mantissa:
                value._mantissa = mantissa
                self._value = value
                return

    def __float__(self):
        """
        Casts to a regular floating point number.
        """
        return float(self._value)

    def __repr__(self):
        """
        For printing.
        """
        return "Resistor: {0}".format(self)
    def __str__(self):
        """
        Casts to a string.
        """
        mantissa = self._value._mantissa
        exponent = self._value._exponent

        # round to nearest power of 1000
        mantissa *= 10 ** int(exponent % 3)
        exponent = int(exponent / 3)

        output = str(mantissa)
        output = output.replace('.', ['R', 'K', 'M'][exponent])
        return output.strip("0")

    def __add__(self, param):
        """
        Addition in parallel.
        """
        if (param == 0):
            return self
        return DecimalFloat(1 / ((1 / float(self)) + (1 / float(param))))

    def __radd__(self, param):
        """
        Addition in parallel.
        """
        if (param == 0):
            return self
        return DecimalFloat(1 / ((1 / float(param)) + (1 / float(self))))

    def __sub__(self, param):
        """
        Subtraction in parallel.
        """
        if (float(self) == float(param)):
            return 0
        return DecimalFloat(1 / ((1 / float(self)) - (1 / float(param))))

    def __rsub__(self, param):
        """
        Subtraction in parallel.
        """
        return DecimalFloat(1 / ((1 / float(param)) - (1 / float(self))))

def approximateResistor(value, tolerance = 0.01):
    """
    Returns an array of standardised resistors that approximate a given value.

    Parameters:
        value: float -- The value to approximate.
    """
    value = float(value)
    output = [Resistor(value)]
    try:
        while True:
            currentValue = 0
            for approxValue in output:
                currentValue = approxValue + currentValue

            if abs(float(currentValue) - value) / value < tolerance:
                return output

            difference = Resistor.__sub__(value, currentValue)
            output.append(Resistor(difference))
    except ValueError:
        # We fucked up, and the largest possible resistor value was reached
        return output

def main(argv):
    # check invalid arguments
    if len(argv) == 1 or len(argv) > 3:
        print("Usage: {0} Resistance [Tolerance]".format(argv[0]))
        exit()

    # calculate resistance
    if len(argv) == 3:
        # tolerance needs to be calculated
        tolerance = argv[2]
        if tolerance[-1] == "%":
            tolerance = float(tolerance[:-1]) / 100
        else:
            tolerance = float(tolerance)
        approximation = approximateResistor(argv[1], tolerance)
    else:
        approximation = approximateResistor(argv[1])

    # format and print output
    print(".")
    for approxValue in approximation[:-1]:
        print("├─ {0}".format(approxValue))
    print("└─ {0}".format(approximation[-1]))

if __name__ == "__main__":
    main(sys.argv)
