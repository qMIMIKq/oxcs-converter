import re
import pylab as pl
from logging import exception

import ezdxf
import os
import matplotlib
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

matplotlib.use('agg')
fm = matplotlib.font_manager
fm._get_fontconfig_fonts.cache_clear()

#
# font_dirs = ["./fonts"]
# font_files = fm.findSystemFonts(fontpaths=font_dirs)
#
# for font_file in font_files:
#     fm.fontManager.addfont(font_file)
#
# path = os.path.join(matplotlib.get_data_path(), "fonts/ttf/GOST_AU.ttf")
# prop = fm.FontProperties(fname=path)
# plt.rcParams['font.family'] = prop.get_name()
# print(matplotlib.matplotlib_fname())
#
# la = pl.matplotlib.font_manager.FontManager()
# lu = pl.matplotlib.font_manager.FontProperties(family='GOST_AU')
# print(la.findfont(lu))

# print(matplotlib.get_cachedir())

# fm._rebuild()

class DXF2IMG(object):
    default_img_format = '.png'
    default_img_res = 200

    def convert_dxf2img(self, names, img_format=default_img_format, img_res=default_img_res):
        for name in names:
            doc = ezdxf.readfile(name)
            msp = doc.modelspace()
            # Recommended: audit & repair DXF document before rendering
            auditor = doc.audit()
            # The auditor.errors attribute stores severe errors,
            # which *may* raise exceptions when rendering.
            if len(auditor.errors) != 0:
                raise exception("The DXF document is damaged and can't be converted!")
            else:
                fig = plt.figure()
                ax = fig.add_axes([0, 0, 1, 1])
                ctx = RenderContext(doc)
                ctx.set_current_layout(msp)
                ctx.current_layout_properties.set_colors(bg='#F0F8FF')
                out = MatplotlibBackend(ax)
                Frontend(ctx, out).draw_layout(msp, finalize=True)
                img_name = name[:-4]

                # img_name = re.findall("(\S+)\.", name)  # select the image name that is the same as the dxf file name
                # print(img_name)
                first_param = ''.join(img_name) + img_format  # concatenate list and string
                fig.savefig(first_param, dpi=img_res)
