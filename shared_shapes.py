"""Native, named book primitives. Positions are millimetres, origin bottom left."""
from dataclasses import replace
from pathlib import Path
import json
import numpy as np
import matplotlib as mpl
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Ellipse, Rectangle, FancyBboxPatch, FancyArrowPatch, PathPatch
from matplotlib.path import Path as MplPath
from book_style import STYLE, font_properties, rc_settings
from layout_utils import BuildResult, new_canvas, register
from palette import resolve, tint, PRIMARY, SECONDARY, ACCENT, SUPPLEMENT, INK, MUTED, BACKGROUND

ROOT = Path(__file__).resolve().parent


class Drawing:
    def __init__(self, figure_id, height=100):
        self.id = figure_id
        self.style = replace(STYLE, height_mm=height)
        with mpl.rc_context(rc_settings()):
            self.figure, self.ax = new_canvas(self.style)
        self.figure.set_facecolor(BACKGROUND)
        self.artists = {}
        self.spec = json.loads((ROOT / "figure_specs" / f"{figure_id}.json").read_text())
        self.spec["size_mm"] = [170, height]
        self.spec["relations_drawn"] = []
        self.spec["palette"] = PALETTE_NAME = "海青与铜"

    def add(self, name, item, role):
        return register(self.artists, f"{self.id}.{name}", item, role)

    def text(self, name, value, xy, *, size=9.5, color="ink", ha="center", va="center"):
        item = self.ax.text(*xy, value, fontproperties=font_properties(size), color=resolve(color),
                            ha=ha, va=va, linespacing=1.25, zorder=10)
        return self.add(name, item, "text")

    def heading(self, name, value, xy, *, ha="left"):
        return self.text(name, value, xy, size=11.5, ha=ha)

    def note(self, value, *, y=8, name="scope.note"):
        return self.text(name, value, (6, y), size=8.5, color="muted", ha="left")

    def line(self, name, points, *, color="primary", width=1.1, dashed=False, role="structure", zorder=4):
        x,y=np.asarray(points).T
        item=Line2D(x,y,color=resolve(color),linewidth=width,solid_capstyle="round",zorder=zorder)
        if dashed:item.set_linestyle((0,(3,2)))
        self.ax.add_line(item)
        return self.add(name,item,role)

    def rect(self, name, xy, w, h, *, color="primary", fill=None, weight=.10, radius=1.2, dashed=False, role="boundary"):
        edge=resolve(color)
        face="none" if fill is False else (resolve(fill) if isinstance(fill,str) else tint(edge,weight))
        item=FancyBboxPatch(xy,w,h,boxstyle=f"round,pad=0,rounding_size={radius}",
                           linewidth=.8,edgecolor=edge,facecolor=face,zorder=1)
        if dashed:item.set_linestyle((0,(3,2)))
        self.ax.add_patch(item)
        return self.add(name,item,role)

    def node(self, name, value, center, w=32, h=14, *, color="primary", fill=None, size=9.5):
        x,y=center
        self.rect(name+".boundary",(x-w/2,y-h/2),w,h,color=color,fill=fill)
        self.text(name+".label",value,center,size=size)
        return {"center":center,"left":(x-w/2,y),"right":(x+w/2,y),"top":(x,y+h/2),"bottom":(x,y-h/2)}

    def ellipse(self, name, center, w, h, *, color="secondary", fill=None, weight=.08, role="containment"):
        edge=resolve(color)
        face="none" if fill is False else (resolve(fill) if isinstance(fill,str) else tint(edge,weight))
        item=Ellipse(center,w,h,edgecolor=edge,facecolor=face,linewidth=.8,zorder=1)
        self.ax.add_patch(item)
        return self.add(name,item,role)

    def circle(self, name, center, r=2.1, *, color="primary", fill=None, weight=.16):
        return self.ellipse(name,center,2*r,2*r,color=color,fill=fill,weight=weight,role="object")

    def edge(self, name, start, end, *, kind="process", label=None, label_xy=None, color=None, rad=0, source=None, target=None):
        colors={"process":"primary","template":"primary","influence":"muted","conditional":"muted",
                "observe":"supplement","zoom":"muted","intervention":"accent","order":"muted"}
        color=resolve(color or colors[kind])
        styles={"process":"-|>","template":"->","influence":"->","conditional":"->",
                "observe":"-","zoom":"-","intervention":"-|>","order":"-"}
        dashes={"template":(0,(3,2)),"influence":(0,(7,3)),"conditional":(0,(7,3)),
                "observe":(0,(1,2.5)),"zoom":(0,(3,2))}
        item=FancyArrowPatch(start,end,arrowstyle=styles[kind],mutation_scale=8.5,
                             connectionstyle=f"arc3,rad={rad}",shrinkA=0,shrinkB=0,
                             linewidth=1.1,edgecolor=color,facecolor=color if kind in ("process","intervention") else "none",zorder=3)
        if kind in dashes:item.set_linestyle(dashes[kind])
        self.ax.add_patch(item);self.add(name,item,kind)
        if label:
            pos=label_xy or ((start[0]+end[0])/2,(start[1]+end[1])/2+4)
            self.text(name+".label",label,pos,size=8.5,color="muted")
        self.spec["relations_drawn"].append({"id":name,"kind":kind,"source":source,"target":target,"label":label})
        return item

    def bracket(self,name,x0,x1,y,*,color="ink",depth=1.5):
        return self.line(name,[(x0,y+depth),(x0,y),(x1,y),(x1,y+depth)],width=.8,color=color,role="set_or_region")

    def dna(self,name,x,y,w,*,gap=4,color="primary",region=None,rungs=True):
        if region:
            rx,rw=region
            self.rect(name+".region",(rx,y-.6),rw,gap+1.2,color="accent",weight=.18,radius=0,role="region_fill")
        self.line(name+".upper",[(x,y+gap),(x+w,y+gap)],color=color)
        self.line(name+".lower",[(x,y),(x+w,y)],color=color)
        if rungs:
            for i,xx in enumerate(np.arange(x+2,x+w,3)):
                self.line(name+f".pair.{i}",[(xx,y),(xx,y+gap)],color=color,width=.8)

    def strand(self,name,x,y,w,*,color="primary",dashed=False):
        return self.line(name,[(x,y),(x+w,y)],color=color,width=1.5,dashed=dashed)

    def segments(self,name,labels,x,y,*,segment_w=12,h=6,gap=2,color="primary"):
        for i,value in enumerate(labels):
            xx=x+i*(segment_w+gap)
            self.rect(f"{name}.segment.{i}",(xx,y),segment_w,h,color=color,radius=0)
            self.text(f"{name}.label.{i}",str(value),(xx+segment_w/2,y+h/2),size=8.5)
            if i:self.line(f"{name}.join.{i}",[(xx-gap,y+h/2),(xx,y+h/2)],color=color,width=.8)

    def result(self):
        return BuildResult(self.figure,self.ax,self.artists,self.spec)
