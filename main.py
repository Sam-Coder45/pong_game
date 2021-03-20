from kivy.app import App
from kivy.lang import Builder 
from kivy.uix.widget import Widget 
from kivy.properties import NumericProperty, ReferenceListProperty as ListProperty, ObjectProperty
from kivy.vector import Vector 
from kivy.clock import Clock
from random import randint 

speed = 6

class PongPaddle(Widget):
    score = NumericProperty(0)
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1.05

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ListProperty(velocity_x,  velocity_y)
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    
    def on_touch_move(self, touch):
        if touch.x < self.width/2 - 6:
            self.player1.center_y = touch.y
        if touch.x > self.width * 2/4 + 6:
            self.player2.center_y = touch.y
        
        
        if self.player1.center_y <= 150:
            self.player1.center_y = 150
        if self.player2.center_y <= 150:
            self.player2.center_y = 150
            
        if self.player1.center_y >= self.height - 150:
            self.player1.center_y = self.height - 150
        if self.player2.center_y >= self.height - 150:
            self.player2.center_y = self.height - 150
    
    def serve_ball(self):
        self.ball.velocity = Vector(speed,0).rotate(randint(0,360))
    
    def update(self, dt):
        self.ball.move()
        
        if (self.ball.y < 0) or (self.ball.y > self.height - 100):
            self.ball.velocity_y *= -1
        if (self.ball.x < 0) :
            self.ball.velocity_x *= -1
            self.player2.score += 1
        
        if (self.ball.x > self.width - 100):
            self.ball.velocity_x *= -1
            self.player1.score += 1
       
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

class MainApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1 / 60)
        
        return game
MainApp().run()
