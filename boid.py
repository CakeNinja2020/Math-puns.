import numpy as np
import pygame
from random import randint, random, uniform
import os
import math
import time

# VARIABLES:
boidNumber = 20

coherenceValue = 100
seperationValue = 0
alignmentValue = 2




pngRes = 25
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
        self.velocity = np.multiply(np.array([uniform(-1,1),uniform(-1,1)]),1)

        self.maxForce = 1
        self.maxSpeed = 4
        self.visualRange = 300


    def movement(self):
        #self.velocity[0] += self.accerleration[0]
        #self.velocity[1] += self.accerleration[1]

        #if self.velocity[0] > self.maxSpeed:
         #   self.velocity[0] = self.maxSpeed
        #if self.velocity[1] > self.maxSpeed:
          #  self.velocity[1] = self.maxSpeed

        if self.position[0] < 0:
            self.position[0] = width - pngRes
        if self.position[0] > width - pngRes:
            self.position[0] = 0

        if self.position[1] < 0:
            self.position[1] = height - pngRes

        if self.position[1] > height - pngRes:
            self.position[1] = 0

        self.position = np.add(self.position, self.velocity)
        self.velocity = np.add(self.velocity, self.accerleration)
        if self.velocity[0] > self.maxSpeed:
            self.velocity[0] = self.maxSpeed
        if self.velocity[1] > self.maxSpeed:
            self.velocity[1] = self.maxSpeed

        if self.velocity[0] < -self.maxSpeed:
            self.velocity[0] = -self.maxSpeed
        if self.velocity[1] < -self.maxSpeed:
            self.velocity[1] = -self.maxSpeed

        self.accerleration = np.multiply(self.accerleration,0)


    def align(self):
        steering = np.array([0,0])
        total = 0
        for boid in boids:
            for boid2 in boids:

                distance = math.hypot((boid.position[0]+boid.position[1]),(boid2.position[0]+boid2.position[1]))
                if distance < boid.visualRange and boid != boid2:
                    steering = np.add(steering,boid.velocity)
                    total += 1
        if total > 0:
            steering = np.divide(steering,total)
            steering = np.multiply(steering,boid.maxSpeed)
            steering = np.subtract(steering,boid.velocity)

            if steering[0] > boid.maxForce:
                steering[0] = boid.maxForce
            if steering[1] > boid.maxForce:
                steering[1] = boid.maxForce
            if steering[0] < -boid.maxForce:
                steering[0] = -boid.maxForce
            if steering[1] < -boid.maxForce:
                steering[1] = -boid.maxForce

        return steering

    def cohesion(self):
        steering = np.array([0, 0])
        total = 0
        for boid in boids:
            for boid2 in boids:

                distance = math.hypot((boid.position[0] + boid.position[1]), (boid2.position[0] + boid2.position[1]))
                if distance < boid.visualRange and boid != boid2:
                    steering = np.add(steering, boid.position)
                    total += 1
        if total > 0:

            steering = np.divide(steering, total)
            steering = np.subtract(steering, boid.position)
            steering = np.multiply(steering, boid.maxSpeed)
            steering = np.subtract(steering, boid.velocity)

            if steering[0] > boid.maxForce:
                steering[0] = boid.maxForce
            if steering[1] > boid.maxForce:
                steering[1] = boid.maxForce
            if steering[0] < -boid.maxForce:
                steering[0] = -boid.maxForce
            if steering[1] < -boid.maxForce:
                steering[1] = -boid.maxForce

        return steering


    def seperation(self):
        steering = np.array([0, 0])
        total = 0
        for boid in boids:
            for boid2 in boids:

                distance = math.hypot((boid.position[0] + boid.position[1]), (boid2.position[0] + boid2.position[1]))
                if distance < boid.visualRange and boid != boid2:
                    diff = np.subtract(boid.position,boid2.position)
                    diff = np.divide(diff,distance * distance)
                    steering = np.add(steering, diff)
                    total += 1
        if total > 0:

            steering = np.divide(steering, total)
            steering = np.subtract(steering, boid.position)
            steering = np.multiply(steering, boid.maxSpeed)
            steering = np.subtract(steering, boid.velocity)

            if steering[0] > boid.maxForce:
                steering[0] = boid.maxForce
            if steering[1] > boid.maxForce:
                steering[1] = boid.maxForce
            if steering[0] < -boid.maxForce:
                steering[0] = -boid.maxForce
            if steering[1] < -boid.maxForce:
                steering[1] = -boid.maxForce

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

        print(self.accerleration)


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


