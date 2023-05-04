import pygame
import numpy
from scipy.constants import pi

def load_image(path_to_file: str, scaling_factor: float = 1)->tuple:
    image = zoom_image(pygame.image.load(path_to_file), scaling_factor).convert_alpha()
    return image, image.get_rect()

def zoom_image(image: pygame.Surface, scaling_factor: float = 1)->pygame.Surface:
    image_width, image_height = image.get_size()
    new_image_size = image_width*scaling_factor, image_height*scaling_factor
    new_image = pygame.transform.scale(image, new_image_size)
    return new_image

class GameObject(pygame.sprite.Sprite):
    def __init__(self, path_to_image: str, position: tuple[int, int] = (100, 100), velocity: tuple[float, float] = (0, 0), scaling_factor: float = 1, mass: float=1000):
        super().__init__()
        self.image, self.rect = load_image(path_to_image, scaling_factor)
        self.rect.x, self.rect.y = position
        self._init_velocity_x, self._init_velocity_y = velocity
        self._velocity_x, self._velocity_y = self.init_velocity_x, self.init_velocity_y
        self._size = (self._width, self._height) = self.image.get_size()
        self._mass = mass

    # size of an object
    def get_width(self):
        return self._width
    
    def get_height(self):
        return self._height
    
    def get_size(self):
        return self._size
    
    # initial velocity projection on axis x
    @property
    def init_velocity_x(self):
        return self._init_velocity_x
    
    @init_velocity_x.setter
    def init_velocity_x(self, new_init_velocity_x: float):
        self._init_velocity_x = new_init_velocity_x
    
    # initial velocity projection on axis y
    @property
    def init_velocity_y(self):
        return self._init_velocity_y
    
    @init_velocity_y.setter
    def init_velocity_y(self, new_init_velocity_y: float):
        self._init_velocity_y = new_init_velocity_y

    # initial velocity
    @property
    def init_velocity(self):
        return (self.init_velocity_x, self.init_velocity_y)
    
    @init_velocity.setter
    def init_velocity(self, new_init_velocity_projections: tuple):
        self.init_velocity_x, self.init_velocity_y = new_init_velocity_projections

    # coordinates
    @property
    def x(self):
        return self.rect.x
    
    @property
    def y(self):
        return self.rect.y
    
    @property
    def position(self):
        return (self.x, self.y)

    @x.setter
    def x(self, new_x_value: int):
        self.rect.x = new_x_value

    @y.setter
    def y(self, new_y_value: int):
        self.rect.y = new_y_value

    @position.setter
    def position(self, new_position_value: tuple):
        self.x, self.y = new_position_value

    
    # getting current velocities
    @property
    def velocity_x(self):
        return self._velocity_x
    
    @velocity_x.setter
    def velocity_x(self, new_velocity_x):
        if numpy.absolute(self._velocity_x)<10:
            self._velocity_x = new_velocity_x

    @property
    def velocity_y(self):
        return self._velocity_y
    
    @velocity_y.setter
    def velocity_y(self, new_velocity_y):
        if numpy.absolute(self._velocity_y)<10:
            self._velocity_y = new_velocity_y

    @property
    def velocity(self):
        return (self.velocity_x, self.velocity_y)

    # getting mass
    @property
    def mass(self):
        return self._mass
    

    
    # basics methods
    def draw(self, destination: pygame.Surface):
        destination.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, dx: float, dy: float):
        self.rect.x += dx
        self.rect.y += dy

    def interact_with_user(self, speed: float=50, dt: float=0.001):
        keys = pygame.key.get_pressed()

        # axis y points down
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.move(0, -speed*dt)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.move(0, speed*dt)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move(-speed*dt, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move(speed*dt, 0)

        return self

    def update(self, dt: float):
        self.move(self._velocity_x*dt, self._velocity_y*dt)
        return self

    def restrict(self, display: pygame.Surface, top: int = 0, bottom: int = 600, left: int = 0, right: int = 1000):
        if self.x < left: self.x = left
        if self.x > right: self.x = right
        # the axis y points down
        if self.y < top: self.y = top
        if self.y > bottom: self.y = bottom

        """
        if self.x <= left or self.x >= right:
            self._velocity_x = -self._velocity_x
        if self.y >= bottom or self.y <= top:
            self._velocity_y = -self._velocity_y
        """

        return self
    

"""
class ViscousFluid:
    def __init__(self, dynamic_viscosity = 1.4):
        self.__viscosity = dynamic_viscosity

    @property
    def viscosity(self):
        return self.__viscosity
    
    @viscosity.setter
    def viscosity(self, dynamic_viscosity):
        if dynamic_viscosity<=0:
            raise ValueError("Viscosity can't be less than or equal to zero.")
        self.__viscosity = dynamic_viscosity
    

    def damping(self, part: GameObject, dt):
        part_width = part.get_width()
        radius = part_width/2

        attenuation_coefficient = 6*pi*self.viscosity*radius/part.mass

        dv_x = attenuation_coefficient*numpy.absolute(part.velocity_x)*dt
        dv_y = attenuation_coefficient*numpy.absolute(part.velocity_y)*dt

        if part.velocity_x>0:
            part.velocity_x -= dv_x
        if part.velocity_x<0:
            part.velocity_x += dv_x
        if numpy.absolute(part.velocity_x)<15:
            part.velocity_x = 0

        if part.velocity_y>0:
            part.velocity_y -= dv_y
        if part.velocity_y<0:
            part.velocity_y += dv_y
        if numpy.absolute(part.velocity_y)<15:
            part.velocity_y = 0
"""


# There are a few more specific classes for only snake-game below
# palette: https://coolors.co/palette/0d1b2a-1b263b-415a77-778da9-e0e1dd

class Playground:
    def __init__(self, screen: pygame.Surface, position: tuple[int, int]=(100, 100), table: tuple[int, int]=(10,10), cell_size: int = 21):
        self._screen = screen
        self._x, self._y = position
        self._rows, self._columns = table
        self._cell_size = cell_size
        self._width = self._columns*self._cell_size
        self._height = self._rows*self._cell_size

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height
    
    def draw(self, layer_1_color: str = "#778DA9", grid_color: str = "#1B263B"):

        pygame.draw.rect(self._screen, layer_1_color, (self._x, self._y, self.get_width(), self.get_height()), border_radius = 2)
        for r in range(self._rows):
            raw_y = self._y + r*self._cell_size
            pygame.draw.line(self._screen, grid_color, (self._x, raw_y), (self._x + self.get_width(), raw_y), width=1)
        for c in range(self._columns):
            column_x = self._x + c*self._cell_size
            pygame.draw.line(self._screen, grid_color, (column_x, self._y), (column_x, self._y + self.get_height()), width=1)


class SnakeBlock(GameObject):
    def __init__(self, path_to_image: str, position: tuple[int, int] = (100, 100), velocity: tuple[float, float] = (0, 0), scaling_factor: float = 1):
        super().__init__(path_to_image, position, velocity, scaling_factor)

    def interact_with_user(self, speed: float = 100):
        keys = pygame.key.get_pressed()

        # axis y points down
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.init_velocity_x, self.init_velocity_y = 0, -speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.init_velocity_x, self.init_velocity_y = 0, speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: 
            self.init_velocity_x, self.init_velocity_y = -speed, 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.init_velocity_x, self.init_velocity_y = speed, 0

        self._velocity_x, self._velocity_y = self.init_velocity_x, self.init_velocity_y

        return self
        