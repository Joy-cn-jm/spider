# 知乎批量爬虫

批量获取知乎用户的所有回答、文章，以及问题下的所有回答。

## 核心原理

知乎 API（`/api/v4/*`）要求每个请求携带动态签名头：

| 请求头 | 说明 |
|---|---|
| `x-zse-93` | 固定值 `101_3_3.0` |
| `x-zse-96` | `2.0_` + encrypt(md5(路径+d_c0+x-zst-81)) |
| `x-zst-81` | webpack 混淆代码生成，依赖 canvas 指纹 |

传统做法是扣出知乎的 webpack 加密模块在本地执行，但代码约 9 万行且深度混淆，
知乎每次更新都可能导致失效。

**本方案**：用 Scrapling（底层 Playwright）启动真实浏览器，在页面上下文中
直接调 `window.fetch()`。知乎自己的 JS 已经 hook 了 fetch，会自动附上签名头，
完全不需要手动逆向加密算法。

## 安装

```bash
pip install "scrapling[fetchers]"
scrapling install
```

## 使用

### 命令行

```bash
# 爬取用户全部回答 + 文章
python zhihu_scrapling.py user <用户ID>

# 爬取问题全部回答
python zhihu_scrapling.py question <问题ID>

# 无头模式（需提前登录过）
python zhihu_scrapling.py user <用户ID> --headless
```

### 代码调用

```python
from zhihu_scrapling import ZhihuScraplingSpider

with ZhihuScraplingSpider(headless=False) as spider:
    # 用户信息
    info = spider.get_user_info("用户ID")

    # 全部回答
    answers = spider.get_user_answers("用户ID")

    # 全部文章
    articles = spider.get_user_articles("用户ID")

    # 保存
    spider.save_json(answers, "answers.json")
```

详细示例见 `example_scrapling.py`。

### 首次登录

首次运行会弹出浏览器窗口，手动扫码登录即可。登录态自动持久化到 `./zhihu_profile/`，
后续无需重复登录。

### 获取 Cookie（备用）

如果需要在其他脚本中使用 Cookie，浏览器打开知乎 → F12 → Console → 粘贴运行
`get_cookies.js`，即可一键复制 JSON 格式的 Cookie。

## 文件说明

| 文件 | 作用 |
|---|---|
| `zhihu_scrapling.py` | 核心爬虫 |
| `example_scrapling.py` | 使用示例 |
| `get_cookies.js` | 浏览器提取 Cookie 脚本 |
| `requirements.txt` | 依赖清单 |

数据默认导出到 `./output/` 目录。

## ⚠️ 法律声明与使用限制

### 合法性说明

**爬虫的内容和方式**
- 本项目声明遵守 robots 协议和知乎用户协议
- 仅抓取公开内容，不对知乎服务器造成负担
- 不绕过验证码、登录限制等反爬虫措施

**用途限制**
- **仅限学习研究，禁止商用**
- 不得用于大规模数据获取、二次分发或商品化
- 不得用于任何违法或侵犯他人权益的行为

**知识产权与隐私**
- 知乎上的内容受版权保护，未经授权不得二次分发
- 避免采集用户隐私信息（账号、评论、点赞等）
- 抓取的数据仅供个人学习研究使用

**中国相关法律**
- 遵守《网络安全法》《数据安全法》《个人信息保护法》等法律法规
- 不得进行数据出境等违规操作
- 如数据量大、范围广，可能面临法律风险

### 免责声明

- 本项目仅供学习交流使用，开发者不对使用本代码产生的任何后果负责
- 如收到知乎律师函或 DMCA 投诉，请立即停止使用并删除相关数据
- 第三方使用本代码进行商业或非法行为，与开发者无关

### 建议

- 完善项目 LICENSE（建议 MIT 或 Apache 2.0）
- 严格限制数据抓取频率和规模
- 如需商用，请获得知乎官方授权
- 遇到法律问题，请咨询专业律师

**重要提醒**：请勿将本项目用于商用、大规模数据获取或再次分发。
