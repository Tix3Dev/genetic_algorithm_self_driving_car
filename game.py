import pygame
import random

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
        self.generation_count = 0
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

        for i in range(self.popul_size):
            # based on current radar situation, let DNA decide what to do next
            decision = self.cars[i].dna.genes[self.cars[i].dna.key_repr(self.cars[i].get_data())]
            self.cars[i].angle += decision

            if not self.cars[i].is_alive():
                continue
            still_alive_count += 1

            self.cars[i].update()
            self.cars[i].draw()

            self.cars[i].fitness = self.cars[i].get_reward() # just the distance
            if self.frame_count + 1 == self.frame_lifespan:
                # reaching this means car didn't crash till end, which is very good
                self.cars[i].fitness *= 2

        self.frame_count += 1
        if self.frame_count == self.frame_lifespan or still_alive_count == 0:
            # TODO: average fitness states etc.

            # normalise fitness
            max_fitness = 0
            for car in self.cars:
                if car.fitness > max_fitness:
                    max_fitness = car.fitness

            for i in range(self.popul_size):
                self.cars[i].fitness /= max_fitness

            # create mating pool
            for i in range(self.popul_size):
                # fit cars have a higher chance of becoming parents / to mate
                significance = int(round(self.cars[i].fitness * 100, 0))
                for j in range(significance):
                    self.mating_pool.append(self.cars[i])

            # select new generation
            for i in range(self.popul_size):
                parent1 = random.choice(self.mating_pool)
                self.mating_pool.remove(parent1)
                parent2 = random.choice(self.mating_pool)
                self.mating_pool.append(parent1)

                # child_dna = parent1.dna
                # child_dna.crossover_with(parent2.dna)
                # child_dna.mutation(0.1)
                
                temp = parent1.dna

                child_dna = parent1.dna.crossover_with(parent2.dna)
                print(child_dna)
                # child_dna.mutation(0.1)

                if temp == child_dna:
                    print("wut1")
                elif parent2.dna == child_dna:
                    print("wut2")
                else:
                    print("ayyyy")

                self.cars[i] = Car(self.screen, self.game_map, self.border_color, child_dna) # TODO: check if this changes car

            self.generation_count += 1
            self.frame_count = 0
        
        text = self.generation_font.render("Generation: " + str(self.generation_count), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        self.screen.blit(text, text_rect)

        text = self.alive_font.render("Still Alive: " + str(still_alive_count), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        self.screen.blit(text, text_rect)
