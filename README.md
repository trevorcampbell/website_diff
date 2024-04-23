# Website Diff

`website_diff` is a utility that compares two HTML websites, and outputs a diff *as a third HTML website*.
The diff site has insertion/deletion highlighting, automatic scroll-to-next and scroll-to-previous key bindings,
image diffing, and highlighting of links pointing to diffed pages.

## Why would I use `website_diff`?
This tool is primarily meant to help see/find differences in websites that are automatically generated from some source
documents (e.g. documentation pages, Jupyterbooks, etc) that may not be obvious from source diffs produced by GitHub.
This is particularly useful when the source documents run code whose output may silently change, even though the source
files remain constant.

## Installation
Ensure you have Rust and Cargo installed. Instructions can be found [here](https://www.rust-lang.org/tools/install).

```
pip install website_diff
```

## Usage
`website_diff` takes as an input two folders each containing an `index.html` file, as well as the name of a third folder to be created
that will contain the diffed website.
```
website_diff --old path/to/old/site/ --new path/to/new/site/ --diff path/where/diff/site/will/be/created
```
If `website_diff` runs successfully, the diff website will be available at
```
path/where/diff/site/will/be/created/index.html
```

To access the command line interface help documentation, run
```
website_diff --help
```
