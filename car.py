# Original version from https://github.com/NeuralNine/ai-car-simulation

# The following license applies to all changes made:

# This file is part of simulation for cars learning how to steer using a Genetic Algorithm
# Everything is openly developed on GitHub: https://github.com/Tix3Dev/genetic_algorithm_self_driving_car
#
# Copyright (C) 2023  Yves Vollmeier <https://github.com/Tix3Dev>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pygame
import math
import random

from dna import DNA

CAR_SIZE_X = 60
CAR_SIZE_Y = 60

class Car:
    def __init__(self, screen, game_map, border_color, dna=None):
        self.screen = screen

        self.sprite = pygame.image.load('assets/car.png').convert()
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite 

        self.game_map = game_map
        self.border_color = border_color 

        self.position = [830, 920]
        self.angle = 0
        # self.speed = 4 + random.random()
        self.speed = 10
        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2]

        if dna:
            self.dna = dna
        else:
            self.dna = DNA()
        self.fitness = 0

        self.radars = []
        self.radar_max_len = 300
        # we now need to do this already, oltherwise first training data GA gets is all zero
        # From -45 To 75 With Step-Size 45 Check Radar
        for d in range(-45, 75, 45):
            self.check_radar(d)

        self.alive = True
        self.dist_passed = 0 # TODO: I could add time_passed, mostly makes sense if car should learn to accelerate too

    def draw(self):
        self.screen.blit(self.rotated_sprite, self.position)
        self.draw_radar()

    def draw_radar(self):
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(self.screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(self.screen, (0, 255, 0), position, 5)

    def check_collision(self):
        self.alive = True
        for point in self.corners:
            # If Any Corner Touches Border Color -> Crash
            # Assumes Rectangle
            if self.game_map.get_at((int(point[0]), int(point[1]))) == self.border_color:
                self.alive = False
                break

    def check_radar(self, degree):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # TODO: this is fantastic, there is a max length to the radars, just like in the DNA
        # While We Don't Hit self.border_color AND length < prec * 10 (e.g. 7 * 10) -> go further and further
        while not self.game_map.get_at((x, y)) == self.border_color and length < self.radar_max_len:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])
    
    def update(self):
        # Get Rotated Sprite And Move Into The Right X-Direction
        # Don't Let The Car Go Closer Than 20px To The Edge
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], self.screen.get_size()[0] - 120)

        # Increase Distance and Time
*/
        self.dist_passed += self.speed
        
        # Same For Y-Position
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], self.screen.get_size()[0] - 120)

        # Calculate New Center
        self.center = [int(self.position[0]) + CAR_SIZE_X / 2, int(self.position[1]) + CAR_SIZE_Y / 2]

        # Calculate Four Corners
        # Length Is Half The Side
        length = 0.5 * CAR_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Check Collisions And Clear Radars
        self.check_collision()
        self.radars.clear()

        # From -45 To 75 With Step-Size 45 Check Radar
        for d in range(-45, 75, 45):
            self.check_radar(d)

    def get_data(self):
        # Get Distances To Border
        radars = self.radars
        return_values = [0, 0, 0]
        for i, radar in enumerate(radars):
            # radar will have actual length radar_max_len
            # this will be divided into parts, so that they can be counted
            # from 0 to n (inclusive)
            return_values[i] = int(radar[1] / (self.radar_max_len / self.dna.precision))

        return return_values

    def is_alive(self):
        return self.alive

    def get_reward(self):
        # NOTE: hard to check if goes in wrong direction...
        return self.dist_passed / (CAR_SIZE_X / 2)

    def rotate_center(self, image, angle):
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image
