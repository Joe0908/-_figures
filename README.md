# 《运行生命》F01–F30 全书配图

**第十章新增 SMA 剪接示意图：** [F25a 借助 SMN2 改变 RNA 剪接（图片、源码与插图位置）](chapter10_additions/FIGURE_INDEX.md)。并排展示 nusinersen 使用前后的常见剪接结果；F25a 为补充图号，未重编号原有图。

**第八章当前 F22：** [PRS 百分位金字塔（图片、源码及使用说明）](chapter8_revision/FIGURE_INDEX.md)。新版第八章以此图替换旧“相对风险与绝对风险”F22；下方原始 30 图套装保留为历史版本。

本交付按 prompt 4 生成全套 30 张图，并延续已确认的 F01 构图与「海青与铜」配色。原书稿和旧阶段文件保留不动。

- [图与代码浏览目录](FIGURE_INDEX.html)：30 张最终图、原题、认知任务、布局理由、可复用组件和完整源码。
- [30 页矢量合订本](Running_Life_F01-F30.pdf)：按图号阅读，原题保留为 PDF 书签。
- [全部图的文字索引](FIGURE_INDEX.md)
- [统一配色规范](PALETTE_SPECIFICATION.md)
- [简短维护说明](MAINTENANCE.md)
- [原稿对应表](SOURCE_TRACEABILITY.md)
- [独立审计](audit/)

`figures/` 有 30 个独立脚本及相邻 PDF；`outputs/png`、`outputs/pdf`、`outputs/svg` 各有 30 份成图。PDF/SVG 保留矢量对象，SVG 保留可编辑文字和语义 ID；PNG 为 600 dpi 预览。宽度统一为 170 mm，高度按内容调整，文字不小于 8.5 pt。`build_all.py` 默认按 F01→F30 重建。

配图只表达书稿的机制与案例范围。除 F22 的明确假设人数外，不把示意线长、点数或位置当成实测数量。F27 区分机制目标、单名患者早期报告及后续医院更新；所有案例均保留相应限制。

本次已执行检查、修复与版本绑定见 `audit/` 和 `RELEASE_MANIFEST.json`。尚未验证实体印刷/CMYK、真实读者理解、Tavotto 实机回放和全部编辑器兼容性。

## 第四章重构版

[第四章最新版 F09–F13：独立源码、统一 F12 三联图与三格式输出](chapter4_revision/FIGURE_INDEX.md)。原 F01–F30 套图保留，以免其他章节在全书图号同步前失效。


## 第五章新版配图

[第五章最新版 F14–F15：图片、Python 源码、PDF/SVG 与插图位置](chapter5_revision/FIGURE_INDEX.md)。对应《DNA 不变，细胞怎样记住自己是谁？》的新稿，F14 为三联机制图，F15 为复制后甲基化维持及组蛋白重新分配示意图。沿用原书配色，专为 108 mm 正文宽度调整图中文字；旧版 F14/F15 属于历史套图。

运行 `python chapter5_revision/build_chapter5.py` 重建这两张新版图。

## 第八章新版配图

[第八章最新版 F22：PRS 百分位表示相对位置](chapter8_revision/FIGURE_INDEX.md)。采用前10%、中间80%、后10%的示例分组；第95百分位表示相对排名，不表示95%的患病概率。金字塔宽度不编码人数或患病概率。F23 沿用原图。

运行 `python chapter8_revision/F22_prs_percentile_pyramid.py` 重建新版 F22。原 `build_all.py` 仍用于历史 30 图套装。
