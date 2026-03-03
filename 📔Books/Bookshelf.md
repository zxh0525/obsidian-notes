# 📚 我的书架

> 自动从 Books 文件夹同步

```{dataviewjs}
const booksFolder = "📔Books";
const coversFolder = "📔Books/covers";
const books = await dv.io.list(booksFolder);
const epubs = books.files.filter(f => f.endsWith(".epub"));

if (epubs.length === 0) {
  dv.paragraph("书架为空，快放几本 epub 到 Books 文件夹吧！");
} else {
  let html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 20px; padding: 10px;">';
  
  for (const file of epubs) {
    const name = file.replace(".epub", "");
    const coverPatterns = [
      `${name}_cover.jpg`,
      `${name}_cover.jpeg`, 
      `${name}_cover.png`
    ];
    let coverPath = null;
    for (const p of coverPatterns) {
      try {
        await dv.io.load(coversFolder + "/" + p);
        coverPath = coversFolder + "/" + p;
        break;
      } catch {}
    }
    
    html += '<div style="text-align: center;">';
    if (coverPath) {
      html += `<img src="${coverPath}" style="width: 120px; height: 180px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">`;
    } else {
      html += '<div style="width: 120px; height: 180px; background: #eee; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 40px;">📖</div>';
    }
    html += `<div style="margin-top: 8px; font-size: 12px;">${name.substring(0, 15)}${name.length > 15 ? '...' : ''}</div>`;
    html += `<div><a href="${file}">阅读</a></div>`;
    html += '</div>';
  }
  
  html += '</div>';
  dv.el("div", html);
}
```

---

## 添加新书

把 `.epub` 文件扔进'📔Books'文件夹，打开书架自动更新！
