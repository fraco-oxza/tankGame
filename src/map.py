import random


class Map:
    terrain_colors: list[str]
    background_image: str
    storm_color: str
    chosen_biome: int

    def __init__(self, ):
        self.terrain_colors = []
        self.background_image = ""
        self.storm_color = ""
        # 0 : snowy , 1 : forest, 2: desert
        self.chosen_biome = random.randint(0, 2)

    def define_terrain_colors(self):
        if self.chosen_biome == 0:
            self.terrain_colors = ["#3C474F", "#586874", "#99B4C9", "#B8D9F2"]

        elif self.chosen_biome == 1:
            self.terrain_colors = ["#92CF59", "#71A145", "#587D36", "#3B5424"]

        else:
            self.terrain_colors = ["#693C27", "#915336", "#BA6A45", "#DE7F53"]

        return self.terrain_colors

    def define_background_image(self):
        # aqui ya no exploto el codigo
        if self.chosen_biome == 0:
            self.background_image = "images/sky.jpg"

        elif self.chosen_biome == 1:
            self.background_image = "images/forest.jpg"

        else:
            self.background_image = "images/desert.jpg"

        return self.background_image

    def define_storm_color(self):
        if self.chosen_biome == 0:
            self.storm_color = "#FFFFFF"

        elif self.chosen_biome == 1:
            self.storm_color = "#84D9F2"

        else:
            self.storm_color = "#AB7961"

        return self.storm_color
