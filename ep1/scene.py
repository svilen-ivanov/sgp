from manim import *
from manim.animation.animation import DEFAULT_ANIMATION_RUN_TIME

cyr_tex = TexTemplate(preamble=r"""
\usepackage[english,bulgarian,main=english]{babel}
\usepackage{ucs}
\usepackage[utf8x]{inputenc}
\usepackage[T2A]{fontenc}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{dsfont}
\usepackage{setspace}
\usepackage{tipa}
\usepackage{relsize}
\usepackage{textcomp}
\usepackage{mathrsfs}
\usepackage{calligra}
\usepackage{wasysym}
\usepackage{ragged2e}
\usepackage{physics}
\usepackage{xcolor}
\usepackage{microtype}
\DisableLigatures{encoding = *, family = * }
\linespread{1}
""")


class CyrTex(Tex):
    def __init__(self, *tex_strings, **kwargs):
        kwargs['tex_template'] = cyr_tex
        super().__init__(*tex_strings, **kwargs)


title = CyrTex(r'Merge Sort', color=LIGHT_PINK).scale(3)
subtitle = CyrTex(r'\foreignlanguage{bulgarian}{Свилен говори за програмиране}', color=TEAL_E)


class TitleScreen(Scene):
    def construct(self):
        self.time = 0
        self.add_sound("1.ogg")
        self.play(Write(title))
        self.play(title.shift, UP)
        text2 = CyrTex(r'\foreignlanguage{bulgarian}{Сортиране чрез сливане}').scale(1.5)
        self.play(Write(text2))
        subtitle.shift(DOWN * 3)
        self.play(Write(subtitle))
        self.wait()


class PythonImplementation(Scene):
    def construct(self):
        file = open("merge_sort.py", "r")
        code_str = file.read()
        file.close()

        py_func = code_str.split('\n\n\n')

        code1 = Paragraph(py_func[1], font="Hack", size=0.5, line_spacing=0.7)
        self.play(FadeIn(code1))
        # self.wait(10)
        code2 = Paragraph(py_func[2], font="Hack", size=0.5, line_spacing=0.7)
        self.play(FadeOut(code1))
        self.play(FadeIn(code2))
        self.wait(duration=DEFAULT_WAIT_TIME * 10)


