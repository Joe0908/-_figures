"""SMN2 splicing before/after nusinersen, for novice readers.

Run from any directory with the repository requirements installed.
Only exons 6--8 are shown. Arrow widths/shape counts encode no quantities.
"""
from chapter_drawing import ChapterDrawing, export, PRIMARY, ACCENT, MUTED, tint


def rna(d, name, center, y, include7=True, initial=False):
    labels = [6, 7, 8] if include7 else [6, 8]
    positions = [center-20, center, center+20] if include7 else [center-10, center+10]
    for i, (label, x) in enumerate(zip(labels, positions)):
        if i:
            d.line(name+f'.join.{i}', [(positions[i-1]+6,y),(x-6,y)], color=PRIMARY)
        color = ACCENT if label == 7 else PRIMARY
        d.rect(name+f'.exon.{label}', (x-6,y-4), 12,8,
               color=color, fill=tint(color,.16), radius=0)
        d.text(name+f'.number.{label}', str(label), (x,y), size=14.5)
    return positions


def build_figure():
    d = ChapterDrawing('F25a', 184, '借助 SMN2 改变 RNA 剪接',
                       '看懂药物作用于初始 RNA，使第7外显子更常被保留，增加完整 SMN 蛋白。')
    d.spec['source_document'] = '运行生命_第五部分_段落版(1).docx'
    d.spec['sources'] = [
        'https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=dd70cd5f-b0fc-4ba4-a5ea-89a34778bd94&type=display',
        'https://medlineplus.gov/genetics/gene/smn2/',
    ]
    d.text('title','借助 SMN2，改变 RNA 剪接',(85,174),size=19)
    d.text('context','SMN1 功能缺失或不足，完整 SMN 蛋白不够',(85,161))
    d.text('baseline','SMN2 原本也能产生少量完整蛋白',(85,151),size=13.5,color=MUTED)
    d.text('dna.label','SMN2 DNA 序列不被药物改写',(85,139))
    d.dna('dna',63,126,44,gap=3)
    d.edge('transcription.left',(70,124),(43,119),kind='template')
    d.edge('transcription.right',(100,124),(127,119),kind='template')

    for side,c,title in [('left',43,'不使用 nusinersen'),('right',127,'使用 nusinersen 后')]:
        d.text(side+'.title',title,(c,112),size=16)
        d.text(side+'.pre.label','SMN2 初始 RNA',(c,102))
        rna(d,side+'.pre',c,92,initial=True)

    # The ASO binds INTRON 7, downstream of exon 7, not exon 7 itself.
    d.line('drug.contact',[(137,92),(137,85)],color=ACCENT,width=.8)
    d.line('drug.aso',[(134,85),(140,85)],color=ACCENT,width=3.2)
    d.text('drug.label','药物结合初始 RNA 的内含子',(127,77),size=13.5,color=ACCENT)
    d.text('left.splice.label','常跳过第7外显子',(43,77))
    d.text('right.splice.label','第7外显子更常被保留',(127,68))
    for side,c in [('left',43),('right',127)]:
        d.edge(side+'.splicing',(c,61),(c,55),kind='process')
        rna(d,side+'.mature',c,49,include7=side=='right')
        d.text(side+'.mature.label','剪接后的 RNA',(c,39),size=13.5)
        d.edge(side+'.translation',(c,34),(c,27),kind='process')
    d.text('left.protein','主要产生不稳定的蛋白',(43,21),size=14.5)
    d.text('right.protein','完整 SMN 蛋白增加',(127,21),size=14.5,color=PRIMARY)
    d.text('legend','方块是外显子；初始 RNA 中连接方块的线是内含子。',(85,11),size=13.5,color=MUTED)
    # Keep the explanatory limitation in the index/caption so this figure can
    # retain legible type at the supplied 108-mm text-column width.
    d.spec['scope'] = '仅画第6—8外显子。展示常见剪接结果；SMN2 原本也会产生少量完整蛋白。不表示每条 RNA 都走同一路径，也不表示临床疗效。'
    return d.result()


if __name__ == '__main__':
    export(build_figure(), __file__)
