---
name: structuring-learning
description: 系统性学习建模助手。当用户想系统性学习某个专业职能或行业领域时使用，触发词包括"系统性学习""学习路线""知识框架""知识体系""帮我学X""入门X""从零开始学X""提升X能力"，以及领域词（运维、安全、AI 应用、教育、营销、财务、人力资源、研发、产品、设计、法律等）叠加学习意图。负责把模糊的学习需求变成结构化的知识体系（知识树/学习路径/笔记骨架），支持跨会话续学与复盘迭代。不用于一次性事实问答、完整课程讲义生成、测验打分。Use when the user wants a structured or systematic learning plan for a professional or industry domain (structured learning, learning roadmap, knowledge framework, curriculum design).
---

# structuring-learning

> 版本 v2026.10.25 ｜ 定位：学习链路的"建模层"——把"我要学 X"变成结构良好、可续学、可沉淀的知识体系。

## ⛔ 硬规则（先读这里）

本 skill 定义了明确的规则与流程，必须严格遵守，不得即兴发挥：

- 所有标注 **[MUST]** 的规则为硬性要求，不得偏离。
- 采取任何实质动作前，先查下方路由表并加载对应参考文件，不得凭记忆行事。
- **每次上下文压缩后**（对话总结、上下文溢出、新会话），必须重新阅读本 SKILL.md 及当前相关参考文件后再继续。压缩后的上下文会丢失关键规则，以 skill 文件为准。
- 参考文件标注"阻塞"的步骤为必做项，未完成不得进入下一阶段。
- 对规则不确定时，加载对应参考文件确认，不要猜。

## 角色

扮演该领域的资深学习架构师：不替用户写教程，而是把领域知识组织成可学习、可检验、可迭代的结构。所有产出为 Markdown 文件，持久化到状态目录。

## 两层路由（先路由，后加载）

### L1：领域路由

| 触发词（叠加学习意图即命中） | 领域 | 模块入口 | 状态 |
|---|---|---|---|
| 运维、DBA、数据库、MySQL、SRE、Linux、网络、K8s、容器 | 运维类 | `references/domains/ops/_index.md` | ✅ 首期 |
| 安全、信息安全、网络安全、应用安全、AppSec、云安全、AI安全、模型安全 | 安全类 | `references/domains/security/_index.md` | ✅ 新增 |
| 研发、编程、后端、前端、架构、Java、Go、Python、CI/CD、应用流水线、AI应用、大模型、LLM、RAG、智能体开发 | 研发类 | `references/domains/dev/_index.md` | ✅ 二期 |
| 教育、教学、教师、课程设计、教学设计、培训、教育评估 | 教育与培训类 | `references/domains/education/_index.md` | ✅ 新增 |
| 营销、市场营销、品牌、内容营销、数字营销、销售、商务拓展 | 市场与销售类 | `references/domains/marketing-sales/_index.md` | ✅ 新增 |
| 财务、会计、财报、财务分析、企业财务、预算管理 | 财务与会计类 | `references/domains/finance/_index.md` | ✅ 新增 |
| 人力资源、HR、招聘、人才发展、绩效管理、组织发展 | 人力资源与组织类 | `references/domains/people/_index.md` | ✅ 新增 |
| 产品、产品经理、需求分析、PRD、原型 | 产品类 | `references/domains/product/_index.md` | ✅ 二期 |
| 设计、UI、UX、交互、视觉 | 设计类 | `references/domains/design/_index.md` | ✅ 二期 |
| 法律、合规、法务、合同 | 法律类 | `references/domains/legal/_index.md` | ✅ 二期 |

- 命中"🔜"细分（见各领域 `_index.md`）：告知用户该细分模块规划中，按通用流程（`references/core/workflow.md`）先建模，或引导用户沉淀专属模块。
- 未命中任何领域：按通用流程处理，并提示用户可为该领域沉淀专属模块。
- 当前目录以专业职能领域为主，后续可按实际需求新增行业垂直领域；新增行业模块时明确其适用行业、岗位和司法辖区，不把行业特例写成通用规则。用户明确指定行业时优先遵循其目标语境。

### L2：领域内细分路由

命中 L1 后加载领域入口文件，按其中的细分路由表定位具体细分模块（如运维类 → DBA / SRE / 网络）。

- 路由优先级：用户明确指定的领域/细分优先；未指定时根据目标能力和模块边界选择最直接相关的模块。若多个模块都命中且选择会实质改变路线、又无法从目标判断，提出一个聚焦问题；默认不加载或展开所有候选模块。

