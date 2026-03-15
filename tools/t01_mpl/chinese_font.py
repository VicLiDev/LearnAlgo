"""
中文字体配置模块
解决matplotlib中文显示问题
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os


def setup():
    """设置中文字体"""
    font_paths = [
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        'C:/Windows/Fonts/simhei.ttf',
        '/System/Library/Fonts/PingFang.ttc',
    ]

    for p in font_paths:
        if os.path.exists(p):
            fm.fontManager.addfont(p)
            prop = fm.FontProperties(fname=p)
            plt.rcParams['font.sans-serif'] = [prop.get_name(), 'DejaVu Sans']
            break
    else:
        plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'SimHei', 'DejaVu Sans']

    plt.rcParams['axes.unicode_minus'] = False


setup()
