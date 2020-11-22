from manim import *

from ep2.scenes.utils import CyrTex


class Coin(Group):
    def __init__(self, nom, *mobjects, **kwargs):
        super().__init__(*mobjects, **kwargs)
        bg = ImageMobject("coin.png").set_width(1)
        nom_mo = MathTex(str(nom), color="#c89c31", fill_color="#4c3808").scale(1.2)
        self.add(bg, nom_mo)


class Description(Scene):
    def construct(self):
        amount_main = CyrTex(r'\foreignlanguage{english}{\$ 1.42}').scale(3)
        self.play(Write(amount_main))
        self.wait()

        amount_cents = CyrTex(r'\foreignlanguage{english}{142 cents}').scale(3)
        self.play(FadeOutAndShift(amount_main, UP), FadeInFrom(amount_cents, DOWN))
        self.wait()

        all_coins = Group()
        all_coins.add(Coin(1))
        all_coins.add(Coin(2))
        all_coins.add(Coin(5))
        all_coins.add(Coin(10))
        all_coins.add(Coin(20))
        all_coins.add(Coin(50))
        all_coins.arrange()
        self.add(all_coins)
        all_coins.next_to(amount_cents, DOWN, buff=LARGE_BUFF)

        amount_cents_small = CyrTex(r'\foreignlanguage{english}{142 ¢} =').scale(2)
        amount_cents_small.shift(amount_cents_small.get_width() * LEFT + UP)
        self.play(
            amount_cents.shift, amount_cents_small.get_width() * LEFT + UP,
            ReplacementTransform(amount_cents, amount_cents_small),
            all_coins.to_edge, DOWN
        )

        brace = MathTex(r'\underbrace{\qquad\qquad\qquad\qquad}').scale(1).rotate(-PI / 2)
        brace.next_to(amount_cents_small, RIGHT)
        self.play(FadeIn(brace))

        cents50 = all_coins[5]
        cents20 = all_coins[4]
        cents2 = all_coins[1]

        buff = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
        cents50_1 = cents50.copy()
        edge = brace.get_critical_point(RIGHT) + RIGHT * 0.75
        up = (cents50_1.get_height() + buff) * UP
        down = (cents50_1.get_height() + buff) * DOWN

        self.play(cents50_1.move_to, edge + up)
        cents50_2 = cents50.copy()
        self.play(cents50_2.next_to, cents50_1)

        cents20_1 = cents20.copy()
        self.play(cents20_1.move_to, edge)
        cents20_2 = cents20.copy()
        self.play(cents20_2.next_to, cents20_1)

        cents2_1 = cents2.copy()
        self.play(cents2_1.move_to, edge + down)
        self.wait()

        self.wait(10)
