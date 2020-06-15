#!/bin/bash

cd $1

for f in *.{src,tgt}
do
    cp "$f" "$f".bak
    sed 's/&quot; &quot;/"/g; s/&apos;/'\''/g' "$f" > "$f".no_quote
    mv "$f".no_quote "$f"
done
