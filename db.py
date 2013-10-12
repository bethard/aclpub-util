import codecs
import itertools
import os
import re

class Day(object):
    def __init__(self, title):
        self.title = title
        self.slots = []

class TimeSlot(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.sessions = []

class Session(object):
    def __init__(self, start, end, title):
        self.start = start
        self.end = end
        self.title = title
        self.papers = []

class Paper(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.authors = []
        self.start = None
        self.end = None
        self.abstract = None

def to_latex(text):
    replacements = [
        ('\\', r'\\'),
        (u'\u2018', "`"),
        (u'\u2019', "'"),
        (u'\u201c', "``"),
        (u'\u201d', "''"),
        (u'\u2013', "-"),
        (u'\u2014', "-"),
        (u'\u223c', "~"),
        (u'\ufb01', "fi"),
        (u'\ufb03', "ffi"),
        (u'\u2030', r"\textperthousand"),
        (u'\xf3', r"\'{o}"),
        (u'&', r'\&'),
        (u'_', r'\_'),
        (u'$', r'\$'),
        (u'^', r'\^'),
        (u'%', r'\%'),
        ('\x18', ''),
    ]
    for (old, new) in replacements:
        text = text.replace(old, new)
    return text


def load(book_dir):
    dash_regex = re.compile(u'[-\u2013\u2014]')
    author_regex = re.compile(r'\nAuthor{[^}]*}{Firstname}#=%=#(.*)\nAuthor{[^}]*}{Lastname}#=%=#(.*)')
    abstract_regex = re.compile('^Abstract#==#(.*?)^Author{', re.MULTILINE | re.DOTALL)

    def grouper(line):
        if line.isspace():
            return ''
        elif line.startswith('X:'):
            return 'X'
        else:
            return 'P'

    days = []
    with codecs.open(os.path.join(book_dir, 'db'), 'r', 'utf8') as db_file:
        for group_type, lines in itertools.groupby(db_file, grouper):
            if group_type == 'X':
                for line in lines:
                    [x, mark, title] = line.split(' ', 2)
                    title = title.strip()
                    if mark == '*':
                        days.append(Day(title))
                    elif mark == '+' or mark == '=':
                        [time, title] = title.split(' ', 1)
                        [start, end] = dash_regex.split(time.strip('()'))
                        if ((not days[-1].slots)
                            or days[-1].slots[-1].start != start
                            or days[-1].slots[-1].end != end):
                            days[-1].slots.append(TimeSlot(start, end))
                        days[-1].slots[-1].sessions.append(Session(start, end, title))
            elif group_type == 'P':
                paper = Paper()
                for line in lines:
                    [key, value] = line.split(' ', 1)
                    value = value.strip()
                    if key == 'P:':
                        paper.id = value
                    elif key == 'T:':
                        paper.title = value
                    elif key == 'H:':
                        [start, end] = dash_regex.split(value)
                        paper.start = start
                        paper.end = end
                    elif key == "A:":
                        [last, first] = value.split(",")
                        paper.authors.append("{0} {1}".format(first, last))
                    elif key in ['M:', 'L:', 'F:']:
                        pass
                    else:
                        raise Exception("Unsupported key: {0}".format(line))
                last_session = days[-1].slots[-1].sessions[-1]
                if paper.start is None:
                    paper.start = last_session.start
                if paper.end is None:
                    paper.end = last_session.end
                last_session.papers.append(paper)

                # add paper authors and abstract from metadata
                paper_metadata_subpath = 'final/{0}/{0}_metadata.txt'.format(paper.id)
                paper_metadata_path = os.path.join(book_dir, paper_metadata_subpath)
                with codecs.open(paper_metadata_path, 'r', 'utf8') as paper_metadata_file:
                    paper_metadata = paper_metadata_file.read()
                    # NOTE: use this if you want unicode authors
                    #for match in author_regex.finditer(paper_metadata):
                    #    paper.authors.append(u'{0} {1}'.format(match.group(1), match.group(2)))
                    #if not paper.authors:
                    #    raise Exception("No authors found in " + paper_metadata)
                    [abstract] = abstract_regex.findall(paper_metadata)
                    paper.abstract = to_latex(abstract)
    return days
