from manim import *

from ep2.scenes.utils import CyrTex


class GreedyTitle(Scene):
    def construct(self):
        term_en = CyrTex(r"Greedy Algorithm").scale(2)
        group = VGroup(term_en)
        self.play(FadeIn(term_en))
        #term_bg.next_to(term_en, direction=DOWN)
        self.wait(2)
        #self.play(FadeIn(term_bg), group.center)
        self.wait(5)
        self.play(FadeOut(group))

        self.wait(10)
