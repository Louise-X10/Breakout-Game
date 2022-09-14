class GameConfiguration:

    def get_board_width(self):
        """ The width (in pixels) of the game board."""
        return 495

    def get_board_height(self):
        """ The height (in pixels) of the game board."""
        return 600

    def get_initial_y_velocity(self):
        """ The initial vertical velocity."""
        return 3.0

    def get_max_x_velocity(self):
        """ The maximum initial horizontal velocity."""
        return 3.0

    def get_min_x_velocity(self):
        """ The maximum initial horizontal velocity."""
        return 1.0

    def get_num_balls(self):
        """ The initial number of lives provided to a player."""
        return 3

    def get_time_step(self):
        """ Time (in milliseconds) between timer event calls. """
        return 10

    def outline_bricks(self):
        """ Whether to outline bricks using a black line. """
        return True

    def get_color_map(self):
        """ Dictionary mapping letters of the alphabet to hexadecimal color codes. """
        return {"R": "#FF0000", "G": "#00FF00", "B": "#0000FF", "X": None}

    def get_color_matrix(self):
        """
        The initial configuration of the brick wall. It is a list
        of strings, each of which represents a row of bricks.

        A row of k bricks is represented as a string of k letters.
        Each of the letters should be a key in self.get_color_map(),
        which provides its color. If self.get_color_map(letter) == None,
        then there should be no brick in that space.

        """
        return ["BRX",
                "GBR"]

