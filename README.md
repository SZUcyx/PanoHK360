# PanoHK360 论文主页

按照 https://odgs-slam.github.io/ 的页面结构和样式制作，内容来自 `../PanoHK360写作/main.tex`。纯静态 HTML/CSS/JavaScript，无需安装 npm 依赖。

## 本地运行

双击 `start.command`，然后在浏览器打开终端显示的地址。也可以在这个文件夹运行：

```sh
python3 serve.py
```

默认地址为 http://localhost:8000/；端口被占用时自动选择下一个端口。终端按 Ctrl+C 停止。

## 修改内容

- `dist/site.config.js`：作者、机构、会议及会议页面，以及论文、代码、数据集和视频链接。作者的 `corresponding: true` 用于标注通讯作者；空链接保留为灰色禁用按钮。
- `dist/index.html`：论文标题、摘要、数据集介绍和 BibTeX。
- `dist/styles.css`：样式，沿用参考页面的浅灰背景、居中标题、资源按钮和白色内容区。
- `dist/assets/images/`：由论文 Figure1.pdf 和 Figure2.pdf 转换的网页配图。
- `dist/assets/images/shenzhen-university-logo.png` 和 `neurips-logo.svg`：用户提供的深圳大学和 NeurIPS Logo，分别显示在标题区左上角和右上角；手机上两者排在标题上方。
- `dist/assets/paper/PanoHK360.pdf`：原有 main.pdf 的副本，Paper 按钮直接打开此文件。
- `dist/assets/video/PanoHK360.mp4`：已压缩并接入主页的视频，3840×1920、30 fps、H.264，10 秒，约 16.2 MB。
- `dist/assets/images/video-poster.webp`：从压缩视频第一帧提取的播放器封面。

作者依次为 Yunxiao Chen、Honghuan Lin、Ruisheng Wang、Yujun Liu、Kun Zhou、Shangfeng Huang 和 Tsz Nam Chan；Ruisheng Wang 标注为通讯作者，机构为空。NeurIPS 2026 链接到[会议论文页面](https://neurips.cc/virtual/2026/poster/139447)，Code 链接到[代码仓库](https://github.com/William1234i/PanoHK360)，Dataset 链接到[Hugging Face 数据集](https://huggingface.co/datasets/adadai3132/PanoHK360)。视频已接入，顶部 Video 按钮可直接打开 MP4。`main.pdf` 保留原稿内容，可在拿到 camera-ready PDF 后替换网页中的副本。

视频保留原始 2:1 全景比例，不裁切，使用原生播放控件，支持全屏和手机内联播放。默认仅预加载元数据，不自动播放。MP4 使用 faststart，本地服务器支持 HTTP 字节范围请求，方便快速开始播放和拖动进度。

原始 `../video.avi` 保留不动；体积由约 1.1 GB 减少至 16.2 MB，缩小约 98.6%。替换视频时，覆盖 `dist/assets/video/PanoHK360.mp4`，并同步更新封面。发布时只需上传 `dist/`，无需上传原始 AVI。

## GitHub 与 GitHub Pages

目标仓库：https://github.com/SZUcyx/PanoHK360

`.github/workflows/pages.yml` 已配置为：每次推送 `main` 分支时，将 `dist/` 发布到 GitHub Pages。首次使用时，在仓库 **Settings → Pages → Build and deployment → Source** 中选择 **GitHub Actions**，然后在 Actions 中运行 **Deploy PanoHK360 homepage** 工作流。

Pages 成功部署后的主页地址为：https://szucyx.github.io/PanoHK360/

图片、样式、脚本、论文和视频均使用相对路径，适用于 GitHub Pages 的项目子目录。仓库只包含主页文件、论文 PDF、压缩 MP4 和本地启动脚本；原始 AVI、作图 PPTX、完整素材文件夹及转码工具不纳入提交。

## 页面来源

页面布局和样式参考 [ODGS-SLAM project page](https://odgs-slam.github.io/)，保留页脚来源署名；标题、作者、文字、图片、资源入口和引用均已替换为 PanoHK360 内容。
