# Boilerplate display window functionality

from __future__ import annotations
from abc import ABC, abstractmethod

from random import choice
from dataclasses import dataclass
from dataclasses import field
import arcade

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800


@dataclass
class Color:
    """This class defines a color and it's methods
    """

    PALETTE = [
        arcade.color.BLACK,
        arcade.color.LIGHT_GRAY,
        arcade.color.LIGHT_CRIMSON,
        arcade.color.LIGHT_BLUE,
        arcade.color.LIGHT_CORAL,
        arcade.color.LIGHT_CYAN,
        arcade.color.LIGHT_GREEN,
        arcade.color.LIGHT_YELLOW,
        arcade.color.LIGHT_PASTEL_PURPLE,
        arcade.color.LIGHT_SALMON,
        arcade.color.LIGHT_TAUPE,
        arcade.color.LIGHT_SLATE_GRAY,
    ]
    color: tuple = PALETTE[0]
    _color: tuple = field(init=False)

    @property
    def color(self) -> tuple:
        return self._color

    @color.setter
    def color(self, value: tuple) -> None:
        """Sets the color in the class

        Arguments:
            value {tuple} -- the color tuple from COLOR_PALETTE to set
        """
        if value in Color.PALETTE:
            self._color = value


class Shape(ABC):
    """This class defines generic shape object
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        pen: Color = Color(),
        fill: Color = Color(),
        dir_x: int = 1,
        dir_y: int = 1,
        speed_x: int = 1,
        speed_y: int = 1,
    ):
        self._x = x
        self._y = y
        self.width = width
        self.height = height
        self.pen = Color(Color.PALETTE[0])
        self.fill = Color(Color.PALETTE[1])
        self.dir_x = 1 if dir_x > 0 else -1
        self.dir_y = 1 if dir_y > 0 else -1
        self.speed_x = speed_x
        self.speed_y = speed_y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        """Limit the self._x to within the screen dimensions

        Arguments:
            value {int} -- the value to set x to
        """
        if not (0 < value < SCREEN_WIDTH - self.width):
            self.dir_x = -self.dir_x
        self._x += abs(self._x - value) * self.dir_x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        """Limit the self._y to within the screen dimensions

        Arguments:
            value {int} -- the value to set y to
        """
        if not (0 < value < SCREEN_HEIGHT - self.height):
            self.dir_y = -self.dir_y
        self._y += abs(self._y - value) * self.dir_y

    def set_pen_color(self, color: tuple) -> Rectangle:
        """Set the pen color of the rectangle

        Arguments:
            color {tuple} -- the color tuple to set the rectangle pen to

        Returns:
            Rectangle -- returns self for chaining
        """
        self.pen.color = color
        return self

    def set_fill_color(self, color: tuple) -> Rectangle:
        """Set the fill color of the rectangle

        Arguments:
            color {tuple} -- the color tuple to set the rectangle fill to

        Returns:
            Rectangle -- returns self for chaining
        """
        self.fill.color = color
        return self

    @abstractmethod
    def draw(self):
        """This method will be overridden by class that inherit
        Shape
        """
        pass


class Rectangle(Shape):
    """This class defines a simple rectangle object
    """

    def draw(self):
        """Draw the rectangle based on the current state
        """
        arcade.draw_xywh_rectangle_filled(
            self.x, self.y, self.width, self.height, self.fill.color
        )
        arcade.draw_xywh_rectangle_outline(
            self.x, self.y, self.width, self.height, self.pen.color, 3
        )


class Square(Rectangle):
    """This class creates a shape

    Arguments:
        Rectangle {class} -- inherits from Rectangle
    """

    def __init__(
        self,
        x: int,
        y: int,
        size: int,
        pen: Color = Color(Color.PALETTE[0]),
        fill: Color = Color(Color.PALETTE[1]),
        dir_x: int = 1,
        dir_y: int = 1,
        speed_x: int = 1,
        speed_y: int = 1,
    ):
        super().__init__(x, y, size, size, pen, fill, dir_x, dir_y, speed_x, speed_y)


class Circle(Shape):
    """This class creates a circle object

    Arguments:
        Shape {class} -- inherits from the Shape class
    """

    def __init__(
        self,
        x: int,
        y: int,
        size: int,
        pen: Color = Color(Color.PALETTE[0]),
        fill: Color = Color(Color.PALETTE[1]),
        dir_x: int = 1,
        dir_y: int = 1,
        speed_x: int = 1,
        speed_y: int = 1,
    ):
        super().__init__(x, y, size, size, pen, fill, dir_x, dir_y, speed_x, speed_y)

    def draw(self):
        """Draw the circle based on the current state
        """
        radius = self.width / 2
        center_x = self.x + radius
        center_y = self.y + radius
        arcade.draw_circle_filled(center_x, center_y, radius, self.fill.color)
        arcade.draw_circle_outline(
            center_x, center_y, radius, self.pen.color, 3)


class Display(arcade.Window):
    """Main display window
    """

    def __init__(self, screen_title):
        """Initialize the window
        """
        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, screen_title)

        # Create the shapes collection
        self.shapes = []

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)

    def append(self, shape: Shape):
        """Appends an instance of a shape to the list of shapes

        Arguments:
            shape {Shape} -- Shape instance to add to the list
        """
        self.shapes.append(shape)

    def on_update(self, delta_time):
        """Update the position of the shapes in the display
        """
        for shape in self.shapes:
            shape.x += shape.speed_x
            shape.y += shape.speed_y

    def on_draw(self):
        """Called whenever you need to draw your window
        """

        # Clear the screen and start drawing
        arcade.start_render()

        # Draw the rectangles
        for shape in self.shapes:
            shape.draw()

    def change_colors(self, interval):
        """This function is called once a second to
        change the colors of all the rectangles to
        a random selection from COLOR_PALETTE

        Arguments:
            interval {int} -- interval passed in from
            the arcade schedule function
        """
        for shape in self.shapes:
            shape.set_pen_color(choice(Color.PALETTE)).set_fill_color(
                choice(Color.PALETTE)
            )


def main():
    # Create the display instance
    display = Display("Example 01")

    # Append the shapes to the display shapes list
    display.append(Rectangle(20, 20, 100, 200))
    display.append(Square(400, 600, 120, dir_x=-1, dir_y=-1, speed_x=3, speed_y=2))
    display.append(Circle(300, 400, 100, dir_x=1, dir_y=-1, speed_x=6, speed_y=4))

    # Change the shape colors on a schedule, every 1 second
    arcade.schedule(display.change_colors, 1)

    # Run the application
    arcade.run()


if __name__ == "__main__":
    main()
