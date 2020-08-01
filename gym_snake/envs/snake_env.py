import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pygame
import random
import numpy as np

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, render=False):
        self.ENV_HEIGHT = 500 
        self.ENV_WIDTH = 500
        self.VELOCITY = 10 # How much to move per unit  
        self.action_space = spaces.Discrete(4)
        self.SEGMENT_WIDTH = 10
        self.RENDER = render

        # Render using pygame
        if render:
            self.window = pygame.display.set_mode((self.ENV_HEIGHT, self.ENV_WIDTH))

    def step(self, action):
        reward = 0 # initialize per step
        opp_facing = (self.facing + 2) % 4 # Calculate opposite of facing
        # If direction and action is NOT the same and not opposite of current direction facing
        if action != self.facing and action != opp_facing:
            # Update the new snake direction
            self.facing = action   
 
        #* Advancing the snake
        self._move_snake()
        self.done = self._check_collision()
        if self.done:
            reward = -1 # 
        

        #* Consuming apple + growing
        #Simple Reward: Eating apple (1 point)
        if self._check_eaten():
            reward += 10

        #* Additional reward for moving closer towards the red apple
        if self.snake_previous:
            # Distance between 
            if all(abs(np.subtract(self.apple_pos, self.snake_segments[0])) <= abs(np.subtract(self.apple_pos, self.snake_previous))):
                reward += 0.1

        #* Final adjustments
        self.snake_previous = self.snake_segments[0]

        #* Observations
        # State: 4 x collision (True/False), 4 x Snake Facing Direction (True/False), 4 x relative apple position (True/False)
        up_collision, right_collision, down_collision, left_collision = self._next_step_collision()
        face_up, face_right, face_down, face_left = self._facing_direction() 
        apple_above, apple_right, apple_below, apple_left = self._food_relative_direction()

        return (up_collision, right_collision, down_collision, left_collision, face_up, face_right, face_down, face_left, apple_above, apple_right, apple_below, apple_left), reward, self.done, {}

    def reset(self):
        # Snake starting position
        #TODO randomize starting
        self.snake_segments = [(250,250),(250,260),(250,270)]
        self.snake_previous = None # Tuple
        self.facing = 0 # 0 is up, 1 is right, 2 is down, 3 is left #TODO randomize
        # Apple starting position
        self.apple_pos = self._spawn_apple()

        #debug - hardcoding apple_pos
        #self.apple_pos = (250,240)

        # 'Done' state
        self.done = False
  
        return #? need to return state?

    def render(self, mode='human', close=False):
        if not self.render:
            print("[!] Error rendering. Disable during object instantiation.")
            return
        #* Draw & Display
        self.window.fill((0,0,0)) # Clear screen to color black again
        # Snake head
        pygame.draw.rect(self.window, (25,135,75), (self.snake_segments[0][0], self.snake_segments[0][1], self.SEGMENT_WIDTH, self.SEGMENT_WIDTH))

        # Snake body
        for segment in self.snake_segments[1:]:
            pygame.draw.rect(self.window, (25,205,75), (segment[0], segment[1], self.SEGMENT_WIDTH, self.SEGMENT_WIDTH))
        # Apple
        pygame.draw.rect(self.window, (205,25,25), (self.apple_pos[0], self.apple_pos[1], self.SEGMENT_WIDTH, self.SEGMENT_WIDTH))
        pygame.display.update()
            
        return

    def _move_snake(self):
        snake_head = (0,0)
        if self.facing == 0:
            snake_head = np.subtract(self.snake_segments[0], (0, self.SEGMENT_WIDTH))
        elif self.facing == 1:
            snake_head = np.add(self.snake_segments[0], (self.SEGMENT_WIDTH, 0))
        elif self.facing == 2:
            snake_head = np.add(self.snake_segments[0], (0, self.SEGMENT_WIDTH))
        else:
            snake_head = np.subtract(self.snake_segments[0], (self.SEGMENT_WIDTH, 0))

        leftovers = self.snake_segments[:-1]
        self.snake_segments = [] #reset
        self.snake_segments.append(tuple(snake_head))
        for segment in leftovers:
            self.snake_segments.append(segment)

        #debug 
        #print("_move_snake()::self.snake_segments (new snake):", self.snake_segments)

    def _check_collision(self, snake_head=None):
        if np.all(snake_head) == None: 
            snake_head = self.snake_segments[0]

        # Borders
        if snake_head[0] == self.ENV_HEIGHT or snake_head[1] == self.ENV_WIDTH + self.SEGMENT_WIDTH or \
            snake_head[0] == -self.SEGMENT_WIDTH or snake_head[1] == -self.SEGMENT_WIDTH:
            return 1

        # Snake itself
        for segment in self.snake_segments[1:]:
            if self.snake_segments[0] == segment:
                return 1

        return 0

    def _check_eaten(self):
        if self.snake_segments[0] == self.apple_pos:
            pass 
            #print("[+] NOM!") #debug
        else:
            return 0

        #* Growing the snake
        '''
        second_last_segment = self.snake_segments[len(self.snake_segments)-2:-1]   
        last_segment = self.snake_segments[len(self.snake_segments)-1:] #select the last segment

        growth_vector_segment = np.subtract(last_segment, second_last_segment)

        additional_segment = np.add(last_segment, growth_vector_segment)
        '''
        additional_segment = self.snake_segments[len(self.snake_segments)-1:] #select the last segment

        if self.facing == 0: 
            additional_segment = np.add(additional_segment, (0, self.SEGMENT_WIDTH))
        if self.facing == 1:
            additional_segment = np.subtract(additional_segment, (self.SEGMENT_WIDTH, 0))
        if self.facing == 2:
            additional_segment = np.subtract(additional_segment, (0, self.SEGMENT_WIDTH))
        if self.facing == 3:
            additional_segment = np.add(additional_segment, (self.SEGMENT_WIDTH, 0))
        
        self.snake_segments.append(tuple(additional_segment[0]))

        #* Respawn Apple at random location
        self.apple_pos = self._spawn_apple()

        return 1

    def _spawn_apple(self):
        return (random.randrange(0,50) * self.SEGMENT_WIDTH, random.randrange(0,50) * self.SEGMENT_WIDTH)
        
    #* Observations
    # Snake 
    #TODO look-ahead for snake-body new position
    def _next_step_collision(self):
        # snake_segments[0] is the head of the snake

        # UP
        new_snake_head_pos = np.subtract(self.snake_segments[0], (0, self.SEGMENT_WIDTH))
        up_collision = self._check_collision(new_snake_head_pos)

        # RIGHT
        new_snake_head_pos = np.add(self.snake_segments[0], (self.SEGMENT_WIDTH, 0))
        right_collision = self._check_collision(new_snake_head_pos)

        # DOWN
        new_snake_head_pos = np.add(self.snake_segments[0], (0, self.SEGMENT_WIDTH))
        down_collision = self._check_collision(new_snake_head_pos)

        # LEFT
        new_snake_head_pos = np.subtract(self.snake_segments[0], (self.SEGMENT_WIDTH, 0))
        left_collision = self._check_collision(new_snake_head_pos)

        return up_collision, right_collision, down_collision, left_collision
    
    def _facing_direction(self):
        face_up = face_right = face_down = face_left = 0

        if self.facing == 0:
            face_up = 1
        if self.facing == 1:
            face_right = 1
        if self.facing == 2:
            face_down = 1
        if self.facing == 3:
            face_left = 1

        return face_up, face_right, face_down, face_left 

    # From current position, where is the food? Above, right, left or below
    def _food_relative_direction(self):
        apple_above = apple_right = apple_below = apple_left = 0

        # Above
        if self.apple_pos[1] < self.snake_segments[0][1]:
            apple_above = 1

        # Right of 
        if self.apple_pos[0] > self.snake_segments[0][0]:
            apple_right = 1 

        # Below - apple(y) > snake(y)
        if self.apple_pos[1] > self.snake_segments[0][1]:
            apple_below = 1 

        # Left of
        if self.apple_pos[0] < self.snake_segments[0][0]:
            apple_left = 1 

        return apple_above, apple_right, apple_below, apple_left