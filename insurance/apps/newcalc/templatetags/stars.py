# -*- coding: utf-8 -*-

# http://blog.localkinegrinds.com (c) 2007
# Denis Voskvitsov (c) 2011

import math
 
from django.template import Library, Node, TemplateSyntaxError, VariableDoesNotExist, resolve_variable
from django.conf import settings
 
register = Library()
 
IMG_TEMPLATE = '<img src="%s" alt="" title="%%s"/>'
 
PATH_TO_WHOLE_STAR = IMG_TEMPLATE % '/static/images/stars/star.png'
PATH_TO_THREE_QUARTER_STAR = IMG_TEMPLATE % '/static/images/stars/three-quarter.png'
PATH_TO_HALF_STAR = IMG_TEMPLATE % '/static/images/stars/half.png'
PATH_TO_QUARTER_STAR = IMG_TEMPLATE % '/static/images/stars/quarter.png'
PATH_TO_BLANK_STAR = IMG_TEMPLATE % '/static/images/stars/blank.png'
 
class ShowStarsNode(Node):
    """ Default rounding is to the whole unit """
    def __init__(self, context_var, total_stars, round_to, title):
        self.context_var = context_var
        self.total_stars = int(total_stars)
        self.round_to = round_to.lower()
        self.title = title
 
    def render(self, context):
        try:
            stars = resolve_variable(self.context_var, context)
        except VariableDoesNotExist:
            return ''
        try:
            title = resolve_variable(self.title, context)
        except VariableDoesNotExist:
            return ''
 
        if self.round_to == "half":
            stars = round(stars*2)/2
        elif self.round_to == "quarter":
            stars = round(stars*4)/4
        else:
            stars = round(stars)
 
        fraction, integer = math.modf(stars)
        integer = int(integer)
        output = []
 
        for whole_star in range(integer):
            output.append(PATH_TO_WHOLE_STAR % title)
        if self.round_to == 'half' and fraction == .5:
            output.append(PATH_TO_HALF_STAR % title)
        elif self.round_to == 'quarter':
            if fraction == .25:
                output.append(PATH_TO_QUARTER_STAR % title)
            elif fraction == .5:
                output.append(PATH_TO_HALF_STAR % title)
            elif fraction == .75:
                output.append(PATH_TO_THREE_QUARTER_STAR % title)
 
        if fraction:
            integer += 1
 
        blanks = int(self.total_stars - integer)
 
        for blank_star in range(blanks):
            output.append(PATH_TO_BLANK_STAR % title)
 
        return "".join(output)
 
""" show_stars context_var of 5 round to half """
def do_show_stars(parser, token):
    args = token.contents.split()
    if len(args) != 9:
        raise TemplateSyntaxError('%s tag requires exactly 8 arguments' % args[0])
    if args[2] != 'of':
        raise TemplateSyntaxError("second argument to '%s' tag must be 'of'" % args[0])
    if args[4] != 'round':
        raise TemplateSyntaxError("fourth argument to '%s' tag must be 'round'" % args[0])
    if args[5] != 'to':
        raise TemplateSyntaxError("fifth argument to '%s' tag must be 'to'" % args[0])
    if args[7] != 'with':
        raise TemplateSyntaxError("sixth argument to '%s' tag must be 'with'" % args[0])
    return ShowStarsNode(args[1], args[3], args[6], args[8])   
 
register.tag('show_stars', do_show_stars)

