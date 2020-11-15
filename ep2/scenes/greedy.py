import numpy
from manim import *

from ep2.scenes.description import Coin
from ep2.scenes.utils import CyrTex


class Greedy(Scene):
    def construct(self):
        all_coins = Group()
        all_coins.add(Coin(1))
        all_coins.add(Coin(5))
        all_coins.add(Coin(10))
        all_coins.add(Coin(20))
        all_coins.add(Coin(25))
        all_coins.arrange()
        self.add(all_coins)
        all_coins.to_edge(DOWN, buff=LARGE_BUFF)

        amount_cents_small = CyrTex(r'\foreignlanguage{bulgarian}{$40$ ст.} =').scale(2)
        amount_cents_small.shift(amount_cents_small.get_width() * LEFT + UP)
        self.add(amount_cents_small)

        brace = MathTex(r'\underbrace{\qquad\qquad\qquad\qquad}').scale(1).rotate(-PI / 2)
        brace.next_to(amount_cents_small, RIGHT)
        self.play(FadeIn(brace))

        cents25 = all_coins[4]
        cents10 = all_coins[2]
        cents5 = all_coins[1]

        buff = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
        cents25_1 = cents25.copy()

        edge = brace.get_critical_point(RIGHT) + RIGHT * 0.75
        up = (cents25_1.get_height() + buff) * UP
        down = (cents25_1.get_height() + buff) * DOWN

        self.play(cents25_1.move_to, edge + up)

        cents10_1 = cents10.copy()
        self.play(cents10_1.move_to, edge)

        cents5_1 = cents5.copy()
        self.play(cents5_1.move_to, edge + down)
        self.wait()

        wrong_group = Group(cents25_1, cents10_1, cents5_1)
        cross = Cross(wrong_group)
        self.add(cross)
        self.wait()
        self.play(LaggedStart(*[FadeOut(wrong_group), FadeOut(cross), FadeOut(brace)], lag_ratio=0.2))

        brace = MathTex(r'\underbrace{\qquad\qquad\quad}').scale(1).rotate(-PI / 2)
        brace.next_to(amount_cents_small, RIGHT)
        self.play(FadeIn(brace))

        cents20 = all_coins[3]

        up = (cents20.get_height() + buff) * UP * 0.5
        down = (cents20.get_height() + buff) * DOWN * 0.5

        cents20_1 = cents20.copy()
        self.play(cents20_1.move_to, edge + up)
        cents20_2 = cents20.copy()
        self.play(cents20_2.move_to, edge + down)
        self.wait()

        self.play(*[FadeOut(x) for x in self.mobjects])
        self.wait(10)
