from manim import *

from ep2.scenes.description import Coin
from ep2.scenes.utils import CyrTex
from ep2.scripted_debugger import ScriptedInspector
from ep2.coin_change import min_coin_change


class MyVariable(VMobject):
    def __init__(self, var, label, var_type=DecimalNumber, num_decimal_places=2, **kwargs):
        self.label = MathTex(label) if isinstance(label, str) else label
        equals = MathTex("=").next_to(self.label, RIGHT)
        self.label.add(equals)

        self.tracker = ValueTracker(var)

        if var_type == DecimalNumber:
            self.value = DecimalNumber(
                self.tracker.get_value(), num_decimal_places=num_decimal_places
            )
        elif var_type == Integer:
            self.value = Integer(self.tracker.get_value())

        self.value.add_updater(lambda v: v.set_value(self.tracker.get_value())).next_to(
            self.label, RIGHT, buff=SMALL_BUFF
        )

        VMobject.__init__(self, **kwargs)
        self.add(self.label, self.value)


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
        self.items = items
        self.cells = []
        self.label = CyrTex(r"\texttt{" + name + "}").scale(0.50)
        self.add(self.label)
        prev = None
        for item in items:
            mo_item = Cell(item_constructor(str(item))).scale(0.50)
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

    def show_pointer1(self, name, idx, f=lambda x: x):
        self.pointer1 = Line(ORIGIN, UP * 0.5).scale(0.50)
        self.pointer1.add_tip(tip_length=0.1)
        self.pointer1.next_to(self.cells[idx], DOWN, buff=SMALL_BUFF)
        self.var1 = MyVariable(idx, CyrTex(r"$\texttt{" + name + "}$"), var_type=Integer).scale(0.40)
        self.add(self.var1, self.pointer1)
        self.var1.add_updater(lambda mob: mob.next_to(self.pointer1, RIGHT, aligned_edge=LEFT + DOWN, buff=SMALL_BUFF))
        return self.move1_to_idx(idx, f)

    def show_pointer2(self, name, idx, f=lambda x: x):
        self.pointer2 = Line(ORIGIN, DOWN * 0.5).scale(0.50)
        self.pointer2.add_tip(tip_length=0.1)
        self.pointer2.next_to(self.cells[idx], UP, buff=SMALL_BUFF)
        self.var2 = MyVariable(f(idx), CyrTex(r"$\texttt{" + name + "}$"), var_type=Integer).scale(0.40)
        self.add(self.var2, self.pointer2)
        self.var2.add_updater(lambda mob: mob.next_to(self.pointer2, RIGHT, aligned_edge=LEFT + UP, buff=SMALL_BUFF))
        return self.move2_to_idx(idx, f)

    def move1_to_idx(self, idx, f=lambda x: x):
        if idx < 0:
            return self.var1.tracker.set_value, f(idx), \
                   self.pointer1.next_to, self.label, DOWN, {"buff": SMALL_BUFF}, \
                   self.pointer1.set_color, RED, \
                   self.var1.set_color, RED
        else:
            return self.var1.tracker.set_value, f(idx), \
                   self.pointer1.next_to, self.cells[idx], DOWN, {"buff": SMALL_BUFF}, \
                   self.pointer1.set_color, WHITE, \
                   self.var1.set_color, WHITE

    def move2_to_idx(self, idx, f=lambda x: x):
        if idx < 0:
            return self.var2.tracker.set_value, f(idx), \
                   self.pointer2.next_to, self.label, UP, {"buff": SMALL_BUFF}, \
                   self.pointer2.set_color, RED, \
                   self.var2.set_color, RED
        else:
            return self.var2.tracker.set_value, f(idx), \
                   self.pointer2.next_to, self.cells[idx], UP, {"buff": SMALL_BUFF}, \
                   self.pointer2.set_color, WHITE, \
                   self.var2.set_color, WHITE


class CoinListRepr(ListRepresentation):
    def __init__(self, name, items, *vmobjects, **kwargs):
        super().__init__(name, items, *vmobjects, item_constructor=lambda text: Coin(text).scale(0.60), **kwargs)


class NumberListRepr(ListRepresentation):
    def __init__(self, name, items, *vmobjects, **kwargs):
        super().__init__(name, items, *vmobjects, item_constructor=lambda text: Text(text), **kwargs)


