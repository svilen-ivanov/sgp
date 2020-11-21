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
        self.mins = [MinCount(i) for i in range(10)]
        self.eq = CyrTex('$=$')
        self.plus = CyrTex('$+$')
        self.min_word = CyrTex('$min$')
        self.cdots = CyrTex(r'$\cdots$')
        self.zero = CyrTex('$0$')
        self.question_mark = CyrTex('?')
        self.same_min = [[] for _ in self.mins]
        self.iteration_groups = []

    def to_edge(self, direction, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER):
        def update_function(mob):
            """
            Direction just needs to be a vector pointing towards side or
            corner in the 2d plane.
            """
            print(self.camera_frame.get_center())
            target_point = self.camera_frame.get_center() + np.sign(direction) * (
                np.array((
                    self.camera_frame.get_width() / 2,
                    self.camera_frame.get_height() / 2,
                    0))
            )
            point_to_align = mob.get_critical_point(direction)
            shift_val = target_point - point_to_align - buff * np.array(direction)
            mob.shift(shift_val)

        return update_function

    def construct(self):
        coin_group = Group(*self.coins)
        coin_group.arrange()
        coin_group.add_updater(self.to_edge(DOWN))
        self.play(FadeIn(coin_group))
        self.wait()

        mobject9 = self.mins[9].copy()
        self.same_min[9].append(mobject9)
        self.play(FadeIn(mobject9))
        self.wait()

        target = self.animate_question_mark(mobject9, first=True)
        self.wait()

        group9 = self.animate_min(target, [8, 7, 4])
        self.play(*group9.shift_into_focus(self, 0))

        min8eq = self.animate_question_mark(group9.lines[0])
        group8 = self.animate_min(min8eq, [7, 6, 3])

        self.play(*group9.space_out(), self.camera_frame.scale, 2)
        self.play(self.camera_frame.scale, 0.5, *group9.shift_into_focus(self, 1))
        self.wait()

        min7eq = self.animate_question_mark(group9.lines[1])
        group7 = self.animate_min(min7eq, [6, 5, 2])

        self.play(*group9.shift_into_focus(self, 2))
        self.wait()

        min4eq = self.animate_question_mark(group9.lines[2])
        group4 = self.animate_min(min4eq, [3, 2])

        self.play(self.camera_frame.scale, 1.8, self.camera_frame.move_to, group9.get_critical_point(RIGHT),
                  coin_group.to_edge, DR)
        self.wait()

        more_anim = []
        for group in (group8, group7, group4):
            for line in group.lines:
                eq = self.eq.copy()
                eq.next_to(line)
                cdots = self.cdots.copy()
                cdots.next_to(eq)
                group.add(eq, cdots)
                more_anim.append(FadeIn(eq))
                more_anim.append(FadeIn(cdots))
        self.play(*more_anim)
        self.wait()

        self.play(*self.focus_these_fade_rest(self.same_min[7], color="#e86e1c"), run_time=0.5)
        self.wait()

        self.play(*self.focus_others(self.same_min[6], color="#bf1ce8"), run_time=0.5)
        self.wait()

        self.play(*self.focus_others(self.same_min[2], color="#45e81c"), run_time=0.5)
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in self.all_mobjects_in_scene()])

        # new_mobject5 = self.animate_min(new_mobject6, 5, [5, 4, 1])
        # new_mobject4 = self.animate_min(new_mobject5, 4, [4, 3, 0])
        # new_mobject4 = self.animate_min(new_mobject5, 3, [4, 3, 0])
        # self.iteration_groups[2].fade(-1) # super hack - fade value is relative
        # self.iteration_groups[1].fade(-1) # super hack - fade value is relative
        # self.iteration_groups[0].fade(-1) # super hack - fade value is relative
        # self.play(
        #     self.camera_frame.move_to, self.iteration_groups[1],
        #     # VGroup(*self.same_min[6]).fade, 0,
        #     # VGroup(*self.same_min[5]).fade, 0,
        #     VGroup(*self.same_min[6]).set_color, RED,
        #     VGroup(*self.same_min[5]).set_color, YELLOW,
        # )
        self.wait(10)

    def all_mobjects_in_scene(self):
        uniq_mobjects = set()

        def recursive(mobjects):
            for submob in mobjects:
                if isinstance(submob, ScreenRectangle):
                    pass
                elif isinstance(submob, (MinOption, Group, VGroup)):
                    print(f"--- {submob}")
                    recursive(submob.submobjects)
                else:
                    uniq_mobjects.add(submob)

        recursive(self.get_mobjects())
        return uniq_mobjects

    def focus_these_fade_rest(self, to_focus, color=WHITE):
        animations = []
        for mob in self.all_mobjects_in_scene() - set(to_focus):
            animations.extend([mob.fade, 0.5])
        for mob in to_focus:
            animations.extend([mob.set_color, color])
        return animations

    def focus_others(self, to_focus, color=WHITE):
        animations = []
        for mob in to_focus:
            animations.extend([mob.set_color, color, mob.fade, -1])
        return animations

    def animate_question_mark(self, align_to_mobject, first=False):
        eq = self.eq.copy()
        eq.add_updater(lambda mob: mob.next_to(align_to_mobject))
        question_mark = self.question_mark.copy().next_to(eq)

        self.add(align_to_mobject, eq, question_mark)

        group = Group()
        group.add(align_to_mobject, eq, question_mark)
        if first:
            group.center()
            self.wait(5)
            self.play(VGroup(align_to_mobject, eq).to_edge, LEFT, FadeOut(question_mark))
        else:
            self.play(FadeIn(question_mark), run_time=0.5)
            self.play(FadeOut(question_mark), run_time=0.5)
        group.remove(question_mark)

        return eq

    def animate_min(self, target, options):
        group = MinOption()
        self.add(group)
        num_coins = len(options)
        coins = [self.coins[i].copy() for i in range(num_coins)]
        if num_coins == 3:
            brace = MathTex(r'\underbrace{\qquad\qquad\qquad\qquad}').scale(1).rotate(-PI / 2)
            coin_animations = [
                coins[0].next_to, brace, {"aligned_edge": UL},
                coins[1].next_to, brace, {"aligned_edge": LEFT},
                coins[2].next_to, brace, {"aligned_edge": DL},
            ]
        elif num_coins == 2:
            brace = MathTex(r'\underbrace{\qquad\qquad}').scale(1).rotate(-PI / 2)
            coin_animations = [
                coins[0].next_to, brace, {"aligned_edge": UL},
                coins[1].next_to, brace, {"aligned_edge": DL},
            ]
        elif num_coins == 1:
            brace = MathTex(r'\underbrace{\qquad}').scale(1).rotate(-PI / 2)
            coin_animations = [
                coins[0].next_to, brace, {"aligned_edge": LEFT},
            ]
        else:
            coin_animations = None
            brace = None

        if coin_animations:
            min_word = self.min_word.copy()
            min_word.next_to(target)
            brace.next_to(min_word)
            brace.set_height(len(coins) * coins[0].get_height() + (len(coins) - 1) * DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)
            self.play(FadeIn(brace), FadeIn(min_word))
            group.add(brace, min_word, *coins)
            self.play(*coin_animations)

            for i, coin in zip(options, coins):
                plus = self.plus.copy().next_to(coin)
                new_min = self.mins[i].copy().next_to(plus)
                self.same_min[i].append(new_min)
                self.play(FadeIn(VGroup(plus, new_min)))
                group.add(plus, new_min)
                group.add_line(coin, plus, new_min)

            group.add_brace(brace)
            group.add_min_word(min_word)
        else:
            zero = self.zero.copy()
            zero.next_to(target)
            self.play(FadeIn(zero))
            group.add(zero)

        group.add_updater(lambda mob: mob.next_to(target))
        return group

    def shift_into_focus(self, mobject):
        new_pos = mobject.get_critical_point(LEFT) + (config.frame_x_radius - DEFAULT_MOBJECT_TO_EDGE_BUFFER) * X_AXIS
        return self.camera_frame.move_to, new_pos


class MinOption(Group):
    def __init__(self, *mobjects, **kwargs):
        super().__init__(*mobjects, **kwargs)
        self.lines = []
        self.brace = None
        self.min_word = None

    def get_critical_point(self, direction):
        if np.array_equal(direction, LEFT) and self.min_word is not None:
            return self.min_word.get_critical_point(LEFT)
        else:
            return super(MinOption, self).get_critical_point(direction)

    def add_min_word(self, min_word):
        self.min_word = min_word

    def add_brace(self, brace):
        def updater(mobject):
            height = (self.lines[0].get_critical_point(UP) - self.lines[-1].get_critical_point(DOWN))[1]
            mobject.set_height(height, stretch=True)

        if len(self.lines):
            brace.add_updater(updater)
        self.brace = brace

    def add_line(self, coin, plus, new_min):
        self.lines.append(Group(coin, plus, new_min))

    def shift_into_focus(self, scene, line_no):
        new_min = self.lines[line_no]
        return scene.shift_into_focus(new_min)

    def space_out(self, ratio=3):
        return Group(*self.lines).space_out_submobjects, ratio
