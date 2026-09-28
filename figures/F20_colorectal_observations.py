"""F20: 从结肠组织到结直肠癌的跨层观察. Paired, not longitudinal samples."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from shared_shapes import Drawing


def build_figure():
    c=Drawing('F20',height=140)
    c.text('person','同一个人的两份组织样本',(85,131),size=11.5)
    c.node('sample.mucosa','非肿瘤结肠黏膜',(67,114),w=58,h=15,color='secondary',size=9.5)
    c.node('sample.tumor','结直肠癌组织',(133,114),w=58,h=15,color='secondary',size=9.5)
    c.edge('sampling.mucosa',(72,126),(67,123),kind='observe')
    c.edge('sampling.tumor',(108,126),(133,123),kind='observe')
    rows=[
        ('dna',94,'DNA','共同遗传背景','体细胞生长控制变化\n提供可能线索'),
        ('rna',76,'RNA','成熟组织程序','分裂与合成程序\n可能增强'),
        ('protein',58,'蛋白质','日常工作的执行分子','数量／状态可能改变'),
        ('metabolism',40,'代谢物','日常资源利用','资源分配可能改变'),
        ('tissue',22,'组织行为','结构维持与更新','细胞增多／排列紊乱'),
    ]
    for key,y,layer,left,right in rows:
        c.text('layer.'+key,layer,(20,y),size=9)
        c.node('mucosa.'+key,left,(67,y),w=58,h=14,color='secondary',size=8.5)
        c.node('tumor.'+key,right,(133,y),w=58,h=14,color='primary',size=8.5)
    c.note('配对观察示意，不是同一组织的时间演变；跨层解释仍待检验，并非总会同向变化。')
    return c.result()


def main():
    from production_utils import export_figure
    result=build_figure();fig=result.figure;OUT=Path(__file__).resolve().parent
    fig.savefig(OUT/'F20_colorectal_observations.pdf',metadata={'CreationDate':None,'ModDate':None})
    return export_figure(result,ROOT,OUT/'F20_colorectal_observations.pdf')


if __name__=='__main__':
    main()
