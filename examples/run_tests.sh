#!/bin/bash

rm -rf ./temp
rm -rf */diff
rm -rf */*/prerendered
mkdir temp
cp -rf ./* ./temp

for dir in *; do [ -d "$dir" ] && [ "$dir" != "temp" ] && website_diff --old $dir/old/ --new $dir/new/ --diff $dir/diff/; done

cp -rf ./temp/* .
rm -rf ./temp