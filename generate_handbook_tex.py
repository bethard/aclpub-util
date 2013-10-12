#!/usr/bin/env python
import db
import codecs
import sys

book_begin = r"""\documentclass[twoside,makeidx]{book}
\usepackage{pdfpages}
\usepackage{textcomp}
\usepackage[
  paperheight=8.5in, 
  paperwidth=5.5in, 
  inner=.75in,
  outer=.5in,
  bottom=.75in,
  top=.75in,
  twoside]{geometry}
\renewcommand{\normalsize}{\fontsize{8}{9}\selectfont}
\renewcommand{\small}{\fontsize{7}{8}\selectfont}
\renewcommand{\footnotesize}{\fontsize{6}{6}\selectfont}
\renewcommand{\large}{\fontsize{10}{11}\selectfont}
\renewcommand{\Large}{\fontsize{12}{14}\selectfont}
\renewcommand{\huge}{\fontsize{14}{17}\selectfont}

\input{preamble} 
\input{macros}    

\begin{document}

\setcounter{tocdepth}{2}
\tableofcontents
\mainmatter

"""

day_format = r"""\chapter{{{0}}}
"""

day_overview_begin = r"""\section*{Overview}
\begin{tabular}{ l @{} c @{} r l l }
"""

day_overview_slot_format = r"""{0} & -- & {1} & \textbf{{{2}}} \hfill \\
"""

day_overview_subslot_format = r""" & & & \textit{{{0}}} \\
"""

day_overview_slot_end = r'''\\
'''

day_overview_end = r"""\end{tabular}
\clearpage
"""

session_abstracts_begin_format = r"""\section{{{0}}}
\vspace{{-1em}}
"""

paper_format = r"""\par\vspace{{2em}}\noindent%
\begin{{minipage}}{{\linewidth}}%
\begin{{center}}
\textbf{{\normalsize {0}}}\\
\normalsize {1}\\
{{\small {2}--{3}}}\\
\end{{center}}
\end{{minipage}}\\[0.5em]
\nopagebreak%
\noindent%
{{\small {4}}}
"""

session_abstracts_end = r"""\clearpage
"""

book_end = """\end{document}
"""

if __name__ == "__main__":
    [book_dir] = sys.argv[1:]
    handbook_path = "handbook/handbook.tex"

    # read db file
    days = db.load(book_dir)

    # write out tex
    with open(handbook_path, 'w') as handbook_file:
        write = handbook_file.write
        write(book_begin)
        for day in days:
            write(day_format.format(day.title))
            write(day_overview_begin)
            for slot in day.slots:
                if len(slot.sessions) > 1:
                    write(day_overview_slot_format.format(slot.start, slot.end, 'Parallel Sessions'))
                    for session in slot.sessions:
                        write(day_overview_subslot_format.format(session.title))
                else:
                    for session in slot.sessions:
                        write(day_overview_slot_format.format(slot.start, slot.end, session.title))
                write(day_overview_slot_end)
            write(day_overview_end)
            for slot in day.slots:
                for session in slot.sessions:
                    if session.papers:
                        write(session_abstracts_begin_format.format(session.title))
                        for paper in session.papers:
                            authors = ', '.join(paper.authors)
                            abstract = paper.abstract.strip().replace(r'\\', ' ').replace('\n', ' ')
                            write(paper_format.format(paper.title, authors, paper.start, paper.end, abstract))
                        write(session_abstracts_end)
        write(book_end)
