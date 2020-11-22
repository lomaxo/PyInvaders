import pygame


class Game:
    """
    Responsible for handling the main loop and storing various key variables
    """
    def __init__(self):
        # You have to let the pygame library initialise itself
        pygame.init()

        # Using clock allows us fix a particular frame rate later on
        self.clock = pygame.time.Clock()

        # Set up the window that the game will run in
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_WIDTH))
        pygame.display.set_caption("Space Invaders!")

        # Load the background image, scale it to fill the entire window, and copy it to the screen.
        # (screen is the image that we actually see in the window. blit is a function that draws an image onto
        # another image.
        self.background = pygame.image.load('back.png').convert()
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_WIDTH))
        self.screen.blit(self.background, (0, 0))

        # Create a player object (see Player definition later on)
        self.player = Player()

        # Create a list to contain any aliens we create and add one new Alien object to the list.
        self.alien_list = []
        self.alien_list.append(Alien(100, 100, 5))

        # Create a list for any bullets that we create later, but don't actually a bullet yet.
        self.bullet_list = []

    def update_display(self):
        """
        This function gets called every frame do draw everything to the screen.
        """
        # Start by re-drawing the background. This will wipe out anything that was previously drawn
        self.screen.blit(self.background, (0, 0))

        # Call the function that will draw the player. We pass the screen as a parameter so the player object knows
        # where to draw itself
        self.player.draw(self.screen)

        # Run through the entire list of aliens drawing each of them
        for alien in self.alien_list:
            alien.draw(self.screen)

        # Do the same for any bullets
        for bullet in self.bullet_list:
            bullet.draw(self.screen)
        pygame.display.flip()

    def update_logic(self, event_list):
        """
        This function gets called every frame to allow different objects to move or update themselves.
        event_list is a list of events such as buttons being pressed or the mouse moving.
        """

        # We call the update functions for the player, every alien and every bullet in the game.
        self.player.update(event_list)
        for alien in self.alien_list:
            alien.update(event_list)
        for bullet in self.bullet_list:
            bullet.update(event_list)

        # Check collisions. Check every bullet against every alien to so if they are overlapping.
        for bullet in self.bullet_list:
            for alien in self.alien_list:
                if bullet.get_rectangle().colliderect(alien.get_rectangle()):
                    self.bullet_list.remove(bullet)
                    self.alien_list.remove(alien)

    def main_loop(self):
        """
        This is the main loop. Once the game starts it just keeps repeating until the game ends.
        """
        running = True
        while running:
            # Fix the frame rate to 60 fps. If we get here too quickly the tick function
            # halts the program until it's time to move on.
            self.clock.tick(60)

            # Get a list of any input events (mouse or keyboard) that have happened since we last checked.
            event_list = pygame.event.get()

            self.update_logic(event_list)
            self.update_display()

            # After letting the different objects update themselves deal with any other events.
            for event in event_list:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # If the user pressed the space bar, create a new bullet
                        self.bullet_list.append(Bullet(self.player.x, 500))
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        running = False  # quit the game
                elif event.type == pygame.QUIT:
                    running = False

        # If we exit the main loop, the only thing left to do is shut down pygame.
        pygame.quit()


class Player:
    """
    Hold information about the player, such as where they are on the screen.
    Also draws the image and updates their position based on keyboard input.
    """
    def __init__(self):
        self.x = 100
        self.y = 500
        self.x_vel = 0
        self.y_vel = 0
        self._image = pygame.image.load('UFO.png').convert_alpha()

    def draw(self, screen):
        screen.blit(self._image, (self.x, self.y))

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.x_vel -= 10
                if event.key == pygame.K_RIGHT:
                    self.x_vel += 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.x_vel += 10
                if event.key == pygame.K_RIGHT:
                    self.x_vel -= 10
        self.x += self.x_vel
        self.y += self.y_vel


class Alien:
    """
    Very similar to the Player object. The update function causes it to slowly zig zig down the screen.
    """
    def __init__(self, start_x, start_y, speed):
        self.x = start_x
        self.y = start_y
        self.speed = speed
        self.left_limit = 50
        self.right_limit = 500
        self._image = pygame.image.load('Alien.png').convert_alpha()

    def draw(self, screen):
        screen.blit(self._image, (self.x, self.y))

    def update(self, event_list):
        self.x += self.speed
        if self.x < self.left_limit or self.x > self.right_limit:
            self.speed *= -1
            self.y += 10

    def get_rectangle(self):
        rect = self._image.get_rect()
        rect.x = self.x
        rect.y = self.y
        return rect


class Bullet:
    """
    This is actually quite similar to Player and Alien. Once created it just moves up the screen.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 10
        self._image = pygame.image.load('Bullet.png').convert_alpha()

    def draw(self, screen):
        screen.blit(self._image, (self.x, self.y))

    def update(self, event_list):
        self.y -= self.velocity

    def get_rectangle(self):
        rect = self._image.get_rect()
        rect.x = self.x
        rect.y = self.y
        return rect


# This is where the game starts. We create a game object and then call it's main_loop() function.
game = Game()
game.main_loop()
