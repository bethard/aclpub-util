These scripts are designed for the Publication Chair in an ACL-style conference.
They fill in some gaps not covered by the ACLPUB scripts that you get from the
START conference system (https://www.softconf.com/).

Combine proceedings for the conference and workshops
====================================================

The `proceedings.tgz` that you can download from START has already generated
the HTML and PDFs for the main conference and each workshop.
You still need to generate an overall proceedings that combines all of these
pieces together.

1. Download the ACLPUB scripts and the current main conference proceedings from
   the START system: `ACLPUB` -> `Generate` tab -> `All` button -> `[zip]` link.
   Save the zip file to the same directory as this README file.

2. Unzip the downloaded `all.zip`.

3. Set the `ACLPUB` environment variable to point to the directory that you just
   unzipped. In bash, for example:
   ```
   export ACLPUB="$(pwd)/all"
   ```

4. Run the script to download the workshop proceedings and combine them with
   the main conference proceedings.
   ```
   ./make-cdrom.sh <conference-title> <START-conference-name> <START-book-name> [<START-book-name> ...]
   ```
   The `<conference-title>` is the name to be used in the combined bibliography,
   the `<START-conference-name>` is the short name of the conference on START,
   and the `<START-book-name>`s are either `papers`, for the main conference, or
   the short name of each workshop on START.
   For example, at EMNLP 2013 the command looked like:
   ```
   ./make-cdrom.sh EMNLP-2013 emnlp2013 papers SPMRL2013 TextGraphs2013
   ```
   The script will download each of the `proceedings.tgz` files for each of the
   `book`s, extract them to a `books` directory, and execute a Makefile that
   will generate the final `cdrom` directory.

5. (Optional) Remove .ps files from the `cdrom` directory.
   These are not used by the ACL Anthology, and it's unlikely that any of the
   conference attendees will want them, so this will reduce the size of the
   `cdrom` distribution.
   ```
   find cdrom -name "*.ps" -exec rm {} \;
   ```

NOTE: If you get an error message like `Attention: The file "cdrom/index.html" is out of date` this may mean that you have generated the main conference proceedings after the workshop proceedings.
Try going to the workshop proceedings on START and re-generating them.


Check common bugs in proceedings
================================

There are several common bugs that you should check for in the `cdrom`
directory.

* Check that all references to ACL 2010 have been replaced with the name of your
  conference:
  ```
  find cdrom -name "*.html" -exec grep 2010 {} \;
  ```

* Check that there are no non-ascii characters in any of the BibTeX files. (If
  you find any, you will need to contact [Softconf Support](
  http://www.softconf.com/about/support-contacts-support-49) to have the
  conversion scripts updated.
  ```
  find cdrom -name "*.bib" -exec file --mime {} \; | grep -v 'ascii'
  ```
  If you do find some files that are not ASCII, the following command may help
  you to identify exactly where the non-ascii character is:
  ```
  grep --color='auto' "[^ -~]" <filename>
  ```

If you find any of these bugs, you will need to make the appropriate fixes on
the START system, re-generate all of the proceedings on START, and then run
the `make-cdrom.sh` script to download the new `proceedings.tgz` files.

Check capitalization in BibTeX
==============================

Acronyms and some other words (such as language names) should always be
capitalized, and therefore need to be wrapped in {} in BibTeX titles.
There is a script that will help you do this.

1. Open `escape_bibtex_titles.py` and  edit the lists at the top which identify
   system names, proper names and language names that need to be capitalized in
   BibTeX titles. (There are some entries in there now, but these will most
   likely need to be adjusted for each conference.)

2. Run the script on the `books` directory created by the `make-cdrom.sh`
   script:
   ```
   python escape_bibtex_titles.py books
   ```

3. Re-generate the `cdrom` with the updated .bib files:
   ```
   touch books
   make cdrom
   ```

NOTE: These changes will be overwritten if you re-generate and re-download any
books from START.
You must re-run this script each time you re-download.

Generate the conference handbook
================================

The START scripts generate the PDF proceedings, but they do not generate the
conference handbook (a.k.a. booklet) that is printed and handed out to
attendees of the conference.
This procedure is not fully automatic, but there are several scripts and LaTeX
templates that should help you.

1. Specify various metadata not available via the START download, by modifying
   `settings.py`.
   You will need to specify short names for each day of the conference,
   workshop titles and locations, locations for each session on each day,
   and session chairs.

2. Generate a partial draft of the handbook from the main conference papers:
   ```
   python generate_handbook_tex.py books/<abbrev> handbook/handbook.tex
   ```
   where `<abbrev>` is the `Abbreviation` used for the main conference on the
   `CDROM` tab of `ACLPUB` in the START system.
   For example, for EMNLP 2013, the command looked like:
   ```
   python generate_handbook_tex.py books/EMNLP handbook/handbook.tex
   ```
   This will generate, for each day of the conference, an overview page showing
   the schedule, and a list of talk abstracts for each session in the
   conference.
   Note that the generated `handbook.tex` depends on the macros defined in
   `preamble.tex`, which is also in the `handbook` directory.

3. Generate talk abstracts for each of the workshops:
   ```
   python generate_workshop_tex.py books/<abbrev> handbook/handbook-<abbrev>.tex
   ```
   Again, `<abbrev>` is the `Abbreviation` that the workshop used on the
   `CDROM` tab of `ACLPUB` in the START system.
   This will generate a file `handbook/handbook-<abbrev>.tex` that contains
   a single session for the workshop, containing all the workshop talk
   abstracts.

4. Manually add all remaining material.
   This will typically include at least:
   * Filling in `handbook/frontmatter.tex` with pages for:
     * Conference title and logo
     * Welcome message from the general chair
     * Organizing committee
     * Conference sponsors
   * Adding a schedule for the workshop day(s), followed by `\input`ing the `handbook-<abbrev>.tex` files you created above.
   * Adding sessions and abstracts for keynote speakers.
   * Adding talk abstracts for TACL papers (which are typically not on START).
   * Adding a conference venue map.
