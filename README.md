# Space Invaders

## Contents
  
* [Pygame](#pygame)
* [Getting started](#getting-started)
* [The Game Class](#the-game-class)
* [The Player class](#the-player-class)
* [The Alien class](#the-alien-class)
* [The Bullet class](#the-bullet-class)
* [Creating the Game object](#creating-the-game-object)
* [What next?](#what-next-)

## Pygame

We're going to use the [**pygame**](https://www.pygame.org/wiki/about) library to deal with drawing images and getting input from the keyboard. So the first thing to do is import pygame. Pygame works in Trinket but the display is a bit slow. If you are using Python on your laptop, rather than in a browser, you might need to download the pygame library, but try it first as it is often already installed.

Once it is installed, any python prgram that wants to use it needs to start by _importing_ the library.
```
import pygame
```

We're going to use Pygame for a few, specific things:

- Create the window that the game runs in using `pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_WIDTH))`
- Load images from files using `pygame.image.load('image.png')`
- Draw images to the screen using `screen.blit()`
- Get a list of _events_ such as keys being pressed using `pygame.event.get()`

## Getting started

If you jump to the end of the code, after all the class definitions, you'll see just two lines:
```python
game = Game()
game.main_loop()
```
These create a `game` object (we'll only ever create one), and then calls the `main_loop()` function. The whole game will happen inside that `main_loop()` function.

The `main_loop()` function is defined later on in the `Game` class but it's useful to know what it it does. It simply keeps looping for the whole game, ideally repeating 60 times per second. Every repetition is called a _frame_. The following things happen every frame:

- Check to see what buttons have been pressed
- Update the position of every object in the game
- Re-draw every object to the screen

Before actually running the main loop we define some classes. These are templates for any objects we create:

| Class | Description |
| -------|-------------|
| Game | There is only going to be one of these objects created. It will coordinate all the other objects and contain the _game loop_|
|Player | This holds and information about the player such as their possition on the screen. It also has a method (function) that will be called when the player image needs to be drawn to the screen, and one that deals with moving the player when the user presses the arrow keys.|
|Alien | Very similar to Player, this deals with drawing and moving the aliens |
|Bullet | When the player shoots, a Bullet object is created that moves up the screen and hopefully collides with the aliens. |

## The Game Class 
Let's look at the `Game` class definition. 

The first function is `__init__(self):` that gets called automatically when the `game` object is created. The `__init__` function:

- Sets up pygame
- Creates the window that the game will run in
- Creates any objects that will initially be in the game. In this case a player and an alien

```python
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
```

The `update_display()` function gets called every frame by the main loop. It re-draws the screen
```python
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
```

The `update_logic()` function also gets called every frame. It deals with anything else that needs to happen each frame such as moving objects or dealing with user input.

```python
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
```

And this is the main loop itself, where every essentially happens.
```python
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
```

## The Player class
The Player class is relatively small. It only contains 3 methods/funtions:

- `__init__()`: this initialises some variables such as the x and y coordinates and loads the image from a file
- `draw(screen)`: this simply uses the pygame `blit` function to draw the player's image to the screen
- `update(event_list)`: this allows the player to check if the left or right buttons where pressed and change it's velocity appropriately. It then updates the player's position coordinates.

Notice that the buttons actually change a variable called `x_vel` i.e. the x velocity. It is this velocity that gets added to the position each frame. This means the player starts moving when the button is pressed (`pygame.KEYDOWN`) and will keep moving at the same speed until the button is released (`pygame.KEYUP`).

```python
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
```

## The Alien class
Next comes the Alien class. This is very similar to the Player class; so similar in fact that there is some code repetition; look at the `draw()` function. Ideally we could avoid repetition by making both Player and Alien _inherit_ from the same parent class called something like _GameObject_.

There is an additional function here called `get_rectangle()`. This returns a special pygame rectange (`rect`) object that contains the width and height of the image, and the x and y coordinates. We use this rectangle when doing collision detection in the `Game.update_logic()`

In this version of the game, we actually only create one instance of the Alien class, but in the finished game, there would be many of them.

```python
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
```

## The Bullet class
Lastly is the Bullet class. Again, if we where using inheritance, this could inherit from a parent class shareed by Player and Alien.
```python
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
```

## Creating the Game object
That's it, all the classes that we need in the game have been defined. All that's left to do is create an _instance_ of the `Game` class and call its `main_loop()` function. 
```python
# This is where the game starts. We create a game object and then call it's main_loop() function.
game = Game()
game.main_loop()
```

## What next?
If you run the game, you'll see it's not quite a finished product. Here are some ideas for things you could do:

- add more aliens
- change the images to your own drawings
- end the game if the aliens reach the bottom of the screen
- make the aliens speed up as the game goes on
- create different types of aliens
- add a score that increases when you hit aliens
- add a title screen before the game starts
- include sound effects and/or music
- add more levels with different aliens

There are lots of tutorials online if you want to find out more about using Pygame. Just Google. Once you know what's going on, the [pygame documentaion](https://www.pygame.org/docs/) is also quite useful.

## Assets
The images used here came from [OpenGameArt.org](https://opengameart.org/)

- https://opengameart.org/content/8-bit-alien-assets by Alfalfamire@gmail.com

- https://opengameart.org/content/spaceship-bullet

- https://opengameart.org/content/space-background-1

