import pygame, math
import pygame_tools as pgt

class PolygonSim(pgt.GameScreen):
    '''A polygon drawing simulation'''

    SIDE_LEN = 150
    MAX_POLYGONS = 35
    BG = pygame.Color('black')
    FG = pygame.Color('white')
    FGs = [ # rainbow
        pygame.Color(255, 0, 0),
        pygame.Color(255, 128, 0),
        pygame.Color(255, 255, 0),
        pygame.Color(128, 255, 0),
        pygame.Color(0, 255, 0),
        pygame.Color(0, 255, 128),
        pygame.Color(0, 255, 255),
        pygame.Color(0, 128, 255),
        pygame.Color(0, 0, 255),
        pygame.Color(128, 0, 255),
        pygame.Color(255, 0, 255),
        pygame.Color(255, 0, 128)
    ]
    FGs_LEN = len(FGs)

    def __init__(self):
        pygame.init()
        size = pgt.Point(1400, 750)
        super().__init__(pygame.display.set_mode(size), size)
        self.center = self.window_size // 2
        self.color_index = -1 # start before color
        self.fill_polygons = False
        self.draw()

    def update(self):
        '''
        Run each frame; update the screen and attributes
        essensially an image is being displayed so no need for updating each frame
        '''
        pass

    def key_down(self, event: pygame.event.Event):
        '''
        Process a keydown event
        '''
        match event.unicode.lower():
            case ' ':
                self.fill_polygons = not self.fill_polygons
                self.draw()

    def draw(self):
        '''
        Draw everything to screen
        '''
        self.screen.fill(self.BG)
        for n in reversed(range(3, self.MAX_POLYGONS)):
            self.draw_polygon(
                n,
                self.SIDE_LEN,
                self.FG,
                0 if self.fill_polygons else 1,
                math.pi / n + math.pi / 2 # perform 1/2nth turn + 1/4th turn
            )

    def draw_polygon(
        self,
        sides: int,
        side_length: int,
        color: pygame.Color,
        side_width: int = 0,
        offset_angle: float = math.pi / 2,
        center: pgt.Point = None
    ):
        '''
        Draw a polygon with a given number of sides and a side_length
        :sides: the number of sides in the polygon
        :side_length: the length of each of the sides of the polygon
        :color: color of polygon
        :side_width: width of the sides of the polygon; zero for filled polygon
        :offset_angle: the angle to offset the initial angle by
        :center: center of the polygon
        '''
        if center is None:
            center = self.center
        if sides < 3:
            raise ValueError(f'By definition, a polygon must have at least 3 sides, {sides} is not enough sides')
        theta = math.pi - math.pi * 2 / (sides)
        hypot = side_length / 2 / math.cos(theta / 2)
        points = []
        for i in range(sides):
            theta = math.pi * 2 * i / sides + offset_angle
            points.append(self.center + pgt.Point(math.cos(theta), math.sin(theta)) * hypot)
        pygame.draw.polygon(
            self.screen,
            self.get_color(),
            points,
            side_width
        )

    def get_color(self) -> pygame.Color:
        '''
        increments color index and returns the current color
        :returns: a color
        '''
        self.color_index += 1
        if self.color_index >= self.FGs_LEN:
            self.color_index = 0
        return self.FGs[self.color_index]

def main():
    '''Driver code'''
    PolygonSim().run()

if __name__ == "__main__":
    main() # run driver code
