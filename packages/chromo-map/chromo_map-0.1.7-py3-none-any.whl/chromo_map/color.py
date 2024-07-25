"""Color module for chromo_map package."""

import re
import uuid
from typing import Tuple
from textwrap import dedent
import importlib.resources as pkg_resources
import json
from jinja2 import Template
import numpy as np
from _plotly_utils import colors as plotly_colors
from matplotlib.colors import LinearSegmentedColormap as LSC
from matplotlib.colors import ListedColormap as LC
from matplotlib.colors import to_rgba, to_rgb
import matplotlib.pyplot as plt
import svgwrite
import palettable
from palettable.palette import Palette
from pirrtools import AttrDict, find_instances
from pirrtools.sequences import lcm
from . import data


def _rgb_c(c):
    return rf"(?P<{c}>[^,\s]+)"


_COMMA = r"\s*,\s*"
_red = _rgb_c("red")
_grn = _rgb_c("grn")
_blu = _rgb_c("blu")
_alp = _rgb_c("alp")
_rgb_pat = _COMMA.join([_red, _grn, _blu]) + f"({_COMMA}{_alp})?"
_RGB_PATTERN = re.compile(rf"rgba?\({_rgb_pat}\)")

_VALID_MPL_COLORS = plt.colormaps()


def rgba_to_tup(rgbstr):
    """Convert an RGBA string to a tuple."""
    match = _RGB_PATTERN.match(rgbstr)
    if match:
        gdict = match.groupdict()
        red = int(gdict["red"])
        grn = int(gdict["grn"])
        blu = int(gdict["blu"])
        if (alp := gdict["alp"]) is not None:
            alp = float(alp)
            if not 0 <= alp <= 1:
                raise ValueError("Alpha must be between 0 and 1.")
        else:
            alp = 1
        return to_rgb(f"#{red:02x}{grn:02x}{blu:02x}") + (alp,)
    return None


def hexstr_to_tup(hexstr: str) -> Tuple[int, int, int, int]:
    """Convert a hex string to a tuple."""
    try:
        return to_rgba(hexstr)
    except ValueError:
        return None


def clr_to_tup(clr):
    """Convert a color to a tuple."""
    if isinstance(clr, str):
        return hexstr_to_tup(clr) or rgba_to_tup(clr)
    if isinstance(clr, (tuple, list)):
        return clr
    return None


