'''
Script to transform an old RC-car into WiFi-controlled car
using Raspberry Pi and motor driver.
Code has been tested and used on Windows platform using SSH-connection
with MobaXTerm-terminal.
'''

import RPi.GPIO as GPIO
from time import sleep
import pygame
import sys
import pygame.camera

# Choosing the GPIO pins:
# vars named after ports in ln298n
in1 = 24
in2 = 23
en = 25
temp1 = 1
in3 = 27
in4 = 22
en2 = 6

# Setting up GPIO in/out
# By default every pin is setup as 0v output pin
# Setting up default pwm with frequency

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 1000)

GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
s = GPIO.PWM(en2, 1000)


p.start(40)
s.start(100)
print("up=forwards, down=backwards, right=right, left=left,l=low, m=med, h=high, q=quit")
print("\n")

# "Game window" setup
size = width, height = 640, 480

screen = pygame.display.set_mode(size)
# Setuping the pyCamV2
pygame.camera.init()
cam_list = pygame.camera.list_cameras()
# Choosing pyCam from available cameras + Camera resolution
# Using low resolution to get decent frame rates
# And to keep delay as minimal as possible
cam = pygame.camera.Camera(cam_list[0], (160, 120))
cam.start()

# Game loop
# Stetching the camera resolution to match window resolution
while (1):
    image1 = cam.get_image()
    image1 = pygame.transform.scale(image1, (640, 480))
    screen.blit(image1, (0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cam.stop()
            GPIO.cleanup()
            pygame.quit()
            sys.exit()
            break
        # Setting the pin as high (3.3v) moves the car.
        # Changing the pin outputs other way around makes the motor rotate in the other direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print('Left')
                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
            if event.key == pygame.K_RIGHT:
                print("Right")
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.HIGH)
            if event.key == pygame.K_UP:
                print("Forwards")
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
            if event.key == pygame.K_DOWN:
                print("Backwards")
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
            if event.key == ord('l'):
                print("low speed")
                # Changing the PWM freq we can control the speed of the car
                p.ChangeDutyCycle(40)
            if event.key == ord('m'):
                print("medium speed")
                p.ChangeDutyCycle(65)
            if event.key == ord('h'):
                print("high Speed")
                p.ChangeDutyCycle(100)
        # Using KEYDOWN/KEYUP functions we can control the motors with hold instead of toggle
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                print("Left STOP")
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.LOW)
            if event.key == pygame.K_RIGHT:
                print("Right STOP")
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.LOW)
            if event.key == pygame.K_UP:
                print("BRAKING")
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.LOW)
            if event.key == pygame.K_DOWN:
                print("BRAKING")
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.LOW)
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                GPIO.cleanup()
                break