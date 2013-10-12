#!/usr/bin/env python
import codecs
import os
import sys

import db
import formatting
import settings

if __name__ == "__main__":
    [book_dir, workshop_path] = sys.argv[1:]

    # get workshop info
    workshop_abbrev = os.path.basename(book_dir)
    title = settings.workshop_titles[workshop_abbrev]
    location = settings.workshop_locations[workshop_abbrev]

    # read db file
    days = db.load(book_dir)

    # write out tex
    with open(workshop_path, 'w') as workshop_file:
        write = workshop_file.write
        for day in days:
            day_short_name = settings.day_short_names[day.title]

            # write abstracts
            abstract_items = []
            for slot in day.slots:
                for session in slot.sessions:
                    for paper in session.papers:
                        if abstract_items:
                            abstract_items.append(formatting.session_abstract_separator)
                        abstract_items.append(formatting.session_abstract_format(
                            day=day_short_name,
                            start=paper.start,
                            end=paper.end,
                            location=location,
                            title=paper.title,
                            authors=', '.join(paper.authors),
                            abstract=paper.abstract.strip().replace(r'\\', ' ').replace('\n', ' ')))
            write(formatting.session_abstracts_format(
                title=title,
                location=location,
                chair='',
                abstracts=''.join(abstract_items)))
