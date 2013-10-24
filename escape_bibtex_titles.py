#!/usr/bin/env python
import os
import re
import sys

# List of system names, e.g. "Anchor Graph" or "Alpage"
# System names that are a single word with at least two capital letters in them
# do not need to be listed here; they will be handled as acronyms below.
system_names = [
]

# Proper names of people, companies, algorithms, etc.
proper_names = [
    "Bayes",
    "Bayesian",
    "Wikipedia",
    "Wiktionary",
    "Twitter",
    "Starbucks",
    "Yahoo",
    "Freebase",
    "Debatepedia",
]

# Language names. Not currently even close to an exhaustive list.
languages = [
    "Chinese",
    "Russian",
    "Japanese",
    "English",
    "Irish",
    "Lithuanian",
    "Croatian",
    "Serbian",
    "Arabic",
    "Basque",
    "Hindi",
    "Persian",
    "Turkish",
]

names = system_names + proper_names + languages

names_regex = re.compile(r'({0})'.format(r'|'.join(
    r'\b{0}\b'.format(re.escape(name)) for name in names)))

acronym_regex = re.compile(r'\b([A-Z]\w*[A-Z]\w*)\b')

# A regex and a substitution function that place {}s around names and acronyms
# in BibTeX titles
title_regex = re.compile(r'(title\s*=\s*{)([^}]*)(})')
def title_fixer(match):
    title = match.group(2)
    title = acronym_regex.sub(r'{\1}', title)
    title = names_regex.sub(r'{\1}', title)
    return "{0}{1}{2}".format(match.group(1), title, match.group(3))

if __name__ == "__main__":
    [books_dir] = sys.argv[1:]

    # fix titles in all .bib files within the books directory
    for (dirpath, dirnames, filenames) in os.walk(books_dir):
        for filename in filenames:
            if filename.endswith(".bib"):
                # read in the original .bib text
                bib_path = os.path.join(dirpath, filename) 
                with open(bib_path) as bib_file:
                    bib_text = bib_file.read()

                # add {}s as needed
                new_bib_text = title_regex.sub(title_fixer, bib_text)

                # write the revised .bib text over the original
                if new_bib_text != bib_text:
                    with open(bib_path, 'w') as bib_file:
                        bib_file.write(new_bib_text)