class MinChangeStepByStep(Scene):
    CODE = """
        01 def min_coin_change(coins, amount):
        02     num_min_coins = [math.inf] * (amount + 1)
        03     min_coin = [None] * (amount + 1)
        04 
        05     num_min_coins[0] = 0
        06     min_coin[0] = None
        07 
        08     for sub_amount in range(1, amount + 1):
        09         sub_num_min_coins = math.inf
        10         sub_min_coin = None
        11         for coin in coins:
        12             prev_amount = sub_amount - coin
        13             if prev_amount >= 0:
        14                 candidate_num_min_coins = num_min_coins[prev_amount] + 1
        15                 if candidate_num_min_coins < sub_num_min_coins:
        16                     sub_num_min_coins = candidate_num_min_coins
        17                     sub_min_coin = coin
        18 
        19         num_min_coins[sub_amount] = sub_num_min_coins
        20         min_coin[sub_amount] = sub_min_coin
        21 
        22     return min_coin, num_min_coins[amount]
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
        amount_loop_begin = 20
        coin_loop_begin = 24

        initial = trace.current()
        last = trace.step_to_rel_line(21)
        print(last)

        full_width = config.frame_width
        full_width_with_buff = full_width - 2 * DEFAULT_MOBJECT_TO_EDGE_BUFFER

        self.add_code(full_width_with_buff)
        self.add_mask()
        line_height = self.highlight_bar(self.code_text, full_width_with_buff)
        self.code_text.to_edge(UP)

        d_coins = CoinListRepr("coins", last.local_vars['coins'])
        d_coins.show_pointer2("coin", last.local_vars['coins'].index(last.local_vars['coin']),
                              f=lambda i: last.local_vars['coins'][i])
        d_amount = Variable(last.local_vars['amount'], CyrTex(r"$\texttt{amount}$"), var_type=Integer).scale(0.75)
        d_sub_min_coin = Variable(last.local_vars['sub_min_coin'], CyrTex(r"$\texttt{d_sub_min_coin}$"),
                                  var_type=Integer).scale(0.75)
        d_sub_num_min_coins = Variable(last.local_vars['sub_num_min_coins'], CyrTex(r"$\texttt{sub_num_min_coins}$"),
                                       var_type=Integer).scale(0.75)
        d_candidate_num_min_coins = Variable(last.local_vars['candidate_num_min_coins'],
                                             CyrTex(r"$\texttt{candidate_num_min_coins}$"), var_type=Integer).scale(
            0.75)

        d_num_min_coins = ListRepresentation("num_min_coins", last.local_vars['num_min_coins'])
        d_min_coin = CoinListRepr("min_coin", last.local_vars['min_coin'])

        debugger_center = ORIGIN + DOWN * 1.2
        edge = X_AXIS * (full_width / 2 - DEFAULT_MOBJECT_TO_EDGE_BUFFER)

        d_num_min_coins.move_to(debugger_center - edge + DOWN * 0.2, aligned_edge=LEFT)
        d_coins.move_to(debugger_center + edge - RIGHT, aligned_edge=RIGHT)
        d_min_coin.next_to(d_num_min_coins, DOWN * 2, aligned_edge=RIGHT, coor_mask=np.array((1, 1.2, 1)))
        d_num_min_coins.show_pointer1("sub_amount", last.local_vars['sub_amount'])
        d_num_min_coins.show_pointer2("prev_amount", last.local_vars['prev_amount'])
        d_min_coin.show_pointer2("sub_amount", last.local_vars['sub_amount'])

        d_amount.next_to(d_coins, DOWN, aligned_edge=RIGHT)
        d_amount.to_edge(RIGHT)
        d_sub_min_coin.next_to(d_amount, DOWN)
        d_sub_min_coin.to_edge(RIGHT)
        d_sub_num_min_coins.next_to(d_sub_min_coin, DOWN)
        d_sub_num_min_coins.to_edge(RIGHT)
        d_candidate_num_min_coins.next_to(d_sub_num_min_coins, DOWN)
        d_candidate_num_min_coins.to_edge(RIGHT)
        self.add(d_coins, d_amount, d_num_min_coins, d_min_coin,
                 d_sub_num_min_coins, d_candidate_num_min_coins, d_sub_min_coin)

        self.play(*d_num_min_coins.move1_to_idx(-1), *d_num_min_coins.move2_to_idx(-1),)
        self.play(*d_num_min_coins.move1_to_idx(3), *d_num_min_coins.move2_to_idx(3),)
        self.wait(10)

    def add_code(self, full_width_with_buff):
        self.code_text = CairoText(self.CODE, font='Hack', size=1).set_width(full_width_with_buff)
        self.add(self.code_text)

    def line_start(self, line_no):
        print("{:02d}".format(line_no))
        self.find_line(self.code_text, "{:02d}".format(line_no)).get_center() * Y_AXIS

    def highlight_bar(self, code_text, full_width_with_buff):
        line_height = code_text.get_height() / (self.CODE.count('\n') - 1)
        self.highlight = Rectangle(width=full_width_with_buff + DEFAULT_MOBJECT_TO_EDGE_BUFFER,
                                   height=line_height * 1.1,
                                   fill_color="#FEFF2A",
                                   fill_opacity=0.2,
                                   stroke_color="#FEFF2A",
                                   stroke_opacity=0.4)
        self.add(self.highlight)
        return line_height

    def add_mask(self):
        self.mask = SVGMobject("mask.svg", fill_color="#333333", fill_opacity=0.95, stroke_width=0)
        full_width = config.frame_width
        half_height = config.frame_height / 2
        self.mask.set_height(height=half_height, stretch=True)
        self.mask.set_width(full_width, stretch=True)
        self.mask.to_edge(DOWN, buff=0)
        self.add(self.mask)

    def find_line(self, code, line_no):
        for start, end in code.find_indexes(line_no, code.original_text):
            return code.chars[start]
        return None


class TestScene(Scene):
    def construct(self):
        p = NumberListRepr(r"num_min_coins", [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.add(p)
        self.play(*p.show_pointer1("coin", 0))
        self.wait(1)
        self.play(*p.move1_to_idx(1))
        # self.play(*p.move2_to_idx(2))
        self.wait(10)

