# Copyright (C) 2023 Tricia D. Shepherd, Sean Garrett-Roe
import sys
import os
from random import uniform
from random import randrange   # Integers - Note randrange(a,b) b is NOT included
from random import randint     # Integers - Note randint(a,b) b is included
from random import choice      # flip = choice([0,2])
from random import sample
from random import shuffle
import periodictable as pt
from chempy import Substance
from scipy.constants import N_A
import numpy as np
import string
from string import Template 

def eatOnes(innum):
    '''Process a string to eliminate 1's according to chemistry convention.

    Turn input number inum into a string; make the string empty if innum==1. 
    This helps for typesetting of chemical formulas and equations, in which
    the number 1 is not used explicitly.
    '''
    outstr = ''
    if innum!=1:
        outstr = str(innum)
    return outstr

def roundToNSigFigs(x,n=3):
    '''Round an input number x to n significant figures. 

    This function should help computed answers align better with student 
    answers when numbers are presented at a certain level of significance.
    ''' 
    return x if x == 0 else round(x, -int(np.floor(np.log10(abs(x)))) + (n - 1))


def ionform(iform):
    mymol = Substance.from_formula(iform)
    return mymol.latex_name


class myTemplate(Template):
    delimiter='@'
