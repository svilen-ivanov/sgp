from manim import *

cyr_tex = TexTemplate(preamble=r"""
\usepackage[english,bulgarian,main=english]{babel}
\usepackage{ucs}
\usepackage[utf8x]{inputenc}
\usepackage[T1]{fontenc}
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

class Logo(Scene):
    def construct(self):
        logo = Circle(color=TEAL_E)
        text = Tex(r"\foreignlanguage{bulgarian}{СГП}", tex_template=cyr_tex, color=TEAL_E).scale(1.5)
        self.add(logo)
        self.add(text)
        self.wait(10)
