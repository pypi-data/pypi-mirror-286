import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from typing import TypeAlias, List, Tuple, Callable, Any, Literal
import typing
import matplotlib.patches
from scipy import integrate
from matplotlib.animation import FuncAnimation
from functools import cached_property
import multiprocessing
from .sympyfication import SympyManager
from queue import Empty
type_expr: TypeAlias = sp.core.expr.Expr
type_symbols: TypeAlias = Any


class StreamFunctionManager:
    """
    This object handles all the stream functions
    """

    @classmethod
    def cylinder_stream_function_porous(cls,
                                 x_sympy: type_expr,
                                 y_sympy: type_expr,
                                 epsilon_sympy: type_expr,
                                 max_velocity: float = 1.,
                                 max_cylinder_radius: float = 1.,
                                 origin_x: float = 0,
                                 origin_y: float = 0) \
            -> Tuple[type_expr, List[type_expr]]:
        """
        https://en.wikipedia.org/wiki/Potential_flow_around_a_circular_cylinder
        Returns the Sympy expression and the Sympy curl expression
         in the case of a cylinder stream that is porous, of max velocity max_velocity, and of
         cylinder radius max_cylinder_radius with epsilon epsilon_sympy

        Origin x and origin y are where the cylindrical coordinates are
        converted from cartesian coordinates

        :param x_sympy: expression of the x in the sympy language

        :param y_sympy: expression of the x in the sympy language

        :param epsilon_sympy:

        :param max_cylinder_radius:

        :param max_velocity:

        :param max_cylinder_radius:

        :param origin_x:

        :param origin_y:

        :return: Tuple of stream function and curl stream function
        """
        # Translating to cylindrical coordinates
        r = sp.sqrt((x_sympy - origin_x) ** 2 + (y_sympy - origin_y) ** 2)
        theta = sp.atan2(y_sympy, x_sympy)

        # Calculating the stream function:
        expr = max_velocity * sp.sin(theta) * (
                    r - (max_cylinder_radius ** 2 / r))
        expr = expr + max_velocity * sp.sin(2*theta) \
            * epsilon_sympy * (max_cylinder_radius ** 3 / r**2)

        # Calculating the curl
        curl_expr: List[type_expr] = (
            cls.find_curl_cartesian(expr, x_sympy, y_sympy))
        curl_expr = [k.simplify().together().simplify() for k in curl_expr]
        # Simplifying
        expr = expr.simplify().together().simplify()
        # print("expr")
        # print(expr)
        # print("curl")
        # print(curl_expr)
        return expr, curl_expr


    @classmethod
    def cylinder_stream_slightly_distorted(cls,
                                 x_sympy: type_expr,
                                 y_sympy: type_expr,
                                 epsilon_sympy: type_expr,
                                 max_velocity: float = 1.,
                                 max_cylinder_radius: float = 1.,
                                 origin_x: float = 0,
                                 origin_y: float = 0) \
            -> Tuple[type_expr, List[type_expr]]:
        """
        https://en.wikipedia.org/wiki/Potential_flow_around_a_circular_cylinder
        Returns the Sympy expression and the Sympy curl expression
         in the case of a cylinder stream that is slightly distored of max velocity max_velocity, and of
         cylinder radius max_cylinder_radius with epsilon epsilon_sympy

        Origin x and origin y are where the cylindrical coordinates are
        converted from cartesian coordinates

        :param x_sympy: expression of the x in the sympy language

        :param y_sympy: expression of the x in the sympy language

        :param epsilon_sympy: Epsilon

        :param max_cylinder_radius:

        :param max_velocity:

        :param max_cylinder_radius:

        :param origin_x:

        :param origin_y:

        :return: Tuple of stream function and curl stream function
        """
        # Translating to cylindrical coordinates
        r = sp.sqrt((x_sympy - origin_x) ** 2 + (y_sympy - origin_y) ** 2)
        theta = sp.atan2(y_sympy, x_sympy)

        # Calculating the stream function:
        adimensional_length = max_cylinder_radius/r
        expr = max_velocity * sp.sin(theta) * (
                    r - (max_cylinder_radius ** 2 / r))
        expr = expr + max_velocity * (r/2) \
            * epsilon_sympy * (3*(adimensional_length**2)*sp.sin(theta)-1*(adimensional_length**4)*(sp.sin(3*theta)))
        expr = expr.expand().simplify()
        print(expr)
        # Calculating the curl
        curl_expr: List[type_expr] = (
            cls.find_curl_cartesian(expr, x_sympy, y_sympy))
        print(curl_expr)

        def my_task(curl_expr, result_queue):
            result = [k.simplify().together().simplify() for k in curl_expr]
            result_queue.put(result)


        # Create a multiprocessing pool with one worker
        result_queue = multiprocessing.Queue()

        # Apply the task asynchronously
        p = multiprocessing.Process(target=my_task, args=(curl_expr, result_queue))
        p.start()

        p.join(timeout=5)
        print("Test")
        if p.is_alive():
            # print(f"Pool timed out trying to simplify {repr(curl_expr)}")
            p.terminate()
            output = curl_expr
        else:
            try:
                output = result_queue.get(
                    timeout=1)  # Adjust timeout as needed
                # print("Task output:", output)
            except Empty:
                # If the queue is empty, it means the task did not produce any output
                # print(
                #     f"Pool timed out trying to simplify {repr(curl_expr)}")
                output = curl_expr

        # Simplifying
        expr = expr.simplify().together().simplify()
        # print("expr")
        # print(expr)
        # print("curl")
        # print(curl_expr)
        return expr, curl_expr


    @classmethod
    def cylinder_stream_janzen_rayleigh_expansion(cls,
                                 x_sympy: type_expr,
                                 y_sympy: type_expr,
                                 m_sympy: type_expr,
                                 epsilon_sympy: type_expr,
                                 max_velocity: float = 1.,
                                 max_cylinder_radius: float = 1.,
                                 origin_x: float = 0,
                                 origin_y: float = 0) \
            -> Tuple[type_expr, List[type_expr]]:
        """
        https://en.wikipedia.org/wiki/Potential_flow_around_a_circular_cylinder
        Returns the Sympy expression and the Sympy curl expression
         in the case of a cylinder stream  Janzen–Rayleigh expansion, and of
         cylinder radius max_cylinder_radius with epsilon epsilon_sympy

        Origin x and origin y are where the cylindrical coordinates are
        converted from cartesian coordinates

        Note 1: There is an error on the Wikipédia article, they wrote a plus instead of a minus. This code takes a minus.

        Note 2: The vorticity takes too long to compute, so I just give a TimeoutError instead.

        :param x_sympy: expression of the x in the sympy language

        :param y_sympy: expression of the x in the sympy language

        :param epsilon_sympy: Epsilon

        :param epsilon_sympy: M

        :param max_cylinder_radius:

        :param max_velocity:

        :param max_cylinder_radius:

        :param origin_x:

        :param origin_y:

        :return: Tuple of stream function and curl stream function
        """
        # Translating to cylindrical coordinates
        r = sp.sqrt((x_sympy - origin_x) ** 2 + (y_sympy - origin_y) ** 2)
        theta = sp.atan2(y_sympy, x_sympy)

        # Calculating the stream function:
        adimensional_length = max_cylinder_radius/r
        expr = max_velocity * sp.sin(theta) * (
                    r - (max_cylinder_radius ** 2 / r)) # There is an error on the Wikipedia article, they wrote "+" instead of minus but they are wrong.
        term_1 = 13*(adimensional_length**2) - 6*(adimensional_length**4) + 1*(adimensional_length**6)
        term_2 = 1*(adimensional_length**4) - 3*(adimensional_length**2)
        expr = expr + (m_sympy**2)*max_velocity*(r/12)*(term_1*sp.sin(theta) + term_2*sp.sin(3*theta))
        expr = expr.expand().simplify()
        print(expr)
        # Calculating the curl
        NON_FUNCTIONAL = True
        if NON_FUNCTIONAL:
            return expr, TimeoutError
        curl_expr: List[type_expr] = (
            cls.find_curl_cartesian(expr, x_sympy, y_sympy))
        print(curl_expr)

        def my_task(curl_expr, result_queue):
            result = [k.simplify().together().simplify() for k in curl_expr]
            result_queue.put(result)


        # Create a multiprocessing pool with one worker
        result_queue = multiprocessing.Queue()

        # Apply the task asynchronously
        p = multiprocessing.Process(target=my_task, args=(curl_expr, result_queue))
        p.start()

        p.join(timeout=5)
        print("Test")
        if p.is_alive():
            # print(f"Pool timed out trying to simplify {repr(curl_expr)}")
            p.terminate()
            output = curl_expr
        else:
            try:
                output = result_queue.get(
                    timeout=1)  # Adjust timeout as needed
                # print("Task output:", output)
            except Empty:
                # If the queue is empty, it means the task did not produce any output
                # print(
                #     f"Pool timed out trying to simplify {repr(curl_expr)}")
                output = curl_expr

        # Simplifying
        expr = expr.simplify().together().simplify()
        # print("expr")
        # print(expr)
        # print("curl")
        # print(curl_expr)
        return expr, curl_expr

    @classmethod
    def cylinder_stream_function_slight_vorticity_linear_shear(cls,
                                 x_sympy: type_expr,
                                 y_sympy: type_expr,
                                 epsilon_sympy: type_expr,
                                 max_velocity: float = 1.,
                                 max_cylinder_radius: float = 1.,
                                 origin_x: float = 0,
                                 origin_y: float = 0) \
            -> Tuple[type_expr, List[type_expr]]:
        """
        https://en.wikipedia.org/wiki/Potential_flow_around_a_circular_cylinder
        Returns the Sympy expression and the Sympy curl expression
         in the case of a cylinder stream with slight vorticity in the case of a linear shear,
          of max velocity max_velocity, and of
         cylinder radius max_cylinder_radius with epsilon epsilon_sympy

        Origin x and origin y are where the cylindrical coordinates are
        converted from cartesian coordinates

        :param x_sympy: expression of the x in the sympy language

        :param y_sympy: expression of the x in the sympy language

        :param epsilon_sympy:

        :param max_cylinder_radius:

        :param max_velocity:

        :param max_cylinder_radius:

        :param origin_x:

        :param origin_y:

        :return: Tuple of stream function and curl stream function
        """
        # Translating to cylindrical coordinates
        r = sp.sqrt((x_sympy - origin_x) ** 2 + (y_sympy - origin_y) ** 2)
        theta = sp.atan2(y_sympy, x_sympy)

        # Calculating the stream function:
        expr = max_velocity * sp.sin(theta) * (
                    r - (max_cylinder_radius ** 2 / r))
        parens_expr_1 = (r/max_cylinder_radius)*(1- sp.cos(2*theta))
        parens_expr_3 = (max_cylinder_radius / r)
        parens_expr_2 = (parens_expr_3**3)* sp.cos(2*theta)

        expr = expr + (epsilon_sympy * max_velocity * (r/4) *
                (parens_expr_1 + parens_expr_2 - parens_expr_3))
        print(expr)
        print(sp.latex(expr))
        # Calculating the curl
        curl_expr: List[type_expr] = (
            cls.find_curl_cartesian(expr, x_sympy, y_sympy))
        curl_expr = [k.simplify().together().simplify() for k in curl_expr]
        # Simplifying
        expr = expr.simplify().together().simplify()
        # print("expr")
        # print(expr)
        # print("curl")
        # print(curl_expr)
        return expr, curl_expr



    @classmethod
    def cylinder_stream_function_slight_vorticity_parabolic_shear(cls,
                                 x_sympy: type_expr,
                                 y_sympy: type_expr,
                                 epsilon_sympy: type_expr,
                                 chi_sympy: type_expr,
                                 max_velocity: float = 1.,
                                 max_cylinder_radius: float = 1.,
                                 origin_x: float = 0,
                                 origin_y: float = 0) \
            -> Tuple[type_expr, List[type_expr]]:
        """
        https://en.wikipedia.org/wiki/Potential_flow_around_a_circular_cylinder
        Returns the Sympy expression and the Sympy curl expression
         in the case of a cylinder stream with slight vorticity in the case of a parabolic shear,
          of max velocity max_velocity, and of
         cylinder radius max_cylinder_radius with epsilon epsilon_sympy

        Origin x and origin y are where the cylindrical coordinates are
        converted from cartesian coordinates

        :param x_sympy: expression of the x in the sympy language

        :param y_sympy: expression of the x in the sympy language

        :param epsilon_sympy: Epsilon in parabolic shear

        :param chi_sympy: Xi in parabolic shear

        :param max_cylinder_radius:

        :param max_velocity:

        :param max_cylinder_radius:

        :param origin_x:

        :param origin_y:

        :return: Tuple of stream function and curl stream function
        """
        # Translating to cylindrical coordinates
        r = sp.sqrt((x_sympy - origin_x) ** 2 + (y_sympy - origin_y) ** 2)
        theta = sp.atan2(y_sympy, x_sympy)

        # Calculating the stream function:
        expr = max_velocity * sp.sin(theta) * (
                    r - (max_cylinder_radius ** 2 / r))
        parens_expr_1 = (r*sp.sin(theta)/max_cylinder_radius)**2
        parens_expr_2 = 3*r*sp.log(r)*sp.sin(theta)

        expr = expr + (epsilon_sympy * max_velocity * (r/6) *
                       (parens_expr_1 - parens_expr_2 + chi_sympy))
        print(expr)
        print(sp.latex(expr))
        # Calculating the curl
        curl_expr: List[type_expr] = (
            cls.find_curl_cartesian(expr, x_sympy, y_sympy))
        curl_expr = [k.simplify().together().simplify() for k in curl_expr]
        # Simplifying
        expr = expr.simplify().together().simplify()
        # print("expr")
        # print(expr)
        # print("curl")
        # print(curl_expr)
        return expr, curl_expr


    @classmethod
    def cylinder_stream_function(cls,
                                 x_sympy,
                                 y_sympy,
                                 max_velocity: float = 1.,
                                 max_cylinder_radius: float = 1.,
                                 origin_x: float = 0,
                                 origin_y: float = 0) \
            -> Tuple[type_expr, List[type_expr]]:
        """
        https://en.wikipedia.org/wiki/Potential_flow_around_a_circular_cylinder
        Returns the Sympy expression and the Sympy curl expression
         in the case of a cylinder stream, of max velocity max_velocity, and of
         cylinder radius max_cylinder_radius

        Origin x and origin y are where the cylindrical coordinates are
        converted from cartesian coordinates

        :param x_sympy: expression of the x in the sympy language

        :param y_sympy: expression of the x in the sympy language

        :param max_cylinder_radius:

        :param max_velocity:

        :param max_cylinder_radius:

        :param origin_x:

        :param origin_y:

        :return: Tuple of stream function and curl stream function
        """
        # Translating to cylindrical coordinates
        r = sp.sqrt((x_sympy - origin_x) ** 2 + (y_sympy - origin_y) ** 2)
        theta = sp.atan2(y_sympy, x_sympy)

        # Calculating the stream function:
        expr = max_velocity * sp.sin(theta) * (
                    r - (max_cylinder_radius ** 2 / r))

        # Calculating the curl
        curl_expr: List[type_expr] = (
            cls.find_curl_cartesian(expr, x_sympy, y_sympy))
        curl_expr = [k.simplify().together().simplify() for k in curl_expr]
        # Simplifying
        expr = expr.simplify().together().simplify()
        # print("expr")
        # print(expr)
        # print("curl")
        # print(curl_expr)
        return expr, curl_expr

    @classmethod
    def corner_stream_cartesian_function(cls,
                                         x_sympy: type_symbols,
                                         y_sympy: type_symbols,
                                         n: float = 0.5,
                                         max_velocity: float = 1.):
        """
        Returns the Sympy expression and the Sympy curl expression
         in the case of a corner, of max velocity max_velocity, of power n

        :param x_sympy: expression of the x in the sympy language

        :param y_sympy: expression of the x in the sympy language

        :param n: power

        :param max_velocity:

        :return: Tuple of stream function and curl stream function

        :raise NotImplementedError: Raises implemented error if n==1
        """
        if n == 1:
            raise NotImplemented("Not functional")
        r = sp.sqrt(x_sympy ** 2 + y_sympy ** 2)
        theta = sp.atan2(x_sympy, y_sympy)
        expr = max_velocity * (r ** n) * sp.sin(n * theta)
        # print(expr)
        curl_expr: List[type_expr] = (
            cls.find_curl_cartesian(expr, x_sympy, y_sympy))
        expr = expr.simplify().together().simplify()
        return expr, curl_expr

    @classmethod
    def source_sink_stream_function(cls,
                                    x_sympy: type_symbols,
                                    y_sympy: type_symbols,
                                    source_term: float = 1.):  # Not Functional
        # r = sp.sqrt(x_sympy ** 2 + y_sympy ** 2)
        # theta = sp.atan2(y_sympy, x_sympy)
        i_symbol = sp.symbols('i')
        expr = (source_term / (2 * sp.pi)) * sp.log(
            x_sympy + i_symbol * y_sympy)
        # print(expr)
        curl_expr: List[type_expr] = (
            cls.find_curl_cartesian(expr, x_sympy, y_sympy))
        expr = expr.simplify().together().simplify()
        return expr, curl_expr

    @classmethod
    def find_curl_cartesian(cls,
                                  psi: type_expr,
                                  x_sympy: type_symbols,
                                  y_sympy: type_symbols
                                  ) -> List[type_expr]:
        return SympyManager.find_curl_cartesian(
            psi,
            x_sympy,
            y_sympy
        )


