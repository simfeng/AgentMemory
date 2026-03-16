# 第一阶段实施文档

这份文档只写两件事：

1. 第一阶段三个 skill 具体做什么
2. 第一阶段目录和文件怎么设计

## 一、第一阶段 Skills

第一阶段只做三个 skill，全部放在主对话里执行。

每轮主对话内部顺序：

1. `what-you-are`
2. `who-you-want-to-be`
3. `matter-manager`

这一阶段的原则：

- 记录长期有价值且判断清楚的信息
- `matter-manager` 只使用 `~/.lifementor/matters/`

### 1. `what-you-are`

作用：理解用户是谁。

写入文件：

- `lifementor/who-you-are.md`

负责更新：

- 用户当前身份和角色
- 用户当前阶段
- 稳定偏好和厌恶
- 稳定行为方式
- 长期压力和限制条件

输出结果：

- `no_update`
- `profile_update`
- `profile_correction`

### 2. `who-you-want-to-be`

作用：理解用户想成为什么样的人，向往怎样的生活，以及想用什么方式处理事情。

写入文件：

- `lifementor/who-you-want-to-be.md`

负责更新：

- 想成为什么样的人
- 向往的生活方式
- 想用什么方式做事和做决定
- 长期的人生方向变化

输出结果：

- `no_update`
- `direction_update`
- `direction_priority_change`
- `direction_correction`

### 3. `matter-manager`

作用：把事项识别、事项修正、`meta.md` 更新、`facts.md` 追加放在一个 skill 里完成。

写入文件：

- `~/.lifementor/matters/<category>/<matter-slug>/meta.md`
- `~/.lifementor/matters/<category>/<matter-slug>/facts.md`

负责处理：

- 判断这轮对话是否属于某个已有事项
- 判断是否需要新建事项
- 判断事项分类和名称是否需要修正
- 当归属不明确时先向用户反问一句
- 更新 `meta.md`
- 追加新的事实进展到 `facts.md`

规则：

- 只允许通过 `skills/matter-manager/scripts/` 下的脚本操作事项文件
- 先看事项目录名，再看 `meta.md`，最后在需要时看 `facts.md`
- `facts.md` 默认只读取最后 100 行
- 需要时可以按文件行号范围读取，例如 `1-100`、`101-200`、`201-300`
- 行号从 `1` 开始，且包含起止行
- `facts.md` 只允许追加，不重写
- 所有脚本只使用 Python 标准库

脚本：

- `scan-matters.py`：扫描已有分类和事项目录
- `read-matter-meta.py`：读取候选事项的 `meta.md`
- `read-matter-facts.py`：按尾部或按行范围读取 `facts.md`
- `upsert-matter-meta.py`：创建或更新 `meta.md`，并确保 `facts.md` 存在
- `move-matter.py`：移动事项目录，完成改分类或改名称
- `append-matter-fact.py`：只向 `facts.md` 追加事实行

## 二、目录和文件设计

第一阶段只保留最必要的目录。

```text
lifementor/
  who-you-are.md
  who-you-want-to-be.md
  matters/
    <category>/
      <matter-slug>/
        meta.md
        facts.md
```

### `lifementor/who-you-are.md`

至少放：

- 用户是谁
- 用户目前处在什么阶段
- 用户稳定的偏好
- 用户稳定的限制条件

### `lifementor/who-you-want-to-be.md`

至少放：

- 用户想成为什么样的人
- 用户向往怎样的生活
- 用户想用什么方式处理事情和做决定

### `~/.lifementor/matters/<category>/<matter-slug>/meta.md`

至少放：

- 事项名称
- 一句话说明这件事是什么
- 这件事为什么重要
- 当前状态
- 可用于匹配的关键词或别名

### `~/.lifementor/matters/<category>/<matter-slug>/facts.md`

至少放：

- 历史事实记录

当前结论：

- 第一阶段只做 `what-you-are`、`who-you-want-to-be`、`matter-manager`
- 先把这套最小结构跑通，再讨论后面的提醒、review、归档
