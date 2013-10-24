# This file contains settings that will differ from conference to conference
# You will very likely need to modify all of the settings in this file

# Mapping from full day names (in ACLPUB db) to short names
day_short_names = {
    'Friday, October 18, 2013': 'Friday',
    'Saturday, October 19, 2013': 'Saturday',
    'Sunday, October 20, 2013': 'Sunday',
    'Monday, October 21, 2013': 'Monday',
}

# Mapping from workshop abbreviations (as in ACLPUB CDROM tab) to full names
workshop_titles = {
    'TextGraphs': 'TextGraphs-8: Graph-based Methods for Natural Language Processing',
    'SPMRL': 'Statistical Parsing of Morphologically-Rich Languages',
}

# Mapping from workshop abbreviations (as in ACLPUB CDROM tab) to locations
workshop_locations = {
    'TextGraphs': 'Eliza Anderson Amphitheater',
    'SPMRL': 'Blewett Suite',
}

# Mapping from ACLPUB day names to ACLPUB session names to session locations
# Sessions within a single day must have unique names (or must all be held
# in the same location)
day_session_locations = {
    'Saturday, October 19, 2013': {
        "Breakfast": "Leonesa Foyer",
        "Opening Remarks": "Leonesa Ballroom",
        "Information Extraction I": "Leonesa I and II",
        "Language Acquisition and Processing": "Leonesa  III",
        "NLP for Social Media I": "Eliza Anderson Amphitheater",
        "Break": "Leonesa Foyer",
        "NLP Applications I": "Leonesa I and II",
        "Semantics I": "Leonesa  III",
        "Language Resources": "Eliza Anderson Amphitheater",
        "Lunch": "", # no location
        "First invited talk: Andrew Ng": "Leonesa Ballroom",
        "Machine Translation I": "Leonesa I and II",
        "Dialogue and Discourse": "Leonesa  III",
        "Morphology and Phonology": "Eliza Anderson Amphitheater",
        "Poster Session A": "Princessa Ballroom and Foyer",
        "Poster Session B": "Princessa Ballroom and Foyer",
    },
    'Sunday, October 20, 2013' : {
        "Breakfast": "Leonesa Foyer",
        "Second invited talk: Fernando Pereira": "Leonesa Ballroom",
        "Break": "Leonesa Foyer",
        "Machine Learning for NLP": "Leonesa I and II",
        "Summarization and Generation": "Leonesa  III",
        "Information Extraction and Social Media Analysis": "Eliza Anderson Amphitheater",
        "Lunch": "", # no location
        "Machine Translation II": "Leonesa I and II",
        "Semantics II": "Leonesa  III",
        "Opinion Mining and Sentiment Analysis I": "Eliza Anderson Amphitheater",
        "Machine Translation III": "Leonesa I and II",
        "Information Extraction II": "Leonesa  III",
        "NLP Applications II": "Eliza Anderson Amphitheater",
    },
    'Monday, October 21, 2013' : {
        "Breakfast": "Leonesa Foyer",
        "Information Extraction III": "Leonesa I and II",
        "Opinion Mining and Sentiment Analysis II": "Leonesa  III",
        "NLP for Social Media II": "Princessa",
        "Break": "Leonesa Foyer",
        "Parsing": "Leonesa I and II",
        "Semantics III": "Leonesa  III",
        "NLP Applications III": "Princessa",
        "SIGDAT business meeting": "Princessa",
        "Lunch": "", # no location
        "Plenary session I": "Leonesa Ballroom",
        "Plenary Session II": "Leonesa Ballroom",
        "Closing session": "Leonesa Ballroom",
    },
}


# Mapping from ACLPUB day names to ACLPUB session names to session chairs
# These only need to be specified for sessions that include papers
day_session_chairs = {
    'Saturday, October 19, 2013': {
        "Information Extraction I": "Steven Bethard",
        "Language Acquisition and Processing": "Julia Hockenmaier",
        "NLP for Social Media I": "Noah Smith",
        "NLP Applications I": "Hang Li",
        "Semantics I": "Luke Zettlemoyer",
        "Language Resources": "Emily Bender",
        "Machine Translation I": "Kevin Knight",
        "Dialogue and Discourse": "Eugene Charniak",
        "Morphology and Phonology": "Anders Sogaard",
        "Poster Session A": "", # no chair
        "Poster Session B": "", # no chair
    },
    'Sunday, October 20, 2013' : {
        "Machine Learning for NLP": "Chris Dyer",
        "Summarization and Generation": "Lucy Vanderwende",
        "Information Extraction and Social Media Analysis": "Soumen Chakrabarti",
        "Machine Translation II": "Kristina Toutanova",
        "Semantics II": "Dipanjan Das",
        "Opinion Mining and Sentiment Analysis I": "Oren Tsur",
        "Machine Translation III": "Taro Watanabe",
        "Information Extraction II": "Ellen Riloff",
        "NLP Applications II": "Min-Yen Kan",
    },
    'Monday, October 21, 2013' : {
        "Information Extraction III": "Andreas Vlachos",
        "Opinion Mining and Sentiment Analysis II": "Bing Liu",
        "NLP for Social Media II": "Chin-Yew Lin",
        "Parsing": "Keith Hall",
        "Semantics III": "Martha Palmer",
        "NLP Applications III": "Richart Sproat",
        "Plenary session I": "Anna Korhonen",
        "Plenary Session II": "Tim Baldwin",
    },
}
