from manim import *

cyr_tex = TexTemplate(preamble=r"""
\usepackage[T2A,T1]{fontenc}
\usepackage{ucs}
\usepackage[utf8x]{inputenc}
\usepackage[main=english,bulgarian]{babel}

\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{pbox}
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
\usepackage{underscore}
\DisableLigatures{encoding = *, family = * }
\linespread{1}
""")


class CyrTex(Tex):
    def __init__(self, *tex_strings, **kwargs):
        kwargs['tex_template'] = cyr_tex
        super().__init__(*tex_strings, **kwargs)
