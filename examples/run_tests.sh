#!/bin/bash

rm -rf */diff
rm -rf */*/prerendered_viz

for dir in *; do [ -d "$dir" ] && website_diff --old $dir/old/ --new $dir/new/ --diff $dir/diff/; done