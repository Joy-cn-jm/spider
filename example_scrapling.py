"""
知乎批量爬虫 — Scrapling 使用示例

运行前确保：
    pip install "scrapling[fetchers]"
    scrapling install

首次运行弹出浏览器窗口，扫码登录后持久化。
"""

from zhihu_scrapling import ZhihuScraplingSpider, OUTPUT_DIR


def demo_batch_user():
    """批量抓取用户全部回答 + 文章"""
    with ZhihuScraplingSpider(headless=False) as spider:
        # 1. 查用户信息
        user_id = "zhangsan"  # ← 替换为目标用户
        info = spider.get_user_info(user_id)
        print(f"\n{'='*50}")
        print(f"用户: {info.get('name')}")
        print(f"回答: {info.get('answer_count')} 篇")
        print(f"文章: {info.get('articles_count')} 篇")
        print(f"关注者: {info.get('follower_count')}")
        print(f"{'='*50}\n")

        # 2. 批量获取回答（限制 100 条）
        answers = spider.get_user_answers(user_id, max_count=100)
        print(f"\n获取回答: {len(answers)} 条")

        # 打印前 3 条概览
        for i, a in enumerate(answers[:3]):
            title = a.get("question", {}).get("title", "无标题")
            excerpt = (a.get("excerpt", "") or "")[:80]
            print(f"  [{i+1}] {title}")
            print(f"      {excerpt}...")

        # 3. 批量获取文章
        articles = spider.get_user_articles(user_id, max_count=100)
        print(f"\n获取文章: {len(articles)} 篇")

        for i, art in enumerate(articles[:3]):
            print(f"  [{i+1}] {art.get('title', '无标题')}")

        # 4. 保存
        spider.save_json(answers, f"{user_id}_answers.json")
        spider.save_json(articles, f"{user_id}_articles.json")
        spider.save_json({
            "user_info": info,
            "answers": answers,
            "articles": articles,
        }, f"{user_id}_complete.json")

        print(f"\n✅ 数据已保存至 {OUTPUT_DIR}/")


def demo_batch_question():
    """批量抓取某个问题下的全部回答"""
    with ZhihuScraplingSpider(headless=False) as spider:
        qid = 2041195866896209545  # ← 替换为目标问题 ID
        answers = spider.get_question_answers(qid, max_count=50)
        print(f"问题 {qid} 获取回答: {len(answers)} 条")

        for a in answers[:5]:
            author = a.get("author", {}).get("name", "匿名")
            excerpt = (a.get("excerpt", "") or "")[:60]
            print(f"  [{author}] {excerpt}")

        spider.save_json(answers, f"question_{qid}_answers.json")


def demo_search_and_scrape():
    """搜索关键词并批量获取搜索结果中的内容"""
    with ZhihuScraplingSpider(headless=False) as spider:
        results = spider.search("Python 爬虫", max_count=30)
        print(f"搜索结果: {len(results)} 条")

        for item in results[:5]:
            obj = item.get("object", {})
            print(f"  [{obj.get('type', '?')}] {obj.get('title', obj.get('excerpt', '?'))}")

        spider.save_json(results, "search_results.json")


def demo_multi_user():
    """批量抓取多个用户"""
    user_ids = ["zhangsan", "lisi", "wangwu"]  # ← 替换为目标用户列表

    with ZhihuScraplingSpider(headless=False) as spider:
        for uid in user_ids:
            info = spider.get_user_info(uid)
            answers = spider.get_user_answers(uid, max_count=50)
            spider.save_json(answers, f"{uid}_answers.json")
            print(f"  {uid}: {len(answers)} 条回答")


if __name__ == "__main__":
    demo_batch_user()
    # demo_batch_question()
    # demo_search_and_scrape()
    # demo_multi_user()
