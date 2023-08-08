import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('_mpl-gallery')

from car import Car

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.generation_font = pygame.font.SysFont("Arial", 30)
        self.alive_font = pygame.font.SysFont("Arial", 20)
        self.game_map = pygame.image.load('assets/map.png').convert()
        
        self.avrg_abs_fit_vals = []
        self.fig, self.ax = plt.subplots()
        plt.ion()
        plt.tight_layout()
        plt.show()

        self.cars = []
        #################################### tweaking mostly in here
        self.popul_size = 50
        self.first_place_reward = 0.4
        self.mutation_prob = 0.005 # this is not percent
        self.crossover_len_divisor = 40
        self.elite_ratio_of_popul = 0.2 # this is not percent
        #################################### tweaking mostly in here
        self.generation_count = 0
        self.frame_count = 0
        self.frame_lifespan = 1200 # -> e.g. 600 10sec lifespan for 60fps

        self.elitism_sort_cars = []
        self.mating_pool = []
        
        self.border_color = (255, 255, 255, 255)

        for i in range(self.popul_size):
            self.cars.append(Car(self.screen, self.game_map, self.border_color))

    def gameloop(self):
        self.screen.blit(self.game_map, (0, 0))

        still_alive_count = 0

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

        self.frame_count += 1
        if self.frame_count == self.frame_lifespan or still_alive_count == 0:
            # normalise fitness
            total_fitness_sum = 0
            max_fitness = 0
            max_fitness_car = self.cars[0]
            for i in range(self.popul_size):
                total_fitness_sum += self.cars[i].fitness
                if self.cars[i].fitness > max_fitness:
                    max_fitness = self.cars[i].fitness
                    max_fitness_car = self.cars[i]

            max_fitness += self.first_place_reward
            max_fitness_car.fitness += self.first_place_reward

            for i in range(self.popul_size):
                self.cars[i].fitness /= max_fitness

            # elitism (TODO: probably not very efficient)
            self.elitism_sort_cars = sorted(self.cars, key=lambda x: x.fitness, reverse=True) # idx=0 -> best
            for car in self.elitism_sort_cars:
                print(car.fitness)

            # stats
            self.avrg_abs_fit_vals.append(total_fitness_sum / self.popul_size)
            # -> print stats
            print("Generation", self.generation_count,
                  " -> Average absolute fitness:", total_fitness_sum / self.popul_size)
            # -> plot stats
            self.ax.step(0.5 + np.arange(len(self.avrg_abs_fit_vals)),
                         self.avrg_abs_fit_vals, linewidth=2.5)
            plt.show(block=False)
            plt.draw()
            plt.pause(0.01)

            # create mating pool
            for i in range(self.popul_size):
                # fit cars have a higher chance of becoming parents / to mate
                significance = int(round(self.cars[i].fitness * 100, 0))
                # print(significance)
                for j in range(significance):
                    self.mating_pool.append(self.cars[i])

            # select new generation
            for i in range(self.popul_size):
                # elitism - keep the best few cars (based on ratio of population)
                if i < self.popul_size * self.elite_ratio_of_popul:
                    self.cars[i] = self.elitism_sort_cars[i]
                    continue

                parent1 = random.choice(self.mating_pool)
                self.mating_pool.remove(parent1)
                parent2 = random.choice(self.mating_pool)
                self.mating_pool.append(parent1)

                child_dna = parent1.dna.crossover_with(parent2.dna, self.crossover_len_divisor)
                child_dna.mutation(self.mutation_prob)

                self.cars[i] = Car(self.screen, self.game_map, self.border_color, child_dna) # TODO: check if this changes car

            # restart gameplay
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
