OpenClaw 的**技能社区**（也就是官方的技能市场/注册中心）主要在这里：

**ClawHub**（最核心、最官方的技能广场）：
- 网址：https://clawhub.ai （或部分来源显示 clawhub.dev / clawdhub.com，但当前主流是 clawhub.ai）
- 这里是 OpenClaw 的公共技能注册中心，像“AI Agent 的 npm”一样，你可以：
  - 搜索、浏览、上万个社区技能（截至2026年3月，社区反馈已超1万甚至1.3万+个）
  - 查看每个技能的 SKILL.md 描述、安装量、版本历史
  - 直接复制技能名或链接，让你的 OpenClaw Agent 一键安装（在聊天窗口说“帮我用Clawhub装 skill-name” 或用 CLI）

**安装/使用 ClawHub 的实用方式**（Ubuntu 上最常见）：
1. 先装 ClawHub CLI（全局安装，一次就好）：
   ```
   npm install -g clawhub
   ```
   或直接用 npx（不用全局装）：
   ```
   npx clawhub@latest --help
   ```

2. 搜索技能（超级实用，避免装垃圾）：
   ```
   npx clawhub@latest search 关键词   # 比如 search email 或 search browser
   ```

3. 安装单个技能：
   ```
   npx clawhub@latest install skill-name   # skill-name 从 ClawHub 网站或搜索结果抄
   ```

**其他补充资源**（很多人实际用这些来避坑/找好货）：
- **精选列表**（推荐新手先从这里挑，避免 ClawHub 鱼龙混杂）：
  - https://github.com/VoltAgent/awesome-openclaw-skills （英文，精选5400+个，已分类过滤，星标高）
  - https://github.com/clawdbot-ai/awesome-openclaw-skills-zh （中文版官方技能库，按场景分类，支持中文调用）
  - 一些教程里提到的“最强军火库”也是这个系列的变体

- **官方文档里的 ClawHub 介绍**：https://docs.openclaw.ai/tools/clawhub （解释怎么用、怎么发布自己的技能）

- **社区讨论/反馈**：OpenClaw 的 Discord（https://discord.gg/clawd）里有个 #skills 频道，很多人在分享/求推荐/报 bug

一句话：直接打开 https://clawhub.ai ，搜你想要的功能（比如“抖音”“browser”“email”“daily briefing”），复制技能名丢给你的 OpenClaw Agent，它就会自动帮你拉下来装好。

如果你已经部署好 OpenClaw，先试试在聊天里说：
“用 ClawHub 搜索并安装一个浏览器自动化的技能”

它会直接带你玩起来。需要具体某个方向的技能推荐吗？（比如生产力、浏览器、内容生成类）