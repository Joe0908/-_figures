# 第十章 SMA 剪接补充图

## F25a 借助 SMN2 改变 RNA 剪接

![SMN2 初始 RNA 在未使用和使用 nusinersen 后的常见剪接结果](outputs/png/F25a_smn2_splicing.png)

- [PNG 600 dpi](outputs/png/F25a_smn2_splicing.png)
- [PDF 矢量图](outputs/pdf/F25a_smn2_splicing.pdf)
- [SVG 可编辑文字](outputs/svg/F25a_smn2_splicing.svg)
- [Python 源码](F25a_smn2_splicing.py)
- [布局与格式检查结果](outputs/manifests/F25a_validation.json)

## 插入位置

第十章“不修 DNA，只改变一次剪接”小节，解释 nusinersen 结合初始 RNA、使第七外显子更容易保留的段落之后，“结果是：更多完整的 SMN2 RNA。”之前。当前采用补充图号 F25a，全书正式排版时可统一编号。

## 图注

图 F25a｜借助 SMN2，改变 RNA 剪接。图中只画出第6—8外显子。未用药时，第7外显子常被跳过；nusinersen 结合初始 RNA 的内含子，使它更常被保留，增加完整 SMN 蛋白。SMN2 原本也能产生少量完整蛋白，图中展示的是常见路径，而不是每条 RNA 的必然结果。

## 表达范围

SMN1 功能缺失或不足是案例的起点；治疗借助另一个基因 SMN2 的 RNA。图中药物结合位置在第7外显子下游的内含子，不是 DNA，也不是第7外显子本身。剪接后方块间的短线表示 RNA 片段连接；初始 RNA 中的长线表示内含子。DNA 与 RNA 之间的虚线表示模板关系。方块长度、线长和两条路径均不编码实测比例。

图只解释分子机制，不表示每条转录本的结果或患者临床获益。主图宽170 mm、高184 mm；插入108 mm正文栏时，最小字号约8.6 pt。使用仓库的“海青与铜”配色、Noto Sans SC 字体和原有几何检查，不替换既有 F25 图。

## 复现

在装有仓库 requirements.txt 依赖的 Python 环境中运行：

```sh
python chapter10_additions/F25a_smn2_splicing.py
```

生成 PNG、PDF、SVG 及验证清单。SVG 嵌入字体；PDF 为矢量对象并嵌入字体。

## 机制依据

- [SPINRAZA 官方处方说明，2026年3月修订，§11与§12.1](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=dd70cd5f-b0fc-4ba4-a5ea-89a34778bd94&type=display)：nusinersen 结合 SMN2 第7外显子下游内含子的特定序列，增加第7外显子保留及完整 SMN 蛋白产生。
- [美国国家医学图书馆 MedlinePlus Genetics，SMN2](https://medlineplus.gov/genetics/gene/smn2/)：SMN2 可补充部分缺失的 SMN 蛋白，并能产生完整及较短、不稳定的蛋白版本。

已通过仓库的文字间距、线穿字、边界、缺字与导出格式检查，并查看成图。未做实体印刷或零基础读者测试。
