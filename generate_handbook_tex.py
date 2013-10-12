#!/usr/bin/env python
import codecs
import sys

import db
import formatting
import settings

if __name__ == "__main__":
    [book_dir, handbook_path] = sys.argv[1:]

    # read db file
    days = db.load(book_dir)

    # write out tex
    with open(handbook_path, 'w') as handbook_file:
        write = handbook_file.write
        write(formatting.book_begin)
        for day in days:
            day_short_name = settings.day_short_names[day.title]
            session_locations = settings.day_session_locations[day.title]
            session_chairs = settings.day_session_chairs[day.title]

            # write day header
            write(formatting.day_heading_format(title=day.title))

            # write schedule for the day
            schedule_items = []
            for slot in day.slots:
                # non-parallel sessions
                if len(slot.sessions) == 1:
                    for session in slot.sessions:
                        schedule_items.append(formatting.schedule_session_format(
                            start=slot.start,
                            end=slot.end,
                            title=session.title,
                            location=session_locations[session.title]))
                # parallel sessions
                else:
                    schedule_items.append(formatting.schedule_parallel_session_format(
                        start=slot.start,
                        end=slot.end,
                        items=''.join(
                            formatting.schedule_parallel_session_item_format(
                                title=session.title,
                                location=session_locations[session.title])
                            for session in slot.sessions)))
            write(formatting.schedule_format(items=''.join(schedule_items)))

            # write abstracts for the day
            for slot in day.slots:
                for session in slot.sessions:
                    if session.papers:
                        session_location = session_locations[session.title]
                        session_chair = session_chairs[session.title]
                        abstract_items = []
                        for (i, paper) in enumerate(session.papers):
                            if i != 0:
                                abstract_items.append(formatting.session_abstract_separator)
                            abstract_items.append(formatting.session_abstract_format(
                                day=day_short_name,
                                start=paper.start,
                                end=paper.end,
                                location=session_location,
                                title=paper.title,
                                authors=', '.join(paper.authors),
                                abstract=paper.abstract.strip().replace(r'\\', ' ').replace('\n', ' ')))
                        write(formatting.session_abstracts_format(
                            title=session.title,
                            location=session_location,
                            chair=session_chair,
                            abstracts=''.join(abstract_items)))
        write(formatting.book_end)
