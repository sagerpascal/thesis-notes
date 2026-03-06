# PhD Thesis Notes

**Author:** Pascal Sager

This repository contains notes and source code for my PhD thesis. 

## Structure

*   `main.tex`: The main LaTeX file for compiling the thesis document.
*   `thesis_style.tex`: The central configuration file for styling updates. Here you can change global settings like font colors, hyperlink styles, and heading rules. The document is pre-configured with a modern dark blue/accent color theme. This file also provides helper macros for standardized cross-referencing (e.g. `\figref`, `\tabref`, etc.) powered by `cleveref`. 
*   `thesis.bib`: The central bibliography file.
*   `sections/`: Directory containing the individual `.tex` files for your thesis sections (Introduction, Related Work, etc.).
*   `figures/`: Directory to store your images and figures, including your `titlepage.pdf`.
*   `examples/`: Sample documents and templates from the original `kaobook` latex template that I kept around for reference.
*   `*.sty` and `*.cls`: Template files from `kaobook` that drive the formatting.

## Building

To compile the primary document, simply use your favorite LaTeX compilation method (like `pdflatex` + `biber`) on `main.tex`.

For example:
```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```
