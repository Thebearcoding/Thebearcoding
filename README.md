<div align="center">

<a href="https://athebear.me"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=22&duration=2800&pause=1200&color=2A8BD8&center=true&vCenter=true&width=640&lines=Reading+agent+harnesses+line+by+line;Running+them+for+real;Fixing+what+breaks+upstream" alt="Reading agent harnesses, running them for real, fixing what breaks upstream" /></a>

**Xinran Xiong · athebear**

多模态与 Agent。目前的重点是 **Coding Agent / Agent Harness**：<br>读 harness 源码，在本地把它们跑起来，修上游的 bug。

<a href="https://athebear.me"><img src="https://img.shields.io/badge/Blog-athebear.me-2A8BD8?style=flat-square" alt="Blog" /></a>&nbsp;
<a href="https://athebear.me/notes/lcc-s01-agent-loop/"><img src="https://img.shields.io/badge/Harness_%E7%B2%BE%E8%AF%BB-17_%E7%AF%87-136CB3?style=flat-square" alt="Harness 精读 17 篇" /></a>&nbsp;
<a href="#合并到上游的-pr"><img src="https://img.shields.io/badge/%E4%B8%8A%E6%B8%B8%E5%90%88%E5%B9%B6_PR-7-2DA44E?style=flat-square" alt="上游合并 PR 7 个" /></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Thebearcoding/Thebearcoding/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Thebearcoding/Thebearcoding/output/github-snake.svg" />
  <img alt="贪吃蛇吃掉贡献图的动画" src="https://raw.githubusercontent.com/Thebearcoding/Thebearcoding/output/github-snake.svg" />
</picture>

</div>

### 合并到上游的 PR

| 项目 | PR | 修了什么 |
|---|---|---|
| [BaoCode](https://github.com/baocode-dev/baocode)<br><sub>Claude Code 桌面客户端 · Flutter/Dart</sub> | [#437](https://github.com/baocode-dev/baocode/pull/437) | Claude Code 进程还在启动时按下「立即发送」，消息会丢失。把这个操作接入运行时就绪守卫和消息写入序列，补了 3 个回归测试（修复前失败、修复后通过） |
| [openfilm](https://github.com/openfilm/openfilm)<br><sub>开源 AI 视频 Agent · TypeScript</sub> | [#27](https://github.com/openfilm/openfilm/pull/27) [#28](https://github.com/openfilm/openfilm/pull/28) [#29](https://github.com/openfilm/openfilm/pull/29) | Studio 的三处工程问题：WAV 尾部元数据被算进配音时长；同时导入同名文件互相覆盖；链接的文件夹改为收集成本地副本 |
| [FlashRAG](https://github.com/RUC-NLPIR/FlashRAG)<br><sub>RAG 研究工具包 · Python</sub> | [#257](https://github.com/RUC-NLPIR/FlashRAG/pull/257) | 检索 Precision 指标在空召回样本上除零崩溃，空召回计 0 分并计入均值，补回归测试 |
| [karaoke](https://github.com/Trinkle23897/karaoke)<br><sub>Python</sub> | [#2](https://github.com/Trinkle23897/karaoke/pull/2) | 搜索结果缓存还在有效期内，但分页游标已被 LRU 淘汰，翻页一直返回 410 |
| [a7c2-fl23-research](https://github.com/QAQLeonard/a7c2-fl23-research)<br><sub>Python</sub> | [#35](https://github.com/QAQLeonard/a7c2-fl23-research/pull/35) | 同一路径的输入文件内容变了，离线编译仍复用旧缓存；改为按内容哈希识别 |

### 读 harness：learn-claude-code 精读（17 篇）

[athebear.me/notes/lcc-s01-agent-loop](https://athebear.me/notes/lcc-s01-agent-loop/)

从一个 `while` 循环读到工具、权限、hooks、子 Agent、上下文压缩、记忆、任务图、后台任务、定时任务、多 Agent 团队、MCP、workflow 和 goal loop。每课逐段读 `code.py`，并在本地通过代理接真实模型跑一次，记录跑起来才看得到的现象，比如：

- 上下文压缩从没触发摘要，旧结果被换成路径后模型反复重读，24 次请求发出 90 万字符
- 后台命令早已跑完，结果却要等用户下一句话才被看到
- 多 Agent 时 Lead 答应用 worktree，实际没有创建
- 三个审查维度各自报出同一个 SQL 注入，流程里没有去重

<sub>原文转载自 shareAI-lab/learn-claude-code；导读、真实运行记录和参考答案由 Claude Code 撰写，我用它系统地过一遍这些机制。</sub>

### 最近的笔记

<!-- BLOG-POST-LIST:START -->
- [learn-claude-code s17：Goal Loop，没达标就别停](https://athebear.me/notes/lcc-s17-goal-loop/)
- [learn-claude-code s16：Workflow Runtime，把固定流程写成能续跑的脚本](https://athebear.me/notes/lcc-s16-workflow-runtime/)
- [learn-claude-code s15：Integrated Harness，十几种机制挂在同一个循环上](https://athebear.me/notes/lcc-s15-integrated-harness/)
- [learn-claude-code s14：MCP Tools，工具不再写死在代码里](https://athebear.me/notes/lcc-s14-mcp-plugin/)
- [learn-claude-code s13：Agent Teams，一个 Lead 带几个常驻队友](https://athebear.me/notes/lcc-s13-agent-teams/)
<!-- BLOG-POST-LIST:END -->

### 正在做

**自己的 coding agent harness**：参考 BaoCode 和 DeepSeek Harness 的设计，按「模型循环 → 工具协议 → 上下文 → 权限与取消 → 会话恢复」一块一块地实现。还在早期，做出能演示的版本后再公开。

### 日常

<img src="https://skillicons.dev/icons?i=python,ts,go,flutter&theme=light" alt="Python, TypeScript, Go, Flutter/Dart" />

开发时用 Claude Code、Codex、Cursor。
