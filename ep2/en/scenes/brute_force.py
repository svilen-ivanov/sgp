import numpy
from manim import *

from ep2.scenes.description import Coin
from ep2.scenes.utils import CyrTex


groups = [
    [1, 1, 10, 10, 10, 10, 50, 50],
    [1, 1, 10, 10, 20, 50, 50],
    [1, 1, 20, 20, 50, 50],
    [1, 1, 5, 5, 10, 5 + 5, 10, 50, 50],
    [1, 1, 5, 5, 10, 20, 50, 50],
    [1, 1, 5, 5, 5, 5, 20, 50, 50],
    [1, 2, 2, 2, 5, 10, 10, 10, 50, 50],
    [2, 10, 10, 10, 10, 50, 50],
    [2, 10, 10, 20, 50, 50],
    [2, 20, 20, 50, 50],
    [2, 5, 5, 10, 10, 10, 50, 50],
    [2, 5, 5, 10, 20, 50, 50],
    [2, 5, 5, 5, 5, 10, 10, 50, 50],
    [2, 5, 5, 5, 5, 20, 50, 50],
]




class BruteForce(Scene):
    def construct(self):
        amount_cents_small = CyrTex(r'\foreignlanguage{bulgarian}{142 ¢} $=$').scale(2)
        amount_cents_small.shift(amount_cents_small.get_width() * LEFT + UP * 0.5)
        self.add(amount_cents_small)

        mo_group = Group()
        for loop in range(1):
            for group in groups:
                self.remove(mo_group)
                # self.play(FadeOut(mo_group, run_time=0.05))
                mo_group = Group()
                uniq, counts = numpy.unique(group, return_counts=True)
                print(uniq)
                first = None
                for coin, count in zip(uniq, counts):
                    print(f"{count} x {coin}")
                    mo_coins = [Coin(coin) for _ in range(count)]
                    mo_group.add(*mo_coins)
                    if first:
                        mo_coins[0].next_to(first, DOWN)
                    first = mo_coins[0]
                    for prev, cur in zip(mo_coins, mo_coins[1:]):
                        cur.next_to(prev, RIGHT)
                brace = Brace(mo_group, direction=LEFT)
                brace2 = BraceLabel(mo_group, r'\foreignlanguage{english}{$' + str(len(group)) + "$ coins}", label_constructor=CyrTex)
                mo_group.add(brace, brace2)
                mo_group.shift(amount_cents_small.get_critical_point(RIGHT) - brace.get_tip() + X_AXIS * DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)
                self.add(mo_group)
                # self.play(FadeIn(mo_group, run_time=0.05))
                self.wait(0.2)

        self.wait()
        self.play(FadeOut(amount_cents_small), FadeOut(mo_group))
        self.wait(10)
