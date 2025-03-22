<div align="center">
  <h1>AutoPressAI</h1>
</div>
<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg"/></a>
  <a href="https://wordpress.org/"><img src="https://img.shields.io/badge/Platform-WordPress-blue.svg"/></a>
  <a href="https://open.bigmodel.cn/"><img src="https://img.shields.io/badge/ZhipuAI-GLM--4--Flash-brightgreen.svg"/></a>
  <a href="https://github.com/Adoubf/AutoPressAI/issues"><img src="https://img.shields.io/github/issues/Adoubf/AutoPressAI.svg"/></a>
  <a href="https://github.com/Adoubf/AutoPressAI/commits/main"><img src="https://img.shields.io/github/last-commit/Adoubf/AutoPressAI.svg" /></a>
</p>
## 🧠  项目简介

AutoPressAI 是一个基于智普AI GLM-4-Flash 模型构建的全自动内容发布系统，专为 WordPress 平台设计。该工具可自动获取 AI 生成内容，智能识别文章主题，完成分类与标签分配，并支持批量发布与图片格式优化。通过高度自动化的流程，大幅提升内容运营效率与一致性，适用于内容型网站、博客平台与自动内容生成应用场景。

## 🧱 项目结构

```
wordpress_v2/
├── main.py                     # 主入口文件
├── config.json                 # 配置文件
├── README.md                   # 项目说明文档
├── requirements.txt            # 依赖库列表
├── api/                        # API交互模块
│   ├── __init__.py
│   ├── wordpress_api.py        # WordPress API客户端
│   ├── external_api.py         # 外部API(图片,内容)客户端
│   └── zhipu_ai.py             # 智普AI API客户端
├── config/                     # 配置管理模块
│   ├── __init__.py
│   ├── api_config.py           # API配置管理
│   ├── loader.py               # 配置加载器
│   ├── validator.py            # 配置验证器
│   └── taxonomy_converter.py   # 分类标签转换器
├── core/                       # 核心功能模块
│   ├── __init__.py
│   └── publisher.py            # 文章发布器
├── utils/                      # 工具模块
│   ├── __init__.py
│   ├── logger_config.py        # 日志配置
│   ├── content_formatter.py    # 内容格式化入口
│   └── formatters/             # 格式化子模块
│       ├── __init__.py
│       ├── article_formatter.py # 文章整体格式化
│       ├── paragraph_formatter.py # 段落格式化
│       ├── question_formatter.py # 问题格式化
│       └── source_formatter.py   # 来源格式化
└── logs/                       # 日志文件夹(自动创建)
```

## ✨ 功能特性

- 🔄**批量自动发布**：根据提供的关键词列表自动获取内容并发布到WordPress
- 🧠 **AI自动分类与标签**：使用智普 GLM-4-Flash 模型自动识别内容主题
- 🧾**分类/标签自动创建**：使用分类和标签名称，自动创建不存在的分类/标签
- 🖼️**WebP图片优化**：自动将图片转换为WebP格式，减小体积，失败则回退到原始格式
- 📱**响应式HTML设计**：文章内容使用美观的响应式HTML格式，适配各类设备
- 📊**详细的日志记录**：记录所有操作并提供错误跟踪
- ⚙️**可配置性强**：通过外部配置文件自定义所有设置
- 🧩**模块化架构**：代码结构清晰，易于扩展和维护

## 🧱 安装要求

- 🐍 Python 3.8或更高版本
- 🌐 WordPress站点需启用REST API
- 🔑 智普AI API密钥 (可选，用于AI分类功能)

## 🧾 配置说明

在`config.json`中配置以下内容:

```json
{
    "wp_url": "https://your-wordpress-site.com",
    "wp_username": "your_username",
    "wp_password": "your_password",
    
    "category_names": ["技术", "旅游", "美食", "体育", "健康"],
    "tag_names": ["热门", "推荐", "最新"],
    
    "keywords": ["旅游业最新发展", "人工智能应用"],
    
    "publish_interval": 30,
    
    "use_zhipu_ai": true,
    "zhipu_api_key": "your_api_key.your_secret"
}
```

## 🛠️ 使用方法

1. 📦 安装依赖:
```bash
pip install -r requirements.txt
```

2. ⚙️ 创建配置文件:
```bash
cp config.json.example config.json
```
然后编辑配置文件，填入WordPress站点信息和关键词等。

3. 🚀 启动程序:
```bash
python main.py
```

## 🧬 高级功能

### 📌 自动分类与标签分配

当配置中设置`use_zhipu_ai: true`时，系统会使用智普AI模型自动判断文章最适合的分类和标签。AI会分析文章内容、标题和关键词，选择最相关的分类以及最匹配的标签组合。

### 🖼️ WebP图片优化

系统会自动将特色图片转换为WebP格式，大幅减小图片体积(通常减少30-50%)，提高页面加载速度。如果 WebP 转换或上传失败，系统会自动回退到原始图片格式。

### 🎨 自定义样式

所有HTML样式都集中在formatters目录下的各个格式化器中，可以根据需要修改CSS样式。文章采用了现代化的响应式设计，包括:

- 优雅的文章布局和排版
- 高亮的重点内容
- 精美的相关问题卡片
- 使用纯CSS实现的信息来源手风琴效果
- 移动设备友好的响应式设计

## 📎注意事项
- 项目中使用的AI搜索接口使用的是免费的API，地址为 [PearAPI-AI网络搜索](https://api.pearktrue.cn/info/362)
- 项目中使用的获取图片接口使用的是免费的API，地址为[PearAPI-自定义随机缩略图](https://api.pearktrue.cn/info/326)
- 项目中使用的WordPress API接口使用的是WordPress自带的API，请确保你的WordPress站点开启了REST API功能
- 智普AI API需要申请密钥，详见[智普AI开放平台](https://open.bigmodel.cn/)

## 📎特别注意
- 免费的API存在不可靠性，可能会导致图片获取失败或者内容获取失败，可以自行替换为其他API,或者提issue给我，我会尽快修复
- config.json中的标签和分类名称可以自行修改，但是请确保你的WordPress站点中存在这些分类和标签，否则会报错

## 💡常见问题

### > ❓ 如何修改文章格式和样式?
A: 编辑`utils/formatters/`目录下的相应文件，可以自定义HTML和CSS样式。

### > ❓ 支持哪些WordPress版本?
A: 本项目支持WordPress 5.0及以上版本，需开启REST API功能。

### > ❓ 如何使用自己的内容源而不是默认API?
A: 修改`api/external_api.py`文件中的`get_article_content`方法，替换为自己的内容获取逻辑。

## 👨‍💻开发指南

如需扩展本项目功能:

- ➕**添加新的内容来源**: 扩展`ExternalAPI`类或创建新的API客户端类
- 🎨**调整文章格式**: 修改`utils/formatters/`目录下的格式化模块
- **🤖增加新的AI模型**: 创建新的AI客户端类，实现与`ZhipuAIClient`类似的接口

## 📜许可证

本项目使用MIT许可证 - 详见[LICENSE](https://github.com/Adoubf/AutoPressAI/blob/v1.0/LICENSE)文件
