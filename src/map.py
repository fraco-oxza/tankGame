import random


class Map:
    terrain_colors: list[str]
    background_image: str
    storm_color: str
    chosen_biome: int

    def __init__(
        self,
    ):
        self.terrain_colors = []
        self.background_image = ""
        self.storm_color = ""
        # 0 : snowy , 1 : forest, 2: desert, 3: city, 4:island
        self.chosen_biome = random.randint(0, 4)

    def define_terrain_colors(self):
        if self.chosen_biome == 0:
            self.terrain_colors = ["#3C474F", "#586874", "#99B4C9", "#B8D9F2"]

        elif self.chosen_biome == 1:
            self.terrain_colors = ["#3B5424", "#587D36", "#71A145", "#92CF59"]

        elif self.chosen_biome == 2:
            self.terrain_colors = ["#693C27", "#915336", "#BA6A45", "#DE7F53"]

        elif self.chosen_biome == 3:
            self.terrain_colors = ["#231F20", "#322E2D", "#40413C", "#635852"]

        else:
            self.terrain_colors = ["#563F49", "#856860", "#D6B393", "#F8DAB6"]

        return self.terrain_colors

    def define_background_image(self):
        # aqui ya no exploto el codigo
        if self.chosen_biome == 0:
            self.background_image = "images/sky.jpg"

        elif self.chosen_biome == 1:
            self.background_image = "images/forest.jpg"

        elif self.chosen_biome == 2:
            self.background_image = "images/desert.jpg"

        elif self.chosen_biome == 3:
            self.background_image = "images/city.jpg"

        else:
            self.background_image = "images/island.jpg"

        return self.background_image

    def define_storm_color(self):
        if self.chosen_biome == 0:
            self.storm_color = "#FFFFFF"

        elif self.chosen_biome == 1:
            self.storm_color = "#84D9F2"

        elif self.chosen_biome == 2:
            self.storm_color = "#AB7961"

        elif self.chosen_biome == 3:
            self.storm_color = "#231F20"

        else:
            self.storm_color = "#AB7961"
        return self.storm_color
