from manim import *

from ep2.scenes.description import Coin
from ep2.scenes.utils import CyrTex


class MinCount(CyrTex):
    def __init__(self, sum, **kwargs):
        super().__init__(r'$min(\text{\foreignlanguage{bulgarian}{\textit{\textbf{' + str(sum) + r'} ст.}}})$',
                         **kwargs)


class Algo(MovingCameraScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.coin1 = Coin(1)
        self.coin2 = Coin(2)
        self.coin5 = Coin(5)
        self.coins = [self.coin1, self.coin2, self.coin5]
        self.mins = [MinCount(i) for i in range(8)]
        self.eq = CyrTex('$=$')
        self.plus = CyrTex('$+$')
        self.min_word = CyrTex('$min$')
        self.question_mark = CyrTex('?')
        self.same_min = [[] for _ in self.mins]
        self.iteration_groups = []
        print(self.same_min)

    def construct(self):
        Group(*self.coins).arrange().to_edge(DOWN)
        self.add(*self.coins)

        mobject7 = self.mins[7].copy()
        self.same_min[7].append(mobject7)
        new_mobject6 = self.animate_min(mobject7, 6, [6, 5, 2], first=True)
        new_mobject5 = self.animate_min(new_mobject6, 5, [5, 4, 1])
        new_mobject4 = self.animate_min(new_mobject5, 4, [4, 3, 0])
        self.iteration_groups[2].fade(-1) # super hack - fade value is relative
        self.iteration_groups[1].fade(-1) # super hack - fade value is relative
        self.iteration_groups[0].fade(-1) # super hack - fade value is relative
        self.play(
            self.camera_frame.move_to, self.iteration_groups[1],
            # VGroup(*self.same_min[6]).fade, 0,
            # VGroup(*self.same_min[5]).fade, 0,
            VGroup(*self.same_min[6]).set_color, RED,
            VGroup(*self.same_min[5]).set_color, YELLOW,
        )
        self.wait(10)

    def animate_min(self, align_to_mobject, next, options, first=False):
        eq = self.eq.copy().next_to(align_to_mobject)
        question_mark = self.question_mark.copy().next_to(eq)

        self.add(align_to_mobject, eq, question_mark)

        group = Group()
        group.add(align_to_mobject, eq, question_mark)
        if first:
            group.center()
            self.play(VGroup(align_to_mobject, eq).to_edge, LEFT, FadeOut(question_mark))
        else:
            self.play(FadeIn(question_mark), run_time=0.5)
            self.play(FadeOut(question_mark), run_time=0.5)
        group.remove(question_mark)

        min_word = self.min_word.copy().next_to(eq)
        brace = MathTex(r'\underbrace{\qquad\qquad\qquad\qquad}').scale(1).rotate(-PI / 2)

        brace = brace.copy().next_to(min_word)
        self.play(FadeIn(brace), FadeIn(min_word))
        group.add(brace, min_word)

        coins = copy.deepcopy(self.coins)

        self.play(
            coins[0].next_to, brace.get_critical_point(UR), {"aligned_edge": UL},
            coins[1].next_to, brace.get_critical_point(RIGHT), {"aligned_edge": LEFT},
            coins[2].next_to, brace.get_critical_point(DR), {"aligned_edge": DL},
        )
        group.add(*coins)

        pluses = [self.plus.copy().next_to(coin) for coin in coins]
        self.play(FadeIn(VGroup(*pluses)))
        group.add(*pluses)

        new_mins = [new_min.copy().next_to(plus) for plus, new_min in zip(pluses, [self.mins[i] for i in options])]
        self.play(FadeIn(VGroup(*new_mins)))
        group.add(*new_mins)

        next_min = new_mins[options.index(next)]
        self.play(*[(ApplyMethod(mo.fade, fade_value)) for mo, fade_value in map(lambda x: (x, 0.5 if x != next_min else 0), group.submobjects)])

        for i, opt in enumerate(options):
            self.same_min[opt].append(new_mins[i])

        target = align_to_mobject.get_center()
        self.play(
            self.camera_frame.shift, next_min.get_center() - target,
            Group(*self.coins).shift,  next_min.get_center() - target,
        )

        self.iteration_groups.append(group)

        return next_min
