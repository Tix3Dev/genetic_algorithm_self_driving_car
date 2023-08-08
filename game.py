import pygame

from car import Car

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.generation_font = pygame.font.SysFont("Arial", 30)
        self.alive_font = pygame.font.SysFont("Arial", 20)
        self.game_map = pygame.image.load('assets/map.png').convert()
        # self.game_map = self.game_map.convert_alpha()

        self.cars = []
        self.popul_size = 3
        self.gen_count = 0
        self.frame_count = 0
        self.frame_lifespan = 1200 # -> e.g. 600 10sec lifespan for 60fps

        self.mating_pool = []
        
        self.border_color = (255, 255, 255, 255)

        for i in range(self.popul_size):
            self.cars.append(Car(self.screen, self.game_map, self.border_color))

    def gameloop(self):
        self.screen.blit(self.game_map, (0, 0))

        still_alive_count = 0

        # DEBUG
        # time.sleep(1)

        for i, car in enumerate(self.cars):
            # DEBUG
            # print("Action taken for Car No.", i, " using this radar data:", car.get_data())

            # based on current radar situation, let DNA decide what to do next
            decision = car.dna.genes[car.dna.key_repr(car.get_data())]
            car.angle += decision

            if not car.is_alive():
                continue
            still_alive_count += 1

            car.update()
            car.draw()

            car.fitness = car.get_reward() # just the distance
            if self.frame_count + 1 == self.frame_lifespan:
                # reaching this means car didn't crash till end, which is very good
                car.fitness *= 2

            # DEBUG
            # print(car.fitness)
            # print("Car No.", i, " still alive | Reward for that:", car.get_reward())


        # print("flaggy one")
        # for car in self.cars:
        #     print(car.fitness)

        self.frame_count += 1
        if self.frame_count == self.frame_lifespan or still_alive_count == 0:
            # TODO: average fitness states etc.

            # normalise fitness
            max_fitness = 0
            for car in self.cars:
                if car.fitness > max_fitness:
                    max_fitness = car.fitness

            for car in self.cars:
                car.fitness /= max_fitness

            # print("flaggy two")
            # for car in self.cars:
            #     print(car.fitness)
            #
            # quit()

            # create mating pool
            for car in self.cars:
                # fit cars have a higher chance of becoming parents / to mate
                significance = int(round(car.fitness * 100, 0))
                for i in range(significance):
                    mating_pool.append(car)

            # select new generation
            for car in self.cars:


            
            # DEBUG
            # for i in range(self.popul_size):
            #     self.cars[i] = Car(self.screen, self.game_map, self.border_color)

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
