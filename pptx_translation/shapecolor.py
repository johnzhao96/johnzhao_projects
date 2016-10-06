"""
Jiayang Zhao
shapecolor: Module for extracting and mapping PPTX colors
"""

from pptx.enum.dml import MSO_COLOR_TYPE, MSO_FILL_TYPE, MSO_THEME_COLOR_INDEX
from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE, PP_PLACEHOLDER
from pptx.opc.constants import RELATIONSHIP_TYPE
from pptx.oxml import parse_xml

class ColorMap:
	"""
	Maps PPTX accent names to RGB hexadecimal values
	"""
	def __init__(self):
		self.colormap = {}

	def get_rgb_from_theme(self, theme_color):
		if theme_color in self.colormap:
			return self.colormap[theme_color]
		else:
			return '000000'

def construct_theme_color_map(pres):
	"""
	Returns a ColorMap mapping obtained from parsing the theme part of a presentation
	"""
	theme_map = ColorMap()
	theme_elm = parse_theme_element(pres)
	theme_map.colormap = {}
	for clr_elm in theme_elm.xpath('./a:themeElements/a:clrScheme/child::*', namespaces = {'a' : 'http://schemas.openxmlformats.org/drawingml/2006/main'}):
		thm_clr_name = clr_elm.tag[55:]
		rgb_str = clr_elm.xpath('./child::*/@val')[0]
		if rgb_str == 'windowText':
			rgb_str = '000000'
		if rgb_str == 'window':
			rgb_str = 'FFFFFF'
		theme_map.colormap[THEME_COLOR_ENUMS[thm_clr_name]] = rgb_str
	return theme_map

def construct_pres_color_map(pres):
	"""
	Returns a ColorMap mapping obtained from parsing the p:clrMap element of the presentation slide master
	"""
	theme_map = construct_theme_color_map(pres)
	master_map = ColorMap()
	for name in THEME_COLOR_ENUMS:
		clr_lst = pres.slide_master.element.xpath('./p:clrMap/@{}'.format(name))
		if len(clr_lst) > 0:
			master_map.colormap[THEME_COLOR_ENUMS[name]] = theme_map.colormap[THEME_COLOR_ENUMS[clr_lst[0]]]
		else:
			master_map.colormap[THEME_COLOR_ENUMS[name]] = theme_map.colormap[THEME_COLOR_ENUMS[name]]
	return master_map

def parse_theme_element(pres):
	"""
	Constructs a theme element from the theme xml part that the slide master is related to
	"""
	relationships = pres.slide_master.part.rels
	for relidx in relationships:
		if relationships[relidx].reltype == RELATIONSHIP_TYPE.THEME:
			return parse_xml(relationships[relidx].target_part.blob)

def get_shapetype(shape):
	"""
	Gets the shape_type attribute of a shape
	"""
	try:
		return shape.shape_type
	except NotImplementedError:
		print("Not Implemented Shape: {}".format(shape.name))
		return None

def get_fill_color(shape, clr_map):
	"""
	Given a shape, returns the color of the shape
	"""
	if get_shapetype(shape) == MSO_SHAPE_TYPE.AUTO_SHAPE:
	    clr = extract_color_from_format(shape.fill, clr_map)
	    if clr == 'no color':
	    	return 'fill-opacity:0 ;'
	    else:
	    	return 'fill:{} ; fill-opacity:100'.format(clr)
	return 'fill-opacity:0 ;'

def extract_color_from_format(fill_format, clr_map):
	"""
	Gets the color from a pptx.FillFormat object and returns the color as an RGB value
	"""
	if fill_format.type == MSO_FILL_TYPE.SOLID:
	    fore = fill_format.fore_color
	    if fore.type == MSO_COLOR_TYPE.RGB:
	        return '#{}'.format(fore.rgb.__str__())
	    elif fore.type == MSO_COLOR_TYPE.SCHEME:
	        return '#{}'.format(clr_map.get_rgb_from_theme(fore.theme_color))
	return 'no color'

# Map of Theme color string names to their enumerations in the python-pptx library
THEME_COLOR_ENUMS = {
	'accent1' : MSO_THEME_COLOR_INDEX.ACCENT_1,
	'accent2' : MSO_THEME_COLOR_INDEX.ACCENT_2,
	'accent3' : MSO_THEME_COLOR_INDEX.ACCENT_3,
	'accent4' : MSO_THEME_COLOR_INDEX.ACCENT_4,
	'accent5' : MSO_THEME_COLOR_INDEX.ACCENT_5,
	'accent6' : MSO_THEME_COLOR_INDEX.ACCENT_6,
	'bg1' : MSO_THEME_COLOR_INDEX.BACKGROUND_1,
	'bg2' : MSO_THEME_COLOR_INDEX.BACKGROUND_2,
	'dk1' : MSO_THEME_COLOR_INDEX.DARK_1,
	'dk2' : MSO_THEME_COLOR_INDEX.DARK_2,
	'folHlink' : MSO_THEME_COLOR_INDEX.FOLLOWED_HYPERLINK,
	'hlink' : MSO_THEME_COLOR_INDEX.HYPERLINK,
	'lt1' : MSO_THEME_COLOR_INDEX.LIGHT_1,
	'lt2' : MSO_THEME_COLOR_INDEX.LIGHT_2,
	'tx1' : MSO_THEME_COLOR_INDEX.TEXT_1,
	'tx2' : MSO_THEME_COLOR_INDEX.TEXT_2
}
