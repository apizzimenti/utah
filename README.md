# `utah`

This project is a wrapper for doing proration, graph analysis, and MCMC
districting analysis for Utah.

## Installation
**If you want to do preprocessing**, navigate to this repository and run
`$ git clone https://github.com/gerrymandr/Preprocessing.git`. Then make sure
all the required packages are installed, and you're set.

**If you don't want to do preprocessing**, then don't do anything. Skip to
the usage section.

## Usage
As of now, simply run `$ ./utah.sh <number of runs>` (e.g. `$./utah.sh 1000`) to do all the things
(including proration). Then, output is stored in `./output`, including a short
text file containing basic graph analysis, images of the queen and rook adjacency
grpahs, and histograms from the chain run.

## Notes
If, after proration, the `Running data analysis on the dual graphs.` output
doesn't show up, hit ctrl + c to kill the Python process. Then, the a
`KeyboardInterrupt` will be printed to the screen and the bash script will
continue.
