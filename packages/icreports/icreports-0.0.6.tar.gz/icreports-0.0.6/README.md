# icreports

This project is a collection of tools and templates for generating reports at IHCEC.

# Contents #

## Latex Templates ##

### Technical Report ###

There is a sample Technical Report template in `meida/templates/latex/technical_report.tex`, which can be converted to a PDF with `pdflatex`.

### Gantt Chart ###

There is a sample Gantt Chart template in `media/templates/latex/gantt.tex`. It needs a few LaTeX packages for use:

``` shell
tlmgr install pgfgantt standalone helvetic
```

Then it can be used to generate a PDF with `pdflatex`.

## Python Module ##

The `icreports` Python module is used to generated the ICHEC handbook. It is a wrapper over JupyterBook, with extra features to allow separate public and internal builds and dynamic generation of images defined in text formats (e.g. tikz).

You can install it with:

``` shell
pip install icreports
```

# Copyright #

Copyright 2024 Irish Centre for High End Computing

The software in this repository can be used under the conditions of the GPLv3+ license, which is available for reading in the accompanying LICENSE.txt file.
