from manim import *

from ep2.scenes.utils import CyrTex


class BruteForceTitle(Scene):
    def construct(self):
        term_en = CyrTex(r"Brute Force").scale(2)
        term_bg = CyrTex(r"\foreignlanguage{bulgarian}{\textit{Метод на грубата сила}}").scale(1.5)
        group = VGroup(term_bg, term_en)
        self.play(FadeIn(term_en))
        term_bg.next_to(term_en, direction=DOWN)
        self.wait()
        self.play(FadeIn(term_bg), group.center)
        self.wait(2)
        self.play(FadeOut(group))
