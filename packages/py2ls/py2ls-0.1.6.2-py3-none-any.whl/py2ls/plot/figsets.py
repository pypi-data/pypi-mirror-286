
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tck 
import seaborn as sns
from cycler import cycler


def get_cmap():
    return plt.colormaps()

def read_mplstyle(style_file):
    # Load the style file
    plt.style.use(style_file)

    # Get the current style properties
    style_dict = plt.rcParams

    # Convert to dictionary
    style_dict = dict(style_dict)
    # Print the style dictionary
    for i, j in style_dict.items():
        print(f"\n{i}::::{j}")
    return style_dict
# #example usage:
# style_file = "/ std-colors.mplstyle"
# style_dict = read_mplstyle(style_file)

def figsets(*args,**kwargs):
    """
    usage:
        figsets(ax=axs[1],
            ylim=[0, 10],
            spine=2,
            xticklabel=['wake','sleep'],
            yticksdddd=np.arange(0,316,60),
            labels_loc=['right','top'],
            ticks=dict(
            ax='x',
            which='minor',
            direction='out',
            width=2,
            length=2,
            c_tick='m',
            pad=5,
            label_size=11),
            grid=dict(which='minor',
                    ax='x',
                    alpha=.4,
                    c='b',
                    ls='-.',
                    lw=0.75,
                    ),
            supertitleddddd=f'sleep druations\n(min)',
            c_spine='r',
            minor_ticks='xy',
            style='paper',
            box=['right','bottom'],
            xrot=-45,
            yangle=20,
            font_sz = 2,
            legend=dict(labels=['group_a','group_b'],
                        loc='upper left',
                        edgecolor='k',
                        facecolor='r',
                        title='title',
                        fancybox=1,
                        shadow=1,
                        ncols=4,
                        bbox_to_anchor=[-0.5,0.7],
                        alignment='left')
        )
    """
    fig = plt.gcf()
    fontsize = 11
    fontname = "Arial"
    sns_themes = ["white", "whitegrid", "dark", "darkgrid", "ticks"]
    sns_contexts = ["notebook", "talk", "poster"]  # now available "paper"
    scienceplots_styles = ["science","nature",
        "scatter","ieee","no-latex","std-colors","high-vis","bright","dark_background","science",
        "high-vis","vibrant","muted","retro","grid","high-contrast","light","cjk-tc-font","cjk-kr-font",
    ]
    def set_step_1(ax,key, value):
        if ("fo" in key) and (("size" in key) or ("sz" in key)):
            fontsize=value
            plt.rcParams.update({"font.size": value})
        # style
        if "st" in key.lower() or "th" in key.lower():
            if isinstance(value, str):
                if (value in plt.style.available) or (value in scienceplots_styles):
                    plt.style.use(value)
                elif value in sns_themes:
                    sns.set_style(value)
                elif value in sns_contexts:
                    sns.set_context(value)
                else:
                    print(
                        f"\nWarning\n'{value}' is not a plt.style,select on below:\n{plt.style.available+sns_themes+sns_contexts+scienceplots_styles}"
                    )
            if isinstance(value, list):
                for i in value:
                    if (i in plt.style.available) or (i in scienceplots_styles):
                        plt.style.use(i)
                    elif i in sns_themes:
                        sns.set_style(i)
                    elif i in sns_contexts:
                        sns.set_context(i)
                    else:
                        print(
                            f"\nWarning\n'{i}' is not a plt.style,select on below:\n{plt.style.available+sns_themes+sns_contexts+scienceplots_styles}"
                        )
        if "la" in key.lower():
            if "loc" in key.lower() or "po" in key.lower():
                for i in value:
                    if "l" in i.lower() and not 'g' in i.lower():
                        ax.yaxis.set_label_position("left") 
                    if "r" in i.lower() and not 'o' in i.lower():
                        ax.yaxis.set_label_position("right")
                    if "t" in i.lower() and not 'l' in i.lower():
                        ax.xaxis.set_label_position("top")
                    if "b" in i.lower()and not 'o' in i.lower():
                        ax.xaxis.set_label_position("bottom")
            if ("x" in key.lower()) and (
                "tic" not in key.lower() and "tk" not in key.lower()
            ):
                ax.set_xlabel(value, fontname=fontname)
            if ("y" in key.lower()) and (
                "tic" not in key.lower() and "tk" not in key.lower()
            ):
                ax.set_ylabel(value, fontname=fontname)
            if ("z" in key.lower()) and (
                "tic" not in key.lower() and "tk" not in key.lower()
            ):
                ax.set_zlabel(value, fontname=fontname)
        if key=='xlabel' and isinstance(value,dict):
            ax.set_xlabel(**value)
        if key=='ylabel' and isinstance(value,dict):
            ax.set_ylabel(**value)
        # tick location
        if "tic" in key.lower() or "tk" in key.lower():
            if ("loc" in key.lower()) or ("po" in key.lower()):
                if isinstance(value,str):
                    value=[value]
                if isinstance(value, list):
                    loc = []
                    for i in value:
                        if ("l" in i.lower()) and ("a" not in i.lower()):
                            ax.yaxis.set_ticks_position("left")
                        if "r" in i.lower():
                            ax.yaxis.set_ticks_position("right")
                        if "t" in i.lower():
                            ax.xaxis.set_ticks_position("top")
                        if "b" in i.lower():
                            ax.xaxis.set_ticks_position("bottom")
                        if i.lower() in ["a", "both", "all", "al", ":"]:
                            ax.xaxis.set_ticks_position("both")
                            ax.yaxis.set_ticks_position("both")
                        if i.lower() in ["xnone",'xoff',"none"]:
                            ax.xaxis.set_ticks_position("none")
                        if i.lower() in ["ynone",'yoff','none']:
                            ax.yaxis.set_ticks_position("none")
            # ticks / labels
            elif "x" in key.lower():
                if value is None:
                    value=[]
                if "la" not in key.lower():
                    ax.set_xticks(value)
                if "la" in key.lower():
                    ax.set_xticklabels(value)
            elif "y" in key.lower():
                if value is None:
                    value=[]
                if "la" not in key.lower():
                    ax.set_yticks(value)
                if "la" in key.lower():
                    ax.set_yticklabels(value)
            elif "z" in key.lower():
                if value is None:
                    value=[]
                if "la" not in key.lower():
                    ax.set_zticks(value)
                if "la" in key.lower():
                    ax.set_zticklabels(value)
        # rotation
        if "angle" in key.lower() or ("rot" in key.lower()):
            if "x" in key.lower():
                if value in [0,90,180,270]:
                    ax.tick_params(axis="x", rotation=value)
                    for tick in ax.get_xticklabels():
                        tick.set_horizontalalignment('center')
                elif value >0:
                    ax.tick_params(axis="x", rotation=value)
                    for tick in ax.get_xticklabels():
                        tick.set_horizontalalignment('right')
                elif value <0:
                    ax.tick_params(axis='x', rotation=value)
                    for tick in ax.get_xticklabels():
                        tick.set_horizontalalignment('left')
            if "y" in key.lower():
                ax.tick_params(axis="y", rotation=value)
                for tick in ax.get_yticklabels():
                    tick.set_horizontalalignment('right')

        if "bo" in key in key:  # box setting, and ("p" in key or "l" in key):
            if isinstance(value, (str, list)):
                locations = []
                for i in value:
                    if "l" in i.lower() and not 't' in i.lower():
                        locations.append("left")
                    if "r" in i.lower()and not 'o' in i.lower(): # right
                        locations.append("right")
                    if "t" in i.lower() and not 'r' in i.lower(): #top
                        locations.append("top")
                    if "b" in i.lower() and not 't' in i.lower():
                        locations.append("bottom")
                    if i.lower() in ["a", "both", "all", "al", ":"]:
                        [
                            locations.append(x)
                            for x in ["left", "right", "top", "bottom"]
                        ]
                for i in value:
                    if i.lower() in "none":
                        locations = []
                # check spines
                for loc, spi in ax.spines.items():
                    if loc in locations:
                        spi.set_position(("outward", 0))
                    else:
                        spi.set_color("none")  # no spine
        if 'tick' in key.lower(): # tick ticks tick_para ={}
            if isinstance(value, dict):
                for k, val in value.items():
                    if "wh" in k.lower():
                        ax.tick_params(
                            which=val
                        )  # {'major', 'minor', 'both'}, default: 'major'
                    elif "dir" in k.lower():
                        ax.tick_params(direction=val)  # {'in', 'out', 'inout'}
                    elif "len" in k.lower():# length
                        ax.tick_params(length=val)
                    elif ("wid" in k.lower()) or ("wd" in k.lower()): # width
                        ax.tick_params(width=val)
                    elif "ax" in k.lower(): # ax
                        ax.tick_params(axis=val)  # {'x', 'y', 'both'}, default: 'both'
                    elif ("c" in k.lower()) and ("ect" not in k.lower()):
                        ax.tick_params(colors=val)  # Tick color.
                    elif "pad" in k.lower() or 'space' in k.lower():
                        ax.tick_params(
                            pad=val
                        )  # float, distance in points between tick and label
                    elif (
                        ("lab" in k.lower() or 'text' in k.lower())
                        and ("s" in k.lower())
                        and ("z" in k.lower())
                    ): # label_size
                        ax.tick_params(
                            labelsize=val
                        )  # float, distance in points between tick and label

        if "mi" in key.lower() and "tic" in key.lower():# minor_ticks
            if "x" in value.lower() or "x" in key.lower():
                ax.xaxis.set_minor_locator(tck.AutoMinorLocator())  # ax.minorticks_on()
            if "y" in value.lower() or "y" in key.lower():
                ax.yaxis.set_minor_locator(
                    tck.AutoMinorLocator()
                )  # ax.minorticks_off()
            if value.lower() in ["both", ":", "all", "a", "b", "on"]:
                ax.minorticks_on()
        if key == "colormap" or key == "cmap":
            plt.set_cmap(value)
    def set_step_2(ax,key, value):
        if key == "figsize":
            pass
        if "xlim" in key.lower():
            ax.set_xlim(value)
        if "ylim" in key.lower():
            ax.set_ylim(value)
        if "zlim" in key.lower():
            ax.set_zlim(value)
        if "sc" in key.lower(): #scale
            if "x" in key.lower():
                ax.set_xscale(value)
            if "y" in key.lower():
                ax.set_yscale(value)
            if "z" in key.lower():
                ax.set_zscale(value)
        if key == "grid":
            if isinstance(value, dict):
                for k, val in value.items():
                    if "wh" in k.lower(): # which
                        ax.grid(
                            which=val
                        )  # {'major', 'minor', 'both'}, default: 'major'
                    elif "ax" in k.lower(): # ax
                        ax.grid(axis=val)  # {'x', 'y', 'both'}, default: 'both'
                    elif ("c" in k.lower()) and ("ect" not in k.lower()): # c: color
                        ax.grid(color=val)  # Tick color.
                    elif "l" in k.lower() and ("s" in k.lower()):# ls:line stype
                        ax.grid(linestyle=val)
                    elif "l" in k.lower() and ("w" in k.lower()): # lw: line width
                        ax.grid(linewidth=val)
                    elif "al" in k.lower():# alpha:
                        ax.grid(alpha=val)
            else:
                if value == "on" or value is True:
                    ax.grid(visible=True)
                elif value == "off" or value is False:
                    ax.grid(visible=False)
        if "tit" in key.lower():
            if "sup" in key.lower():
                plt.suptitle(value)
            else:
                ax.set_title(value)
        if key.lower() in ["spine", "adjust", "ad", "sp", "spi", "adj","spines"]:
            if isinstance(value, bool) or (value in ["go", "do", "ja", "yes"]):
                if value:
                    adjust_spines(ax)  # dafault distance=2
            if isinstance(value, (float, int)):
                adjust_spines(ax=ax, distance=value)
        if "c" in key.lower() and ("sp" in key.lower() or "ax" in key.lower()):# spine color
            for loc, spi in ax.spines.items():
                spi.set_color(value)
        if 'leg' in key.lower(): # legend
            legend_kws = kwargs.get('legend', None)
            if legend_kws:
                # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
                ax.legend(**legend_kws) 
    
    for arg in args:
        if isinstance(arg,matplotlib.axes._axes.Axes):
            ax=arg
            args=args[1:]
    ax = kwargs.get('ax',plt.gca())
    if 'ax' not in locals() or ax is None:
        ax=plt.gca()
    for key, value in kwargs.items():
        set_step_1(ax, key, value)
        set_step_2(ax, key, value)
    for arg in args:
        if isinstance(arg, dict):
            for k, val in arg.items():
                set_step_1(ax,k, val)
            for k, val in arg.items():
                set_step_2(ax,k, val)
        else:
            Nargin = len(args) // 2
            ax.labelFontSizeMultiplier = 1
            ax.titleFontSizeMultiplier = 1
            ax.set_facecolor("w")

            for ip in range(Nargin):
                key = args[ip * 2].lower()
                value = args[ip * 2 + 1]
                set_step_1(ax,key, value)
            for ip in range(Nargin):
                key = args[ip * 2].lower()
                value = args[ip * 2 + 1]
                set_step_2(ax,key, value)
    colors = [
        "#474747",
        "#FF2C00",
        "#0C5DA5",
        "#845B97",
        "#58BBCC",
        "#FF9500",
        "#D57DBE",
    ]
    matplotlib.rcParams["axes.prop_cycle"] = cycler(color=colors)
    if len(fig.get_axes()) > 1:
        plt.tight_layout()
        plt.gcf().align_labels()