class Color:
    """A class for representing colors."""

    def __init__(self, clr, alpha=None):
        if isinstance(clr, Color):
            self.__dict__.update(clr.__dict__)
            if alpha is not None:
                self.alpha = alpha
        else:
            if isinstance(clr, (tuple, list)):
                red, grn, blu, *alp = clr
                if alpha is not None:
                    alp = alpha
                elif alp:
                    alp = alp[0]
                else:
                    alp = 1

            elif isinstance(clr, str):
                tup = clr_to_tup(clr)
                if tup is None:
                    raise ValueError("Invalid color input.")
                red, grn, blu, alp = tup
                alp = alpha or alp

            else:
                raise ValueError("Invalid color input.")

            if all(map(lambda x: 0 <= x <= 1, (red, grn, blu, alp))):
                self.r = red
                self.g = grn
                self.b = blu
                self.a = alp
            else:
                raise ValueError("Color values must be between 0 and 1.")

    @property
    def tup(self):
        return self.r, self.g, self.b, self.a

    @property
    def hexatup(self):
        return tuple(int(x * 255) for x in self.tup)

    @property
    def hextup(self):
        return self.hexatup[:3]

    @property
    def rgbtup(self):
        return self.hextup

    @property
    def rgbatup(self):
        return self.rgbtup + (self.a,)

    @property
    def hex(self):
        r, g, b = self.hextup
        return f"#{r:02x}{g:02x}{b:02x}"

    @property
    def hexa(self):
        r, g, b, a = self.hexatup
        return f"#{r:02x}{g:02x}{b:02x}{a:02x}"

    @property
    def rgb(self):
        r, g, b = self.rgbtup
        return f"rgb({r}, {g}, {b})"

    @property
    def rgba(self):
        r, g, b, a = self.rgbatup
        return f"rgba({r}, {g}, {b}, {a})"

    def interpolate(self, other, factor):
        r = self.r + (other.r - self.r) * factor
        g = self.g + (other.g - self.g) * factor
        b = self.b + (other.b - self.b) * factor
        a = self.a + (other.a - self.a) * factor
        return Color((r, g, b, a))

    def __or__(self, other):
        return self.interpolate(other, 0.5)

    def _repr_html_(self):
        random_id = uuid.uuid4().hex
        style = dedent(
            f"""\
        <style>
            #_{random_id} {{ 
                position: relative;
                display: inline-block;
                cursor: pointer;
                background: {self.rgba};
                width: 50px; height: 50px;
            }}
            #_{random_id}::after {{
                content: attr(data-tooltip);
                position: absolute;
                bottom: 50%;
                left: 0%;
                transform: translateY(50%);
                padding: 2px;
                white-space: pre;
                font-size: 12px;
                font-family: monospace;
                background: rgba(0, 0, 0, 0.6);
                backdrop-filter: blur(5px);
                color: white;
                border-radius: 5px;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.1s ease-in-out;
                z-index: -1;
            }}
            #_{random_id}:hover::after {{
                opacity: 1;
                z-index: 1;
            }}
        </style>       
        """
        )
        tooltip = dedent(
            f"""\
        RGBA: {self.rgba[5:-1]}
        HEXA: {self.hexa}\
        """
        )
        return dedent(
            f"""\
            <div>
                {style}
                <div id="_{random_id}" class="color" data-tooltip="{tooltip}"></div>
            </div>
        """
        )


