import pygame
import sys
import os
import random
import subprocess

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)

class StartMenu:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Start Menu")

        self.clock = pygame.time.Clock()

        self.robot_images = [pygame.transform.scale(pygame.image.load(f"img/RB ({i}).png"), (200, 200)) for i in range(1, 30)]
        self.robot_left_image = pygame.transform.scale(pygame.image.load("img/L1.png"), (120, 200))
        self.robot_right_image = pygame.transform.scale(pygame.image.load("img/R1.png"), (120, 200))

        self.light_images = [pygame.transform.scale(pygame.image.load(f"img/P ({i}).jpg"), (200, 200)) for i in range(1, 170)]

        self.pt2_image = pygame.transform.scale(pygame.image.load("img/PT2.png"), (200, 100))
        self.background_images = [pygame.image.load(f"img/F ({i}).jpg") for i in range(1, 89)]

        self.robot_rect = self.robot_images[0].get_rect()
        self.robot_rect.width, self.robot_rect.height = 40, 40
        self.robot_rect.center = (150, SCREEN_HEIGHT // 2)

        self.light_rect = self.light_images[0].get_rect()
        self.light_rect.width, self.light_rect.height = 50, 50
        self.light_rect.topleft = (500, SCREEN_HEIGHT // 2 - 25)

        self.pt2_rect = self.pt2_image.get_rect()
        self.pt2_rect.width, self.pt2_rect.height = 50, 50
        self.pt2_rect.topleft = (500, SCREEN_HEIGHT // 2 - 150)

        self.robot_direction = ""
        self.robot_index = 0
        self.light_index = 0
        self.background_index = 0

        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)
                elif event.type == pygame.KEYUP:
                    self.handle_keyup(event)

            self.move_robot(5 if self.robot_direction == "right" else -5 if self.robot_direction == "left" else 0)

            self.display_background()
            self.display_light()
            self.display_pt2()
            self.display_robot()

            if self.robot_rect.x >= 500:
                subprocess.Popen(["python", "play_video.py"])
                pygame.quit()
                sys.exit()

            pygame.display.flip()
            self.clock.tick(30)

    def handle_keydown(self, event):
        if event.key == pygame.K_LEFT:
            self.robot_direction = "left"
        elif event.key == pygame.K_RIGHT:
            self.robot_direction = "right"

    def handle_keyup(self, event):
        if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            self.robot_direction = ""

    def move_robot(self, dx):
        self.robot_rect.move_ip(dx, 0)
        self.robot_index = (self.robot_index + 1) % 29 

    def display_robot(self):
        if self.robot_direction == "left":
            self.screen.blit(self.robot_left_image, self.robot_rect)
        elif self.robot_direction == "right":
            self.screen.blit(self.robot_right_image, self.robot_rect)
        else:
            self.screen.blit(self.robot_images[self.robot_index // 2], self.robot_rect)

    def display_light(self):
        self.screen.blit(self.light_images[self.light_index], self.light_rect)
        self.light_index = (self.light_index + 1) % len(self.light_images)

    def display_background(self):
        background_image = pygame.transform.scale(self.background_images[self.background_index], (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(background_image, (0, 0))
        self.background_index = (self.background_index + 1) % len(self.background_images)

    def display_pt2(self):
        self.screen.blit(self.pt2_image, self.pt2_rect)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    start_menu = StartMenu()
