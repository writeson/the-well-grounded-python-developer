# Using a class to encapsulate a rectangle and how to draw and animate it
# and limit the rectangle to within the screen space
# It also makes use of Inheritance

from __future__ import annotations
from abc import ABC, abstractmethod

from random import choice
import arcade

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

COLOR_PALETTE = [
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


class Shape(ABC):
    """This class defines generic shape object
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        pen_color: tuple = COLOR_PALETTE[0],
        fill_color: tuple = COLOR_PALETTE[1],
        dir_x: int = 1,
        dir_y: int = 1,
        speed_x: int = 1,
        speed_y: int = 1,
    ):
        self._x = x
        self._y = y
        self.width = width
        self.height = height
        self.pen_color = pen_color
        self.fill_color = fill_color
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
        self.pen_color = color
        return self

    def set_fill_color(self, color: tuple) -> Rectangle:
        """Set the fill color of the rectangle

        Arguments:
            color {tuple} -- the color tuple to set the rectangle fill to

        Returns:
            Rectangle -- returns self for chaining
        """
        self.fill_color = color
        return self

    @abstractmethod
    def draw(self):
        """This method will be overridden by class that inherit
        from Shape
        """
        pass


class Rectangle(Shape):
    """This class defines a simple rectangle object
    """

    def draw(self):
        """Draw the rectangle based on the current state
        """
        arcade.draw_xywh_rectangle_filled(
            self.x, self.y, self.width, self.height, self.fill_color
        )
        arcade.draw_xywh_rectangle_outline(
            self.x, self.y, self.width, self.height, self.pen_color, 3
        )


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

    def append(self, shape):
        """Appends an instance of a shape to the list of shapes

        Arguments:
            shape {shape} -- shape instance to add to the list
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

        # Draw the shapes
        for shape in self.shapes:
            shape.draw()

    def change_colors(self, interval):
        """This function is called once a second to
        change the colors of all the shapes to
        a random selection from COLOR_PALETTE

        Arguments:
            interval {int} -- interval passed in from
            the arcade schedule function
        """
        for shape in self.shapes:
            shape.set_pen_color(choice(COLOR_PALETTE)).set_fill_color(
                choice(COLOR_PALETTE)
            )


# Main code entry point
def main():
    # Create the display instance
    display = Display("Example 01")

    # Append the rectangles to the display rectangles list
    display.append(Rectangle(20, 20, 100, 200))

    # Change the rectangle colors on a schedule
    arcade.schedule(display.change_colors, 1)

    # Run the application
    arcade.run()


if __name__ == "__main__":
    main()