class ColorGradient(LSC):
    """A class for representing color gradients."""

    def __init__(self, colors, name=None, alpha=None):
        if isinstance(colors, (list, tuple, np.ndarray)):
            temp_colors = []
            for clr in colors:
                try:
                    temp_colors.append(Color(clr, alpha=alpha))
                except ValueError:
                    pass

            if not temp_colors:
                raise ValueError("No valid colors found.")

            self.colors = temp_colors
            self.__dict__.update(
                LSC.from_list(name=name, colors=self.tup, N=len(self.colors)).__dict__
            )
        elif isinstance(colors, ColorGradient):
            self.colors = tuple(Color(clr, alpha=alpha) for clr in colors.colors)
            self.__dict__.update(
                LSC.from_list(
                    name=name or colors.name,
                    colors=self.tup,
                    N=len(self.colors)
                ).__dict__
            )
        elif isinstance(colors, Palette):
            self.__dict__.update(
                ColorGradient(colors.mpl_colors, name=name, alpha=alpha).__dict__
            )
        elif isinstance(colors, LSC):
            self.colors = tuple(Color(colors(i), alpha=alpha) for i in range(colors.N))
            self.__dict__.update(colors.__dict__)
        elif isinstance(colors, LC):
            self.__dict__.update(
                ColorGradient(colors.colors, name=name, alpha=alpha).__dict__
            )
        elif isinstance(colors, str) and colors in _VALID_MPL_COLORS:
            cmap = plt.get_cmap(colors)
            if isinstance(cmap, LSC):
                self.__dict__.update(
                    ColorGradient(cmap, name=name, alpha=alpha).__dict__
                )
            else:
                self.__dict__.update(
                    ColorGradient(cmap.colors, name=name, alpha=alpha).__dict__
                )
        else:
            super().__init__(name, colors)
            self.colors = tuple(Color(self(i), alpha=alpha) for i in range(self.N))

    def __getattr__(self, name):
        pass_through = (
            "tup",
            "hex",
            "hexa",
            "rgb",
            "rgba",
            "hextup",
            "rgbtup",
            "hexatup",
            "rgbatup",
            "r",
            "g",
            "b",
            "a",
        )
        if name in pass_through:
            return [getattr(clr, name) for clr in self.colors]
        raise AttributeError(f"'ColorGradient' object has no attribute '{name}'")

    def __getitem__(self, key):
        if isinstance(key, slice):
            start = key.start or 0
            stop = key.stop or 1
            num = key.step or len(self.colors)
            return self[np.linspace(start, stop, num)]
        if isinstance(key, int) and 0 <= key < len(self):
            return self.colors[key]
        if isinstance(key, float) and 0 <= key <= 1:
            if key == 0:
                return self.colors[0]
            if key == 1:
                return self.colors[-1]

            x, i = np.modf(key * (self.N - 1))
            i = int(i)
            j = i + 1
            c0 = self.colors[i]
            c1 = self.colors[j]
            return c0.interpolate(c1, x)
        if isinstance(key, (list, tuple, np.ndarray)):
            return ColorGradient([self[x] for x in key])
        raise IndexError(f"Invalid index: {key}")

    def __iter__(self):
        return iter(self.colors)

    def reversed(self, name=None):
        if name is None:
            name = f"{self.name}_r"
        return ColorGradient(super().reversed(name=name))

    @property
    def _r(self):
        return self.reversed()

    def get(self, key, default=None):
        try:
            return self[key]
        except IndexError:
            return default

    def __len__(self):
        return len(self.colors)

    def resize(self, num):
        """Resize the gradient to a new number of colors."""
        return ColorGradient(self._resample(num))

    def to_div(self):
        """Convert the gradient to an HTML div."""
        max_flex_width = 500
        n = len(self.colors)
        if n == 0:
            return ""
        div_width = max_flex_width // n
        template = Template(
            dedent(
                """\
        <div>
            <style>
                #_{{ random_id }} { display: flex; gap: 0px; width: {{ max_width }}px; }
                #_{{ random_id }} div { flex: 1 1 1px; }
                #_{{ random_id }} div.color { width: 100%; }
            </style>
            <h4>{{ name }}</h4>
            <div id="_{{ random_id }}" class="color-map">
                {% for clr in colors %}
                    {{ clr._repr_html_() }}
                {% endfor %}
            </div>
        </div>
        """
            )
        )
        random_id = uuid.uuid4().hex
        return template.render(
            name=self.name,
            colors=self.colors,
            random_id=random_id,
            max_width=max_flex_width,
            div_width=div_width,
        )

    def to_matplotlib(self):
        """Convert the gradient to a matplotlib figure."""
        gradient = np.linspace(0, 1, self.N)
        gradient = np.vstack((gradient, gradient))

        _, ax = plt.subplots(figsize=(5, 0.5))
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        ax.set_position([0, 0, 1, 1])
        ax.margins(0)
        ax.imshow(gradient, aspect="auto", cmap=self)
        ax.set_title(self.name)
        ax.axis("off")
        plt.show()

    def to_drawing(self, width=500, height=50, filename=None):
        """Convert the gradient to an SVG drawing."""
        dwg = svgwrite.Drawing(filename, profile="tiny", size=(width, height))
        rect_width = width / self.N

        left = 0
        for i, color in enumerate(self, 1):
            right = int(i * rect_width)
            actual_width = right - left + 1
            dwg.add(
                dwg.rect(
                    insert=(left, 0),
                    size=(actual_width, height),
                    fill=color.hex,
                    fill_opacity=color.a,
                )
            )
            left = right

        return dwg

    def _repr_html_(self):
        return self.to_div()

    def __add__(self, other):
        name = f"{self.name} + {other.name}"
        return ColorGradient(self.colors + other.colors, name=name)

    def __mul__(self, other):
        if isinstance(other, int):
            return ColorGradient(self.colors * other, name=self.name)
        raise ValueError("Invalid multiplication.")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return ColorGradient(self[:: other * len(self)], name=self.name)
        raise ValueError("Invalid division.")

    def __or__(self, other):
        n = lcm(len(self), len(other))
        a = self.resize(n)
        b = other.resize(n)
        name = f"{self.name} | {other.name}"
        return ColorGradient([x | y for x, y in zip(a, b)], name=name)


