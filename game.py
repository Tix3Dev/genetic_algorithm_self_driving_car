import pygame

from car import Car

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.generation_font = pygame.font.SysFont("Arial", 30)
        self.alive_font = pygame.font.SysFont("Arial", 20)
        self.game_map = pygame.image.load('assets/map.png').convert()

        self.cars = []
        self.popul_size = 1
        self.gen_count = 0
        self.frame_count = 0
        self.frame_lifespan = 6000 # -> 100sec lifespan for 60fps
        
        self.border_color = (255, 255, 255, 255)

        for i in range(self.popul_size):
            self.cars.append(Car(self.screen, self.game_map, self.border_color))

    def gameloop(self):
        self.screen.blit(self.game_map, (0, 0))

        still_alive_count = 0

        # debugging purposes
        # time.sleep(1)

        for i, car in enumerate(self.cars):
            print("Action taken for Car No.", i, " using this radar data:", car.get_data())
            # based on current radar situation, let DNA decide what to do next
            decision = car.dna.genes[car.dna.key_repr(car.get_data())]
            car.angle += decision

            car.update()

            if not car.is_alive():
                continue
            still_alive_count += 1

            # set fitness stuff
            print("Car No.", i, " still alive | Reward for that:", car.get_reward())

            car.draw()

        self.frame_count += 1
        if self.frame_count == self.frame_lifespan or still_alive_count == 0:
            # go through each car and evaluate the whole population like that (we already have fitness stuff)
            # after this the cars array will be different so no additional code after this needed (except for those two lines)
            
            # this is just for testing
            for i in range(self.popul_size):
                self.cars[i] = Car(self.screen, self.game_map, self.border_color)

            self.gen_count += 1
            self.frame_count = 0
        
        text = self.generation_font.render("Generation: " + str(self.gen_count), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        self.screen.blit(text, text_rect)

        text = self.alive_font.render("Still Alive: " + str(still_alive_count), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        self.screen.blit(text, text_rect)
