# 《运行生命》F01–F30 全书配图

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

