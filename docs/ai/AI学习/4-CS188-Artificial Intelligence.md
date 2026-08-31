## Lecture1-Introduction
### 1、AI是什么
Being rational means acting to maximize your expected utility
A better title for this course might be COMPUTATIONAL RATIONALITY

#### 我们如何看待智能？

- skills-based perspective: 能做某件事
- embodiment perspective: 具身
- Psychometrics perspective: 衡量能力，尤其是未知的任务
- Human-compatible perspective
	- machine's objective is to maximize human utility
	- initially uncertain about human preferences
	- must learn about preferences from human behavior
- Specialization is for insects

#### 大脑呢？
brains are very good at making rational decisions, but not perfect.
brains aren't as modular as software, so hard to reverse engineer!
AI may be better than brains at some tasks

Still, the brain can be a great inspiration for AI

#### 人工智能简史

![[4-CS188-Artificial Intelligence-1788005226292.webp]]

![[4-CS188-Artificial Intelligence-1788005259338.webp]]

#### 课程主题

Search & Planning: How can I use my model of the world to find a sequence of actions to achieve my goal?
Probability & inference: How can I make sense of uncertainty
Supervised learning: How can I learn a model of a world from data
reinforcement learning: How can I learn a policy for any situation so that I can maximize utility

### 2、Agents

> 这是2023年8月的note

智能体需要能够与环境交互，行动作用于环境。一种智能体是不思考直接行动的；另一种是能提前思考行为后果再行动的。
智能体如何设计，很大程度上取决于环境。
不同的环境：

- 部分可观测：智能体无法获得完整信息，需要估计；完全可观测：智能体拥有完整信息
- 随机环境：某个行动可能产生多个不同概率的结果
- 多智能体环境：智能体会随机化其行动避免被预测（智斗）
- 静态环境：智能体的作用不改变；动态环境：智能体的作用改变环境
- 物理规律是否已知：如果已知，智能体可以利用规律；如果未知，智能体需要做出行动学习动态特性

## Lecture2-Search

### 1、Agents that Plan Ahead
#### Reflex Agent(反射型)

- 基于当前感知/记忆选择行动
- may have memory or a model of the world's current state
- 不考虑行动后果
- 只考虑世界“现在”的状态

#### Planning agent(规划型)

- Ask "What if"
- Decisions based on (hypothesized) consequences of actions
- Must have a model of how the wold evolves in response to actions
- Must formulate a goal
- 考虑世界“将来”会是怎么样

### 2、Search Problems

A search problem consist of:

- A state space
- A successor function(with actions)
- A start state and a goal test

A solution is a sequence of actions which transforms the start state to a goal state


