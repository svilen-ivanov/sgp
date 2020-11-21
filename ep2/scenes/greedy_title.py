from manim import *

from ep2.scenes.utils import CyrTex


class GreedyTitle(Scene):
    def construct(self):
        term_en = CyrTex(r"Greedy Algorithm").scale(2)
        term_bg = CyrTex(r"\foreignlanguage{bulgarian}{\textit{Алчен алгоритъм}}").scale(1.5)
        group = VGroup(term_bg, term_en)
        self.play(FadeIn(term_en))
        term_bg.next_to(term_en, direction=DOWN)
        self.wait()
        self.play(FadeIn(term_bg), group.center)
        self.wait(5)
        self.play(FadeOut(group))

        self.wait(10)
