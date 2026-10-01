"""F22: PRS percentile groups, a symbolic pyramid, not a probability distribution.
Run from any directory: python chapter8_revision/F22_prs_percentile_pyramid.py
Adjust LAYOUT and LABELS below. All geometry is in mm; output width is 108 mm.
"""
from pathlib import Path
import sys, json, hashlib, io, base64, re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from fontTools import subset
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from book_style import rc_settings, font_properties, FONT_PATH, missing_glyphs
from palette import PRIMARY, SECONDARY, ACCENT, INK, MUTED, tint
HERE=Path(__file__).resolve().parent
LAYOUT=dict(width=108,height=116,center=28.5,left=5,right=52,base=45,tip=98,
            label_x=57,leader_end=54,font=9,note_font=8.5)
LABELS=[('较高遗传风险','前 10%','第90百分位及以上'),
        ('中间遗传风险','中间 80%','第10至90百分位之间'),
        ('较低遗传风险','后 10%','第10百分位以下')]

def build_figure():
    L=LAYOUT
    with plt.rc_context(rc_settings()):
        fig=plt.figure(figsize=(L['width']/25.4,L['height']/25.4))
        ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,L['width']),ylim=(0,L['height']));ax.axis('off')
        labels=[]
        def text(name,txt,x,y,size=9,color=INK,ha='left'):
            t=ax.text(x,y,txt,fontproperties=font_properties(size),color=color,ha=ha,va='center')
            t.set_gid('F22.'+name);labels.append(t);return t
        text('title','PRS 百分位：在参考人群中的位置',4,110,10.5)
        def bounds(y):
            f=(L['tip']-y)/(L['tip']-L['base'])
            return L['center']-(L['center']-L['left'])*f,L['center']+(L['right']-L['center'])*f
        edges=[98,80.333333,62.666667,45]
        for i,(top,bot,col,lines) in enumerate(zip(edges,edges[1:],[ACCENT,PRIMARY,SECONDARY],LABELS)):
            lt,rt=bounds(top);lb,rb=bounds(bot)
            poly=Polygon([(lt,top),(rt,top),(rb,bot),(lb,bot)],closed=True,
                         facecolor=tint(col,.16),edgecolor=col,lw=.9)
            poly.set_gid(f'F22.tier.{i}');ax.add_patch(poly)
            yy=(top+bot)/2;_,right=bounds(yy)
            ax.plot([right+1,L['leader_end']],[yy,yy],color=col,lw=.7)
            for j,txt in enumerate(lines):text(f'tier.{i}.label.{j}',txt,L['label_x'],yy+4.5-j*4.5,9 if j<2 else 8.5,col if j==0 else INK)
        text('example','第95百分位 ≠ 95%的患病概率',4,32,10,ACCENT)
        text('interpretation','表示分数高于参考人群中约95%的人。',4,25,9)
        text('threshold.note','分组界线仅为示例，不是统一的临床标准。',4,13,8.5,MUTED)
        text('geometry.note','金字塔宽度不表示人数或患病概率。',4,7,8.5,MUTED)
        fig.canvas.draw();renderer=fig.canvas.get_renderer()
        boxes=[t.get_window_extent(renderer) for t in labels]
        errors=[]
        for i,a in enumerate(boxes):
            if not fig.bbox.contains(a.x0,a.y0) or not fig.bbox.contains(a.x1,a.y1):errors.append('out of bounds: '+labels[i].get_gid())
            for j,b in enumerate(boxes[:i]):
                if a.overlaps(b):errors.append('text overlap: '+labels[i].get_gid()+' / '+labels[j].get_gid())
        missing=missing_glyphs(''.join(t.get_text() for t in labels))
        if errors or missing:raise ValueError((errors,missing))
        return fig,labels

def main():
    fig,labels=build_figure();stem=Path(__file__).stem;outputs={}
    with plt.rc_context(rc_settings()):
        for fmt in ['png','pdf','svg']:
            p=HERE/'outputs'/fmt/(stem+'.'+fmt);p.parent.mkdir(parents=True,exist_ok=True)
            fig.savefig(p,dpi=600,metadata={'Date':None} if fmt=='svg' else {'CreationDate':None,'ModDate':None} if fmt=='pdf' else None)
            outputs[fmt]=p
    # Preserve editable SVG text and bundle the used font glyphs.
    opts=subset.Options();opts.flavor='woff';font=subset.load_font(str(FONT_PATH),opts)
    sub=subset.Subsetter(options=opts);sub.populate(text=''.join(t.get_text() for t in labels));sub.subset(font)
    font.flavor='woff';buf=io.BytesIO();font.save(buf)
    css='<style type="text/css">@font-face {font-family: "Noto Sans SC"; src: url(data:font/woff;base64,'+base64.b64encode(buf.getvalue()).decode()+') format("woff");}</style>'
    svg=outputs['svg'].read_text();svg=svg.replace('<defs>','<defs>'+css,1);outputs['svg'].write_text(svg)
    record={'figure':'F22','size_mm':[108,116],'palette':'海青与铜','illustrative_percentile_groups':[10,80,10],
            'geometry_represents_population_size':False,'clinical_threshold':False,'example_percentile':95,
            'minimum_font_pt':8.5,'text_bounds_and_overlap':'passed','glyph_check':'passed',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'outputs':{k:{'path':str(v.relative_to(HERE)),'sha256':hashlib.sha256(v.read_bytes()).hexdigest()} for k,v in outputs.items()}}
    p=HERE/'outputs'/'manifests'/'F22_validation.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(record,ensure_ascii=False,indent=2))
    print(json.dumps(record,ensure_ascii=False,indent=2));plt.close(fig)
if __name__=='__main__':main()
