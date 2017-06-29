# Terminal Markdown Viewer #

Render markdown in a terminal! Why? Because although Markdown is still readable as-is, if you use Markdown a lot, it's nice to have something to render it with the proper formatting - with **bold text** and *emphasis*, etc.

An example:

![A screenshot displaying an example Markdown document, rendered using vmd][https://github.com/cpascoe95/vmd/blob/master/example.png]

## Installation ##

Requires Python 3. Install via pip:

`$ sudo pip3 install vmd`

Note that some features of the render use Unicode (such as for link indicies), so for now terminals that don't support Unicode (or aren't configured to use Unicode and you don't want to change it, which is fair enough) may experience a few issues. If this is a problem, raise an issue or create a pull request.

## Usage ##

`$ vmd file.md`

Or via standard in:

`$ generate-markdown | vmd --stdin`

With `less`:

`$ vmd file.md | less -rc`
