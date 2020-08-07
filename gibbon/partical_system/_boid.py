import time
import numpy as np
from threading import Thread, Event, Lock


RADIUS = 250
SPEED_MAX = 150
SPEED_MIN = 25

# TODO: VIEW ANGLE
# TODO: VIEW_ANGLE = 110
BOID_COLLISION_DISTANCE = 45
OBSTACLE_COLLISION_DISTANCE = 250
MAX_COLLISION_VELOCITY = 1

WEIGHT_COHESION = .03
WEIGHT_ALIGNMENT = .045
WEIGHT_AVOIDANCE_BOID = 7.5
WEIGHT_AVOIDANCE_OBSTACLE = 300
WEIGHT_ATTRACTOR = .0035
WEIGHT_NOISE = .45

STATUS_COHESION = True
STATUS_ALIGNMENT = True
STATUS_AVOIDANCE_BOID = True
STATUS_AVOIDANCE_OBSTACLE = True
STATUS_ATTRACTOR = True
STATUS_NOISE = True


class BoidSystem:
    def __init__(self):
        self.lock = Lock()
        self.event = Event()
        self.boids = list()

    def compute(self):
        for i in range(len(self.boids)):
            current = self.boids[i]
            neighbors = list()

            for j in range(len(self.boids)):
                if i == j:
                    continue

                boid = self.boids[j]

                if current.distance_to(boid) <= RADIUS:
                    neighbors.append(boid)

            current.move(neighbors)

    def start(self):
        while self.event.is_set():
            with self.lock:
                self.compute()
            time.sleep(.01)


class Boid:
    def __init__(self, x, y, z):
        self._position = np.array([x, y, z])
        self.velocity = np.zeros(3)

    @property
    def position(self):
        return self._position + self.velocity

    def move(self, neighbors, attractors=None, obstacles=None):
        alignment = self.get_alignment(neighbors)
        weight_align = WEIGHT_ALIGNMENT if STATUS_ALIGNMENT else 0
        alignment *= weight_align

        separation = self.get_separation(neighbors)
        weight_separation = WEIGHT_AVOIDANCE_BOID if STATUS_AVOIDANCE_BOID else 0
        separation *= weight_separation

        cohesion = self.get_cohesion(neighbors)
        weight_cohesion = WEIGHT_COHESION if STATUS_COHESION else 0
        cohesion *= weight_cohesion

        noise = np.random.uniform(low=-1, high=1, size=(2))
        weight_noise = WEIGHT_NOISE if STATUS_NOISE else 0
        noise *= weight_noise

    def distance_to(self, boid):
        return np.linalg.norm(self.position - boid.position)

    def get_alignment(self, neighbors):
        quantity = len(neighbors)

        if quantity <= 0:
            return np.zeros(3)

        velocitys = [boid.velocity for boid in neighbors]
        average = np.sum(velocitys) / quantity
        return average - self.velocity

    def get_separation(self, neighbors):
        results = np.zeros(3)

        for obj in neighbors:
            distance = self.distance_to(obj)

            if self.distance_to(obj) < BOID_COLLISION_DISTANCE:
                diff = self.position - obj.position
                diff.normalize()
                diff /= distance
                results += diff

        return results

    def get_cohesion(self, neighbors):
        quantity = len(neighbors)

        if quantity <= 0:
            return np.zeros(3)

        positions = [boid.position for boid in neighbors]
        average = np.sum(positions) / quantity
        return average - self.position

    def close_attractors(self, attractors):
        if attractors is None:
            return np.zeros(3)

        return np.sum(attractors - self.position)

    def avoid_obstacles(self, obstacles):
        results = np.zeros(3)

        for obj in obstacles:
            distance = self.distance_to(obj)

            if self.distance_to(obj) < OBSTACLE_COLLISION_DISTANCE:
                diff = self.position - obj.position
                diff.normalize()
                diff /= distance
                results += diff

        return results



if __name__ == '__main__':
    pass