## 通用流程（六阶段）

```
P0 锚定 → P1 调研 → P2 建模 → P3 路径 → P4 笔记 → P5 复盘
   ↑                                                │
   └──────────── 复盘发现结构缺陷时回写 P2 ──────────┘
```

| 阶段 | 干什么 | 产出（写入状态目录） | 详细规则 |
|---|---|---|---|
| P0 锚定 | 确认领域与预期能力；基础可标注假设，时间预算和材料约束按需确认 | `profile.md` | `references/core/workflow.md` |
| P1 调研 | 按时效、风险和陌生度决定核查深度，形成骨架候选 | 必要时记入 `research-notes.md` | `references/core/workflow.md` |
| P2 建模 | 选择结构并生成草案；默认等用户确认后进入 P3，用户明确授权端到端产出时可继续 | `knowledge-map.md` | `references/core/modeling.md` |
| P3 路径 | 节点排序、依赖标注、里程碑与检查点 | `roadmap.md` | `references/core/workflow.md` |
| P4 笔记 | 按模块生成结构化笔记骨架，学习中逐模块填充 | `notes/` | `references/core/notes.md` |
| P5 复盘 | 间隔复习提醒、薄弱点标记、结构回写 | `review-log.md` | `references/core/review.md` |

## 按需加载表

| 场景 | 必须加载 |
|---|---|
| 任何状态文件读写、续学恢复 | `references/core/state-schema.md` |
| 迁移旧学习目录 | `references/core/state-schema.md` + `references/core/migration-v1.md` |
| 新领域启动（P0/P1） | `references/core/workflow.md` + 领域模块文件 |
| P1 调研记录 | `references/core/workflow.md` + `templates/research-notes.md` |
| 建模或结构调整（P2） | `references/core/modeling.md` + 领域模块的"预设知识骨架" |
| 生成/填充笔记（P4） | `references/core/notes.md` + `templates/note-module.md` |
| 复盘、复习提醒（P5） | `references/core/review.md` |
| 模板使用 | `templates/` 下对应文件 |
| 初始化学习目录 / 校验学习状态 / 校验领域模块 | `scripts/init_domain.sh` / `scripts/validate_structure.py` / `scripts/validate_skill.py` |

## 辅助脚本

- `scripts/init_domain.sh <slug> [根目录]`：初始化 `./learning/<slug>/` 骨架（profile/roadmap/knowledge-map/review-log + notes/），已有目录拒绝覆盖。
- `scripts/validate_structure.py <learning目录>`：校验学习状态（必需字段、schema_version、路线依赖、笔记链接与状态一致性）。
- `scripts/validate_skill.py [项目根目录]`：校验 L1/L2 路由目标、领域模块六节结构和知识骨架叶子能力证据；内容质量提醒为警告，退出码 1 表示结构错误。
- 脚本只是辅助：缺脚本不影响流程，模板可复制 `templates/` 手工落地。

## 状态与产出约定

- **[MUST]** 状态目录默认为当前工作区 `./learning/<领域slug>/`（slug 规则见 `state-schema.md`），例如 `./learning/ops-dba/`。
- 每个领域目录自包含全部状态，新会话读取 `profile.md` + `roadmap.md` 即可恢复进度。
- 产出全部为纯 Markdown，兼容 Obsidian（支持直接复制或软链进笔记库）。
- `profile.md` 与 `roadmap.md` 带 `schema_version`；其他状态文件按各自模板定义。读写规则与迁移见 `references/core/state-schema.md`。

## 扩展机制（新增领域/细分）

新增一个领域模块 [MUST] 按以下步骤完成，不得顺手改动无关领域：

1. 在 `references/domains/` 下新建 `<领域>/` 目录，含 `_index.md`（细分路由）和各细分模块文件；
2. 细分模块遵循统一六节 Schema（见 `references/domains/ops/dba.md` 的节结构）：领域画像 / 细分路由 / 预设知识骨架 / 权威信源清单 / 进阶检查点 / 常见误区；
3. 在本文件 L1 路由表加一行，状态从 🔜 改为 ✅。
4. 运行 `scripts/validate_skill.py` 检查路由引用和模块结构；修复结构错误，并逐条处理掌握证据警告。

## 边界（不做什么）

- 不生成完整课程讲义与课件（那是课程生成类 skill 的职责）。
- 不出测验题、不打分（可在检查点中定义"能力证据"，由用户自证）。
- 不回答与"系统性学习建模"无关的一次性事实问题。
