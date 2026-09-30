"""Answer figure: sequence possibilities realized through cellular contexts."""
from chapter_drawing import *

def build_figure():
    d=ChapterDrawing('F13',195,'调控可能性怎样成为不同的细胞身份','收束 sequence、grammar、context、output 四层关系')
    d.heading('title','同一套 DNA，怎样产生不同细胞程序',(7,184))
    d.text('genome','同一套基因组',(85,167))
    d.dna('same.dna',62,155,46,gap=3)
    d.edge('to.possibilities',(85,150),(85,143),kind='order')
    d.node('possibilities','调控序列 ＋ 组合关系（调控语法）',(85,132),150,16,size=LABEL)
    d.text('possibilities.scope','提供可能性',(85,116),size=NOTE)
    for n,cx in [('neuron',43),('skin',127)]:
        d.edge(n+'.context.link',(cx,109),(cx,103),kind='order')
        d.rect(n+'.context',(cx-36,69),72,32,color=PRIMARY,weight=.06)
        d.text(n+'.context.heading','一种读取环境' if n=='neuron' else '另一种读取环境',(cx,94))
        d.text(n+'.context.questions','看得到 · 谁来读 · 碰得到',(cx,84),size=NOTE)
        d.text(n+'.context.inputs','发育历史、已有状态、信号',(cx,75),size=NOTE)
        d.edge(n+'.context.to.output',(cx,68),(cx,60),kind='conditional')
        d.text(n+'.expression','不同的基因表达程序',(cx,54))
        d.edge(n+'.to.products',(cx,49),(cx,42),kind='process')
        d.text(n+'.products','不同 RNA / 蛋白质组合',(cx,36),size=NOTE)
        d.edge(n+'.to.function',(cx,30),(cx,23),kind='process')
        d.text(n+'.identity','神经元' if n=='neuron' else '皮肤细胞',(cx,17))
        d.text(n+'.function','突起与信号传递' if n=='neuron' else '连接与屏障功能',(cx,10),size=NOTE)
    
    return d.result()

if __name__=='__main__':export(build_figure(),__file__)
