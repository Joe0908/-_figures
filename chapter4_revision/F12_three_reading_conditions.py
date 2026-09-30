"""One controlled three-panel comparison: access, reader, spatial opportunity."""
from chapter_drawing import *

def build_figure():
    d=ChapterDrawing('F12',252,'看得到吗？谁来读？碰得到吗？','每个 panel 只改变一个条件；三者构成统一读取环境')
    # a: retain the same unbound TF on both sides; only local packaging differs.
    y=174
    d.heading('a.title','a　看得到吗？',(7,y+68))
    d.text('a.left.state','较易接近',(46,y+51))
    d.text('a.right.state','包装遮挡较多',(129,y+51))
    for n,x in [('left',9),('right',93)]:
        d.mini_locus('a.'+n,x,y+23,packaged=n=='right')
        d.protein('a.'+n+'.available.tf',x+20.5,y+38)
    d.text('a.conclusion','同一序列；被接近的机会不同',(85,y+2),size=NOTE)
    # b: identical loci and packaging; one side lacks the corresponding TF.
    y=91
    d.heading('b.title','b　谁来读？',(7,y+68))
    d.text('b.left.state','有匹配、活跃的因子',(46,y+51),size=NOTE)
    d.text('b.right.state','缺少相应活跃因子',(129,y+51),size=NOTE)
    for n,x in [('left',9),('right',93)]:
        d.mini_locus('b.'+n,x,y+23)
    d.protein('b.left.tf',29.5,y+38)
    d.edge('b.recognition',(29.5,y+32),(29.5,y+28),kind='template')
    d.text('b.conclusion','同一基序、同样可接近；参与读取的蛋白质不同',(85,y+2),size=NOTE)
    # c: same regions and proteins; only the folding changes.
    y=8
    d.heading('c.title','c　碰得到吗？',(7,y+68))
    d.text('c.left.state','线性序列上相距较远',(46,y+57),size=NOTE)
    d.text('c.right.state','折叠后空间靠近',(129,y+60),size=NOTE)
    d.mini_locus('c.linear',9,y+30)
    d.protein('c.linear.tf',29.5,y+42)
    d.ellipse('c.linear.machine',(65.5,y+42),28,9,color=MACHINE,weight=.12,role='protein')
    d.text('c.linear.machine.label','转录机器',(65.5,y+42),size=NOTE)
    # A continuous DNA curve, no enhancer-to-promoter on-switch arrow.
    from matplotlib.path import Path as MplPath
    from matplotlib.patches import PathPatch
    vertices=[(96,y+24),(101,y+30),(124,y+30),(154,y+65),(164,y+40),(138,y+24),
              (129,y+24),(140,y+18),(152,y+18),(162,y+24)]
    codes=[MplPath.MOVETO,MplPath.LINETO,MplPath.LINETO,MplPath.CURVE4,MplPath.CURVE4,
           MplPath.CURVE4,MplPath.LINETO,MplPath.LINETO,MplPath.LINETO,MplPath.LINETO]
    # The motif is represented by a short sequence block; the DNA rail runs
    # along its edge so the letter never sits under a drawn stroke.
    vertices[1]=(101,y+33.2);vertices[2]=(124,y+33.2)
    item=PathPatch(MplPath(vertices,codes),fill=False,edgecolor=DNA,linewidth=1.1)
    d.ax.add_patch(item);d.add('c.fold.dna',item,'structure')
    d.region('c.fold.enhancer',101,y+30,23,ENH)
    d.motif('c.fold.motif',112.5,y+30)
    d.region('c.fold.promoter',129,y+24,9,PROM)
    d.region('c.fold.gene',140,y+18,12,GENE)
    d.protein('c.fold.tf',112.5,y+42)
    d.ellipse('c.fold.machine',(135,y+52),28,9,color=MACHINE,weight=.12,role='protein')
    d.text('c.fold.machine.label','转录机器',(135,y+52),size=NOTE)
    d.edge('c.fold.assembly',(135,y+46),(133.5,y+29.5),kind='template')
    d.edge('c.fold.opportunity',(119.5,y+44),(124.5,y+47),kind='order')
    d.artists['F12.c.fold.opportunity'].set_linestyle((0,(3,2)))
    d.text('c.fold.e.label','增强子',(111,y+12),size=NOTE)
    d.text('c.fold.p.label','启动子',(133.5,y+10),size=NOTE)
    d.line('c.fold.p.guide',[(133.5,y+20),(133.5,y+14)],color=MUTED,width=.8)
    d.text('c.conclusion','空间靠近提供协作机会，不保证转录发生',(85,y+2),size=NOTE)
    return d.result()

if __name__=='__main__':export(build_figure(),__file__)
