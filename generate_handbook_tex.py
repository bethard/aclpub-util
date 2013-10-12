#!/usr/bin/env python
import codecs
import sys

import db
import settings

book_begin = r"""\documentclass[twoside,makeidx]{book}

%%%%%%%%%%%%%%%%%%%%
% WARNING: This file was generated automatically. It is likely that
% you will eventually have to modify it by hand, e.g. to add abstracts
% for invited speakers or other papers that were not in the ACLPUB db
% file. However, if you re-generate this file, you will overwrite any
% manual changes you have made. So do not start making manual edits
% until you are certain that everything has been generated correctly.
%%%%%%%%%%%%%%%%%%%%

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

schedule_parallel_session_format = r"""\scheduleparallelsession{{{start}}}{{{end}}}{{{items}}}
""".format

schedule_parallel_session_item_format = r"""\scheduleparallelsessionitem{{{title}}}{{{location}}}
""".format

session_abstracts_format = r"""\sessionabstracts{{{title}}}{{{location}}}{{{chair}}}{{
{abstracts}}}
""".format

session_abstract_format = r"""\sessionabstract{{{day}}}{{{start}}}{{{end}}}{{{location}}}{{{title}}}{{{authors}}}{{{abstract}}}
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
            day_short_name = settings.day_short_names[day.title]
            session_locations = settings.day_session_locations[day.title]
            session_chairs = settings.day_session_chairs[day.title]

            # write day header
            write(day_heading_format(title=day.title))

            # write schedule for the day
            schedule_items = []
            for slot in day.slots:
                # non-parallel sessions
                if len(slot.sessions) == 1:
                    for session in slot.sessions:
                        schedule_items.append(schedule_session_format(
                            start=slot.start,
                            end=slot.end,
                            title=session.title,
                            location=session_locations[session.title]))
                # parallel sessions
                else:
                    schedule_items.append(schedule_parallel_session_format(
                        start=slot.start,
                        end=slot.end,
                        items=''.join(
                            schedule_parallel_session_item_format(
                                title=session.title,
                                location=session_locations[session.title])
                            for session in slot.sessions)))
            write(schedule_format(items=''.join(schedule_items)))

            # write abstracts for the day
            for slot in day.slots:
                for session in slot.sessions:
                    if session.papers:
                        session_location = session_locations[session.title]
                        session_chair = session_chairs[session.title]
                        abstract_items = []
                        for (i, paper) in enumerate(session.papers):
                            if i != 0:
                                abstract_items.append(session_abstract_separator)
                            abstract_items.append(session_abstract_format(
                                day=day_short_name,
                                start=paper.start,
                                end=paper.end,
                                location=session_location,
                                title=paper.title,
                                authors=', '.join(paper.authors),
                                abstract=paper.abstract.strip().replace(r'\\', ' ').replace('\n', ' ')))
                        write(session_abstracts_format(
                            title=session.title,
                            location=session_location,
                            chair=session_chair,
                            abstracts=''.join(abstract_items)))
        write(book_end)
