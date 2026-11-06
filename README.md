# FModel · 简体中文界面版

基于官方 **[4sval/FModel](https://github.com/4sval/FModel)** `dev` 分支
`e952f6c33152dc9d42662101c23a0947cca601e9`（v4.4.4.0 / nov-2026，2026-10-31），
仅对**软件界面文案**做简体中文替换，未改动任何资源解析、导出、AES 解密逻辑。

> **English / 官方原版说明**：[README.upstream.md](README.upstream.md)（保留原样，便于对照上游更新）
>
> 官方 3.1.1 曾提供「Chinese (Simplified) software language」，4.x 重构后已移除；
> 当前设置里的 `Packages Language` 是解析包内游戏文本用的，与界面语言无关。

## 改了什么

共 **412 处**替换，分布在 30 个源文件：

| 类型 | 数量 |
|---|---|
| XAML 界面属性（菜单、按钮、标签、设置项、水印、提示、格式化串） | 391 |
| XAML 元素文本 | 2 |
| 下拉枚举显示名 `[Description]` | 17 |
| 弹窗提示（C# 字符串） | 2 |

覆盖示例：加载模式 / 全部 / 多选 / UE 版本 / 输出目录 / 目录 / 设置 / 加载 /
确定 / 取消 / 导出 / 按名称搜索 / 未找到文件夹或包 / 包内文本语言 /
本地映射文件 / 反编译蓝图 / 区分大小写 / 正则表达式 / 网格视图。

**保持英文**：技术专名（AES、Luaj、Unluac、Oodle、Spine、Nanite、CRIWARE…）、
快捷键（Ctrl+Shift+F 等），以及运行时动态生成的内容（资产名、游戏名、日志、
版本号、JSON 属性名、游戏内文本）。这些不属于界面文案。

用 `git show` 或 `git diff 80ee139..8bc1165 -- FModel/` 可查看完整汉化 diff。

## 仓库结构

```
FModel-zh-CN/
├─ FModel/                 官方源码（含汉化）
├─ CUE4Parse/              gitlink → FabianFG/CUE4Parse @85495b5e
├─ Snooper/                gitlink → FModel/Snooper    @9d44219c
├─ .gitmodules             官方子模块配置
├─ Directory.Build.props   官方 MSBuild 属性（CUE4ParseDir）
├─ LICENSE / NOTICE        官方 GPL-3.0 许可，务必保留
├─ README.md               本文件（简体中文，GitHub 项目主页显示）
├─ README.upstream.md      官方原版英文 README（未改动）
└─ scripts/
   ├─ zh_dict.py           中文映射表
   ├─ apply_zh.py          把映射应用到 FModel/ 源码
   └─ build.sh             编译单文件 exe
```

子模块按上游惯例用 **gitlink** 登记，仓库本身不含它们的源码，clone 后需要
`git submodule update --init --recursive`（见下）。

## 编译

要求：**.NET 10 SDK**、Windows、Git。

```bash
git clone --recurse-submodules https://github.com/<你的用户名>/FModel-zh-CN.git
cd FModel-zh-CN
bash scripts/build.sh
# 产物：out/FModel.exe（约 51 MB，单文件，framework-dependent）
```

若已用别的方式备齐子模块源码，可去掉 `--recurse-submodules`，
只需保证 `CUE4Parse/` 与 `Snooper/` 两个目录结构存在。

`scripts/build.sh` 等价于：

```bash
dotnet publish FModel/FModel.csproj -c Release -r win-x64 \
  --self-contained false -o out \
  -p:PublishSingleFile=true \
  -p:IncludeNativeLibrariesForSelfExtract=true \
  -p:DebugType=None -p:DebugSymbols=false
```

> **必须是 Release**：`UserSettings.FilePath` 在源码里硬编码为
> `%AppData%\FModel\AppSettings.json`；Debug 构建会改读 `AppSettings_Debug.json`。
> 两者与程序集名/版本无关，所以正常 Release 构建不会动用户已有配置
> （AES 密钥、游戏目录、UE 版本等全部保留）。

## 重新汉化 / 升级上游

```bash
# 1. 拿到新版官方源码后，把字典重新应用一遍
python scripts/apply_zh.py

# 2. 编辑 scripts/zh_dict.py 增补新增的英文文案，再跑一次
#    注意：译文若以 { 开头，必须写成 {}{0} ... 的 XAML 转义形式，
#    否则会被当成标记扩展，编译报 MC1000。

# 3. 合并上游
git remote add upstream https://github.com/4sval/FModel.git   # 已预置
git fetch upstream dev
git merge upstream/dev     # 之后重新执行 apply_zh.py 补译新增文案
```

字典是「英文原文 → 中文」的精确映射，只替换 XAML 属性值、元素文本、
`[Description]` 与少量弹窗字符串，不会碰绑定表达式、命令参数、配置键。

> 合并上游时，根目录 `README.md` 可能会提示冲突（上游也会改它）。
> 保留本文件的中文内容即可，英文原版始终在 `README.upstream.md` 里。

## 日常维护

首次推送需要绑定远程地址并推 `main` 分支：

```bash
git remote add origin https://github.com/<你的用户名>/FModel-zh-CN.git
git push -u origin main
```

之后每次改动都是「三拍子」，Git GUI 与命令行一一对应：

| 动作 | Git Bash | Git GUI |
|---|---|---|
| 看状态 | `git status` | Rescan (F5) |
| 挑文件 | `git add -A` | Stage Changed |
| 存快照 | `git commit -m "改了什么"` | 写 Commit Message → Commit |
| 送上网 | `git push` | Remote → Push… → Push |

在 GitHub 网页上直接编辑或拖拽上传文件，本质是让 GitHub 自动帮你建了一个
commit，等价于这三步的合体；但那样本地会落后于远程，下次推送前要先 Pull。

## 使用注意

- FModel 启动会检查更新。**不要点「下载最新版本」**，官方英文版会覆盖汉化 exe。
- 少数固定宽度的设置项，中文可能比英文略长而略显拥挤，不影响功能。
- 中文字符串以 UTF-8 内嵌在编译后的 BAML 中，无需额外字体或语言包。

## 许可

FModel 为 **GPL-3.0**（见 `LICENSE`、`NOTICE`），CUE4Parse / Snooper 同属其生态。
本仓库仅替换界面显示字符串，并保留原始许可文件与官方 README；
衍生分发请遵守 GPL-3.0（开源、保留版权声明、同许可证）。
