from graphics import BulletinBoard, Poster
from graphics import Rectangle, Circle, TextBox

def make_button(msg, color, size="40"):
    poster = Poster()
    circle = Circle(100, color, filled=True)
    poster.pin(circle, 0, 0)
    textbox = TextBox(msg, "Helvetica", size)
    poster.pin(textbox, 0, 0)
    return poster

def make_big_button(msg, color):
    poster = Poster()
    rect = Rectangle(250, 100, color, filled=True)
    poster.pin(rect, -125, -50)
    textbox = TextBox(msg, "Helvetica", "40")
    poster.pin(textbox, 0, 0)
    return poster

def make_spring(msg, width, height, color):
    poster = Poster()
    spring = Rectangle(width, height, "green", outlined=True)
    poster.pin(spring, 0, 0)
    textbox = TextBox(msg, "Helvetica", "15")
    poster.pin(textbox, width/2, height/2)
    return poster

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
        self.color_matrix = config.get_color_matrix()
        self.color_map = config.get_color_map()
        self.outline_bricks = config.outline_bricks()
        self.wall = None
        self.draw_wall()
        self.springl = None
        self.springr = None
        #self.draw_spring()
        self.bricks = self.wall.bricks_num
        self.diameter = 1/25*self.board.get_width()
        self.radius = self.diameter / 2
        self.ball = Circle(self.diameter, "black")
        self.paddle = Rectangle(self.board.get_width()//8,
                                self.board.get_height()//40,
                                "black", filled=True, outlined=False)
        self.init_num_balls = config.get_num_balls()
        self.num_balls = self.init_num_balls
        self.step = config.get_time_step()
        self.min_x = config.get_min_x_velocity()
        self.max_x = config.get_max_x_velocity()
        self.min_y = config.get_initial_y_velocity()
        self.vx = None
        self.vy = None
        self.time = 0000
        self.timer = self.create_textbox("Time: " + str(self.time))
        self.counter = self.create_textbox("You have " + str(self.num_balls) + " balls left.")
        self.score = 0
        self.scoreboard = self.create_textbox("Points: " + str(self.score))
        self.collision = []
        self.easybutton = None
        self.hardbutton = None
        self.challengebutton = None
        self.hard_on = False
        self.challenge_on = False
        self.goal = 0
        self.goalboard = None
        self.retry_button = None
        self.should_retry = False
        self.game_start = False
        self.game_in_process = False
        self.first_game = True
        self.comment1 = None
        self.comment2 = None
        self.comment3 = None
        self.comment4 = None
        
        
    def draw_wall(self):
        self.board.unpin(self.wall)
        self.wall = BrickWall(self.board.get_width(),
                              self.board.get_height()*0.3,
                              self.color_matrix,
                              self.color_map,
                              self.outline_bricks)
        self.board.pin(self.wall, 0, 0.1 * self.board.get_height())
        
    def start(self):
        self.num_balls = self.init_num_balls
        self.score = 0
        self.goal = 0
        self.draw_counter()
        self.draw_scoreboard()
        self.draw_goalboard()
        self.draw_easy_button()
        self.draw_hard_button()
        self.draw_challenge_button()
        self.draw_wall()
        self.board.listen_for("click", self.choose_difficulty)   
    
    def choose_difficulty(self, x, y):
        if self.game_start == False and self.game_in_process == False and self.should_retry == False:
            element = self.board.element_at(x,y)
            if element == self.easybutton or element == self.hardbutton or element == self.challengebutton:
                if element == self.easybutton:
                    self.goal = self.bricks*20
                    self.hard_on = False
                    self.challenge_on = False
                elif element == self.hardbutton:
                    self.goal = int(self.bricks * 1.5)*20
                    self.hard_on = True
                    self.challenge_on = False
                elif element == self.challengebutton:
                    self.goal = self.bricks*20
                    self.hard_on = False
                    self.challenge_on = True
                    #self.draw_timer()
                    #self.draw_spring()
                self.board.unpin(self.easybutton)
                self.board.unpin(self.hardbutton)
                self.board.unpin(self.challengebutton)
                self.draw_goalboard()
                self.board.call_later(self.start_game, 50)
            
    def start_game(self):
        if self.challenge_on == True:
            self.draw_timer()
            self.draw_spring()
        else:
            self.board.unpin(self.timer)
            self.board.unpin(self.springl)
            self.board.unpin(self.springr)
        self.draw_ball(self.board.get_width()//2, self.board.get_height()//2)
        self.game_start = True
        self.vx = 0
        self.vy = 0
        self.board.pin(self.paddle, 0, self.board.get_height()*0.9)
        self.board.listen_for("mousemove", self.respond_to_mouse)
        self.board.listen_for("click", self.start_round)
        if self.first_game == True:
            self.board.call_every(self.move_ball, self.step)
            if self.challenge_on == True:
                self.board.call_every(self.time_pass, 1000)
        
    def respond_to_mouse(self, x, y):
        max_pos = self.board.get_width() - self.board.get_width()//8
        x = min(x, max_pos)
        self.board.unpin(self.paddle)
        self.board.pin(self.paddle, x, self.board.get_height()*0.9)
        
    def start_round(self, x, y):
        from random import uniform
        if self.game_start == True and self.game_in_process == False and self.should_retry == False: #.self.vx == 0 and self.vy == 0:
            self.vx = uniform(self.min_x, self.max_x)
            self.vy = self.min_y
            self.game_in_process = True
        
    def move_ball(self):
        if self.game_in_process == True:
            x, y = self.ball.get_center()
            element, corner = self.collide()
            #if all bricks clear, game end
            if self.wall.bricks_num == 0:
                self.vx = None
                self.vy = None
                self.bricks_clear()
                self.board.unpin(self.ball)
            elif self.num_balls > 0:
                #challenge mode: if ball hits spring, bounce and change speed
                if self.challenge_on == True:
                    if element == self.springl:
                        self.vy = -abs(self.vy)-1
                        self.collision = []
                    elif element == self.springr:
                        self.vy = -abs(self.vy)+1
                        self.collision = []
                #if ball hits bottom wall, reset ball pos, end round(life -1)
                if y >= self.board.get_height():
                    x = self.board.get_width()//2
                    y = self.board.get_height()//2
                    self.end_round()
                #if ball hits 3 walls, bounce
                elif y - self.radius <= 0:
                    self.vy = -self.vy
                elif x + self.radius >= self.board.get_width() or x - self.radius <= 0:
                    self.vx = -self.vx
                #if ball hits paddle, bounce
                elif element == self.paddle:
                    self.vy = -abs(self.vy)
                    self.collision = []
                #if ball hits brick wall, bounce, remove brick
                elif element == self.wall:
                    self.vy = -self.vy
                    brick = self.wall.brick_at(self.board, corner)
                    self.wall.unpin(brick)
                    self.wall.bricks_num += -1
                    self.collision += [element]
                    self.update_score()
                x = x + self.vx
                y = y + self.vy
                self.draw_ball(x, y)
            elif self.num_balls == 0:
                self.vx = None
                self.vy = None
                self.game_over()
                self.board.unpin(self.ball)

    def corners(self):
        x, y = self.ball.get_center()
        radius = self.ball.get_radius()
        corners = [(x-radius,y+radius), (x+radius,y+radius), 
                   (x-radius,y-radius), (x+radius,y-radius)]
        sides = [(x, y+radius+1), (x, y-radius-1), 
                 (x+radius+1, y), (x-radius-1, y)]
        return corners + sides
    
    def collide(self):
        corners = self.corners()
        for x,y in corners:
            element = self.board.element_at(x,y)
            if element != None:
                corner = (x,y)
                return element, corner
        return None, None
    
    def end_round(self):
        self.vy = 0
        self.vx = 0
        self.num_balls += -1
        self.draw_counter() 
        self.game_in_process = False
        
    def bricks_clear(self):
        self.comment1 = self.create_textbox("BRICKS CLEAR!")
        self.board.pin(self.comment1, self.board.get_width()//2, 200)
        if self.hard_on == True:
            bonus = 150
        else:
            bonus = 100
        self.print_score(bonus)
        self.print_comment()
        self.draw_retry()
    
    def print_score(self, bonus):
        if self.score >= self.goal:
            final_score = int((self.score + self.num_balls*100)*bonus*0.01)
            final_text = "Final score = (" + str(self.score) + " + " + str(self.num_balls) + "*100 ) * " + str(bonus) + "% = "+ str(final_score)
            self.comment2 = self.create_textbox(final_text)
        else:
            score_needed = self.goal - self.score
            final_score = int(self.score + self.num_balls*100 - (score_needed)*10)
            final_text = "Final score = (" + str(self.score) + " + " + str(self.num_balls) + "*100 - " + str(score_needed) + "*10 ) * " + str(bonus) + "%= "+ str(final_score)
            self.comment2 = self.create_textbox(final_text)
        self.board.pin(self.comment2, self.board.get_width()//2, 260)
    
    def print_comment(self):  
        if self.hard_on == False and self.score > self.goal:
            self.comment3 = self.create_textbox("YOU WIN! You exceeded the goal! Try the hard mode!")
        elif self.hard_on == True and self.score < self.goal: 
            self.comment3 = self.create_textbox("OH NO! The goal is not met!")
        else:
            self.comment3 = self.create_textbox("YOU WIN! Congradulations!")
        self.board.pin(self.comment3, self.board.get_width()//2, 300)
        if self.challenge_on == True:
            self.comment4 = self.create_textbox("You spent " + str(self.time) + " seconds! ")
            self.board.pin(self.comment4, self.board.get_width()//2, 330)
        
    def game_over(self):
        self.comment1 = self.create_textbox("GAME OVER")
        self.board.pin(self.comment1, self.board.get_width()//2, 50)
        self.comment2 = self.create_textbox("Final score = " + str(self.score))
        self.board.pin(self.comment2, self.board.get_width()//2, 260)
        self.comment3 = self.create_textbox("YOU LOSE! Play another game!")
        self.board.pin(self.comment3, self.board.get_width()//2, 300)
        self.draw_retry()
        
    def create_textbox(self, msg):
        return TextBox(msg, font_size=20, font_color="blue")

    def draw_retry(self):
        self.retry_button = make_big_button("Play again!", "yellow")
        self.board.pin(self.retry_button, self.board.get_width()//2, 400)
        self.game_start = False
        self.game_in_process = False
        self.time = 0000
        self.should_retry = True
        self.board.listen_for("click", self.retry)
        
    def retry(self, x, y):
        if self.should_retry == True:
            elt = self.board.element_at(x,y)
            if elt == self.retry_button:
                self.board.unpin(self.retry_button)
                self.board.unpin(self.wall)
                self.board.unpin(self.comment1)
                self.board.unpin(self.comment2)
                self.board.unpin(self.comment3)
                self.board.unpin(self.comment4)
                self.should_retry = False
                self.first_game = False
                self.board.call_later(self.start, 10)
                
    def draw_counter(self):
        self.board.unpin(self.counter)
        self.counter = self.create_textbox("You have " + str(self.num_balls) + " balls left.")
        self.board.pin(self.counter, 100, 20)
    
    def draw_scoreboard(self):
        self.board.unpin(self.scoreboard)
        self.scoreboard = self.create_textbox("Points: " + str(self.score))
        self.board.pin(self.scoreboard, 245, 20)
        
    def draw_goalboard(self):
        self.board.unpin(self.goalboard)
        self.goalboard = self.create_textbox("Goal: " + str(self.goal))
        self.board.pin(self.goalboard, 340, 20)
        
    def draw_timer(self):
        self.board.unpin(self.timer)
        self.timer = self.create_textbox("Time: " + str(self.time))
        self.board.pin(self.timer, 440, 20)
        
    def time_pass(self):
        if self.game_in_process == True and self.challenge_on == True: 
            self.time += 1
            self.draw_timer()
        
    def update_score(self):
        combo = len(self.collision)
        if combo == 1:
            self.score += 20
        elif combo >= 2:
            self.score += 20 + 10 * (combo-1)
        self.draw_scoreboard()        
        
    def draw_spring(self):
        width = self.board.get_width()//8+10
        height = self.board.get_height()//20
        self.board.unpin(self.springl)
        self.springl = make_spring("speed up", width, height, "green")
        self.board.pin(self.springl, 0, self.board.get_height()-height)
        
        self.board.unpin(self.springr)
        self.springr = make_spring("slow down", width, height, "green")
        self.board.pin(self.springr, self.board.get_width()-width, self.board.get_height()-height)
        
    def draw_ball(self, x, y):
        self.board.unpin(self.ball)
        self.board.pin(self.ball, x, y)

    def draw_easy_button(self):
        self.board.unpin(self.easybutton)
        self.easybutton = make_button("Easy", "#E56DB1")
        self.board.pin(self.easybutton, 100, 300)
            
    def draw_hard_button(self):
        self.board.unpin(self.hardbutton)
        self.hardbutton = make_button("Hard", "orange")
        self.board.pin(self.hardbutton, 250, 300)
    
    def draw_challenge_button(self):
        self.board.unpin(self.challengebutton)
        self.challengebutton = make_button("Challenge", "red", size="15")
        self.board.pin(self.challengebutton, 380, 300)

        