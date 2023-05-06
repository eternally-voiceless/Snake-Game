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
        #if numpy.absolute(self._velocity_x)<10:
        self._velocity_x = new_velocity_x

    @property
    def velocity_y(self):
        return self._velocity_y
    
    @velocity_y.setter
    def velocity_y(self, new_velocity_y):
        #if numpy.absolute(self._velocity_y)<10:
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

    def set_speed_by_click(self, speed: float=100, dt: float=0.001):
        keys = pygame.key.get_pressed()

        #axis y points down
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.init_velocity_y = - speed
            self.velocity_y += self.init_velocity_y
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.init_velocity_y = speed
            self.velocity_y += self.init_velocity_y
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.init_velocity_x = - speed
            self.velocity_x += self.init_velocity_x
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.init_velocity_x = speed
            self.velocity_x += self.init_velocity_x

        return self
            

    def update(self, dt: float):
        self.move(self.velocity_x*dt, self.velocity_y*dt)
        return self

    def restrict(self, area: pygame.Surface):
        # the axis y points down
        if self.x < area.x:
            self.x = area.x
        if self.x > area.x+area.get_width()-self.get_width():
            self.x = area.x+area.get_width()-self.get_width()
        if self.y < area.y:
            self.y = area.y
        if self.y > area.y+area.get_height()-self.get_height():
            self.y = area.y+area.get_height()-self.get_height()

        return self

    def damping(self, viscosity: float, dt: float):
        radius = self.get_width()/2
        attenuation_coefficient = 6*pi*viscosity*radius/self._mass
        
        dv_x = attenuation_coefficient*numpy.absolute(self.velocity_x)*dt
        dv_y = attenuation_coefficient*numpy.absolute(self.velocity_y)*dt

        if self.velocity_x>0:
            self.velocity_x -= dv_x
        if self.velocity_x<0:
            self.velocity_x += dv_x
        if numpy.absolute(self.velocity_x)<15:
            self.velocity_x = 0

        if self.velocity_y>0:
            self.velocity_y -= dv_y
        if self.velocity_y<0:
            self.velocity_y += dv_y
        if numpy.absolute(self.velocity_y)<15:
            self.velocity_y = 0

        return self


# There are a few more specific classes for only snake-game below
# palette: https://coolors.co/palette/0d1b2a-1b263b-415a77-778da9-e0e1dd

class Grid:
    def __init__(self, screen: pygame.Surface, position: tuple[int, int]=(100, 100), table: tuple[int, int]=(10,10), cell_size: int = 21):
        self._screen = screen
        self.x, self.y = position
        self._rows, self._columns = table
        self._cell_size = cell_size
        self._width = self._columns*self._cell_size
        self._height = self._rows*self._cell_size

        self._nodes = []
        for r in range(self._rows+1):
            node_r = self.y + r*self._cell_size
            row = []
            for c in range(self._columns+1):
                node_c = self.x + c*self._cell_size
                row.append((node_c, node_r))
            self._nodes.append(row)
        

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height
    
    def draw(self, layer_1_color: str = "#778DA9", grid_color: str = "#1B263B"):

        pygame.draw.rect(self._screen, layer_1_color, (self.x, self.y, self.get_width(), self.get_height()), border_radius = 2)
        for r in range(self._rows):
            raw_y = self.y + r*self._cell_size
            pygame.draw.line(self._screen, grid_color, (self.x, raw_y), (self.x + self.get_width(), raw_y), width=1)
        for c in range(self._columns):
            column_x = self.x + c*self._cell_size
            pygame.draw.line(self._screen, grid_color, (column_x, self.y), (column_x, self.y + self.get_height()), width=1)

        """for r in self.get_nodes():
            for node in r:
                pygame.draw.polygon(self._screen, "red", 
                                    [
                                        (node[0]-1, node[1]), 
                                        (node[0]+1, node[1]),
                                        (node[0], node[1]-1),
                                        (node[0], node[1]+1)
                                    ]
                                    , 1)"""

    def get_nodes(self):
        return self._nodes


class SnakeBlock(GameObject):
    def __init__(self, path_to_image: str, position: tuple[int, int] = (100, 100), velocity: tuple[float, float] = (0, 0), scaling_factor: float = 1):
        super().__init__(path_to_image, position, velocity, scaling_factor)

    def interact_with_user(self, grid: Grid, speed: float=100, dt: float=0.001):
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
        
        self.velocity_x, self.velocity_y = self.init_velocity_x, self.init_velocity_y

        # keep block inside the corridor

        return self

    def point_closest_nodes(self, window: pygame.Surface, grid: Grid):
        """This method for debugging"""
        nodes = self.closest_nodes(grid)
        for n in nodes:
            pygame.draw.circle(window, "red", n, 1, 1)

    """def point_next_closest_nodes(self, window: pygame.Surface, grid: Grid):
        "This method for debugging"
        for p in self.closest_nodes(grid):
            if self.velocity_x>0:
                node = (p[0]+grid., p[1])
            pygame.draw.circle(window, "red", p, 1, 1)"""
    
    def closest_nodes(self, grid: Grid)->list[tuple]:
        center_x = self.x + self.get_width()/2
        center_y = self.y + self.get_height()/2

        closest_node = (grid.x, grid.y)
        distance_to_node = numpy.inf
        nodes_around = []

        for r in grid.get_nodes():
            for node in r:
                current_distance = numpy.sqrt(numpy.power(node[0]-center_x, 2) + numpy.power(node[1]-center_y, 2))
                if current_distance<self.get_width():
                    nodes_around.append((node[0], node[1]))
        
        return nodes_around

        
    def restrict(self, grid: Grid):
        # return block to the map
        if self.x<grid.x:
            self.x = grid.x+grid.get_width()-self.get_width()
            
        if self.x>grid.x+grid.get_width()-self.get_width():
            self.x = grid.x
            
        if self.y<grid.y:
            self.y = grid.y+grid.get_height()-self.get_height()
            
        if self.y>grid.y+grid.get_height()-self.get_height():
            self.y = grid.y
        
        return self
    
    
        