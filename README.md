# Website Diff

`website_diff` is a utility that compares two HTML websites, and outputs a diff *as a third HTML website*.
The diff site has insertion/deletion highlighting, automatic scroll-to-next and scroll-to-previous key bindings,
image diffing, and highlighting of links pointing to diffed pages.

![demo](https://github.com/trevorcampbell/website_diff/assets/59274601/369fd570-cb37-4910-8918-ad77bf0cb9ea)

## Why would I use `website_diff`?
This tool is primarily meant to help see/find differences in websites that are automatically generated from some source
documents (e.g. documentation pages, Jupyterbooks, etc) that may not be obvious from source diffs produced by GitHub.
This is particularly useful when the source documents run code whose output may silently change, even though the source
files remain constant.

## Installation
Ensure Rust and Cargo are installed. Instructions can be found [here](https://www.rust-lang.org/tools/install).

```
pip install --upgrade pip
pip install website_diff
```

## Command Line Usage
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

## GitHub Actions Usage
`website_diff` can be used as part of a GitHub Actions workflow that runs when a website source code repository is updated.
See the example workflow in `.github/workflow-templates/example_workflow.yml`. In this example, the workflow:
- Checks out the website repository on the PR branch
- Builds the PR website
- Commits the PR website to the `gh-pages` branch
- Checks out the `gh-pages` branch
- Builds the diff website using `website_diff`
- Commits the diff website to the `gh-pages` branch
- Posts a message on the PR thread pointing users to each website

This example template is based on a real usage of `website_diff` in the [Introduction to Data Science](https://python.datasciencebook.ca) online textbook repository here: https://github.com/UBC-DSCI/introduction-to-datascience-python/blob/main/.github/workflows/deploy_pr_preview.yml

## Visual Diff Style

- **Text:** Diffs are highlighted in green if text was inserted, and red if text was deleted.
- **Links to pages with diffs:** Any links that point to a page containing diffs are yellow.
- **Images:** New images have a green border and are highlighted in green, deleted images have a red border and are highlighted in red, and changed images are outlined in yellow with differences highlighted in red. 

## Keyboard Controls

- When first opening a page with diffs, the browser will scroll to the first diff on the page
- To scroll to the next off-page diff, press the **n** key
- To scroll to the previous off-page diff, press **Shift+n** or **N**

## Examples

There are several examples that can demonstrate the kinds of differences that website_diff will detect. To run website_diff on those examples, simply run the bash script `run_tests.sh` found within the website_diff repo. The `run_tests.sh` script pulls the examples from a separate repo called `website_diff_examples`.  The folder `website_diff_examples/examples` will then contain several folders each representing a different example e.g. lines of text changed, image added, page added, etc. In each of those folders, there will be an `old` and `prerendered_old` folder for the old website and old website with pre-rendered figures, `new` and `prerendered_new` for the new website and new website with pre-rendered figures, and lastly `diff` for the diffed version of the website with an `index.html` file that shows everything that has changed between the old and new versions of the website.
