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

from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    max_fps = 60

    game = Game(screen)
    
    game_running = True
    while game_running:
        clock.tick(max_fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        game.gameloop()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
