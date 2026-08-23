# Git / Branch / PR / ADR / RFC 纪律

## 1. 默认分支
- `main`：只接受通过 CI 与必要 review 的稳定代码。
- Sprint branch：
  - `feat/s0-bootstrap`
  - `feat/s1-case-evidence`
  - `feat/s2-model-registry`
  - `feat/s3-runtime-control`

## 2. Commit
每次提交只承担一个清晰目的。推荐前缀：
- `feat:`
- `fix:`
- `test:`
- `docs:`
- `refactor:`
- `chore:`
- `security:`

## 3. PR 必须说明
- 对应任务 ID；
- 改了什么；
- 没改什么；
- 是否触碰 Absolute Invariants；
- 测试证据；
- migrations；
- 新依赖；
- secrets 风险；
- 已知技术债；
- 是否需要 ADR/RFC。

## 4. ADR vs RFC
**ADR**：实现选择，不改变协议语义，例如 migration 工具、目录内部结构、日志库。

**RFC_REQUIRED**：涉及下列任何变化必须停止自动决定：
- Protocol semantic；
- Case Mode；
- 状态机语义；
- T0/污染规则；
- 权限边界；
- Controller/Domain/Expert 准入；
- Validation/Baseline Parity；
- Dissent/Falsification；
- Safety/Publication；
- 自动现实行动能力。

## 5. Merge-blocking
V0.1 基线建议至少将这些 tests 设为阻断：
AT-01/02/03/05/08/11/12/13/14/15/16/18（按实现 Sprint 分阶段启用）。

## 6. 不允许
- `--no-verify` 绕开测试作为正常开发方式；
- 删除失败测试来“恢复绿色”；
- force push main；
- 把真实 secret 写入历史；
- 未说明的第三方 SaaS 依赖。
