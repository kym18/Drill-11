from pico2d import *
from ball import Ball, BigBall
import game_world
import game_framework
import random

# 이것은 각 상태들을 객체로 구현한 것임.
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0 #시속
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

class Run:

    @staticmethod
    def enter(bird):
        bird.dir, bird.action, bird.face_dir = 1, 2, 1

    @staticmethod
    def exit(bird):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        if (bird.x > 1600 - 50 or bird.x < 50):
            bird.dir *= -1

        bird.action = (bird.action + 1) % 3

    @staticmethod
    def draw(bird):
        if bird.dir == 1:
            bird.image.clip_draw(int(bird.frame) % 5 * 181, bird.action * 170 , 180, 170, bird.x, bird.y,
                                 50, 50)
        else:
            bird.image.clip_composite_draw(int(bird.frame) % 5 * 181, bird.action * 170 , 180, 170, 0,
                                           'h', bird.x, bird.y,50, 50)
class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = Run
    def start(self):
        self.cur_state.enter(self.bird)

    def update(self):
        self.cur_state.do(self.bird)

    def handle_event(self, e):
        # for check_event, next_state in self.transitions[self.cur_state].items():
        #     if check_event(e):
        #         self.cur_state.exit(self.boy, e)
        #         self.cur_state = next_state
        #         self.cur_state.enter(self.boy, e)
        #         return True
        #
        # return False
        pass
    def draw(self):
        self.cur_state.draw(self.bird)





class Bird:
    def __init__(self):
        self.x, self.y = random.randint(100,1500), random.randint(300,600)
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()


    # def fire_ball(self):
    #
    #     if self.item ==   'Ball':
    #         ball = Ball(self.x, self.y, self.face_dir*10)
    #         game_world.add_object(ball)
    #     elif self.item == 'BigBall':
    #         ball = BigBall(self.x, self.y, self.face_dir*10)
    #         game_world.add_object(ball)
    #     # if self.face_dir == -1:
    #     #     print('FIRE BALL LEFT')
    #     #
    #     # elif self.face_dir == 1:
    #     #     print('FIRE BALL RIGHT')
    #
    #     pass

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event()

    def draw(self):
        self.state_machine.draw()
