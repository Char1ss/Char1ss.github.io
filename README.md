# Zhixiang Fan — Research portfolio

英文静态研究主页，目标地址 `https://char1ss.github.io/`。无前端依赖、无分析追踪，无需后台服务器。

## 内容

- 语义 3DGS：LangSplat + ResGS、对象状态与 Web 交互。
- Axis / WAIC：Minecraft 场景、皮肤生成及团队体感交互。
- 医疗 4DGS：四路相机、自采医生缝合操作的动态重建。
- 中国古典园林 Design Skills。
- 五项论文成果，以及英文 CV。

四个项目均有独立页面。已接入用户提供的四张封面、项目图片及六段视频，五篇论文共 22 张配图。视频转换为 H.264 MP4，图片压缩为 WebP，原始素材不变。

网站为白底黑字，媒体保留原色。项目详情页与论文配图使用原生横向滚动画廊，支持左右按钮、触摸滑动、键盘方向键。手绘、项目和论文图片点击后在当前页面的弹窗中放大，支持左右切图、Esc、关闭按钮及点击遮罩关闭；关闭后焦点返回原图。普通链接在当前标签页打开。无自动轮播，切出可见区域的视频会暂停。

Practice 独立位于 Publications 之后，三段经历各列三项具体职责。两篇 ACM 论文仅链接本地 PDF，暂不展示 DOI；MER 按正式 PDF 标注为 MRAC workshop，作者顺序也与 PDF 一致。MER 四张配图直接使用未经重编码、缩放或压缩的源 PNG。

教育经历附两校校徽，下方为 11 张手绘的自适应缩略图墙，点击查看大图。内容和顺序均以 `content.json` 为准；早期素材导入脚本不应重新覆盖本文件中的人工调整。

## 本地预览

```sh
python3 build.py
python3 -m http.server 8765 --bind 127.0.0.1
```

浏览器打开 `http://127.0.0.1:8765/`。网站运行不需要 Python；只有更新内容时使用生成脚本。

## 修改文案或添加图片视频

编辑 `content.json`，再运行 `python3 build.py`。不要只修改生成的 HTML，下次构建会覆盖。

每个项目的媒体放在对应目录：

```text
assets/projects/semantic-3dgs/
assets/projects/axis-waic/
assets/projects/surgical-4dgs/
assets/projects/garden-skills/
```

先选择一张封面，设置 `cover`（相对于网站根目录）。再填写 `gallery`，例如：

```json
{
  "cover": "assets/projects/semantic-3dgs/cover.webp",
  "gallery": [
    {
      "type": "video",
      "src": "assets/projects/semantic-3dgs/demo.mp4",
      "poster": "assets/projects/semantic-3dgs/cover.webp",
      "caption": "Semantic selection and language interaction in a reconstructed scene."
    },
    {
      "type": "image",
      "src": "assets/projects/semantic-3dgs/pipeline.webp",
      "alt": "Processing stages from semantic features to object state and browser interaction.",
      "caption": "The semantic processing and interaction pipeline."
    }
  ]
}
```

视频建议使用 H.264 MP4、720p/1080p、30–60 秒、每段约 5–20 MB；需要语音说明时加字幕或在图注补充文字。截图建议长边 1600–2000 像素，避免缩小后读不清。大模型、原始采集数据和完整训练文件不放到主页仓库。

论文链接没有确认时保持 `url` 为空，不会显示不可用按钮。CV 在 `assets/zhixiang-fan-cv.pdf`。

## 发布到 GitHub Pages

当前仅为本地版本。确认内容后：

1. 在 `Char1ss` 账号创建公开仓库 `Char1ss.github.io`。
2. 上传本站文件，确保 `index.html` 在仓库根目录。
3. 在 Settings → Pages 中选择 Deploy from a branch，分支 `main`、目录 `/ (root)`。
4. 等待 GitHub Pages 部署完成，访问 `https://char1ss.github.io/`。

已生成的 HTML 可以直接发布，不依赖 GitHub Actions 构建，也无需上传任何服务器凭据。
