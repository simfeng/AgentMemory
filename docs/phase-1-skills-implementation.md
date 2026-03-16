# 第一阶段实施文档

这份文档只写两件事：

1. 第一阶段四个 skill 具体做什么
2. 第一阶段目录和文件怎么设计

## 一、第一阶段 Skills

第一阶段只做四个 skill，全部放在主对话里执行。

每轮主对话内部顺序：

1. `what-you-are`
2. `who-you-want-to-be`
3. `matter-detection`
4. `matter-fact-update`

这一阶段的原则很简单：

- 记录长期有价值且判断清楚的信息
- `matter-detection` 和 `matter-fact-update` 只使用 `lifementor/matters/`

### 1. `what-you-are`

作用：理解用户是谁。

负责更新：

- 用户当前身份和角色
- 用户当前阶段
- 稳定偏好和厌恶
- 稳定行为方式
- 长期压力和限制条件

写入文件：

- `lifementor/who-you-are.md`

输出结果：

- `no_update`
- `profile_update`
- `profile_correction`

规则：

- 记录稳定的用户事实

### 2. `who-you-want-to-be`

作用：理解用户想成为什么样的人，向往怎样的生活，以及想用什么方式处理事情。

负责更新：

- 想成为什么样的人
- 向往的生活方式
- 想用什么方式做事和做决定
- 长期的人生方向变化

写入文件：

- `lifementor/who-you-want-to-be.md`

输出结果：

- `no_update`
- `direction_update`
- `direction_priority_change`
- `direction_correction`

规则：

- 记录稳定的人生方向事实

### 3. `matter-detection`

作用：判断这轮对话是否命中某个已有事项，或者是否需要新建事项。

这个 skill 在实际流程里更接近“路由入口”。

只要用户这轮消息里包含实际内容，而不是纯问候或纯寒暄，就应该先经过它，判断这段内容是不是属于某个事项。

负责判断：

- 这是不是一件值得持续跟踪的事
- 它是不是已经有对应的事项
- 如果没有，是否要新建
- 这个事项应该放到哪个分类下面

写入位置：

- 新事项创建到 `lifementor/matters/<category>/<matter-slug>/`

输出结果：

- `match_existing_matter`
- `create_new_matter`
- `no_matter_signal`

规则：

- 优先匹配已有事项
- 在有持续跟踪价值时创建新事项
- 在大多数有效消息里优先运行它做事项归类
- 事项名要尽量带上完整信息，但保持合理长度
- 先看事项目录名，再看 `meta.md`，最后在需要时看 `facts.md`

### 4. `matter-fact-update`

作用：在事项已经确定后，提取这轮对话带来的最新事实。

负责更新：

- 新动作
- 新状态
- 新决定
- 新阻碍
- 新风险

写入文件：

- 对应的 `lifementor/matters/<category>/<matter-slug>/facts.md`

输出结果：

- `no_fact_update`
- `status_update`
- `decision_update`
- `obstacle_update`
- `fact_entry`
- `mixed_update`

规则：

- 记录这轮对话里最新确认的事实

## 二、目录和文件设计

第一阶段只保留最必要的目录。

根目录名直接用：

```text
lifementor/
```

- `lifementor` 就是这套 Agent 记忆本身
- 名字直接、有语义
- 适合作为后续所有长期记录的统一入口

### 推荐结构

```text
lifementor/
  who-you-are.md
  who-you-want-to-be.md
  matters/
    <category-a>/
      <matter-1>/
        meta.md
        facts.md
    <category-b>/
      <matter-2>/
        meta.md
        facts.md
```

这就是第一阶段的完整结构。

### 保留这些文件和目录的原因

`lifementor/who-you-are.md`

- 集中存放稳定的用户认知
- 让 `what-you-are` 只有一个明确写入目标
- 后续读取用户画像时路径固定、成本低
- 按需创建和更新

`lifementor/who-you-want-to-be.md`

- 集中存放人生方向
- 让 `who-you-want-to-be` 只维护一份人生方向主文件
- 按需创建和更新

`lifementor/matters/`

- 这里存放所有事项
- 先按分类组织
- 一件事一个目录，边界清晰
- 每个事项都拆成 `meta.md` 和 `facts.md` 两层
- 主对话里先看目录名，再读 `meta.md`，最后在需要时读 `facts.md`
- `matter-detection` 和 `matter-fact-update` 都使用这里的内容

分类由 `matter-detection` 按需复用或创建。

分类原则是：

- 能帮助后续管理
- 名字清楚
- 粒度适中
- 适合长期使用

## 三、每个文件最少要放什么

### `lifementor/who-you-are.md`

至少放：

- 用户是谁
- 用户目前处在什么阶段
- 用户稳定的偏好
- 用户稳定的限制条件

这个文件存稳定的自我认知。

### `lifementor/who-you-want-to-be.md`

至少放：

- 用户想成为什么样的人
- 用户向往怎样的生活
- 用户想用什么方式处理事情和做决定

这个文件存稳定的人生方向。

### `lifementor/matters/<category>/<matter-slug>/meta.md`

至少放：

- 事项名称
- 一句话说明这件事是什么
- 这件事为什么重要
- 当前状态
- 可用于匹配的关键词或别名

这个文件是事项的轻量识别层。

Agent 在判断当前对话属于哪个事项时，优先读这个文件。

### `lifementor/matters/<category>/<matter-slug>/facts.md`

至少放：

- 最近一次明确事实
- 历史事实记录

这个文件是事项的详细事实层。

Agent 在已经命中某个事项后，读取这个文件并追加最新事实。

## 四、当前结论

第一阶段就做这四个 skill：

- `what-you-are`
- `who-you-want-to-be`
- `matter-detection`
- `matter-fact-update`

第一阶段就用这套目录：

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

先把这套最小结构跑通，再讨论后面的提醒、review、归档。
