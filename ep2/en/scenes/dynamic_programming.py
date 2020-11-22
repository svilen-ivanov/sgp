from manim import *
from numpy.random._generator import default_rng

from ep2.scenes.description import Coin
from ep2.scenes.utils import CyrTex
import numpy as np

random_points = [
    [0.6942365002997297, 1.7215149309793558],
    [1.4615235707967127, 0.3590654639751749],
    [-1.0857984094022441, 1.167152904533249],
    [-0.8876485509305958, 3.134184006256638],
    [6.594314816014638, -0.9324678493937784],
    [4.148978319397896, 0.23115935802323584],
    [0.9677448688914811, 3.4047731063412883],
    [-6.100820505630052, -3.3029656023876743],
    [-6.823560569737589, 2.660958764383504],
    [3.956007124620095, 2.9600971859745533],
    [6.807016422865976, 2.393268513733789],
]


class DynamicProgramming(Scene):
    def construct(self):
        term_en = CyrTex(r"Dynamic Programming").scale(2)
        #term_bg = CyrTex(r"\foreignlanguage{bulgarian}{\textit{Динамично програмиране}}").scale(1.5)

        group = VGroup(term_en)
        self.play(FadeIn(term_en))
        #term_bg.next_to(term_en, direction=DOWN)
        self.wait(2)
        #self.play(FadeIn(term_bg), group.center)
        self.wait(5)
        self.play(FadeOut(group))

        photo = ImageMobject("Richard_Ernest_Bellman.jpg").set_height(6)
        title_below = CyrTex(r"\foreignlanguage{english}{Richard Ernest Bellman}")
        group2 = Group(photo, title_below)
        self.play(FadeIn(photo), photo.to_edge, UP)
        title_below.next_to(photo, direction=DOWN)
        self.play(Write(title_below, run_time=1))
        self.wait(5)
        self.play(FadeOut(group2))
        self.wait(5)

        for x, y in random_points:
            print(f"[{x}, {y}]")
            coin = Coin("10").move_to(np.array((x, y, 0))).shift_onto_screen()
            self.add(coin)
        self.wait(5)
        new_coin = Coin("10").move_to(np.array((2, -2, 0)))
        self.play(FadeIn(new_coin))
        self.wait(10)
