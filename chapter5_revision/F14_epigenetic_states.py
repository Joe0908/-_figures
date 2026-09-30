"""F14: chemical modification and packaging change without sequence change."""
from chapter_drawing import ChapterDrawing, export, PRIMARY, ACCENT, SUPPLEMENT, MUTED, tint, NOTE

LAYOUT = dict(height=180, sequence_y=151, acetyl_y=100, remodel_y=46)

def build_figure():
    c=ChapterDrawing('F14',LAYOUT['height'],
        '相同的 DNA 序列，不同的化学与染色质状态',
        '区分 DNA 甲基化、组蛋白乙酰化与核小体位置调整，不把它们等同于表达开关。')
    c.spec['source_paragraphs']=[19,20,21,23,24,25,26,29,31,32,33,34,35,36]
    c.heading('a.heading','A  DNA 自身的化学修饰',(6,169))
    for tag,x,modified in [('plain',16,False),('methyl',110,True)]:
        for i,ch in enumerate('ATCGAT'):
            c.text('a.'+tag+f'.base.{i}',ch,(x+6.8*i,151))
        if modified:
            c.circle('a.methyl.mark',(x+13.6,159),1.7,color=ACCENT,fill=ACCENT)
        c.text('a.'+tag+'.label','C 未带甲基' if not modified else 'C 上带甲基',(x+17,137),size=NOTE)
    c.edge('a.add.methyl',(61,151),(98,151),kind='process')
    c.text('a.process.label','添加甲基',(80,161),size=NOTE)
    c.text('a.conclusion','字母顺序相同；蛋白质的结合机会可能改变。',(6,125),size=NOTE,ha='left',color=MUTED)

    c.heading('b.heading','B  组蛋白的化学修饰',(6,113))
    for tag,x,modified in [('plain',30,False),('acetyl',121,True)]:
        c.nucleosome('b.'+tag,x,94,modified=modified)
        c.line('b.'+tag+'.left',[(x-18,94),(x-7,94)])
        c.line('b.'+tag+'.right',[(x+7,94),(x+18,94)])
    c.edge('b.add.acetyl',(55,94),(95,94),kind='process')
    c.text('b.process.label','添加乙酰基',(75,102),size=NOTE)
    c.text('b.plain.label','组蛋白',(30,80),size=NOTE)
    c.text('b.acetyl.label','带乙酰基的组蛋白',(121,80),size=NOTE)
    c.text('b.conclusion','局部相互作用、修饰识别蛋白的结合可能改变。',(6,68),size=NOTE,ha='left',color=MUTED)

    c.heading('c.heading','C  核小体位置的调整',(6,57))
    for tag,left,nuc in [('covered',10,32),('exposed',102,145)]:
        c.line('c.'+tag+'.dna',[(left,38),(left+55,38)])
        if tag=='covered':
            c.rect('c.covered.site',(left+16,34),12,8,color=ACCENT,fill=tint(ACCENT,.18),radius=0,role='region_fill')
            c.nucleosome('c.covered.nuc',nuc,38)
        else:
            c.rect('c.exposed.site',(left+16,34),12,8,color=ACCENT,fill=tint(ACCENT,.18),radius=0,role='region_fill')
            c.nucleosome('c.exposed.nuc',nuc,38)
        c.text('c.'+tag+'.label','识别位置不易接近' if tag=='covered' else '同一位置更易接近',(left+27.5,25),size=NOTE)
    c.edge('c.remodel',(68,38),(96,38),kind='process')
    c.text('c.process.label','位置调整',(82,47),size=NOTE)
    c.note('乙酰化不等于核小体移动；更易接近也不保证转录。',y=10)
    return c.result()

def main():
    return export(build_figure(),__file__)

if __name__=='__main__':
    main()
