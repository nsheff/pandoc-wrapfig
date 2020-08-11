#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pandoc filter to allow variable wrapping of LaTeX/pdf documents
through the wrapfig package.

Simply add a " {?}" tag to the end of the caption for the figure, where
? is an integer specifying the width of the wrap in inches. 0 will 
cause the width of the figure to be used.

"""

from pandocfilters import toJSONFilter, Image, RawInline, stringify, Div, RawBlock
import re, sys

FLAG_PAT = re.compile('.*\{(\d+\.?\d?)\}')

def html(x):
    return RawBlock('html', x)



def wrapfig(key, val, fmt, meta):
    # if key == "Div":
    #     sys.stderr.write(key)
    #     # join(str(x) for x in caption)
    #     [[ident, classes, kvs], contents] = val
    #     newcontents = [html('<dt>Theorem ' + str("hello") + '</dt>'),
    #     html('<dd>')] + contents + [html('</dd>')]
    #     return Div([ident, classes, kvs], newcontents)
    if key == 'Latex':
        sys.stderr.write(key)
    if key == 'Image':
        attrs, caption, target = val

        if fmt == 'markdown' or fmt == 'html':
            return [Image(attrs, caption, target)] + \
            [RawInline(fmt, "<span class='caption'>")] + caption + [RawInline(fmt, "</span>")]
        if FLAG_PAT.match(stringify(caption)):
            # Strip tag
            size = FLAG_PAT.match(caption[-1]['c']).group(1)
            stripped_caption = caption[:-2]
            # sys.stderr.write(caption[:-2])  
            if fmt == 'latex':
                latex_begin = r'\setlength{\intextsep}{2pt}\setlength{\columnsep}{8pt}\begin{wrapfigure}{R}{' + size + 'in}'
                if len(stripped_caption) > 0:
                    latex_fig = r'\centering\includegraphics{' + target[0] \
                                + '}\caption{'
                    latex_end = r'}\vspace{-5pt}\end{wrapfigure}'
                    return [RawInline(fmt, latex_begin + latex_fig)] \
                            + stripped_caption + [RawInline(fmt, latex_end)]
                else:
                    latex_fig = r'\centering\includegraphics{' + target[0] \
                                + '}'
                    latex_end = r'\end{wrapfigure}'
                    return [RawInline(fmt, latex_begin + latex_fig)] \
                            + [RawInline(fmt, latex_end)]
            else:
                return Image(attrs, stripped_caption, target)
        

if __name__ == '__main__':
    toJSONFilter(wrapfig)
    sys.stdout.flush() # Should fix issue #1 (pipe error)
