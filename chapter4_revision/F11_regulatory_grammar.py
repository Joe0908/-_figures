"""Identical motif types and TFs; altered spacing/order changes contact geometry."""
from chapter_drawing import *

def build_figure():
    d=ChapterDrawing('F11',145,'相同识别位置，不同组合关系','用相同蛋白质对照间距与顺序，建立调控语法的物理含义')
    d.heading('title','识别位置相同，接触机会可以不同',(7,135))
    d.text('key','A / B / C：三类结合基序；上方是对应转录因子',(85,122),size=NOTE)
    rows=[(97,[48,67,86],['A','B','C'],'原有间距'),(65,[48,100,119],['A','B','C'],'拉大间距'),(33,[48,67,86],['C','B','A'],'改变顺序')]
    for n,(y,xs,letters,label) in enumerate(rows):
        d.text(f'row.{n}.label',label,(7,y+9),ha='left')
        d.region(f'row.{n}.enhancer',39,y,91,ENH)
        d.line(f'row.{n}.dna.upper',[(35,y+3.2),(135,y+3.2)],color=DNA)
        d.line(f'row.{n}.dna.lower',[(35,y-3.2),(135,y-3.2)],color=DNA)
        for i,(x,letter) in enumerate(zip(xs,letters)):
            d.motif(f'row.{n}.motif.{i}',x,y,letter)
            d.protein(f'row.{n}.tf.{i}',x,y+15,letter)
            d.line(f'row.{n}.binding.{i}',[(x,y+9),(x,y+4.6)],color=MUTED,width=.8)
        for i in range(2):
            d.edge(f'row.{n}.contact.{i}',(xs[i]+6.7,y+15),(xs[i+1]-6.7,y+15),kind='order')
            d.artists[f'F11.row.{n}.contact.{i}'].set_linestyle((0,(3,2)))
        d.text(f'row.{n}.physics',('邻近机会' if n==0 else '距离改变' if n==1 else '邻居改变'),(158,y+9),ha='right',size=NOTE)
    d.note('线表示接触机会；不预设哪种排列一定使表达更强。',y=10)
    return d.result()

if __name__=='__main__':export(build_figure(),__file__)
