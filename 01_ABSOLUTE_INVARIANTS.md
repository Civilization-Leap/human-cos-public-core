# Human-COS Runtime V0.1｜绝对不变量

以下内容属于开发基线的工程宪则。Programming AI、技术负责人、普通 PR 均不得静默改变其语义。

## I-01 流程权与认知权分离
Orchestrator 以代码和版本化协议决定状态、权限、解锁、冻结、升级、回退。模型不能决定自己何时看什么。

## I-02 原始证据不可覆盖
Evidence source snapshot、Raw Model Output、Independent Expert Submission 一旦冻结，只能追加 revision，不能原位 UPDATE。

## I-03 独立先于交流
需要独立判断的 Worker / Expert 必须先分别完成并冻结；Cross Examination 只能发生在协议允许的后续 Stage。

## I-04 T0 是数据层边界
历史洁净盲测中，POST_T0 Evidence 不得进入 Worker Context。不能以 Prompt“不要使用后来信息”代替隔离。

## I-05 主体可见世界
Evidence Visibility 必须区分 public、actor、role、time。系统不得把全知视角当作现实参与者视角。

## I-06 分歧是信息
高影响少数意见必须结构化保存。Final Synthesis 不得无来源删除、平均或吞并 Dissent。

## I-07 双向推演
重大判断必须同时包含改善/收益路径与恶化/风险路径，避免系统成为单向风险放大器。

## I-08 可证伪
关键 Final Claim 必须有 `wrong_if`；需要时同时有 `downgrade_if`、`upgrade_if`、`rollback_if`。缺失时不得 Seal。

## I-09 专业资格不能角色扮演
没有合格 Task Capability 的模型不得被 Prompt 临时包装为受限专业 Worker。应产生 Capability Gap。

## I-10 独立性必须精确标记
Context Independence ≠ Model-family Independence。每个 Run 必须记录独立性类型，不能把同一基础模型多会话写成“多模型验证”。

## I-11 证据永远是数据
网页、文件、邮件、检索结果中的指令不具有系统权力。Evidence parser / retriever 的输出不能修改 Tool Policy、System Prompt 或 Protocol。

## I-12 Solver / Judge 分离
同一 Run 中，生成核心答案的 Solver 不能作为唯一 Evaluator / Blind Judge 给自己判分。

## I-13 Human Expert 是正式主体
专家结果与模型结果均需 provenance、freeze、dissent、falsification；专家身份不自动等于真理。

## I-14 Human-COS 不替代成熟专业系统
正式验证必须允许 High-quality Professional Baseline 与 Human-COS 同级比较。系统要证明增量，而非只证明能运行。

## I-15 Human-COS 核心闭环不得被简化
`行为 → 利害 → 人心 → 行为` 必须保留。所谓“人心”只允许通过可观察行为、利益位置、现实约束和方向性预期进入，不做人格式读心。

## I-16 阶段—相位不能被统一硬编码
Runtime 支持 STARTUP / TRANSITION / STABLE / SELF_MAINTAINING 与 Case Phase。不得用稳定期规则机械倒逼启动期，也不得让临时紧急权限永久化。

## I-17 高风险现实执行能力禁止
V0.1 只能研究、推演、评估、记录、发布；不得自动实施军事、金融交易、关键基础设施控制、生物操作等现实行动。

## I-18 流程可复现，不承诺文本复刻
必须能重建输入、权限、模型身份、参数、Prompt、工具、协议和运行 lineage；模型文本重放可以不同。

## I-19 Protocol 语义变更必须 RFC
T0、污染、独立性、基线公平、异议、可证伪、安全、发布规则的语义变化必须 RFC + regression impact review。

## I-20 GitHub 不取代 Runtime 审批
GitHub Environments / reviewers 是部署增强；Human-COS 自己的 Approval State 才是系统主机制。
