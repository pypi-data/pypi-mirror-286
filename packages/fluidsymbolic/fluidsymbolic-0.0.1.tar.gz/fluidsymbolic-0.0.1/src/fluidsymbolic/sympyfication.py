import sympy as sp
import sympy.abc as spa
import sympy.physics.vector
import numpy as np
import matplotlib.pyplot as plt
from typing import TypeAlias, List, Tuple, Callable, Any
import typing
import math
from scipy import integrate
from matplotlib.animation import Animation

type_expr: TypeAlias = sp.core.expr.Expr
type_symbols: TypeAlias = Any



class SympyManager:
    def init_sympy(self) -> Callable:
        """
        Returns  the pretty print function and does init_printing

        :return: pretty print sympy
        """
        def print_sympy(expression):
            sp.pretty_print(expression)

        # Define symbols
        sp.init_printing()
        return print_sympy

    def init_cartesian(self) -> Tuple[
        List[type_symbols],
        Callable]:
        # cartesian coordinates:
        x: type_symbols = spa.x
        y: type_symbols = spa.y

        print_function: Callable = self.init_sympy()
        result: List[type_symbols] = [x, y]
        return (result, print_function)

    @classmethod
    def find_curl_cartesian(cls,
                                    psi: type_expr,
                                    x_sympy: type_symbols,
                                    y_sympy: type_symbols
                                  ) -> List[type_expr]:
        """
        Find the curl/curl in cartesian coordinates

        :param psi: The scalar field stream function in the sympy language

        :param x_sympy: X in the sympy language

        :param y_sympy: Y in the sympy language

        :return: Returns the list of CurlX, CurlY and CurlZ
        """
        curl_x: type_expr = sp.diff(psi, y_sympy)  # Note that V_z is assumed to be 0
        curl_x = curl_x.simplify()
        print("Curl X done")
        curl_y: type_expr = - sp.diff(psi,  x_sympy)  # Note that V_z is assumed to be 0
        curl_y = curl_y.simplify()
        print("Curl Y done")
        curl_z: type_expr = sp.diff(psi, x_sympy) - sp.diff(psi, y_sympy)
        curl_z = curl_z.simplify()
        print("Curl Z done")
        # Represent the curl components as a list
        curl_V = [curl_x, curl_y, curl_z]

        return curl_V