class Swatch:
    """A class for representing a collection of color gradients."""

    def __init__(self, maps):
        self.maps = []
        for name, colors in maps.items():
            try:
                self.maps.append(ColorGradient(colors, name=name))
            except ValueError as e:
                raise e
        self._repr_html_ = self.to_grid

    def __iter__(self):
        return iter(self.maps)

    def __len__(self):
        return len(self.maps)

    def to_div(self):
        """Convert the swatch to an HTML div."""
        n = len(self.maps)
        if n == 0:
            return ""
        template = Template(
            dedent(
                """\
        <style>
            #_{{ random_id }} { display: flex; gap: 0px; flex-direction: column; }
        </style>
        <div id="_{{ random_id }}">
            {% for cmap in maps %}
                {{ cmap.to_div() }}
            {% endfor %}
        </div>
        """
            )
        )
        random_id = uuid.uuid4().hex
        return template.render(maps=self.maps, random_id=random_id)

    def to_grid(self):
        """Convert the swatch to an HTML grid."""
        n = len(self.maps)
        if n == 0:
            return ""
        template = Template(
            dedent(
                """\
            <div id="_{{ random_id }}" class="color-swatch">
                <style>
                    #_{{ random_id }} {
                        display: grid;
                        grid-template-columns: repeat(auto-fill, 250px);
                        gap: 10px;
                        justify-content: start;
                    }
                    #_{{ random_id }} div {
                        width: 250px;
                    }
                    #_{{ random_id }} .color {
                        height: 30px;
                    }
                </style>
                {% for cmap in maps %}
                    {{ cmap.to_div() }}
                {% endfor %}
            </div>
        """
            )
        )
        random_id = uuid.uuid4().hex
        return template.render(maps=self.maps, random_id=random_id)


def _gud_name(name):
    return not (name[0] == "_" or name[-2:] == "_r")


class ColorMaps(AttrDict):
    """A class for representing color maps."""

    def __getattr__(self, item):
        if item in self:
            value = super().__getattr__(item)
            if not isinstance(value, type(self)):
                return self._convert(value, item)
            return value
        temp = type(self)({k: v for k, v in self.items() if k.startswith(item)})
        if temp:
            return temp
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{item}'"
        )

    @property
    def maps(self):
        return type(self)({k: v for k, v in self.items() if self._valid(v)})

    @property
    def swatch(self):
        return Swatch(self.maps)


class PlotlyColorMaps(ColorMaps):

    def _valid(self, value):
        return isinstance(value, list)

    def _convert(self, value, name):
        return ColorGradient(value, name=name)


class PalettableColorMaps(ColorMaps):

    def _valid(self, value):
        return isinstance(value, Palette)

    def _convert(self, value, name):
        return ColorGradient(value.mpl_colors, name=name)
    
class MPLColorMaps(ColorMaps):

    def _valid(self, value):
        return value in _VALID_MPL_COLORS

    def _convert(self, value, name):
        return ColorGradient(value, name=name)

plotly_cmaps = find_instances(
    cls=list,
    module=plotly_colors,
    tracker_type=PlotlyColorMaps,
    filter_func=lambda name, _: _gud_name(name),
)

palettable_cmaps = find_instances(
    cls=Palette,
    module=palettable,
    tracker_type=PalettableColorMaps,
    filter_func=lambda name, _: _gud_name(name),
)

mpl_dat = json.loads(pkg_resources.read_text(data, "mpl_cat_names.json"))
mpl_cmaps = MPLColorMaps({
    cat: {name: name for name in names} for cat, names in mpl_dat
})


cmaps = AttrDict()
cmaps['plotly'] = plotly_cmaps
cmaps['palettable'] = palettable_cmaps
cmaps['mpl'] = mpl_cmaps
