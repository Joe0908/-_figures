# F01 基因组 染色体 DNA 和基因的关系

本图用于《运行生命》第一章，帮助零基础读者形成三个联系：基因是DNA上的一个区域；长DNA与相关蛋白组织成染色体；整套DNA信息称为基因组。本版按新提示词仅应用「海青与铜」统一配色，保留已交付版本的全部构图、文字、字号、线宽和对象关系，并由Python生成PNG、PDF和SVG。配色角色、三套候选和强度参数见 [COLOR_STYLE_SPEC.md](COLOR_STYLE_SPEC.md)，本次改动见 [COLOR_CHANGELOG.md](COLOR_CHANGELOG.md)。正文和第一阶段文件保持原样，没有制作其他图。

## 查看与使用

- `outputs/png/F01_genome_chromosome_dna_gene.png`：600 dpi预览，4015×2362像素。
- `outputs/pdf/F01_genome_chromosome_dna_gene.pdf`：170×100 mm矢量出版文件，中文字体已嵌入。
- `outputs/svg/F01_genome_chromosome_dna_gene.svg`：170×100 mm，保留可编辑text，嵌入当前用字的WOFF字体子集。已在浏览器实际打开检查。某些矢量编辑器不支持SVG内嵌字体，可加载随包提供的完整TTF，或以PDF作为外观参照。
- `figures/F01_genome_chromosome_dna_gene.py`：唯一单图源码；旁边的同名PDF与出版PDF内容相同，用于保留Tavotto所需的脚本与PDF邻接关系。

170 mm是暂定通栏宽，不是已经确定的书稿版心。主要标签9.5 pt、说明8.5–9 pt、重点标签11.5 pt，均按这个物理尺寸设定；放入Word或排版软件时不要任意缩到半宽。图题沿用原稿，避免在图片顶部重复长图题。

## 图怎样表达关系

左侧实线边界定位有核细胞和细胞核；核内的少量曲线只示意部分染色体。基因组以集合括号和“整套DNA信息”说明表达，不增加一个实体容器。右侧把被选中的染色体画成一条连续的折叠DNA曲线，圆形单独标为相关蛋白；再通过无箭头的虚线放大关系，看到同一DNA的一段。HBB的浅铜色区域覆盖在连续双链上，两端仍有DNA延伸。括号与较粗的局部轨道共同标出区域，所以灰度下仍可辨认。

圆形不代表基因；曲线不代表X形；虚线不表示因果、物质转化或时间顺序。曲线、蛋白个数、DNA横档数、HBB所占宽度均为概念示意，不对应真实数量、HBB序列或长度比例。正文举HBB位于11号染色体，本图借其名称定位“一个基因”，不另画染色体编号图谱。本图聚焦核内DNA的组织，不作为细胞全部DNA位置的穷尽图。

科学依据为原稿P0034–P0042及P0053–P0064，图题为P0044。P号是含空段的零基段落编号，不是Word页码。没有新增疾病、疗效或实验结论。

## 重建

已验证环境为Python 3.12与`requirements.txt`所列版本。首次使用可在自己的虚拟环境安装依赖，然后从本目录执行：

```sh
python -m pip install -r requirements.txt
python figures/F01_genome_chromosome_dna_gene.py
python checks/validate_f01.py
```

脚本没有必填参数；导入模块不会生成文件。`build_figure()`返回Figure、Axes、稳定ID索引的独立Artist和来源说明。`main()`执行布局检查，再导出三种格式及`outputs/manifests/F01_validation.json`。失败会报出相关对象ID，不会静默缩字或删标签。

`fonts/`提供Noto Sans SC Regular静态TTF、OFL许可和来源记录。中文、DNA/HBB等拉丁字符使用同一字体；缺字会使检查失败，不静默改成缺少中文的字体。PDF使用嵌入的TrueType字体；图中没有整张位图、位图文字或AI生成图片。

## 修改在哪里

| 要改什么 | 修改位置 |
| --- | --- |
| 把整个基因区域右移2 mm | 单图文件的`F01Layout.gene_x_mm`从108改为110；高亮、加粗轨道、下括号及两条说明文字的水平中心会同步移动 |
| 改基因区域宽度 | `F01Layout.gene_width_mm`，当前26；仅为版面示意，不表示真实长度 |
| 只微移“基因 HBB”文字 | 用`result.artists["F01.gene.label"].set_position((x, y))`；长期采用应写回布局参数或对应label位置 |
| 移动基因主标签的上下位置 | `F01Layout.gene_label_y_mm`，当前22 |
| DNA段、染色体示意或放大选区的位置 | `F01Layout.dna_box`、`chromosome_box`、`dna_selection`及`chromosome_selection`；大改后连同旁边标签一起检查 |
| 统一字体、字号、线宽、间距和画布 | `book_style.py`中的`BookStyle`；改变画布后也需调整单图布局 |
| 统一集合括号、放大框、DNA区域的画法 | `visual_grammar.py`中的对应函数 |
| 查边界、碰撞和导出 | `layout_utils.py`与`export_utils.py`；结果详见验证JSON |

毫米坐标原点在左下角。`gene_x_mm`约束高亮必须位于DNA段内部；不能把高亮拖离DNA。重要对象均有semantic ID，例如`F01.genome.set_bracket`、`F01.chromosome_example.dna`、`F01.dna.backbone.upper`、`F01.dna.gene_region`。文字、线、圆、边界均是独立Matplotlib对象。F01没有科学方向箭头，因此没有为了展示技术而添加箭头。

## Tavotto微调边界

遵循新提示词：科学对象、标签内容、关系和方向、层级、主要布局必须回到Python；将来小幅文字位移、间距和平衡可保存在受版本控制的Tavotto overrides，稳定重要的微调优先写回Python。本次没有使用override，交付三格式均可直接由Python重建。

脚本保留无参`main()`、显式固定的相邻PDF导出和原生Artist。semantic ID是本项目定位方式，不承诺它自动等于Tavotto当前版本的编辑选择器。尚未在Tavotto内实际导入、拖动、保存和重开；未来只能对应用显示为可编辑的属性微调。若需要微调，可先试“基因 HBB”的文字位置、蛋白标注引线长度和放大框留白，随后重新核对DNA区域隶属与引线指向。

官方接口依据：[Tavotto图文件契约](https://github.com/Tavotto/Tavotto/blob/main/codex-plugin/skills/tavotto-figure/references/figure-contract.md)、[兼容说明](https://github.com/Tavotto/Tavotto/blob/main/codex-plugin/skills/tavotto-figure/references/compatibility.md)。这里是契约对照，不是实机验收。

## 已检查与保留事项

已实际执行代码、三格式尺寸与文字检查、字体嵌入与缺字检查、画布边界、文字碰撞和间距、路径穿字检查；有意的包含和DNA区域覆盖不当作碰撞。初版发现并修复了安全边距、引线穿字及局部位置问题，重新导出后检查通过。已打开PNG、PDF渲染图、SVG浏览器页面，并查看灰度、96 dpi尺寸代理预览和去文字图。

在代理评审中，去掉文字后仍能看出“内部对象—局部放大—链内区域”；保留标签时可沿图找到基因、DNA、染色体和基因组。这不是招募零基础读者完成的5秒实验，也不是实体纸张印刷验收。最终版心、真实读者理解与Tavotto实机回放仍待后续验证。