class SortingItem(VGroup):
    def __init__(self, item, width, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.text = Text(str(item))
        self.border = Rectangle(width=width, height=1, fill_color="#333333", fill_opacity=1)
        self.add(self.border, self.text)

    def highlight(self, highlight_color=GREEN):
        self.border.set_stroke(width=DEFAULT_STROKE_WIDTH * 1.5, color=highlight_color)
        self.text.set_color(color=highlight_color)

    def highlight_word(self, word, highlight_color=GREEN):
        for start, end in self.text.find_indexes(word, self.text.original_text.replace(" ", "")):
            self.text.chars[start:end].set_color(color=highlight_color)

    def word(self, word):
        return VGroup(*[self.text.chars[start:end] for start, end in
                        self.text.find_indexes(word, self.text.original_text.replace(" ", ""))])

    def unhighlight(self):
        self.border.set_stroke(width=DEFAULT_STROKE_WIDTH, color=WHITE)
        self.text.set_color(color=WHITE)


class AbstractSortingScene(Scene):
    @staticmethod
    def construct_scene(scene, items, width=1.0):
        scene.time = 0
        scene.items = items
        scene.unsorted = VDict()
        scene.width = width

        prev = None
        for item in scene.items:
            curr = SortingItem(item, scene.width)
            scene.unsorted[item] = curr
            if prev:
                curr.next_to(prev, direction=DOWN, buff=0)
            scene.play(FadeIn(curr), scene.unsorted.move_to, ORIGIN, run_time=0.2)
            prev = curr
        scene.play(scene.unsorted.shift, (scene.unsorted.get_width() / 2 + LARGE_BUFF) * LEFT)
        processing_icon = SVGMobject('gear.svg').scale(0.5)
        scene.play(FadeIn(processing_icon, run_time=0.1))
        scene.play(Rotating(processing_icon, run_time=0.5, radians=PI / 2))
        scene.play(FadeOut(processing_icon, run_time=0.1))
        sorted_items = scene.items[:]
        sorted_items.sort()
        sorted_array = scene.unsorted.copy()
        animations = []
        for i, item in enumerate(sorted_items):
            # print(f"{i}, {item} {self.items[i]}")
            new_item = sorted_array[item]
            old_item = scene.unsorted[scene.items[i]]
            animations += new_item.highlight, new_item.next_to, old_item, {"buff": LARGE_BUFF * 2}
        scene.play(*animations, run_time=0.5)
        scene.play(LaggedStart(*([WiggleOutThenIn(sorted_array[i]) for i in sorted_items]), lag_ratio=0.05))
        scene.play(FadeOut(scene.unsorted), FadeOut(sorted_array), run_time=0.5)

    def highlight_then_swap(self, mo1, mo2):
        self.bring_to_front(mo1, mo2)
        self.play(mo1.highlight, mo2.highlight, )
        self.play(Swap(mo1, mo2))
        self.play(mo1.unhighlight, mo2.unhighlight, )


# class NumberSortingScene(AbstractSortingScene):
#     def __init__(self):
#         super(NumberSortingScene, self).__init__([8, 3, 17, 5, 19])
#
#
# class StringSortingScene(AbstractSortingScene):
#     def __init__(self):
#         super(StringSortingScene, self).__init__()
#
#
# class CardSortingScene(AbstractSortingScene):
#     def __init__(self):
#         super(CardSortingScene, self).__init__(["♥", "♣", "♠", "♦"])

class SortingScene(Scene):
    def construct(self):
        self.time = 0
        self.add_sound("2.ogg")
        AbstractSortingScene.construct_scene(self, [8, 3, 17, 5, 19])
        AbstractSortingScene.construct_scene(self, ["банан", "вишна", "авокадо", "ябълка"], width=3.0)
        AbstractSortingScene.construct_scene(self, ["♥", "♣", "♠", "♦"])


class TwoPassSorting(Scene):
    def __init__(self, items, width=1.0):
        super(TwoPassSorting, self).__init__()
        self.items = items
        self.unsorted = VDict()
        self.width = width
        self.time = 0
        self.add_sound("3.ogg")

    def construct(self):
        text_below = CyrTex(r"Алгоритъмът е \emph{стабилен}")
        self.play(Write(text_below))
        self.wait(1)
        pyramids = ImageMobject("All_Gizah_Pyramids.jpg").set_height(6)
        pyramids.to_edge(UP)
        self.play(text_below.to_edge, DOWN, FadeIn(pyramids))
        self.wait(13)
        self.play(FadeOut(pyramids), FadeOut(text_below))
        prev = None
        for item in self.items:
            curr = SortingItem(self.to_key(item), self.width).scale(0.95)
            self.unsorted[self.to_key(item)] = curr
            if prev:
                curr.next_to(prev, direction=DOWN, buff=0)
            self.play(FadeIn(curr), self.unsorted.move_to, ORIGIN, run_time=0.5)
            prev = curr
        self.play(self.unsorted.shift, (self.unsorted.get_width() / 2 + LARGE_BUFF) * LEFT)
        processing_icon = SVGMobject('gear.svg').scale(0.5)
        self.play(FadeIn(processing_icon, run_time=0.2))
        self.play(Rotating(processing_icon, run_time=1, radians=PI / 2))
        self.play(FadeOut(processing_icon, run_time=0.2))
        sorted_items = self.items[:]
        sorted_items.sort(key=lambda arr: arr[0])
        sorted_array1 = self.unsorted.copy()
        animations = []
        for i, item in enumerate(sorted_items):
            # print(f"{i}, {item} {self.items[i]}")
            new_item = sorted_array1[self.to_key(item)]
            old_item = self.unsorted[self.to_key(self.items[i])]
            animations += new_item.highlight_word, item[0], GREEN, \
                          new_item.highlight_word, item[1], RED, \
                          new_item.next_to, old_item, {"buff": LARGE_BUFF * 2}
        self.play(*animations, run_time=1)
        self.play(LaggedStart(*([WiggleOutThenIn(sorted_array1[self.to_key(i)].word(i[0])) for i in sorted_items]),
                              lag_ratio=0.1))
        self.play(
            LaggedStart(*([ShowPassingFlashAround(sorted_array1[self.to_key(i)].word(i[1])) for i in sorted_items]),
                        lag_ratio=0.1))
        self.play(FadeOut(self.unsorted), sorted_array1.move_to, self.unsorted, ORIGIN)
        self.play(FadeIn(processing_icon, run_time=0.2))
        self.play(Rotating(processing_icon, run_time=1, radians=PI / 2))
        self.play(FadeOut(processing_icon, run_time=0.2))
        sorted_items2 = sorted_items[:]
        sorted_items2.sort(key=lambda arr: self.to_key(arr))
        sorted_array2 = sorted_array1.copy()
        animations2 = []
        for i, item in enumerate(sorted_items2):
            # print(f"{i}, {item} {self.items[i]}")
            new_item = sorted_array2[self.to_key(item)]
            old_item = sorted_array1[self.to_key(sorted_items[i])]
            animations2 += new_item.highlight, GREEN, \
                           new_item.next_to, old_item, {"buff": LARGE_BUFF * 2}
        self.play(*animations2, run_time=1)
        self.play(
            LaggedStart(*([WiggleOutThenIn(sorted_array2[self.to_key(i)]) for i in sorted_items2]), lag_ratio=0.1))
        self.wait()

    @staticmethod
    def to_key(item):
        return " ".join(item)


class StudentsSortingScene(TwoPassSorting):
    def __init__(self):
        super(StudentsSortingScene, self).__init__(
            [["Александър", "Петров"],
             ["Борис", "Симеонов"],
             ["Борис", "Георгиев"],
             ["Александър", "Иванов"]], width=6.0)


class Complexity(GraphScene):
    CONFIG = {
        "include_tip": True,
        "y_axis_label": "",
        "x_axis_label": "$n$",
        "y_max": 120,
        "y_min": 0,
        "x_max": 22,
        "x_min": 0,
        # "y_tick_frequency": 100,
        # "x_tick_frequency": 5,
        # "axes_color": BLUE,
        "y_labeled_nums": range(0, 101, 20),
        "x_labeled_nums": range(0, 21, 5),
        # "x_labeled_nums": list(np.arange(2, 7.0 + 0.5, 0.5)),
        # "x_label_decimal": 1,
        # "y_label_direction": RIGHT,
        # "x_label_direction": UP,
        # "y_label_decimal": 3
        "y_axis_config": {
            "tick_frequency": 10
        }
    }

    def construct(self):
        self.time = 0
        self.add_sound("4.ogg")
        self.setup_axes(animate=True)
        y_label = CyrTex(r"\foreignlanguage{bulgarian}{\textit{итерации}}")
        y_label.next_to(self.y_axis.get_corner(UP + RIGHT))
        self.add(y_label)
        self.wait(1)
        graph1 = self.get_graph(lambda n: n * np.log2(n),
                                color="#00FF00",
                                x_min=1,
                                x_max=21,
                                stroke_width=DEFAULT_STROKE_WIDTH * 2
                                )

        graph1label = self.get_graph_label(graph1, label=r"n\cdot\log(n)")
        self.play(
            ShowCreation(graph1),
            ShowCreation(graph1label),
            run_time=2
        )
        self.wait(5)

        graph2 = self.get_graph(lambda n: n,
                                color="#999999",
                                x_min=1,
                                x_max=21,
                                stroke_width=DEFAULT_STROKE_WIDTH
                                )
        graph3 = self.get_graph(lambda n: n * n,
                                color="#999999",
                                x_min=1,
                                x_max=21,
                                )

        graph2label = self.get_graph_label(graph2, label=r"n")
        graph3label = self.get_graph_label(graph3, label=r"n^2")

        self.play(
            ShowCreation(graph2),
            ShowCreation(graph2label),
            ShowCreation(graph3),
            ShowCreation(graph3label),
            run_time=1
        )
        line1 = self.line_to_y(graph1, 10)
        line2 = self.line_to_y(graph2, 10)
        line3 = self.line_to_y(graph3, 10)

        self.play(
            ShowCreation(line1),
            ShowCreation(line2),
            ShowCreation(line3),
        )
        line1b = self.line_to_y(graph1, 20)
        self.play(
            TransformFromCopy(line1, line1b),
            FadeOut(line2),
            FadeOut(line3),
            FadeOut(graph2),
            FadeOut(graph3),
            FadeOut(graph2label),
            FadeOut(graph3label),
        )
        self.wait()


    def line_to_y(self, graph, x):
        zero = self.coords_to_point(0, 0)
        point = self.input_to_graph_point(x, graph)
        horiz = zero * (1, 0, 1) + point * (0, 1, 0)
        vert = zero * (0, 1, 1) + point * (1, 0, 0)
        return VGroup(
            Dot(point, color=graph.color),
            DashedLine(horiz, point, color=graph.color),
            DashedLine(vert, point, color=GRAY),
            Dot(horiz, color=graph.color)
        )


class DivideAndConquer(Scene):
    def construct(self):
        self.time = 0
        self.add_sound("5.ogg")
        von_neumann = ImageMobject("JohnvonNeumann-LosAlamos.gif").set_height(6)
        self.play(FadeIn(von_neumann))
        self.play(von_neumann.to_edge, UP)
        title_below = CyrTex(r"\foreignlanguage{bulgarian}{Джон фон Нойман}")
        title_below.next_to(von_neumann, DOWN)

        self.play(Write(title_below, run_time=1))
        self.wait()
        self.play(FadeOut(Group(von_neumann, title_below)))

        divide_and_conquer_en = Tex(r"""Divide and Conquer""").scale(2)
        divide_and_conquer_bg = CyrTex(r"""\foreignlanguage{bulgarian}{\textit{Разделяй и владей}}""").scale(1.5)

        self.play(FadeIn(divide_and_conquer_en))
        divide_and_conquer_bg.next_to(divide_and_conquer_en, direction=DOWN)
        self.wait()
        self.play(FadeIn(divide_and_conquer_bg))
        self.wait()
        self.play(FadeOut(VGroup(divide_and_conquer_bg, divide_and_conquer_en)))

        t = MathTex(r"5", '-', '3', '+', "4", r"\cdot", "2").scale(2)

        self.play(Write(t), run_time=2)
        self.play(t.shift, UP * 1.5, run_time=2)

        first_half = VGroup(*t.submobjects[0:3])
        second_half = VGroup(*t.submobjects[4:7])
        self.play(
            first_half.shift, LEFT,
            second_half.shift, RIGHT,
            run_time=2
        )

        first_half_copy = first_half.copy()
        secondt_half_copy = second_half.copy()

        self.add(first_half_copy, secondt_half_copy)
        self.play(
            first_half_copy.shift, DOWN * 1.5,
            secondt_half_copy.shift, DOWN * 1.5,
            run_time=2

        )

        res1 = MathTex(r"2").scale(2)
        res2 = MathTex(r"8").scale(2)
        res1.move_to(first_half_copy)
        res2.move_to(secondt_half_copy)

        self.play(
            ReplacementTransform(first_half_copy, res1),
            ReplacementTransform(secondt_half_copy, res2),
            run_time=2
        )

        plus = t.submobjects[3].copy()

        self.play(plus.shift, DOWN * 1.5,
                  run_time=2)

        self.play(
            res1.next_to, plus, LEFT, MED_LARGE_BUFF,
            res2.next_to, plus, RIGHT, MED_LARGE_BUFF,
            run_time=2
        )

        eq = VGroup(res1, res2, plus).copy()
        final_res = MathTex(r"10").scale(2)

        final_res.move_to(plus, aligned_edge=DOWN).shift(DOWN * 1.5)

        self.play(ReplacementTransform(eq, final_res),
                  run_time=2)
        self.play(FadeToColor(final_res, GREEN), WiggleOutThenIn(final_res),
                  run_time=2)
        self.wait()


class MergeSort(Scene):
    def __init__(self):
        super(MergeSort, self).__init__()
        self.unsorted = VDict()
        self.items = ["5", "6", "3", "1", "8", "7", "2", "4"]

    def construct(self):
        self.time = 0
        self.add_sound("7.ogg")
        prev = None
        for item in self.items:
            curr = SortingItem(item, 1)
            self.unsorted[item] = curr
            if prev:
                curr.next_to(prev, direction=RIGHT, buff=0)
            self.play(FadeIn(curr), self.unsorted.move_to, ORIGIN, run_time=0.5)
            prev = curr
        self.play(self.unsorted.shift, DOWN * 2, run_time=0.5)
        self.wait()

        up = 1.5 * UP
        left_step = LEFT / 2
        right_step = RIGHT / 2

        positions4 = self.record_positions()
        self.play(
            self.unsorted["5"].shift, 2 * left_step + up,
            self.unsorted["6"].shift, 2 * left_step + up,
            self.unsorted["3"].shift, 2 * left_step + up,
            self.unsorted["1"].shift, 2 * left_step + up,
            self.unsorted["8"].shift, 2 * right_step + up,
            self.unsorted["7"].shift, 2 * right_step + up,
            self.unsorted["2"].shift, 2 * right_step + up,
            self.unsorted["4"].shift, 2 * right_step + up,
            run_time=0.5

        )
        self.wait()
        positions3 = self.record_positions()

        self.play(
            self.unsorted["5"].shift, left_step + up,
            self.unsorted["6"].shift, left_step + up,
            self.unsorted["3"].shift, right_step + up,
            self.unsorted["1"].shift, right_step + up,
            run_time=0.5
        )
        self.play(
            self.unsorted["8"].shift, left_step + up,
            self.unsorted["7"].shift, left_step + up,
            self.unsorted["2"].shift, right_step + up,
            self.unsorted["4"].shift, right_step + up,
            run_time=0.5
        )
        self.wait()
        positions2 = self.record_positions()
        self.play(
            self.unsorted["5"].shift, left_step / 2 + up,
            self.unsorted["6"].shift, right_step / 2 + up,
            run_time=0.5
        )
        self.play(
            self.unsorted["3"].shift, left_step / 2 + up,
            self.unsorted["1"].shift, right_step / 2 + up,
            run_time=0.5
        )
        self.play(
            self.unsorted["8"].shift, left_step / 2 + up,
            self.unsorted["7"].shift, right_step / 2 + up,
            run_time=0.5
        )
        self.play(
            self.unsorted["2"].shift, left_step / 2 + up,
            self.unsorted["4"].shift, right_step / 2 + up,
            run_time=0.5
        )
        self.wait()

        self.animate_2n_row(positions2, [0], [1])
        self.wait()
        self.animate_2n_row(positions2, [2], [3])
        self.wait()
        self.animate_2n_row(positions2, [4], [5])
        self.wait()
        self.animate_2n_row(positions2, [6], [7])
        self.wait()

        self.animate_2n_row(positions3, [0, 1], [2, 3])
        self.wait()
        self.animate_2n_row(positions3, [4, 5], [6, 7])
        self.wait()

        self.animate_2n_row(positions4, [0, 1, 2, 3], [4, 5, 6, 7])

        self.play(self.unsorted.move_to, ORIGIN)
        self.play(WiggleOutThenIn(self.unsorted))
        self.wait()

    def record_positions(self):
        res = []
        for idx, item in enumerate(self.items):
            res.append(self.unsorted[item].get_center())
        return res

    def animate_2n_row(self, positions, ar, br):
        ar.sort(key=lambda i: self.items[i])
        br.sort(key=lambda i: self.items[i])
        while True:
            if len(ar) > 0:
                cl = ar[0]
            else:
                cl = None

            if len(br) > 0:
                cr = br[0]
            else:
                cr = None

            if cl is not None and cr is not None:
                lm = self.unsorted[self.items[cl]]
                rm = self.unsorted[self.items[cr]]
                self.bring_to_front(lm, rm)
                self.play(lm.highlight, YELLOW, rm.highlight, YELLOW)
                self.wait()
                p = positions.pop(0)
                if self.items[cl] < self.items[cr]:
                    ar.pop(0)
                    self.play(lm.highlight, GREEN, WiggleOutThenIn(lm))
                    self.play(lm.move_to, p, lm.unhighlight, run_time=0.5)
                else:
                    br.pop(0)
                    self.play(rm.highlight, GREEN, WiggleOutThenIn(rm))
                    self.wait()
                    self.play(rm.move_to, p, rm.unhighlight, run_time=0.5)
            elif cl is not None or cr is not None:
                if cl is not None:
                    c = ar.pop(0)
                else:
                    c = br.pop(0)
                m = self.unsorted[self.items[c]]
                p = positions.pop(0)
                # self.play(m.highlight, YELLOW)
                self.bring_to_front(m)
                self.play(m.highlight, GREEN, WiggleOutThenIn(m))
                self.play(m.move_to, p, m.unhighlight, run_time=0.5)
            else:
                break
            self.wait()


class MainAlgo(Scene):
    def construct(self):
        self.time = 0
        self.add_sound("6.ogg")
        algo = CyrTex(r"""
        \begin{tabular}{p{25em}}
        \begin{otherlanguage}{bulgarian}
        \begin{enumerate}
          \item 
                \emph{Разделяме} списъка на подсписъци, докато 
                стигнем до подсписък само с 1 елемент.
                Списък с един елемент се счита за сортиран.
          \item 
                \emph{Сливаме} съседни двойки от сортирани списъци 
                като създаваме нов списък, в който запазваме 
                подредбата.
          \item 
                Продължаваме докато остане един списък. 
                \emph{Това е подредения списък}.
        \end{enumerate}
        \end{otherlanguage}
        \end{tabular}
        """)
        self.wait(2)
        item1 = FadeInFrom(VGroup(*algo.submobjects[0][0:106]), direction=DOWN)
        item2 = FadeInFrom(VGroup(*algo.submobjects[0][106:195]), direction=DOWN)
        item3 = FadeInFrom(VGroup(*algo.submobjects[0][195:]), direction=DOWN)
        self.play(item1)
        self.wait(8)
        self.play(item2)
        self.wait(6)
        self.play(item3)
        self.wait()


class Final(Scene):
    def construct(self):
        self.time = 0
        self.add_sound("8.ogg")
        # algo = CyrTex(r"""
        # \begin{tabular}{p{25em}}
        # \begin{enumerate}
        #   \item
        #         \foreignlanguage{bulgarian}{Примерна реализация на} Python:
        #         github.com/svilen-ivanov/sgp/merge_sort.py
        #  \end{enumerate}
        # \end{tabular}
        # """)
        # item1 = FadeInFrom(algo, direction=DOWN)
        # self.play(item1)
        # self.wait()
        item1 = Text("Примерна реализация на Python:")
        item2 = Text("https://github.com/svilen-ivanov/sgp/ep1/merge_sort.py", font="Hack").scale(0.5)
        item2.next_to(item2, direction=DOWN)
        self.play(FadeIn(item1))
        self.play(FadeIn(item2))
        self.wait(3)
        self.play(FadeOut(item1), FadeOut(item2))
        item3 = Text("Благодаря за вниманието!", color=TEAL_E)
        self.play(FadeIn(item3))
        self.wait(3)
        self.play(FadeOut(item3))




# class Final(Scene):
#     scenes = [
#         # TitleScreen,
#         NumberSortingScene,
#         StringSortingScene,
#         CardSortingScene,
#     ]
#
#     def construct(self):
#         for sub_scene in self.scenes:
#             self.attach(sub_scene)
#
#     def attach(self, sub_scene):
#         mobjects = filter(lambda mo: mo != title, self.mobjects)
#         fade_out = list(map(lambda mo: FadeOut(mo), mobjects))
#         if fade_out:
#             self.play(*fade_out)
#             self.remove(*mobjects)
#             self.wait()
#         s = sub_scene()
#         s.construct()
