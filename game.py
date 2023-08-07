import pygame

from car import Car

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.generation_font = pygame.font.SysFont("Arial", 30)
        self.alive_font = pygame.font.SysFont("Arial", 20)
        self.game_map = pygame.image.load('assets/map.png').convert()

        self.cars = []
        self.popul_size = 3
        self.gen_count = 0
        self.frame_count = 0
        self.frame_lifespan = 600 # -> 10sec lifespan for 60fps
        
        self.border_color = (255, 255, 255, 255)

        for i in range(self.popul_size):
            self.cars.append(Car(self.screen))

    def gameloop(self):
        self.screen.blit(self.game_map, (0, 0))

        still_alive_count = 0

        for i, car in enumerate(self.cars):
            # evaluate current situation using sensors and decision based on DNA
            decision = False
            if decision:
                car.angle += 1

            car.update(self.game_map)

            if not car.is_alive():
                continue
            still_alive_count += 1

            # set fitness stuff
            print("Car still alive | Reward for that: ", car.get_reward())

            car.draw()

        self.frame_count += 1
        if self.frame_count == self.frame_lifespan or still_alive_count == 0:
            # go through each car and evaluate the whole population like that (we already have fitness stuff)
            # after this the cars array will be different so no additional code after this needed (except for those two lines)

            
            for i in range(self.popul_size):
                self.cars[i] = Car(self.screen)

            self.gen_count += 1
            frame_count = 0

        
        text = self.generation_font.render("Generation: " + str(self.gen_count), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        self.screen.blit(text, text_rect)

        text = self.alive_font.render("Still Alive: " + str(still_alive_count), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        self.screen.blit(text, text_rect)

        pygame.display.flip()

        # while True:
        #     for i, car in enumerate(self.cars):
        #         pass
        #         # car.speed += 1
        #         # car.angle += 1
        #
        #     still_alive = 0
        #     for i, car in enumerate(self.cars):
        #         if car.is_alive():
        #             still_alive += 1
        #             car.update(game_map)
        #             
        #             # TODO: increase fitness
        #
        #     print(still_alive)
        #     if still_alive == 0:
        #         break
        #
        #     self.screen.blit(game_map, (0, 0))
        #     for car in self.cars:
        #         if car.is_alive():
        #             car.draw()
        #
        #     text = generation_font.render("Generation: " + str(self.gen_count), True, (0,0,0))
        #     text_rect = text.get_rect()
        #     text_rect.center = (900, 450)
        #     self.screen.blit(text, text_rect)
        #
        #     text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        #     text_rect = text.get_rect()
        #     text_rect.center = (900, 490)
        #     self.screen.blit(text, text_rect)
        #
        #     pygame.display.flip()
