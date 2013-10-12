#!/usr/bin/env python
import db
import codecs
import sys

book_begin = r"""\documentclass[twoside,makeidx]{book}

\input{preamble} 

\begin{document}

\setcounter{tocdepth}{2}
\tableofcontents
\mainmatter

"""

day_heading_format = r"""\dayheading{{{title}}}
""".format

schedule_format = r"""\schedule{{
{items}}}
""".format

schedule_session_format = r"""\schedulesession{{{start}}}{{{end}}}{{{title}}}{{{location}}}
""".format

schedule_parallel_session_format = r"""\scheduleparallelsession{{{start}}}{{{end}}}{{{location}}}{{{items}}}
""".format

schedule_parallel_session_item_format = r"""\scheduleparallelsessionitem{{{title}}}
""".format

session_abstracts_format = r"""\sessionabstracts{{{title}}}{{
{abstracts}}}
""".format

session_abstract_format = r"""\sessionabstract{{{start}}}{{{end}}}{{{title}}}{{{authors}}}{{{abstract}}}
""".format

session_abstract_separator = r"""\sessionabstractsep
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
            # write day header
            write(day_heading_format(title=day.title))

            # write schedule for the day
            schedule_items = []
            for slot in day.slots:
                if len(slot.sessions) == 1:
                    for session in slot.sessions:
                        schedule_items.append(schedule_session_format(
                            start=slot.start,
                            end=slot.end,
                            title=session.title,
                            location='TODO'))
                else:
                    schedule_items.append(schedule_parallel_session_format(
                        start=slot.start,
                        end=slot.end,
                        location='TODO',
                        items=''.join(
                            schedule_parallel_session_item_format(title=session.title)
                            for session in slot.sessions)))
            write(schedule_format(items=''.join(schedule_items)))

            # write abstracts for the day
            for slot in day.slots:
                for session in slot.sessions:
                    if session.papers:
                        abstract_items = []
                        for (i, paper) in enumerate(session.papers):
                            if i != 0:
                                abstract_items.append(session_abstract_separator)
                            abstract_items.append(session_abstract_format(
                                start=paper.start,
                                end=paper.end,
                                title=paper.title,
                                authors=', '.join(paper.authors),
                                abstract=paper.abstract.strip().replace(r'\\', ' ').replace('\n', ' ')))
                        write(session_abstracts_format(
                            title=session.title,
                            abstracts=''.join(abstract_items)))
        write(book_end)
