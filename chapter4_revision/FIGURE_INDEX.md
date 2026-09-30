# 第四章最新版配图 F09–F13

唯一正文依据为本轮上传的《运行生命_第四章_最终精修版(3).docx》。对应成稿为《运行生命_第四章_图文整合版.docx》。F12a / F12b / F12c 合并为一张 F12，内部保留 a、b、c；正文引用与图注已同步。

| 图号 | 图题 | 认知任务 | Python 源码 | PNG | PDF | SVG |
| --- | --- | --- | --- | --- | --- | --- |
| F09 | 同一套基因组，不同细胞程序 | 提出问题；同一 DNA 对应不同 RNA、蛋白质及细胞功能，暂不解释机制 | [源码](F09_same_genome_different_programs.py) | [预览](outputs/png/F09_same_genome_different_programs.png) | [矢量](outputs/pdf/F09_same_genome_different_programs.pdf) | [可编辑](outputs/svg/F09_same_genome_different_programs.svg) |
| F10 | 调控序列与读取它们的蛋白质 | 同一模型中区分 DNA 区域、短基序、蛋白质与制造 RNA 的转录机器 | [源码](F10_minimal_regulatory_model.py) | [预览](outputs/png/F10_minimal_regulatory_model.png) | [矢量](outputs/pdf/F10_minimal_regulatory_model.pdf) | [可编辑](outputs/svg/F10_minimal_regulatory_model.svg) |
| F11 | 相同识别位置，不同组合关系 | 保留相同基序和蛋白质，对照间距与顺序造成的接触机会变化 | [源码](F11_regulatory_grammar.py) | [预览](outputs/png/F11_regulatory_grammar.png) | [矢量](outputs/pdf/F11_regulatory_grammar.pdf) | [可编辑](outputs/svg/F11_regulatory_grammar.svg) |
| F12 | 看得到吗？谁来读？碰得到吗？ | 统一三联图：a 只比较局部包装；b 只比较活跃因子；c 比较空间关系 | [源码](F12_three_reading_conditions.py) | [预览](outputs/png/F12_three_reading_conditions.png) | [矢量](outputs/pdf/F12_three_reading_conditions.pdf) | [可编辑](outputs/svg/F12_three_reading_conditions.svg) |
| F13 | 调控可能性怎样成为不同的细胞身份 | 与 F09 呼应，收束调控可能性、读取环境、表达输出和细胞身份 | [源码](F13_regulatory_possibilities_to_identity.py) | [预览](outputs/png/F13_regulatory_possibilities_to_identity.png) | [矢量](outputs/pdf/F13_regulatory_possibilities_to_identity.pdf) | [可编辑](outputs/svg/F13_regulatory_possibilities_to_identity.svg) |

## 布局与科学边界

- F09 使用相同 DNA 图形分成两路。RNA 线条与蛋白形状只示意不同组合，不是实测种类或数量。
- F10 中增强子是区域，A/B/C 是区域内部的短识别位置；TF 是框上方的蛋白质。RNA 的产生连接到转录机器。远端的虚线表示可能影响，不是开关。
- F11 只用三组排列；不排序表达强弱，不把接触线解释为必然发生的协作。基序组合并非普适固定句法。
- F12 的 a/b 两组保持基序、增强子、启动子、基因坐标一致。a 两边提供同样的因子；b 两边包装相同。c 使用同一套区域和蛋白质，只改变 DNA 的空间摆放。全部为示意，不代表真实比例或接触频率。
- F13 顶部无箭头连接表示理解层级；读取环境到输出采用条件影响线；表达产物到结构功能采用过程箭头。已有状态、发育历史与信号属于读取环境。
- 开放、匹配因子或空间靠近都不独自保证转录。没有加入 TAD、CTCF、化学修饰或第五章的状态维持机制。

## 复现

从仓库根目录运行：

```sh
python chapter4_revision/build_chapter4.py
python chapter4_revision/validate_chapter4.py
```

每张图在此目录拥有自己的源码；不再映射根目录旧 Fxx 图。`chapter_drawing.py` 是本章适配层，直接复用根目录的 `book_style.py`、`palette.py`、`shared_shapes.py`、`layout_utils.py`、`production_utils.py` 和 `export_utils.py`。未复制或修改共享视觉库。

母版宽度 170 mm，PNG 为 600 dpi；PDF 为嵌入字体的矢量图，SVG 保留可编辑文字与内嵌字体。延续海青与铜配色、0.8/1.1/1.5 pt 线宽及仓库关系线语义。为适应原 Word 108 mm 正文栏，母版标签使用 14.5 pt、注释 13.5 pt，排入 Word 后最小约 8.58 pt，未修改页面或正文样式。

每图实际导出验证记录在 `outputs/manifests/Fxx_validation.json`；本章汇总在 [chapter4_validation.json](outputs/manifests/chapter4_validation.json)。检查覆盖真实文字与线条几何、字号、边界、PNG 分辨率、PDF 矢量与字体、SVG 文字及输出/源码哈希。联合审查记录见 [VISUAL_REVIEW.md](VISUAL_REVIEW.md)。这些检查不等于真实读者理解测试，也未验证实体印刷或所有矢量编辑器的往返兼容性。

根目录 F01–F30 及其索引、manifest、fonts 均保持原版；全书重新编号留待合稿处理。旧第四章临时映射与输出由本目录当前五图替换，旧版本仍可在 Git 历史查看。
