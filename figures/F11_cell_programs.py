"""F11: 同一基因组运行不同细胞程序. Geometry is in millimetres."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing


def draw_program_row(c, key, y, cell_name, version, function):
    c.text(key+'.cell', cell_name, (26, y+13), size=9)
    c.dna(key+'.dna', 15, y-2, 23, gap=4)
    c.node(key+'.regulation', '可接近区域\n与调控组合 '+version, (65,y), w=36,h=19,size=9)
    c.text(key+'.products.label','组合 '+version,(108,y+7),size=9)
    for i in range(3):
        lengths=(12,9,14) if version=='A' else (8,14,10)
        c.strand(key+f'.rna.{i}',94,y-1-i*3,lengths[i],color='primary' if (i+(version=='B'))%2==0 else 'secondary')
        c.circle(key+f'.protein.{i}',(113+i*4,y-4),1.3,color='supplement' if (i+(version=='B'))%2==0 else 'secondary')
    c.node(key+'.function', function, (148,y),w=29,h=18,color='secondary',size=9)
    for j,(x0,x1) in enumerate(((40,45),(85,91),(125,131))):
        c.edge(key+f'.influence.{j}',(x0,y),(x1,y),kind='conditional')


def build_figure():
    c=Drawing('F11',height=116)
    c.heading('shared.heading','相近的信息背景，不同的使用程序',(6,107))
    for i,(x,value) in enumerate(((26,'相近 DNA'),(65,'调控状态'),(108,'RNA 与蛋白'),(148,'细胞工作'))):
        c.text(f'column.{i}',value,(x,96),size=9)
    draw_program_row(c,'neuron',76,'神经元','A','信号传递')
    draw_program_row(c,'skin',39,'皮肤细胞','B','屏障与更新')
    c.line('row.separator',[(8,57),(162,57)],color='muted',width=.8,dashed=True)
    c.note('示意：DNA高度相似；图符不是实测数量，也不表示单一基因决定细胞身份。')
    return c.result()


def main():
    from production_utils import export_figure
    result=build_figure(); fig=result.figure; OUT=Path(__file__).resolve().parent
    fig.savefig(OUT/'F11_cell_programs.pdf',metadata={'CreationDate':None,'ModDate':None})
    return export_figure(result,ROOT,OUT/'F11_cell_programs.pdf')


if __name__=='__main__':
    main()
