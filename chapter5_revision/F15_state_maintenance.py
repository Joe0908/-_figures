"""F15: partial state maintenance and rebuilding, rather than perfect copying."""
from chapter_drawing import ChapterDrawing, export, PRIMARY, ACCENT, SUPPLEMENT, SECONDARY, MUTED, NOTE

LAYOUT=dict(height=216, parent_x=22, daughter_x=80, maintained_x=138)

def build_figure():
    c=ChapterDrawing('F15',LAYOUT['height'],
        'DNA 复制以后，部分表观状态如何得到维持或重建',
        '看见旧链与旧组蛋白留下部分线索，状态延续还依赖持续的调控活动。')
    c.spec['source_paragraphs']=[51,52,53,54,55,56,57,58,59]
    c.heading('a.heading','A  部分 DNA 甲基化模式的维持',(6,205))
    for name,x,label in [('parent',22,'复制前'),('daughter',80,'复制后'),('maintained',138,'甲基化维持后')]:
        c.text('a.'+name+'.heading',label,(x+7,191),size=NOTE)
    c.cpg('a.parent',22,150,upper_mark=True,lower_mark=True)
    c.cpg('a.daughter.1',80,170,upper_mark=True,lower_new=True)
    c.cpg('a.daughter.2',80,133,lower_mark=True,upper_new=True)
    c.cpg('a.maintained.1',138,170,upper_mark=True,lower_mark=True,lower_new=True)
    c.cpg('a.maintained.2',138,133,upper_mark=True,lower_mark=True,upper_new=True)
    c.edge('a.replication.1',(49,156),(68,169),kind='process')
    c.edge('a.replication.2',(49,144),(68,134),kind='process')
    c.edge('a.maintenance.1',(105,170),(125,170),kind='process')
    c.edge('a.maintenance.2',(105,133),(125,133),kind='process')
    c.text('a.explanation','旧链保留的甲基化，可帮助相关分子在新链建立修饰。',(6,109),size=NOTE,ha='left',color=MUTED)
    c.line('a.key.old',[(8,97),(19,97)],color=PRIMARY)
    c.text('a.key.old.label','旧链',(22,97),size=NOTE,ha='left')
    c.line('a.key.new',[(47,97),(58,97)],color=SECONDARY,dashed=True)
    c.text('a.key.new.label','新链',(61,97),size=NOTE,ha='left')
    c.circle('a.key.methyl',(91,97),1.7,color=ACCENT,fill=ACCENT)
    c.text('a.key.methyl.label','甲基（只标 C）',(98,97),size=NOTE,ha='left')

    c.heading('b.heading','B  旧组蛋白保留，新组蛋白加入',(6,83))
    # One schematic parental pair redistributes across two daughter regions.
    c.line('b.parent.dna',[(12,61),(61,61)])
    c.nucleosome('b.parent.h1',25,61,modified=True)
    c.nucleosome('b.parent.h2',48,61,modified=True)
    for tag,y,oldx,newx in [('d1',67,101,142),('d2',42,142,101)]:
        c.line('b.'+tag+'.dna',[(87,y),(157,y)])
        c.nucleosome('b.'+tag+'.old',oldx,y,modified=True)
        c.nucleosome('b.'+tag+'.new',newx,y,new=True)
    c.edge('b.redistribute.1',(64,64),(83,67),kind='process')
    c.edge('b.redistribute.2',(64,55),(83,42),kind='process')
    c.text('b.parent.label','复制前',(36,42),size=NOTE)
    c.text('b.old.label','填色：旧组蛋白；空心：新组蛋白',(6,25),size=NOTE,ha='left')
    c.note('图示数量不代表比例；部分状态还需调控分子持续参与重建。',y=10)
    return c.result()

def main():
    return export(build_figure(),__file__)

if __name__=='__main__':
    main()
