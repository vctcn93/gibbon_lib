import numpy as np
import random


class Boid:
    def __init__(self, x, y):
        self.position = np.array([x, y])
        self.direction = np.zeros(3)
        self.think_timer = np.random.randint(10)
        # !self.shade = np.random.random(255)
        self.neighbors = list()

    def move(self):
        self.increment()
        self.wrap()

        if self.think_timer == 0:
            self.get_neighbors()

        self.flock()
        self.position += self.direction

    def flock(self):
        align = self.get_align_vector()
        avoid = self.get_avoid_vector()
        cohese = self.get_cohese_vector()
        noise = np.random.uniform(low=-1, high=1, size=(2))
        avoid_object = self.get_avoid_objects()

        if not self.status_neighbors:
            align *= 0
        align *= self.weight_align

        if not self.status_crowd:
            avoid *= 0
        avoid *= self.weight_avoid

        if not self.status_cohese:
            cohese *= 0
        cohese *= self.weight_cohese

        if not self.status_noise:
            noise *= 0
        noise *= self.weight_noise

        self.direction += align
        self.direction += avoid
        self.direction += cohese
        self.direction += noise
        self.direction += avoid_object

        self.limit(self.max_speed)

    def get_neighbors(self):
        results = list()

        for boid in range(self.boids):

            if boid == self:
                continue

            if abs(boid.position.x - self.position.x) < self.radius and \
                abs(boid.position.y - self.position.y) < self.radius:
                results.append(boid)

        return results

    def get_align_vector(self):
        quantity = len(self.boids)

        if quantity == 0:
            return np.zeros(3)

        vs = [boid.direction for boid in self.neighbors]
        v = np.sum(vs) / quantity
        return v.normalize()
