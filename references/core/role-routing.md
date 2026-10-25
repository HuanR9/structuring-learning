# 岗位导向路由

当用户以目标岗位、转岗或岗位任务描述学习需求时，使用本文件把岗位目标映射到现有专业模块。岗位路由是知识模块的组合入口，不是独立、穷尽的职业分类，也不替代领域模块。

## 路由原则

1. 先识别用户希望承担的岗位或完成的工作任务，再定位其核心能力；用户只想学某专业领域或单项能力时，直接按 `SKILL.md` 的领域路由处理。
2. 将岗位要求拆成核心模块、必要协作模块和可选扩展。优先使用现有领域模块，不复制知识骨架；只展开与目标任务和目标熟练度相关的部分。
3. 表内映射是起点而不是岗位标准。公司、行业、资历和地区会改变职责边界；用户提供的岗位说明书、实际任务和目标行业优先于通用映射。
4. 不清楚具体岗位时，先用目标任务建模；只有岗位选择会实质改变学习结构时才追问。不要为了填充档案而强行选择岗位。
5. 岗位、行业和司法辖区分开记录。岗位先映射到专业模块；若行业会改变任务或风险，再查 `references/industries/_index.md` 选择情境叠加。涉及法规、准则或监管要求时，确认适用司法辖区并核验现行来源。

## 常见岗位映射

| 目标岗位/岗位族 | 核心模块 | 可按目标加入的协作模块 |
|---|---|---|
| DBA / 数据库管理员 | `references/domains/ops/dba.md` | `references/domains/ops/system.md`、`references/domains/ops/network.md`、`references/domains/security/cloud-security.md` |
| SRE / 可靠性工程师 | `references/domains/ops/sre.md` | `references/domains/ops/system.md`、`references/domains/ops/network.md`、`references/domains/ops/cloud-native.md`、`references/domains/security/security-operations.md` |
| 后端工程师 | `references/domains/dev/backend.md` | `references/domains/dev/architecture.md`、`references/domains/dev/qa.md`、`references/domains/security/application-security.md` |
| 前端工程师 | `references/domains/dev/frontend.md` | `references/domains/dev/qa.md`、`references/domains/design/ui-ux.md`、`references/domains/security/application-security.md` |
| QA / 测试工程师 | `references/domains/dev/qa.md` | `references/domains/dev/backend.md` 或 `references/domains/dev/frontend.md`，按被测系统选择 |
| AI 应用工程师 | `references/domains/dev/ai-engineering.md` | `references/domains/dev/backend.md`、`references/domains/dev/qa.md`、`references/domains/security/application-security.md` |
| 应用安全工程师 | `references/domains/security/application-security.md` | `references/domains/dev/backend.md`、`references/domains/dev/qa.md`、`references/domains/security/cloud-security.md` |
| 产品经理 | `references/domains/product/pm.md` | `references/domains/product/data.md`、`references/domains/product/growth.md`、`references/domains/design/ui-ux.md` |
| UI/UX 设计师 | `references/domains/design/ui-ux.md` | `references/domains/design/design-system.md`、`references/domains/design/visual.md`、`references/domains/product/pm.md` |
| 教师 / 教学岗位 | `references/domains/education/teaching-assessment.md` | 课程或单元设计是目标时加入 `references/domains/education/instructional-design.md` |
| 教学设计师 / 课程设计师 | `references/domains/education/instructional-design.md` | 教学实施与评估是目标时加入 `references/domains/education/teaching-assessment.md`；企业培训可加入 `references/domains/people/people-development.md` |
| 市场营销人员 | `references/domains/marketing-sales/marketing.md` | `references/domains/product/growth.md`、`references/domains/product/data.md` |
| 销售 / 商务拓展 | `references/domains/marketing-sales/sales.md` | `references/domains/marketing-sales/marketing.md`、`references/domains/product/b-end.md` |
| 会计 / 财务报告岗位 | `references/domains/finance/accounting.md` | 数据隐私或跨境报告是实际职责时再关联 `references/domains/legal/data-compliance.md`；税务和审计要求按司法辖区补充核查 |
| 财务分析 / FP&A | `references/domains/finance/financial-analysis.md` | `references/domains/finance/accounting.md`、`references/domains/product/data.md` |
| 数据分析师 | `references/domains/product/data.md` | `references/domains/finance/financial-analysis.md`、`references/domains/product/pm.md`；依分析对象选择 |
| 招聘 / 人才获取岗位 | `references/domains/people/talent-acquisition.md` | `references/domains/people/people-development.md`；用工规则关联 `references/domains/legal/labor.md` |
| 人才发展 / 组织发展岗位 | `references/domains/people/people-development.md` | `references/domains/education/instructional-design.md`；用工规则关联 `references/domains/legal/labor.md` |
| 法务 / 合规岗位 | 按目标从 `references/domains/legal/_index.md` 选择细分 | 需要时加入 `references/domains/security/application-security.md` 或 `references/domains/finance/accounting.md` |

表中“核心模块”只表示通用起点，不表示所有岗位都必须掌握完整模块；协作模块按工作任务选择。其他岗位按相同方法组合现有模块；暂时没有合适模块时，按通用流程建立目标结构并提示模块缺口，不臆造岗位标准。

## 路线裁剪

- **入门/转岗**：纳入岗位核心任务所需的基础和前置知识；先说明通用假设，避免仅凭职位名称推断具体公司要求。
- **在岗提升**：从用户遇到的任务、交付物或瓶颈反推需要加强的模块，不默认重学完整基础路线。
- **资深/管理职责**：按目标加入架构、风险、协作、决策或人才管理内容；不把职级名称直接等同能力等级。
- 若用户提供招聘描述或岗位标准，抽取要求并标注哪些是原文要求、哪些是根据模块作出的推断；差异较大时呈现待确认项。
