import numpy as np
import pygame
from random import randint, random, uniform
import os
import math
import time
import p5


# VARIABLES:


boidNumber = 50

coherenceValue = 1
seperationValue = 0
alignmentValue = 1


pngRes = 10
width, height = 1000,700
boids = []
background = (120,120,120)
Display = pygame.display.set_mode((width, height),pygame.RESIZABLE)
birdGraphic = pygame.image.load(os.path.join("redcircle.png")).convert_alpha()
Running = True

spawnCounter = 0
stopSpawning = False

class boid:
    def __init__(self):
        self.position = np.array([randint(0,width-pngRes),randint(0,height-pngRes)])
        self.accerleration = np.array([0,0])

        self.velocity = np.array([uniform(-1,1),uniform(-1,1)])


        self.maxForce = 1
        self.maxSpeed = 2
        self.visualRange = 100


    def movement(self):
        #self.velocity[0] += self.accerleration[0]
        #self.velocity[1] += self.accerleration[1]

        #if self.velocity[0] > self.maxSpeed:
         #   self.velocity[0] = self.maxSpeed
        #if self.velocity[1] > self.maxSpeed:
          #  self.velocity[1] = self.maxSpeed

        if self.position[0] < 0:
            self.velocity[0] = -self.velocity[0]

        if self.position[0] > width - pngRes:
            self.velocity[0] = -self.velocity[0]

        if self.position[1] < 0:
            self.velocity[1] = -self.velocity[1]

        if self.position[1] > height - pngRes:
            self.velocity[1] = -self.velocity[1]



        self.position = np.add(self.position, self.velocity)
        self.velocity = np.add(self.velocity, self.accerleration)

        self.velocity = np.array(p5.clamp_norm(self.velocity, self.maxSpeed))

        self.accerleration = np.array([0,0])


    def align(self):
        steering = np.array([0,0])
        total = 0
        for boid in boids:
            distance = (math.sqrt((self.position[0]-boid.position[0])**2 +(self.position[1]-boid.position[1])**2))
            if distance < boid.visualRange and self != boid:
                steering = np.add(steering,boid.velocity)
                total += 1
        if total > 0:
            steering = np.divide(steering,total)

            Mag = math.sqrt(steering[0] * steering[0] + steering[1] * steering[1])
            steering[0] = (steering[0] * self.maxSpeed / Mag)
            steering[1] = (steering[1] * self.maxSpeed / Mag)

            steering = np.subtract(steering,self.velocity)


            steering = np.array(p5.clamp_norm(steering, self.maxForce))



        return steering

    def cohesion(self):
        steering = np.array([0, 0])
        total = 0
        for boid in boids:
            distance = (math.sqrt((self.position[0]-boid.position[0])**2 +(self.position[1]-boid.position[1])**2))
            if distance < boid.visualRange and boid != self:
                steering = np.add(steering, boid.position)
                total += 1
        if total > 0:

            steering = np.divide(steering, total)
            steering = np.subtract(steering, boid.position)


            Mag = math.sqrt((steering[0] * steering[0] + steering[1] * steering[1]))
            steering[0] = (steering[0] * self.maxSpeed / Mag)
            steering[1] = (steering[1] * self.maxSpeed / Mag)

            steering = np.subtract(steering, boid.velocity)
            steering = np.array(p5.clamp_norm(steering, self.maxForce))

        return steering


    def seperation(self):
        steering = np.array([0, 0])
        total = 0
        for boid in boids:
            distance = (math.sqrt((self.position[0]-boid.position[0])**2 +(self.position[1]-boid.position[1])**2))
            if distance < boid.visualRange and boid != self:
                diff = np.subtract(self.position,boid.position)

                diff = np.divide(diff,distance**2)
                steering = np.add(steering, diff)
                total += 1
        if total > 0:

            steering = np.divide(steering, total)

            Mag = math.sqrt(steering[0] * steering[0] + steering[1] * steering[1])
            steering[0] = (steering[0] * self.maxSpeed / Mag)
            steering[1] = (steering[1] * self.maxSpeed / Mag)

            steering = np.subtract(steering, boid.velocity)

            steering = np.array(p5.clamp_norm(steering, self.maxForce))

        return steering
    def display(self):
        Display.blit(birdGraphic, (self.position[0], self.position[1]))

    def flock(self):

        alignment = self.align()
        coherence = self.cohesion()
        seperation = self.seperation()


        alignment = np.multiply(alignment,alignmentValue )
        coherence = np.multiply(coherence, coherenceValue)
        seperation = np.multiply(seperation, seperationValue)

        self.accerleration = np.add(self.accerleration,alignment)
        self.accerleration = np.add(self.accerleration,coherence)
        self.accerleration = np.add(self.accerleration,seperation)



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
        boid.display()
    for boid in boids:
        boid.flock()
    for boid in boids:
        boid.movement()

    pygame.display.flip()


