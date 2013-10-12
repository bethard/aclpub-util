#!/bin/bash
set -e

archive_dir="archives"
books_dir="books"

# check the parameters
if [ $# -lt 3 ]; then
    script_name=`basename $0`
    echo "usage: $script_name conference-title START-conference-name START-book-name [START-book-name ...]"
    echo "  e.g. $script_name EMNLP-2013 emnlp2013 papers SPMRL2013 TextGraphs2013"
    exit 1
fi
: ${ACLPUB:?"The ACLPUB variable must be set to point to the directory extracted from all.zip"}

conf_title=$1
shift
conf_name=$1
shift

# create the archives directory if necessary
if [ ! -d $archive_dir ]; then
    mkdir $archive_dir
fi

# fix problems in ACLPUB
echo "ACLPUB=$ACLPUB"
echo "Fixing problems in ACLPUB scripts"
sed -i.bak -e 's/ --no-run-if-empty//g' -e "s/ACL-2005/$conf_title/g" $ACLPUB/make/Makefile*

# copy Makefile for full conference
cp $ACLPUB/make/Makefile_pubchair Makefile

# create directories if necessary
if [ ! -d $books_dir ]; then
    mkdir -p $books_dir
fi

# download each book and unpack it to the right place
for book_name in "$@"; do
    url="https://www.softconf.com/$conf_name/$book_name/manager/aclpub/proceedings.tgz"
    echo "Downloading $url"
    curl -fo $archive_dir/$conf_name-$book_name-proceedings.tgz $url
    tar -xzf $archive_dir/$conf_name-$book_name-proceedings.tgz
    cp -f $ACLPUB/make/Makefile_bookchair proceedings/Makefile
    abbrev=`perl -ne 'print if s/abbrev\s+//' proceedings/meta`;
    if [[ -e $books_dir/$abbrev ]]; then
	echo "Removing previous books/$abbrev"
	rm -rf $books_dir/$abbrev
    fi
    echo "Creating $books_dir/$abbrev"
    mv -f proceedings $books_dir/$abbrev
done

# generate the CDROM files
make cdrom
