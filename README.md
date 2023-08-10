# genetic_algorithm_self_driving_car
*Very small side project*

This is a simulation of cars, that learn how to steer (and subsequently drive) through a map (that can be customly drawn). The learning is purely based off the idea of Genetic Algorithms.

# Demonstration
![](https://github.com/Tix3Dev/genetic_algorithm_self_driving_car/blob/main/README%20stuff/demo.gif)

*(If you are interested in a more high quality GIF, just run the code for yourself and make a PR :D)*

What you can see above are two (not shown in full length) simulations, each of them on another map. By continuously pressing "e" until the game is over, a data **e**xport of the best car is created, including information about the map, the configurations of the GA, and it's DNA, which may be imported later to start learning at a more advanced level.
![](https://github.com/Tix3Dev/genetic_algorithm_self_driving_car/blob/main/README%20stuff/export.png)

Additionally during the whole simulation, a constantly updating graph will be presented. It shows the Average Absolute Fitness (blue) and the Best Absolute Fitness (red). Note that the spikes in the red plot are due to special rewards when reaching a new peak.
![](https://github.com/Tix3Dev/genetic_algorithm_self_driving_car/blob/main/README%20stuff/plot.png)

A good configuration (aka good learning behavior) of the GA should result in a curve that keeps increasing, although a plateau is likely (unavoidable at some point). A plateau may be temporary (e.g. when facing a difficult obstacle/part of the map) or absolute (when near perfect driving is achieved and since there is a maximum running time, fitness won't increase anymore).

Regarding that point, the need for elitism becomes apparent: Without keeping a small number of the best few cars, it's probabilistically very likely, that there is a drop in fitness. Since in the shown simulations elitism is present, the red curve will never drop.

# Details of the DNA
There are three sensors (=radars) present in the car. Each sensor is split into *n* chunks (I call it `self.precision` in the code). As an example, when a sensor is far away from a wall, the value will be high, e.g. 7, and when the sensor is close to a wall, the value will be low, at least 0. The numbers are integers.

In every given positioning of the car, the three sensors will have a certain value, which all together may be stored in an array like the following: `[3, 4, 0]`.

Now, the DNA is a dictionary, where the keys are such arrays (only that they are first converted to a string, so for the previous example the key would be `"[3,4,0]"`). The assigned values are in the first generation random, however over time crossovers and mutations will change those values, so that in an active learning environment, the values will approach the optimal value (Genetic Algorithms are basically just nature inspired optimization algorithms).

Those values can be between *-x* and *x*, where *x* is the maximum steering angle. All values thus represent an "amount of turning the steering wheel".

Last but not least, every time in the gameloop, the car generates an array representing the values of the sensors. Then, in the DNA dictionary, it looks up the value for the just generated key\* and adds that value to the angle (the values may be negative, to steer in the other direction).

\*: To better understand this, have a look at the code for that
```python
self.precision = 7 # radar will have int outputs from 0 to precision (inclusive)
self.dna_len = (self.precision+1)**3 # how many genes

self.max_steer = 4

for a in range(self.precision+1):
    for b in range(self.precision+1):
        for c in range(self.precision+1):
            self.genes[self.key_repr([a, b, c])] = self.random_steer() # value between -self.max_steer and +self.max_steer
```
This is why all possible sensor values are already present in the dictionary as keys.

# Helpful resources
- https://towardsdatascience.com/introduction-to-genetic-algorithms-including-example-code-e396e98d8bf3
    -> Concept of Genetic Algorithms
- https://youtu.be/bGz7mv2vD6g
    -> Possible implementation of Genetic Algorithms
- https://stackoverflow.com/questions/31196780/genetic-algorithm-new-generations-getting-worse
    -> Concept of elitism
- https://github.com/NeuralNine/ai-car-simulation
    -> Car game code from here, nice to see how their (NEAT) solution compares to mine (Genetic Algorithm)
