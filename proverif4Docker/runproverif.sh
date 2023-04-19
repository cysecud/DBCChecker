#!/bin/bash
if [ $3 = "text" ]; then
    /root/.opam/default/bin/proverif $1 > $2
    echo "Proverif executed on file $1, result can be found in $2"
elif [ $3 = html ]; then
    /root/.opam/default/bin/proverif -html $2 $1
    echo "Proverif executed on file $1, result can be found in $2"
else
    echo "Wrong option, please use: text or html"
fi
exit 0