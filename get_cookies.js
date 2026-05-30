/**
 * 知乎 Cookie 提取脚本
 *
 * 在知乎页面打开 F12 → Console，粘贴运行此脚本，
 * 即可复制 cookies 到剪贴板（JSON 格式）。
 * 可配合 spider.py 使用，或单独保存备用。
 */
(function () {
  const cookies = document.cookie.split("; ").reduce((acc, item) => {
    const [k, ...rest] = item.split("=");
    acc[k] = rest.join("=");
    return acc;
  }, {});

  const output = JSON.stringify(cookies, null, 2);
  console.log("=== 知乎 Cookies ===");
  console.log(output);

  // 尝试复制到剪贴板
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(output)
      .then(() => console.log("✅ 已复制到剪贴板"))
      .catch(() => console.log("⚠️ 复制失败，请手动复制上方 JSON"));
  } else {
    // fallback: 创建一个 textarea
    const ta = document.createElement("textarea");
    ta.value = output;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand("copy");
      console.log("✅ 已复制到剪贴板");
    } catch {
      console.log("⚠️ 复制失败，请手动复制上方 JSON");
    }
    document.body.removeChild(ta);
  }
})();
