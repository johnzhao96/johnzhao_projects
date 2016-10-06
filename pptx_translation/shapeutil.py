"""
Jiayang Zhao
shapeutil: Module containing miscellaneous useful functions.
"""

from pptx.util import Inches, Emu, Pt, Centipoints

def emu_to_px(value, ppi):
    """
    Converts a value in EMU to pixels, using the ppi (pixels per inch)
    """
    return Emu(value).inches * ppi

def str_emu_to_px(value, ppi):
    """
    Converts a value in EMU to pixels, using the ppi (pixels per inch), then writes it as a string.
    """
    return str(Emu(value).inches * ppi)

def str_cpt_to_px(value, ppi):
    """
    Converts a value in centipoints to pixels, using the ppi (pixels per inch), then writes it as a string.
    """
    return str(Centipoints(value).inches * ppi)

def replace_spaces(str):
    """
    Replaces a string's spaces with '&emsp14' characters
    """
    ret = ''
    for c in str:
        if c != ' ':
            ret += c
        else:
            ret += '&emsp13;'
    return ret
