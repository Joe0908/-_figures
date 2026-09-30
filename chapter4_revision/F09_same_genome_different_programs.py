"""Question figure: shared DNA, contrasting products and cell functions."""
from chapter_drawing import *

def build_figure():
    d=ChapterDrawing('F09',152,'同一套基因组，不同细胞程序','提出问题；不提前解释调控机制')
    d.heading('title','同一套 DNA，为什么形成不同细胞？',(7,142))
    d.text('genome','同一套基因组',(85,126))
    d.edge('branch.left',(71,120),(43,112),kind='order')
    d.edge('branch.right',(99,120),(127,112),kind='order')
    for name,cx in [('neuron',43),('skin',127)]:
        d.dna(name+'.dna',cx-23,104,46,gap=3)
        d.text(name+'.same','相同 DNA',(cx,97),size=NOTE)
        d.edge(name+'.to.rna',(cx,92),(cx,90),kind='order')
        d.text(name+'.rna.label','RNA 组合',(cx,86))
        for i,offset in enumerate([0,5,10] if name=='neuron' else [0,7]):
            xx=np.linspace(cx-20,cx+20-(i*3 if name=='neuron' else 0),80)
            d.line(name+f'.rna.{i}',np.c_[xx,78-offset+1.2*np.sin((xx-cx)*.6)],color=SECONDARY)
        d.edge(name+'.to.protein',(cx,63),(cx,60),kind='process')
        d.text(name+'.protein.label','蛋白质组合',(cx,56))
        for i,(dx,letter) in enumerate([(-14,'A'),(0,'B'),(14,'C')] if name=='neuron' else [(-14,'B'),(0,'B'),(14,'A')]):
            d.protein(name+f'.protein.{i}',cx+dx,45,letter)
            label=d.artists.pop(f'F09.{name}.protein.{i}.label');label.remove()
        d.edge(name+'.to.cell',(cx,38),(cx,34),kind='process')
    # Cell morphology is informative without importing a regulatory mechanism.
    d.ellipse('neuron.soma',(43,24),12,9,color=PRIMARY)
    for i,pts in enumerate([[(37,26),(27,29),(22,34)],[(37,23),(24,21),(17,26)],[(48,26),(58,30),(63,35)],[(48,22),(65,20),(72,23)]]):
        d.line(f'neuron.process.{i}',pts,color=PRIMARY)
    for i,x in enumerate([108,122,136]):
        d.rect(f'skin.cell.{i}',(x,20),13,10,color=PRIMARY,radius=1.2)
    d.text('neuron.function','神经元：传递信号',(43,10),size=NOTE)
    d.text('skin.function','皮肤细胞：形成屏障',(127,10),size=NOTE)
    return d.result()

if __name__=='__main__':export(build_figure(),__file__)
