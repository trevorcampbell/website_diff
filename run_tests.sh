#!/bin/bash

if ! [ -d "website_diff_examples" ]; then
    git clone git@github.com:trevorcampbell/website_diff_examples.git
fi

examples_dir="website_diff_examples/examples"

rm -rf $examples_dir/*/diff
rm -rf $examples_dir/*/*/prerendered
rm -rf $examples_dir/*/prerendered_*

for dir in $examples_dir/*; do [ -d "$dir" ] && [ "$dir" != "$examples_dir/temp" ] && website_diff --old $dir/old/ --new $dir/new/ --diff $dir/diff/; done