class Plot_Velocity_Field_Manager:
    def __init__(self, xlim=(-3., 3.), ylim=(-3., 3.)):
        self.xlim = xlim
        self.ylim = ylim
        self.current_stream_function: typing.Union[int, type_expr] = 0
        self.current_curl: List[typing.Union[int, type_expr]] = [0,
                                                                       0,
                                                                       0]
        self.circles = []
        self.angle: typing.Union[None, float] = None

    @staticmethod
    def find_velocity_field(psi_arg: type_symbols,
                            x_sympy: type_symbols,
                            y_sympy: type_symbols,
                            dict_eval: typing.Optional[typing.Dict[str, typing.Tuple[type_expr, typing.Any]]] = None):
        # Replacing symbol
        psi = psi_arg
        if dict_eval is not None:
            for _, (sympy_symbol, value_symbol) in dict_eval.items():
                psi = psi.subs(sympy_symbol, value_symbol)
        u = sp.lambdify((x_sympy, y_sympy), psi.diff(y_sympy), 'numpy')
        v = sp.lambdify((x_sympy, y_sympy), -psi.diff(x_sympy), 'numpy')
        return u, v


class StreamFuncAnim:

    def __init__(self,
                 X: type_symbols,
                 Y: type_symbols,
                 stream_function,
                 dict_eval,
                 dt=0.05,
                 xlim=(-1, 1),
                 ylim=None,
                 num_points=50,
                 vorticity: typing.Optional[typing.List[type_expr]] = None,
                 streamline_options: typing.Optional[typing.Dict[str, typing.Any]] = None,
                 hide_latex: bool = False,
                 suptitle = ""):
        if streamline_options is None:
            self.streamline_options = dict()
        else:
            self.streamline_options = streamline_options
        self.dt = dt
        self.counter_anim_max = 300
        self.vorticity = vorticity
        self.stream_function = stream_function
        self.suptitle = suptitle
        # Initialize velocity field and displace *functions*
        self.u, self.v = \
            Plot_Velocity_Field_Manager.find_velocity_field(
                stream_function,
                X,
                Y,
            dict_eval=dict_eval)

        self.hide_latex = hide_latex
        self.displace = self.displace_func_from_velocity_funcs(self.u,
                                                               self.v)
        # Save bounds of plot
        self.xlim = xlim
        self.ylim = ylim if ylim is not None else xlim
        # Animation objects must create `fig` and `ax` attributes.
        self.fig, self.ax = plt.subplots()
        self.scatter_plot = self.ax.scatter([], [], color="red")
        self.ax.set_aspect('equal')
        self.xlim_min, self.xlim_max = self.xlim
        self.ylim_min, self.ylim_max = self.ylim
        self.num_points = num_points
        self._init_points()
        self._plot_points()


    def _init_points(self):
        self.points = [[
            self.xlim_min, k] for k in
            np.linspace(self.ylim_min, self.ylim_max, num=self.num_points)
        ]

    def add_circle_patch(self,
                         origin,
                         radius=1.):
        patch = matplotlib.patches.Circle((origin[0], origin[1]), radius, edgecolor="red", facecolor="none")
        self.ax.add_patch(patch)

    def _remove_particles(self):
        pts = np.array(self.points)
        if len(pts) == 0:
            self.points = []
            return
        xlim = [self.xlim_min, self.xlim_max]
        ylim = [self.ylim_min, self.ylim_max]
        outside_xlim = (pts[:, 0] < xlim[0]) | (pts[:, 0] > xlim[1])
        outside_ylim = (pts[:, 1] < ylim[0]) | (pts[:, 1] > ylim[1])
        outside = outside_xlim | outside_ylim
        keep = ~(outside)
        array = pts[keep]
        self.points = list(array)

    def update(self,
               frame):
        points_existing = self.points.copy()
        #if self.hide_latex:
        #    self.ax.set_title(f"Frame {frame}")
        #else:
        #    self.ax.set_title(f"{self.latex_label}; Frame {frame}")
        if self.suptitle != "":
            self.ax.set_title(self.suptitle)
        #print(frame, self.points)
        if frame % 10 == 0:
            print(f"Rendering frame {frame}")
        new_points_list = self.displace(points_existing, self.dt)

        self.points = new_points_list
        self._remove_particles()
        if len(self.points) == 0:
            self._init_points()
        self._plot_points()

    def _plot_points(self):
        X_iter = np.array([k[0] for k in self.points])
        Y_iter = np.array([k[1] for k in self.points])
        self.scatter_plot.set_offsets(np.stack([X_iter, Y_iter]).T)

    def init_background(self):
        """Draw background with streamlines of flow.

        Note: artists drawn here aren't removed or updated between frames.
        """
        x0, x1 = self.xlim
        y0, y1 = self.ylim
        # Create 100 x 100 grid of coordinates.
        Y, X = np.mgrid[x0:x1:100j, y0:y1:100j]
        # Horizontal and vertical velocities corresponding to coordinates.
        U = self.u(X, Y)
        V = self.v(X, Y)
        self.ax.streamplot(X, Y, U, V, color='0.7', **self.streamline_options)



    @cached_property
    def latex_label(self) -> str:
        latex_stream = sp.latex(self.stream_function)
        if self.vorticity is not None:
            #latex_rotx = sp.latex(self.curl[0])
            #latex_roty = sp.latex(self.curl[1])
            #latex_rotz = sp.latex(self.curl[2])
            rot_tot = self.vorticity[0] + self.vorticity[1] + self.vorticity[2]
            rot_tot = rot_tot.expand().simplify()
            label_rot_tot = sp.latex(rot_tot)
            label = \
                f"$\\psi = {latex_stream}$; $\\omega = " + f"{label_rot_tot}$"
            return label
        else:
            label = f"$\\psi = {latex_stream}$"
            return label


    def displace_func_from_velocity_funcs(self,
                                          u_func,
                                          v_func,
                                          method: Literal['euler', 'scipy']
                                          = 'scipy'):
        """Return function that calculates particle positions after time step.

        Parameters
        ----------
        u_func, v_func : functions
            Velocity fields which return velocities at arbitrary coordinates.
        method : {'euler' | 'scipy'}
            Integration method to update particle positions at each time step.
        """

        def velocity(xy, t=0):
            """Return (u, v) velocities for given (x, y) coordinates."""
            # Dummy `t` variable required to work with integrators
            # Must return a list (not a tuple) for scipy's integrate functions.
            return [u_func(*xy), v_func(*xy)]

        def euler(f, pts, dt):
            vel = np.asarray([f(xy) for xy in pts])
            # print(pts, vel, dt)
            return pts + vel * dt

        def ode_scipy(f, pts, dt):
            new_pts = [integrate.odeint(f, xy, [0, dt])[-1] for xy in pts]
            return new_pts

        available_integrators = dict(euler=euler, scipy=ode_scipy)
        odeint = available_integrators[method]

        def displace(xy, dt):
            # print(xy, dt, velocity)
            return odeint(velocity, xy, dt)

        return displace

    def return_animator(self,
                        max_frames,
                        FPS = 100):
        if FPS > 1000:
            raise ValueError("FPS above 1000 has no effect")
        self.init_background()
        animation_real = FuncAnimation(
            fig=self.fig,
            init_func=self.init_background,
            func=self.update,
            frames=max_frames,
            interval=1/float(FPS)
        )
        return animation_real

    def save_animator(self,
                      filename,
                      max_frames,
                      FPS = 100):
        animation_real = self.return_animator(max_frames, FPS)
        animation_real.save(filename)