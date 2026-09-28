"""Assemble a local, offline figure catalog and vector review volume."""
from pathlib import Path
import html
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from PIL import Image,ImageDraw,ImageFont
import pymupdf
from book_style import FONT_PATH


def main():
    specs=[json.loads(p.read_text()) for p in sorted((ROOT/'figure_specs').glob('F??.json'))]
    assert len(specs)==30
    cards=[];md=['# 《运行生命》全书图索引','',
      '版本 1.0。按原稿图号排序；图题逐字保留。成图、完整代码、认知任务、布局理由与复用组件均可在下方找到。',
      '', '[浏览全部成图](FIGURE_INDEX.html) · [30 页矢量合订本](Running_Life_F01-F30.pdf) · [配色规范](PALETTE_SPECIFICATION.md) · [维护说明](MAINTENANCE.md)', '']
    trace=['# 图与原稿来源对应','', 'P编号来自本次原稿的顶层段落顺序；不改动原 DOCX。各图是概念示意，F22为原稿明确设定的假设人数。', '']
    volume=pymupdf.open();toc=[]
    overview=Image.new('RGB',(2100,30//5*405+70),'#F4F5F4')
    font=ImageFont.truetype(str(FONT_PATH),17)
    ImageDraw.Draw(overview).text((25,20),'《运行生命》F01–F30 · 海青与铜',font=ImageFont.truetype(str(FONT_PATH),27),fill='#26353E')
    for i,s in enumerate(specs):
        fid=s['id'];src=next((ROOT/'figures').glob(fid+'_*.py'));stem=src.stem
        links={f:f'outputs/{f}/{stem}.{f}' for f in ['png','pdf','svg']};links['Python']=str(src.relative_to(ROOT))
        caption=f"图 {fid}｜{s['title']}"
        linktext=' · '.join(f'[{k}]({v})' for k,v in links.items())
        md += [f'## {caption}','',f"**认知任务：** {s['cognitive_task']}",'',f"**布局理由：** {s['layout_rationale']}",'',f"**复用组件：** {s['components']}",'',linktext,'',f"![{caption}]({links['png']})",'']
        trace += [f'## {caption}','',s['source_paragraphs'],'',f"关系边界：{s['relationships']}",'',f"防止误读：{s['misconceptions']}",'']
        esc=html.escape
        linkhtml=''.join(f'<a href="{esc(v)}">{esc(k)}</a>' for k,v in links.items())
        code=esc(src.read_text())
        cards.append(f'''<article id="{fid}"><div class="eyebrow">{fid} / 30</div><h2>{esc(caption)}</h2>
        <p class="task">{esc(s['cognitive_task'])}</p><img src="{esc(links['png'])}" alt="{esc(caption)}" loading="lazy">
        <div class="links">{linkhtml}</div><dl><dt>布局理由</dt><dd>{esc(s['layout_rationale'])}</dd><dt>复用组件</dt><dd>{esc(s['components'])}</dd><dt>书稿来源</dt><dd>{esc(s['source_paragraphs'])}</dd></dl>
        <details><summary>完整 Python 代码</summary><pre><code>{code}</code></pre></details></article>''')
        pdf=pymupdf.open(ROOT/links['pdf']);volume.insert_pdf(pdf);toc.append([1,caption,i+1]);pdf.close()
        preview=Image.open(ROOT/links['png']).convert('RGB');preview.thumbnail((400,330))
        x=(i%5)*420+10;y=(i//5)*405+70
        overview.paste(preview,(x+(400-preview.width)//2,y))
        draw=ImageDraw.Draw(overview);label=fid+' '+s['title'];wrap=[label[j:j+19] for j in range(0,len(label),19)]
        for j,line in enumerate(wrap):draw.text((x+5,y+337+j*24),line,font=font,fill='#26353E')
    volume.set_toc(toc);volume.set_metadata({'title':'运行生命 F01–F30 全书配图','author':'','subject':'科学机制图；原图题作为书签'})
    volume.save(ROOT/'Running_Life_F01-F30.pdf',deflate=True,garbage=4);volume.close()
    overview.save(ROOT/'OVERVIEW.jpg',quality=94)
    (ROOT/'FIGURE_INDEX.md').write_text('\n'.join(md))
    (ROOT/'SOURCE_TRACEABILITY.md').write_text('\n'.join(trace))
    nav=''.join(f'<a href="#F{n:02d}">F{n:02d}</a>' for n in range(1,31))
    css='''*{box-sizing:border-box}body{margin:0;background:#eef2f2;color:#26353E;font-family:Arial,"Noto Sans SC","PingFang SC",sans-serif;font-size:16px;line-height:1.7}header{max-width:1050px;margin:48px auto 28px;padding:0 32px}h1{font-size:34px;letter-spacing:.02em}h2{font-size:24px;line-height:1.5;margin:.25em 0}.intro{max-width:800px}nav{display:flex;flex-wrap:wrap;gap:5px;margin:28px 0}a{color:#2F6174;text-decoration:none}nav a,.links a{border:1px solid #ccd8dc;padding:6px 11px;border-radius:4px;background:white}main{max-width:1050px;margin:auto;padding:0 32px 64px}article{background:white;border:1px solid #dbe3e3;padding:34px;margin-bottom:26px;border-radius:8px;scroll-margin-top:16px}.eyebrow{color:#A6633F;font-size:13px;letter-spacing:.08em}.task{font-size:18px}img{display:block;width:100%;height:auto;border:1px solid #edf0ef;margin:22px 0}.links{display:flex;gap:10px;flex-wrap:wrap}dl{font-size:15px}dt{font-weight:600;margin-top:13px}dd{margin:2px 0;color:#53636b}summary{cursor:pointer;color:#2F6174}pre{font-size:12px;line-height:1.65;overflow:auto;background:#f4f6f5;padding:20px}footer{font-size:14px;color:#677278}@media(max-width:600px){main{padding:0 12px}header{padding:0 18px}article{padding:18px}h2{font-size:20px}}@media print{nav,.links,details{display:none}body{background:white}article{break-inside:avoid;border:0}}'''
    body=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>运行生命 · 全书配图</title><style>{css}</style><header><div class="eyebrow">RUNNING LIFE · FIGURE SYSTEM 1.0</div><h1>《运行生命》全书配图</h1><p class="intro">30 张科学机制图，统一采用「海青与铜」。每张图保留原稿标题，附成图、完整源码与布局说明。本页可离线浏览。</p><p><a href="Running_Life_F01-F30.pdf">30 页矢量合订本</a> · <a href="PALETTE_SPECIFICATION.md">统一配色</a> · <a href="MAINTENANCE.md">维护说明</a> · <a href="audit/">审计记录</a></p><nav>{nav}</nav></header><main>{''.join(cards)}<footer>概念图不按真实比例。除 F22 的原稿假设人数外不引入定量数据。sRGB 交付；实体印刷、真人理解、Tavotto 回放及全部编辑器兼容性尚未验证。</footer></main></html>'''
    (ROOT/'FIGURE_INDEX.html').write_text(body)
    print('Catalog, traceability, overview and 30-page vector PDF updated.')

if __name__=='__main__':main()
