import math
import os
from random import randint, uniform

import numpy as np
import pygame

import p5

# VARIABLES:

boidNumber = 20

# COHERENCE VIRKER IKKE SÆRLIGT GODT
coherenceValue = 0
seperationValue = 2
alignmentValue = 0.5

pngRes = 10
width, height = 1000, 700
boids = []
background = (120, 120, 120)
Display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
birdGraphic = pygame.image.load(os.path.join("redcircle.png")).convert_alpha()
Running = True

spawnCounter = 0
stopSpawning = False


class boid:
    def __init__(self):
        self.position = np.array([randint(0, width - pngRes), randint(0, height - pngRes)])
        self.accerleration = np.array([0, 0])

        self.velocity = np.array([uniform(-1, 1), uniform(-1, 1)])

        self.maxForce = 0.2
        self.maxSpeed = 2
        self.visualRange = 50

    def movement(self):

        if self.position[0] < 0:
            self.position[0] = width - pngRes

        if self.position[0] > width - pngRes:
            self.position[0] = 0

        if self.position[1] < 0:
            self.position[1] = height - pngRes

        if self.position[1] > height - pngRes:
            self.position[1] = 0

        self.velocity = np.add(self.velocity, self.accerleration)
        self.position = np.add(self.position, self.velocity)
        self.velocity = np.array(p5.limit(self.velocity, self.maxSpeed))
        self.accerleration = np.array([0, 0])

    def align(self):
        steering = np.array([0, 0])
        total = 0
        for boid in boids:
            distance = (
                math.sqrt((self.position[0] - boid.position[0]) ** 2 + (self.position[1] - boid.position[1]) ** 2))
            if distance < boid.visualRange and self != boid:
                steering = np.add(steering, boid.velocity)
                total += 1
        if total > 0:
            steering = np.divide(steering, total)
            #steering = np.linalg.norm(steering, self.maxSpeed)
            steering = np.subtract(steering, self.velocity)

            steering = np.array(p5.limit(steering, self.maxForce))

        return steering

    def cohesion(self):
        steering = np.array([0, 0])
        total = 0
        for boid in boids:
            distance = (
                math.sqrt((self.position[0] - boid.position[0]) ** 2 + (self.position[1] - boid.position[1]) ** 2))
            if distance < boid.visualRange and boid != self:
                steering = np.add(steering, boid.position)
                total += 1
        if total > 0:
            steering = np.divide(steering, total)
            steering = np.subtract(steering, self.position)

            # SET THE MAGNITUDE
            #steering = np.linalg.norm(steering, self.maxSpeed,axis=0)

            steering = np.subtract(steering, self.velocity)
            steering = np.array(p5.limit(steering, self.maxForce))

        return steering

    def seperation(self):
        steering = np.array([0, 0])
        total = 0
        for boid in boids:
            distance = (
                math.sqrt((self.position[0] - boid.position[0]) ** 2 + (self.position[1] - boid.position[1]) ** 2))
            if distance < boid.visualRange and boid != self:
                diff = np.subtract(self.position, boid.position)

                diff = np.divide(diff, distance ** 2)
                steering = np.add(steering, diff)
                total += 1
        if total > 0:
            steering = np.divide(steering, total)

            #steering = np.linalg.norm(steering, self.maxSpeed)

            steering = np.subtract(steering, boid.velocity)

            steering = np.array(p5.limit(steering, self.maxForce))

        return steering

    def display(self):
        Display.blit(birdGraphic, (int(self.position[0]), int(self.position[1])))

    def flock(self):
        alignment = self.align()
        coherence = self.cohesion()
        seperation = self.seperation()

        alignment = np.multiply(alignment, alignmentValue)
        coherence = np.multiply(coherence, coherenceValue)
        seperation = np.multiply(seperation, seperationValue)

        self.accerleration = np.add(self.accerleration, alignment)
        self.accerleration = np.add(self.accerleration, coherence)
        self.accerleration = np.add(self.accerleration, seperation)


while not stopSpawning:
    boids.append(boid())
    spawnCounter += 1
    if spawnCounter >= boidNumber:
        stopSpawning = True

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    pygame.init()
    Display.fill(background)

    for boid in boids:
        boid.flock()
        boid.movement()
        boid.display()

    pygame.display.flip()
