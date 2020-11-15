from manim import *
from ep2.scripted_debugger import ScriptedInspector
from ep2.coin_change import min_coin_change

Y_ONLY = np.array((0, 1, 0))


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

    def construct(self):
        coins = [1, 2, 5]
        amount = 7

        inspector = ScriptedInspector(func_to_inspect=min_coin_change, args=(coins, amount))
        trace = inspector.collect_trace()
        amount_loop_begin = 20
        coin_loop_begin = 24

        full_width = config.frame_width
        full_width_with_buff = full_width - 2 * DEFAULT_MOBJECT_TO_EDGE_BUFFER

        self.add_code(full_width_with_buff)
        self.add_mask()

        line_height = self.highlight_bar(self.code_text, full_width_with_buff)

        self.code_text.to_edge(UP)
        self.wait(4)
        # self.play(self.code_text.move_to, 5 * np.array((0, line_height, 0)))

        # self.highlight.move_to(self.line_start(10), coor_mask=np.array((0, 1, 0)))

        self.wait(10)

    def add_code(self, full_width_with_buff):
        self.code_text = CairoText(self.CODE, font='Hack', size=1).set_width(full_width_with_buff)
        self.add(self.code_text)

    def line_start(self, line_no):
        print("{:02d}".format(line_no))
        self.find_line(self.code_text, "{:02d}".format(line_no)).get_center() * Y_ONLY

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


class Cell(VGroup):
    def align_points_with_larger(self, larger_mobject):
        pass

    def __init__(self, value, width=1, height=1, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.rect = Rectangle(width=width, height=height, **kwargs)
        self.add(self.rect)
        self.add(value)


class ListRepresentation(VGroup):

    def align_points_with_larger(self, larger_mobject):
        pass

    def __init__(self, items, item_constructor=Text, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.items = items
        prev = None
        for item in items:
            mo_item = Cell(item_constructor(str(item)))
            self.add(mo_item)
            if prev:
                mo_item.next_to(prev, RIGHT, buff=0)
            prev = mo_item
        self.center()

    def show_pointer1(self, idx):
        arrow = Arrow(ORIGIN, UP)
        arrow.next_to(self.submobjects[idx], DOWN)
        value = Text(str(idx))
        value.add_updater(lambda m: m.next_to(arrow, RIGHT, aligned_edge=LEFT + DOWN))
        self.add(arrow, value)
        self.pointer1 = arrow
        return arrow

    def move_to_idx(self, idx):
        self.pointer1.next_to(self.submobjects[idx], DOWN)


class TestScene(Scene):
    def construct(self):
        p = ListRepresentation([1, 2, 3], item_constructor=lambda text: Text(text))
        self.add(p)
        self.wait(1)
        p.show_pointer1(0)
        self.wait(1)
        self.play(p.move_to_idx, 1)
        self.play(p.move_to_idx, 2)
        self.wait(10)

