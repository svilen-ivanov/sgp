import math
from collections import Iterable

from manim import *

from ep2.coin_change import min_coin_change
from ep2.scenes.description import Coin
from ep2.scenes.utils import CyrTex
from ep2.scripted_debugger import ScriptedInspector


class Cell(Group):
    def align_points_with_larger(self, larger_mobject):
        pass

    def __init__(self, value, width=1, height=1, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.rect = Rectangle(width=width, height=height, **kwargs)
        self.add(self.rect)
        self.add(value)


class ListRepresentation(Group):
    def align_points_with_larger(self, larger_mobject):
        pass

    def __init__(self, name, items, item_constructor=Text, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.item_constructor = item_constructor
        self.items = items
        self.cells = []
        self.label = CyrTex(r"\texttt{" + name + "}").scale(0.50)
        self.add(self.label)
        prev = None
        for item in items:
            if item is None:
                value = VGroup()
            else:
                value = item_constructor(str(item))
            mo_item = Cell(value).scale(0.50)
            self.add(mo_item)
            self.cells.append(mo_item)
            if prev:
                mo_item.next_to(prev, RIGHT, buff=0)
            else:
                mo_item.next_to(self.label, RIGHT, buff=SMALL_BUFF)
            prev = mo_item
        self.center()
        self.pointer1 = None
        self.var1 = None
        self.pointer2 = None
        self.var2 = None
        self.scale_factor = 1

    def scale(self, scale_factor, **kwargs):
        self.scale_factor *= scale_factor
        return super().scale(scale_factor, **kwargs)

    def set_value(self, new_value):
        animations = []
        for old_v, new_v, i in zip(self.items, new_value, range(0, len(new_value))):
            print(f"old_v={old_v}, new_v={new_v}")
            if old_v != new_v:
                if new_v is None:
                    new_mo = VGroup()
                else:
                    new_mo = self.item_constructor(str(new_v))
                new_cell = Cell(new_mo).scale(self.scale_factor * 0.50)
                new_cell.move_to(self.cells[i])
                animations.extend([FadeInFrom(new_cell, UP), FadeOutAndShift(self.cells[i], DOWN)])
                self.cells[i] = new_cell
                self.items[i] = new_v
        return animations

    def label_center(self):
        return self.label.get_center()

    #def move_by_label(self, new_center):
    #    rel_center = self.get_center() - self.label.get_center()
    #    self.move_to(new_center + rel_center)

    def show_pointer1(self, name, idx, f=lambda x: x):
        animations = []
        if self.pointer1 is None:
            self.pointer1 = Line(ORIGIN, UP * 0.5).scale(self.scale_factor * 0.50)
            self.pointer1.add_tip(tip_length=0.1)
            self.pointer1.next_to(self.cells[idx], DOWN, buff=SMALL_BUFF)
            self.var1 = ProgVariable(name, idx).scale(self.scale_factor * 0.40)
            self.var1.add_updater(
                lambda mob: mob.next_to(self.pointer1, RIGHT, aligned_edge=LEFT + DOWN, buff=SMALL_BUFF))
            animations.extend([FadeIn(self.var1), FadeIn(self.pointer1)])
        return animations + self.move1_to_idx(idx, f)

    def show_pointer2(self, name, idx, f=lambda x: x):
        animations = []
        if self.pointer2 is None:
            self.pointer2 = Line(ORIGIN, DOWN * 0.5).scale(self.scale_factor * 0.50)
            self.pointer2.add_tip(tip_length=0.1)
            self.pointer2.next_to(self.cells[idx], UP, buff=SMALL_BUFF)
            self.var2 = ProgVariable(name, idx).scale(self.scale_factor * 0.40)
            self.var2.add_updater(
                lambda mob: mob.next_to(self.pointer2, RIGHT, aligned_edge=LEFT + UP, buff=SMALL_BUFF))
            animations.extend([FadeIn(self.var2), FadeIn(self.pointer2)])
        return animations + self.move2_to_idx(idx, f)

    def move1_to_idx(self, idx, f=lambda x: x):
        if idx < 0:
            return [*self.var1.set_value(f(idx)),
                    self.pointer1.move_to, self.cells[0].get_critical_point(DL) - X_AXIS * self.cells[0].get_width() / 2 - Y_AXIS * SMALL_BUFF, {"aligned_edge": UP},
                    self.pointer1.set_color, RED,
                    self.var1.set_color, RED
                    ]
        else:
            return [*self.var1.set_value(f(idx)),
                    self.pointer1.next_to, self.cells[idx], DOWN, {"buff": SMALL_BUFF},
                    self.pointer1.set_color, WHITE,
                    self.var1.set_color, WHITE]

    def move2_to_idx(self, idx, f=lambda x: x):
        if idx < 0:
            return [*self.var2.set_value(f(idx)),
                    self.pointer2.move_to, self.cells[0].get_critical_point(UL) - X_AXIS * self.cells[0].get_width() / 2 + Y_AXIS * SMALL_BUFF, {"aligned_edge": DOWN},
                    self.pointer2.set_color, RED,
                    self.var2.set_color, RED]
        else:
            return [*self.var2.set_value(f(idx)),
                    self.pointer2.next_to, self.cells[idx], UP, {"buff": SMALL_BUFF},
                    self.pointer2.set_color, WHITE,
                    self.var2.set_color, WHITE]


class CoinListRepr(ListRepresentation):
    def __init__(self, name, items, *vmobjects, **kwargs):
        super().__init__(name, items, *vmobjects, item_constructor=lambda text: Coin(text).scale(0.60), **kwargs)

    def __str__(self):
        return f"{self.name}"


class NumberListRepr(ListRepresentation):
    def __init__(self, name, items, *vmobjects, **kwargs):
        super().__init__(name, items, *vmobjects, item_constructor=lambda text: Text(text), **kwargs)

    def __str__(self):
        return f"{self.name}"


class MinChangeStepByStep(Scene):
    CODE = """
        01 def min_coin_change(coins, amount):
        02     num_min_coins = [math.inf] * (amount + 1)
        03     min_coin = [None] * (amount + 1)
        04     num_min_coins[0] = 0
        05 
        06     for sub_amount in range(1, amount + 1):
        07         sub_num_min_coins = math.inf
        08         sub_min_coin = None
        09         for coin in coins:
        10             prev_amount = sub_amount - coin
        11             if prev_amount >= 0:
        12                 candidate_num_min_coins = num_min_coins[prev_amount] + 1
        13                 if candidate_num_min_coins < sub_num_min_coins:
        14                     sub_num_min_coins = candidate_num_min_coins
        15                     sub_min_coin = coin
        16 
        17         num_min_coins[sub_amount] = sub_num_min_coins
        18         min_coin[sub_amount] = sub_min_coin
        19 
        20     return min_coin, num_min_coins[amount]
    """

    # coins = [1, 2, 5]
    # amount = 9
    # num_min_coins = [0, 1, 1, 2, 2, 1, 2, 2, 3, 3]
    # min_coin = [None, 1, 2, 1, 2, 5, 1, 2, 1, 2]
    # sub_amount = 9
    # sub_num_min_coins = 3
    # sub_min_coin = 2
    # coin = 5
    # prev_amount = 4
    # candidate_num_min_coins = 3

    def construct(self):
        coins = [1, 2, 5]
        amount = 9

        inspector = ScriptedInspector(func_to_inspect=min_coin_change, args=(coins, amount))
        trace = inspector.collect_trace()
        # amount_loop_begin = 20
        # coin_loop_begin = 24

        full_width = config.frame_width
        full_width_with_buff = full_width - 2 * DEFAULT_MOBJECT_TO_EDGE_BUFFER

        self.add_code(full_width_with_buff)
        self.add_mask()

        self.d_amount = None
        self.d_coins = None
        self.d_sub_min_coin = None
        self.d_sub_num_min_coins = None
        self.d_min_coin = None
        self.d_num_min_coins = None
        self.d_candidate_num_min_coins = None

        prev_step = None
        step = None
        while not trace.at_the_end():
            prev_step = step
            step = trace.step()
            print(step)

            if prev_step is not None:
                self.highlight_line(prev_step.rel_line + 1)

            local_vars = step.local_vars
            animations = []

            if 'coins' in local_vars:
                new_val = local_vars['coins']
                if self.d_coins is not None:
                    animations.extend(self.d_coins.set_value(new_val))
                else:
                    self.d_coins = CoinListRepr("coins", new_val)
                    self.move_by_label(self.d_coins, [1.5, -2, 0])
                    animations.append(FadeIn(self.d_coins))

                if 'coin' in local_vars:
                    anim = self.d_coins.show_pointer2("coin", local_vars['coins'].index(local_vars['coin']),
                                                      f=lambda i: local_vars['coins'][i])
                    animations.extend(anim)

            if 'num_min_coins' in local_vars:
                new_val = self.fix_var(local_vars['num_min_coins'])
                if self.d_num_min_coins is not None:
                    animations.extend(self.d_num_min_coins.set_value(new_val))
                else:
                    self.d_num_min_coins = NumberListRepr("num_min_coins", new_val)
                    self.move_by_label(self.d_num_min_coins, [-5, -2, 0])
                    animations.append(FadeIn(self.d_num_min_coins))

                if 'sub_amount' in local_vars:
                    anim = self.d_num_min_coins.show_pointer1("sub_amount", self.fix_var(local_vars['sub_amount']))
                    animations.extend(anim)
                if 'prev_amount' in local_vars:
                    anim = self.d_num_min_coins.show_pointer2("prev_amount", self.fix_var(local_vars['prev_amount']))
                    animations.extend(anim)

            if 'min_coin' in local_vars:
                new_val = local_vars['min_coin']
                if self.d_min_coin is not None:
                    animations.extend(self.d_min_coin.set_value(new_val))
                else:
                    self.d_min_coin = CoinListRepr("min_coin", new_val)
                    self.move_by_label(self.d_min_coin, [-5, -3.5, 0])
                    # self.d_min_coin.move_by_label([-5.45372370e+00, -2.88000000e+00, 0])
                    animations.append(FadeIn(self.d_min_coin))

                if 'sub_amount' in local_vars:
                    anim = self.d_min_coin.show_pointer2("sub_amount", self.fix_var(local_vars['sub_amount']))
                    animations.extend(anim)


            self.d_amount = self.add_var_update(animations, self.d_amount, local_vars, 'amount',
                                                [6, -3.5 + 3 * MED_LARGE_BUFF, 0.])
            self.d_sub_min_coin = self.add_var_update(animations, self.d_sub_min_coin, local_vars, 'sub_min_coin',
                                                      [6,  -3.5 + 2 * MED_LARGE_BUFF, 0.], use_coin=True)
            self.d_sub_num_min_coins = self.add_var_update(animations, self.d_sub_num_min_coins, local_vars,
                                                           'sub_num_min_coins', [6, -3.5 + 1 * MED_LARGE_BUFF, 0.])
            self.d_candidate_num_min_coins = self.add_var_update(animations, self.d_candidate_num_min_coins, local_vars,
                                                                 'candidate_num_min_coins',
                                                                 [6,  -3.5, 0.])
            if len(animations) > 0:
                self.play(*animations)
            self.wait(1)
        self.wait(10)

    def add_var_update(self, animations, mobject, local_vars, var_name, coord, use_coin=False):
        if var_name in local_vars:
            new_value = self.fix_var(local_vars[var_name])
            if mobject is not None:
                animations.extend(mobject.set_value(new_value))
            else:
                if use_coin:
                    def coin_constructor(x):
                        if x == '\varnothing':
                            return CyrTex(r"${" + str(x) + "}$")
                        else:
                            return Coin(x).scale(0.45)

                    mobject = ProgVariable(var_name, new_value, constructor=coin_constructor).scale(0.75)
                else:
                    mobject = ProgVariable(var_name, new_value).scale(0.75)
                self.move_by_label(mobject, coord)
                animations.append(FadeIn(mobject))
        return mobject

    def add_code(self, full_width_with_buff):
        self.code_text = CairoText(self.CODE, font='Hack', size=1).set_width(full_width_with_buff).to_edge(UP)
        lines = (self.CODE.count('\n') - 1)
        self.line_no = [None] + [self.find_line(i) for i in range(1, lines + 1)]
        self.top_line_no = 1
        self.current_line_no = self.top_line_no
        self.current_line = self.line_no[self.top_line_no]
        self.add(self.code_text)
        self.highlight_bar(full_width_with_buff, lines)

    def scroll_to_line(self, new_top):
        new_top_line = self.line_no[new_top]
        current_top_line = self.line_no[self.top_line_no]
        res = [(current_top_line.get_center() - new_top_line.get_center()) * Y_AXIS]
        self.top_line_no = new_top
        return res

    def highlight_bar(self, full_width_with_buff, lines):
        line_height = self.code_text.get_height() / lines
        self.highlight = Rectangle(width=full_width_with_buff + DEFAULT_MOBJECT_TO_EDGE_BUFFER,
                                   height=line_height * 1.1,
                                   fill_color="#FEFF2A",
                                   fill_opacity=0.2,
                                   stroke_color="#FEFF2A",
                                   stroke_opacity=0.4)

        self.highlight.move_to(self.current_line.get_center() * Y_AXIS)
        self.code_text.add(self.highlight)

    def add_mask(self):
        self.mask = SVGMobject("mask.svg", fill_color="#333333", fill_opacity=0.95, stroke_width=0)
        full_width = config.frame_width
        half_height = config.frame_height / 2 - 0.7
        self.mask.set_height(height=half_height, stretch=True)
        self.mask.set_width(full_width, stretch=True)
        self.mask.to_edge(DOWN, buff=0)
        self.add(self.mask)

    def find_line(self, line_no):
        for start, end in self.code_text.find_indexes("{:02d}".format(line_no), self.code_text.original_text):
            return self.code_text.chars[start]
        return None

    def highlight_line(self, line_no):
        target_line = self.line_no[line_no]
        if self.top_line_no <= line_no < self.top_line_no + 10:
            self.play(self.highlight.shift, (target_line.get_center() - self.current_line.get_center()) * Y_AXIS)
        else:
            if line_no - self.current_line_no > 0:
                new_top = line_no - 10
            else:
                new_top = line_no
            shift = self.scroll_to_line(new_top)
            self.play(
                self.code_text.shift, shift,
                self.highlight.shift, (target_line.get_center() - self.current_line.get_center() + shift) * Y_AXIS
            )
        self.current_line = target_line
        self.current_line_no = line_no

    def move_by_label(self, variable, label_center):
        rel_center = variable.get_center() - variable.label.get_critical_point(RIGHT)
        variable.move_to(label_center + rel_center)

    def fix_var(self, var):
        if var == math.inf:
            return "∞"
        elif var is None:
            return r"\varnothing"
        elif isinstance(var, Iterable):
            return list(map(self.fix_var, var))
        else:
            return var


class ProgVariable(Group):
    def __init__(self, name, initial_value, constructor=lambda x: CyrTex(r"${" + str(x) + "}$"), *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.label = CyrTex(r"$\texttt{" + name + "} =$")
        self.value_mob = None
        self.old_value = None
        self.set_value(initial_value)
        self.add(self.label)
        self.center()
        self.scale_factor = 1
        self.constructor = constructor

    def scale(self, scale_factor, **kwargs):
        self.scale_factor *= scale_factor
        return super().scale(scale_factor, **kwargs)

    def set_value(self, new_value):
        old_value_mob = self.value_mob
        if old_value_mob is not None:
            if self.old_value != new_value:
                self.value_mob = self.constructor(new_value)
                self.value_mob.scale(self.scale_factor)
                self.value_mob.next_to(self.label, buff=self.scale_factor*DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)
                self.remove(old_value_mob)
                self.add(self.value_mob)
                self.old_value = new_value
                return [FadeOutAndShift(old_value_mob, DOWN), FadeInFrom(self.value_mob, UP)]
            else:
                return []
        else:
            self.value_mob = CyrTex(r"${" + str(new_value) + "}$")
            self.value_mob.next_to(self.label)
            self.old_value = new_value
            self.add(self.value_mob)

class TestScene(Scene):
    def construct(self):
        x1 = ProgVariable("a", 0).scale(0.75)
        x2 = ProgVariable("very_long_name", 1234).scale(0.75)
        self.move_by_label(x1, [3, 0, 0])
        self.move_by_label(x2, [3, 1, 0])
        self.add(x1, x2)
        self.wait(10)

    def move_by_label(self, x, new_center):
        rel_center = x.get_center() - x.label.get_critical_point(RIGHT)
        x.move_to(new_center + rel_center)
