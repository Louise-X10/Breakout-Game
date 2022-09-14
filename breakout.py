from graphics import BulletinBoard, Poster
from graphics import Rectangle, Circle, TextBox


class BrickWall(Poster):

    def __init__(self, width, height, color_matrix,
                 color_map, outline_bricks):
        super().__init__()
        self.width = width
        self.height = height
        self.brick_height = height//len(color_matrix)
        self.brick_width = width//len(color_matrix[0])
        self.bricks_num = 0
        bricks = []
        row_count = 0
        for row in color_matrix:
            brick_count = 0
            brick_row = []
            for letter in row:
                brick_color = color_map[letter]
                if brick_color != None:
                    brick = Rectangle(self.brick_width, self.brick_height, brick_color,
                                      filled=True, outlined=outline_bricks)
                    self.pin(brick, brick_count*self.brick_width, row_count*self.brick_height)
                    brick_row += [brick]
                    self.bricks_num += 1
                else:
                    brick_row += ["None"]
                brick_count += 1
            bricks += [brick_row]
            row_count += 1
        self.bricks = bricks
    
    def brick_at(self, board, corner):
        x, y = corner
        y = y - 0.1 * board.get_height()
        col_num = int(x//self.brick_width)
        row_num= int(y//self.brick_height)
        element = self.bricks[row_num][col_num]
        if element != None:
            return element
        return None

class BreakoutGame:

    def __init__(self, config):
        self.board = BulletinBoard(config.get_board_width(),
                                   config.get_board_height())
        self.draw_wall(config)
        self.ball_diameter = 1/25*self.board.get_width()
        self.ball = Circle(self.ball_diameter, "black")
        self.draw_ball(self.board.get_width()//2, self.board.get_height()//2)
        self.paddle = Rectangle(self.board.get_width()//8,
                                self.board.get_height()//40,
                                "black", filled=True, outlined=False)
        self.board.pin(self.paddle, 0, self.board.get_height()*0.9)
        self.num_balls = config.get_num_balls()
        self.should_end_game = False
        self.step = config.get_time_step()
        self.min_x = config.get_min_x_velocity()
        self.max_x = config.get_max_x_velocity()
        self.min_y = config.get_initial_y_velocity()
        self.init_x = None
        self.init_y = None
        self.vx = 0
        self.vy = 0
    
    def start(self):
        self.board.listen_for("mousemove", self.respond_to_mouse)
        self.board.listen_for("click", self.start_round)
        self.board.call_every(self.move_ball, self.step)
        
    def respond_to_mouse(self, x, y):
        max_pos = self.board.get_width() - self.board.get_width()//8
        x = min(x, max_pos)
        self.board.unpin(self.paddle)
        self.board.pin(self.paddle, x, self.board.get_height()*0.9)
        
    def start_round(self, x, y):
        from random import uniform
        if self.vx == 0 and self.vy == 0:
            self.init_x = uniform(self.min_x, self.max_x)
            self.init_y = self.min_y
            self.vx = self.init_x
            self.vy = self.init_y
        
    def move_ball(self):
        x, y = self.ball.get_center()
        element, corner = self.collide()
        if self.num_balls > 0:
            #if ball hits bottom wall, end game, life -1
            if y >= self.board.get_height():
                x = self.board.get_width()//2
                y = self.board.get_height()//2
                self.end_round()
            #if all bricks clear, win game
            elif self.wall.bricks_num == 0:
                self.vx = 0
                self.vy = 0
                self.win()
            #if ball hits 3 walls, bounce
            elif y + self.ball_diameter/2 <= 0:
                self.vy = -self.vy
            elif x + self.ball_diameter/2 >= self.board.get_width() or x - self.ball_diameter/2 <= 0:
                self.vx = -self.vx
            #if ball hits paddle, bounce
            elif element == self.paddle:
                self.vy = -self.vy
            #if ball hits brick wall, bounce, remove brick
            elif element == self.wall:
                self.vy = -self.vy
                brick = self.wall.brick_at(self.board, corner)
                self.wall.unpin(brick)
                self.wall.bricks_num += -1        
            x = x + self.vx
            y = y + self.vy
            self.draw_ball(x, y)
        if self.num_balls == 0:
            self.game_over()
            self.board.unpin(self.ball)

    def corners(self):
        x, y = self.ball.get_center()
        radius = self.ball.get_radius()
        corners = [(x-radius,y+radius), (x+radius,y+radius), 
                   (x-radius,y-radius), (x+radius,y-radius)]
        return corners
    
    def collide(self):
        corners = self.corners()
        for x,y in corners:
            element = self.board.element_at(x,y)
            if element != None:
                corner = (x,y)
                return element, corner
        return None, None

    def game_over(self):
        text = TextBox("GAME OVER", font_size=20, font_color="blue")
        self.board.pin(text, self.board.get_width()//2, 20)
        
    def win(self):
        text = TextBox("YOU WIN!", font_size=20, font_color="blue")
        self.board.pin(text, self.board.get_width()//2, 20)
        
    def end_round(self):
        self.vy = 0
        self.vx = 0
        self.num_balls += -1
        #print("number of balls left: ", self.num_balls)        
        #print("number of bricks left: ", self.wall.bricks_num)     

    def draw_wall(self, config):
        self.wall = BrickWall(self.board.get_width(),
                              self.board.get_height()*0.3,
                              config.get_color_matrix(),
                              config.get_color_map(),
                              config.outline_bricks())
        self.board.pin(self.wall, 0, 0.1 * self.board.get_height())
        
    def draw_ball(self, x, y):
        self.board.unpin(self.ball)
        self.board.pin(self.ball, x, y)
        
    
            
    