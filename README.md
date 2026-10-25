# structuring-learning

> 学习链路的"建模层"——把"我要学 X"变成结构良好、可续学、可沉淀的知识体系。

一个遵循开放 [Agent Skills](https://agentskills.io/specification) 规范的 AI Agent 技能：当你说"帮我系统性学习 X"时，它不会直接扔给你一份课程，而是先带你完成**知识结构建模**——产出知识树、学习路径、结构化笔记与复盘机制，全部落为纯 Markdown，可直接进 Obsidian 等知识库长期维护。

## 核心特性

- **领域模块化路由**：触发词 → L1 专业领域或行业领域 → L2 细分方向，每域独立维护、独立触发
- **预置知识骨架**：34 个细分模块各带预设知识骨架，叶子节点标注可观察的能力证据（如何判断掌握），不从零起步
- **分级信源清单**：每个模块配权威信源（官方文档 > 经典书籍 > 优质社区）
- **六阶段流水线**：锚定 → 调研 → 建模 → 路径 → 笔记 → 复盘，复盘结果可回写修正知识结构（迭代闭环）
- **可续学状态**：每个学习领域一套自包含状态文件（档案/知识地图/路径/笔记），schema 版本化，新会话读档案即恢复进度
- **目标能力驱动**：按用户希望完成的任务和前置依赖裁剪内容，不把树的层级直接当作能力等级
- **序号化笔记**：`notes/<两位序号>-<slug>.md`，序号取自学习路径表，目录顺序即学习顺序

## 覆盖领域

| 领域 | 细分模块 |
|---|---|
| 运维 ops | DBA · SRE · 系统运维 · 网络运维 · 容器与云原生 |
| 安全 security | 应用安全 · 云与容器安全 · 安全运营与事件响应 |
| 研发 dev | 后端 · 前端 · 移动 · 测试工程 · 架构设计 · AI 应用工程 |
| 教育与培训 education | 教学设计 · 教学与评估 |
| 市场与销售 marketing-sales | 市场与营销 · 销售 |
| 财务与会计 finance | 会计与财务报告 · 财务分析与企业财务 |
| 人力资源与组织 people | 招聘与选拔 · 人才与组织发展 |
| 产品 product | 产品经理核心 · B端产品 · 数据分析 · 增长产品 |
| 设计 design | UI/UX · 视觉 · 动效 · 设计系统 |
| 法律 legal | 合同法务 · 劳动用工 · 数据合规 · 公司与投融资 |

每个模块统一六节结构：领域画像 / 细分路由 / 预设知识骨架 / 权威信源清单 / 进阶检查点 / 常见误区。

## 目录结构

```
structuring-learning/
├── SKILL.md                        # 入口：触发词表 + 两层路由表 + 硬规则
├── references/
│   ├── core/                       # 领域无关的通用方法论（所有模块共用）
│   │   ├── workflow.md             #   六阶段流程
│   │   ├── modeling.md             #   建模方法论（树/网/链模式选择）
│   │   ├── notes.md                #   结构化笔记规范（Obsidian 兼容）
│   │   ├── review.md               #   间隔复习与复盘回写规则
│   │   ├── state-schema.md         #   状态文件 schema 与版本号
│   │   └── migration-v1.md         #   旧学习目录迁移说明
│   └── domains/                    # 领域模块注册处
│       ├── ops/  security/  dev/  education/  marketing-sales/  finance/  people/
│       ├── product/  design/  legal/
├── templates/                      # 产出物模板（档案/调研记录/知识地图/路径/模块笔记）
└── scripts/
    ├── init_domain.sh              # 初始化一个学习领域目录骨架
    ├── validate_structure.py       # 校验产出物结构完整性
    ├── validate_skill.py           # 校验领域路由、模块结构与掌握证据
    └── sync-to-workbuddy.sh        # 本仓库 → WorkBuddy 工具内目录同步
```

## 安装

本项目的 `SKILL.md` 和配套 `references/`、`scripts/`、`templates/` 遵循 Agent Skills 的目录约定。Agent 是否能使用它，还取决于该 Agent 是否支持此规范，以及它从哪里发现技能：**格式可复用，安装目录和自动发现能力由各工具决定**。对未列出的 Agent，请查阅其官方文档，将完整目录放到它支持的 skills 位置；不能仅凭存在 `SKILL.md` 就假设工具会自动加载。

以下是已提供 Agent Skills 支持的工具的常用安装位置。把仓库完整克隆到目标目录后，`SKILL.md` 应直接位于 `structuring-learning/` 下。

| Agent | 用户级安装位置 | 项目级安装位置 | 官方说明 |
|---|---|---|---|
| Codex | `~/.agents/skills/structuring-learning/` | `<项目>/.agents/skills/structuring-learning/` | [Codex Skills](https://developers.openai.com/codex/skills) |
| Claude Code | `~/.claude/skills/structuring-learning/` | `<项目>/.claude/skills/structuring-learning/` | [Claude Code Skills](https://code.claude.com/docs/en/skills) |
| Gemini CLI | `~/.agents/skills/structuring-learning/`（也支持 `~/.gemini/skills/`） | `<项目>/.agents/skills/structuring-learning/`（也支持 `.gemini/skills/`） | [Gemini CLI Agent Skills](https://geminicli.com/docs/cli/skills/) |

例如，在 macOS/Linux 上安装到 Codex 和 Gemini CLI 共用的用户级目录：

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/HuanR9/structuring-learning.git \
  ~/.agents/skills/structuring-learning
```

安装到 Claude Code 用户级目录：

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/HuanR9/structuring-learning.git \
  ~/.claude/skills/structuring-learning
```

项目级安装适合团队共享并纳入版本控制。在目标项目根目录执行对应命令：

```bash
# Codex 或 Gemini CLI
mkdir -p .agents/skills
git clone https://github.com/HuanR9/structuring-learning.git \
  .agents/skills/structuring-learning

# Claude Code
mkdir -p .claude/skills
git clone https://github.com/HuanR9/structuring-learning.git \
  .claude/skills/structuring-learning
```

更新时进入技能目录运行 `git pull`。工具通常会自动发现或在新会话加载技能；若未出现，请按对应工具文档检查目录并重启会话。

### WorkBuddy

WorkBuddy 使用自己的用户级目录，可直接克隆：

```bash
mkdir -p ~/.workbuddy/skills
git clone https://github.com/HuanR9/structuring-learning.git \
  ~/.workbuddy/skills/structuring-learning
```

如果已将仓库克隆到其他位置，也可以使用仓库内的同步脚本：先预览差异，再明确应用：

```bash
./scripts/sync-to-workbuddy.sh
./scripts/sync-to-workbuddy.sh --apply
```

`--apply` 默认保留目标目录中本仓库没有的文件并保护 `learning/`；只有明确要清理目标独有文件时才加 `--prune`。

## 使用方式

新会话中直接表达学习意图，例如：

- "帮我系统性学习 DBA，零基础，每周能投 5 小时"
- "我想系统学 SRE，有 3 年 Linux 经验"
- "带我做一套 UI/UX 的知识框架"

Skill 会先确认领域与预期能力，再结合基础生成结构；时间预算仅在需要估算排期时追问。

## 设计理念

1. **结构化优先于内容堆砌**：知识的组织形式（树/网/链）影响学习与复用，先建模再填充
2. **掌握证据驱动**：每个叶子节点必须回答"会做什么算过关"，拒绝"学过了"的虚假进度
3. **单一事实来源**：学习路径表是序号的唯一来源，笔记文件名、进度状态全部由它派生
4. **复盘闭环**：复习中发现的薄弱点与结构缺陷，回写修正知识树，结构随学习演进
5. **领域可扩展**：新增细分 = 领域入口中的路由项 + 细分模块；新增领域还需新增入口文件并登记到 L1 路由，不因此改动无关核心规则

## 版本

当前版本 **v2026.10.25**（版本规则：v+日期）

`validate_skill.py` 的掌握证据检查基于叶子节点文本特征，只能发现明显缺项；通过不代表证据具体、充分或已获领域专家确认。

## License

MIT
