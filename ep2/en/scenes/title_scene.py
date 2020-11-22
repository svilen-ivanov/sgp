from manim import *

from ep2.scenes.utils import CyrTex


class TitleScreen(Scene):
    def construct(self):
        title = CyrTex(r'Min Coin Change', color="#83d126").scale(3)
        self.play(Write(title))

        #sub_title = CyrTex(r'\foreignlanguage{bulgarian}{Ресто с най-малък брой монети}').scale(1.5)
        #self.play(title.shift, UP * sub_title.get_height())

        #sub_title.next_to(title, DOWN, buff=SMALL_BUFF)
        #self.play(Write(sub_title))
        self.wait()

        channel_name = CyrTex(r'\foreignlanguage{english}{\textbf{Svilen Talks About Programming}}', color=TEAL_E)
        episode_num = CyrTex(r'\foreignlanguage{english}{Episode №2}', color=TEAL_E).scale(0.8)
        episode_num.next_to(channel_name, DOWN, buff=SMALL_BUFF)
        v_group = VGroup(channel_name, episode_num)
        v_group.to_edge(DOWN)
        self.play(Write(v_group))

        self.wait(10)
