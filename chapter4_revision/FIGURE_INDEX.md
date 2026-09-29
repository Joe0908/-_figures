# 第四章重构配图 F09–F15

这一组与《运行生命》第四章重构版 Word 中的图号一致。原 F01–F30 主图版暂保留不动；不要在全书中混用两套编号。

| 新图号 | 图题 | 来源 |
| --- | --- | --- |
| F09 | 人和小鼠的蛋白质编码序列都只占基因组的一小部分 | 新增 |
| F10 | 人类非编码 DNA 可以从位置、来源和作用三个层次认识 | 新增 |
| F11 | 人的基因组不只有蛋白质编码序列 | 原 F09 |
| F12 | 同一基因组运行不同细胞程序 | 原 F11 |
| F13 | 从 DNA 可接近到基因被使用 | 原 F10 |
| F14 | 细胞怎样接收并回应外部信号 | 原 F12 |
| F15 | 从细胞行为到组织结构的空间反馈 | 原 F13 |

## 正式输出与源码

### 图 F09｜人和小鼠的蛋白质编码序列都只占基因组的一小部分

[png](outputs/png/F09_coding_fraction_human_mouse.png) · [pdf](outputs/pdf/F09_coding_fraction_human_mouse.pdf) · [svg](outputs/svg/F09_coding_fraction_human_mouse.svg) · [Python](F09_coding_fraction_human_mouse.py)

### 图 F10｜人类非编码 DNA 可以从位置、来源和作用三个层次认识

[png](outputs/png/F10_noncoding_annotation_layers.png) · [pdf](outputs/pdf/F10_noncoding_annotation_layers.pdf) · [svg](outputs/svg/F10_noncoding_annotation_layers.svg) · [Python](F10_noncoding_annotation_layers.py)

### 图 F11｜人的基因组不只有蛋白质编码序列

[png](outputs/png/F11_genome_annotation_tracks.png) · [pdf](outputs/pdf/F11_genome_annotation_tracks.pdf) · [svg](outputs/svg/F11_genome_annotation_tracks.svg) · 原始 Python：[原 F09](../figures/F09_genome_annotation_tracks.py)

### 图 F12｜同一基因组运行不同细胞程序

[png](outputs/png/F12_cell_programs.png) · [pdf](outputs/pdf/F12_cell_programs.pdf) · [svg](outputs/svg/F12_cell_programs.svg) · 原始 Python：[原 F11](../figures/F11_cell_programs.py)

### 图 F13｜从 DNA 可接近到基因被使用

[png](outputs/png/F13_access_to_transcription.png) · [pdf](outputs/pdf/F13_access_to_transcription.pdf) · [svg](outputs/svg/F13_access_to_transcription.svg) · 原始 Python：[原 F10](../figures/F10_access_to_transcription.py)

### 图 F14｜细胞怎样接收并回应外部信号

[png](outputs/png/F14_signal_response.png) · [pdf](outputs/pdf/F14_signal_response.pdf) · [svg](outputs/svg/F14_signal_response.svg) · 原始 Python：[原 F12](../figures/F12_signal_response.py)

### 图 F15｜从细胞行为到组织结构的空间反馈

[png](outputs/png/F15_spatial_feedback.png) · [pdf](outputs/pdf/F15_spatial_feedback.pdf) · [svg](outputs/svg/F15_spatial_feedback.svg) · 原始 Python：[原 F13](../figures/F13_spatial_feedback.py)

新图源码复用仓库根目录的 `book_style.py` 与 `fonts/NotoSansSC-Regular.ttf`。原 F14 及之后的图在将来合并完整书稿时都需要顺延两位；这次更新提供可核对的第四章版本，未改动全书其他章节。

### 定量来源

- 人、小鼠蛋白质编码序列约 1.5%：https://www.genome.gov/news/news-release/New-comprehensive-view-of-the-mouse-genome-finds-many-similarities-and-striking-differences-with-human-genome
- 人类外显子约 1.5%：https://www.genome.gov/genetics-glossary/Exome
- 经典草图中可识别的转座元件来源序列约 45%：https://www.nature.com/articles/35057062
- 水稻 37,544 个预测的非转座元件相关蛋白质编码基因（注释估计之一）：https://www.nature.com/articles/nature03895
