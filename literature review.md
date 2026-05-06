# 道路网络巡检文献详细综述

> 每篇文献均由独立子agent直接读取原始PDF并分析，共20篇

---

## 文献概览

- **文献总数**: 20 篇
- **发表年份**: 2021 – 2025
- **涉及核心问题**: CARP、DCARP、UCARP、Drone ARP、Vehicle-Drone协同ARP等
- **主要算法**: Branch-and-Cut、GRASP、Memetic Algorithm、GP Hyper-heuristic、ABC、IALNS、DaAM(深度学习)、MAENS-GN等

---

## 详细文献分析（按编号）

---

### 文献 1：Rich Arc Routing Problem in City Logistics（富弧路由问题）

**来源**: Transportation Research Part B, Vol.166, 2022, pp.143–182  
**作者**: Jiawei Lu, Qinghui Nie, Monirehalsadat Mahmoudi, Jishun Ou, Chongnan Li, Xuesong Simon Zhou  
**DOI**: 10.1016/j.trb.2022.10.007

#### 问题变体场景描述

本文研究的是"富弧路由问题"（Rich Arc Routing Problem, RARP），应用于城市物流场景。具体场景如下：

- **时变行驶时间（Time-Dependent Travel Time）**：城市道路在早晚高峰与非高峰期间速度不同，车辆行驶时间随出发时刻而变化。为精确建模，本文采用流体队列理论（Fluid Queue-based）构建时变行驶时间函数，使得时间估计既满足FIFO（先进先出）性质，又可用闭合形式计算。
- **多约束"富"场景**：在基础CARP（带容量约束弧路由）之上叠加：（1）时间窗约束（time windows）；（2）多个仓库（multi-depot）；（3）强制休息时间（mandatory break times）；（4）路线长度/时间上限；（5）车辆异构（heterogeneous fleet）。典型应用包括市政道路洒水车路由、扫街车路由、冬季撒盐除冰车路由。
- **服务活动自身产生拥堵**：服务车辆在执行道路服务时（如扫地、喷水）会占用车道，对其他交通产生拥堵影响，因此需要将服务活动对行驶时间的反馈纳入模型。

#### 算法核心步骤描述

1. **时变行驶时间建模**：利用流体队列（Fluid Queue）理论，将每条弧的行驶时间建模为出发时刻的分段函数。通过捕捉车流量动态（高峰/非高峰），对每条弧构建时变速度曲线，确保FIFO性质成立。
2. **RARP数学模型构建**：在集覆盖/集划分框架下建立整数规划模型，以路线为变量，每条路线的行程费用通过动态DP（时变最短路径）计算。
3. **Branch-and-Price算法**：主问题（Master Problem）采用列生成（Column Generation）松弛，每次迭代通过求解定价子问题（Pricing Subproblem）来生成有前景的路线。定价子问题为时变有容量约束的最短路径问题，采用动态规划（DP with resource constraints）求解。
4. **时变最短路径计算**：在Branch-and-Price的子问题中，利用时间离散化后的DP算法，计算给定出发时刻下路网中任意两节点之间的最短行驶时间，并维护FIFO性质。
5. **上界启发式**：为加速分支定价，先用基于扫描的构造式启发式生成初始可行解，再用局部搜索（如Or-opt、2-opt*）优化，提供分支定价的上界。

---

### 文献 2：Mothership and Drone Routing Problem with Graphs（母船-无人机弧路由）

**来源**: Computers and Operations Research, Vol.136, 2021, 105445  
**作者**: Lavinia Amorosi, Justo Puerto, Carlos Valverde  
**DOI**: 10.1016/j.cor.2021.105445

#### 问题变体场景描述

本文提出"母船与无人机路由问题"（Mothership and Drone Routing Problem with Graphs, MDRPG），研究母船（地面车辆/船/直升机）与无人机协同，共同完成对**图状目标区域**的巡检任务：

- **图状目标（Target Graphs）**：待巡检目标不是离散点，而是一组"图"（如某一区域的边界多边形、线状管道、河道）。无人机需覆盖这些图中一定比例的边长（edge traversal）或图总长度的一定比例。
- **三种母船运动模式**：
  - **AMDRPG（全地形模式）**：母船在连续欧氏平面内自由移动（如直升机或船），发射/回收地点可取连续空间任意点。
  - **PMDRPG（折线链模式）**：母船只能沿给定的折线路径（Polygonal Chain）移动，如沿公路行驶的保障车。
  - **NMDRPG（网络模式）**：母船在普通道路网络（图）上行驶，发射和回收只能在网络节点处进行。
- **无人机航程限制**：每架无人机有续航时间上限 $N_D$，需在能量耗尽前返回母船充电。
- **完全/部分重叠变体**：多架无人机的飞行时间段可以完全不重叠（同步回收再出发）或部分重叠（一架未回收时另一架已发射）。

#### 算法核心步骤描述

1. **问题离散化（Digitization）**：将连续折线图（Polygonal Chain）离散为有限节点和有向边，以便构建整数规划。
2. **MISOCP模型（混合整数二阶锥规划）**：对连续母船移动模式（AMDRPG），利用二阶锥（SOCP）约束表达无人机从母船任意出发点的欧氏距离约束。对路网模式，采用标准MILP。
3. **有效不等式加强**：引入Big-M约束的上下界紧化、无人机飞行时间的割平面（Cutting Planes）等强化约束，减少LP松弛间隙。
4. **Matheuristic（数学启发式）**：将原问题分解为：（a）母船路由规划（确定停靠点序列），（b）无人机分配（将图分配给无人机），（c）时间协调（确保无人机在限时内完成并返回）。用迭代局部搜索在（a）（b）层面循环优化，用精确求解器处理（c）层的协调约束。
5. **实例测试**：在平面图（Planar Graphs）上测试不同形状的目标图，报告精确解与matheuristic解的比较。

---

### 文献 3：GRASP for Multi-Vehicle Prize Collecting Arc Routing for Connectivity（GRASP连通性优先弧路由）

**来源**: Computers and Operations Research, Vol.143, 2022, 105804  
**作者**: Luana Souza Almeida, Floris Goerlandt, Ronald Pelot, Kenneth Sörensen  
**DOI**: 10.1016/j.cor.2022.105804

#### 问题变体场景描述

本文研究**灾后道路修复/连通性恢复**场景下的弧路由问题（KPC-ARCP，K vehicle Prize Collecting Arc Routing for Connectivity Problem）：

- **灾害响应场景**：地震、洪灾等自然灾害导致道路网络中多条边被阻断，需要派遣多支修复队（Multiple Repair Crews）逐步清除障碍，以尽快恢复受影响区域的可达性（Accessibility）。
- **奖励收集型（Prize Collecting）**：修复队不必修复所有被阻断道路，而是通过选择高优先级道路修复来最大化"连通奖励"（Prize）——即通过打通某些关键边后重新接入关键设施（医院、避难所等）所获得的收益。
- **多车队/多仓库出发**：多支修复队从不同仓库出发，协同修复，最终目标是在有限时间预算内最大化连通区域的优先级总分。
- **与传统ARCP的区别**：传统应急弧路由（如NRCSRP）要求访问所有受损点；KPC-ARCP允许跳过部分边但须最大化连通网络分量的优先级之和。

#### 算法核心步骤描述

1. **问题建模**：在有向图 $G=(V,A)$ 上建立整数规划，目标为最大化修复后各连通分量的优先级总和，约束包括：每支修复队的时间预算、每条弧只能被修复一次、出发/到达约束。
2. **GRASP构造阶段（Greedy Randomized Construction）**：每次迭代随机构造一个可行解：
   - 维护受限候选列表（RCL），按照边修复后带来的边际连通增益（Marginal Connectivity Gain）排序。
   - 从RCL中随机选择下一条修复边，更新连通状态，直至时间预算耗尽。
3. **局部搜索阶段（Local Search）**：对构造解施加以下邻域操作：
   - **Insert**：将某条未修复的边插入某支队伍路线中。
   - **Remove**：从路线中去掉对连通增益最小的边。
   - **Swap**：在两支队伍之间交换分配的修复边段。
4. **精英解集与重启**：保留历史最优解集合（Elite Set），周期性地从精英解出发重新执行局部搜索，防止陷入局部最优。
5. **实验验证**：在合成及真实道路网络实例上测试，与先前数学启发式进行对比，验证GRASP可处理更大规模实例（最多400+节点，700+边）。

---

### 文献 4：Multiple-Drone Arc Routing and Mothership Coordination Problem（多无人机母船协同弧路由）

**来源**: Computers and Operations Research, Vol.159, 2023, 106322  
**作者**: Lavinia Amorosi, Justo Puerto, Carlos Valverde  
**DOI**: 10.1016/j.cor.2023.106322

#### 问题变体场景描述

本文是文献2（MDRPG）的扩展，从单无人机推广到**多架异构无人机**（Fleet of Drones），并深化了母船与无人机的协同模式：

- **多无人机舰队**：母船携带多架无人机，各无人机可被独立派遣到不同目标图（Target Graphs）执行巡检任务。每架无人机的航程上限为 $N_D$，一旦达到限制，必须返回母船充电后才能再次出发。
- **完全重叠（Complete Overlapping）**：一架无人机完成并回收后，另一架才可以发射，母船等待至所有已发射无人机回收后方可继续行进。
- **部分重叠（Partial Overlapping）**：允许母船在已回收某架无人机后立即发射下一架，而不必等待全部无人机回收，增加了时间并发性但引入了复杂的时序约束。
- **应用场景**：海岸线监控（UAV+船）、城市区域巡视、交通流量检测（需对多个路段进行视频覆盖）。
- **目标图访问方式**：（1）覆盖每条边指定比例的长度；（2）覆盖整个图总长度的指定比例。

#### 算法核心步骤描述

1. **决策变量设计**：引入二元变量表示"无人机 $d$ 在时间段 $p$ 访问目标图 $g$"，以及母船从发射点 $L$ 行进到回收点 $R$ 的连续距离变量。
2. **MISOCP精确建模**：
   - 对完全重叠变体（Complete Overlapping），利用线性化技术将时序约束转化为线性约束，建立MILP。
   - 对部分重叠变体（Partial Overlapping），需引入额外的时间阶段变量，建立更复杂的MILP，并以Big-M方式连接不同无人机的发射/回收时序。
3. **有效不等式（Valid Inequalities）**：
   - 无人机飞行时间上界的切割平面。
   - 对母船路程的三角不等式松弛。
   - 对无人机发射/回收顺序的先后序约束割。
4. **Matheuristic**：
   - **分解策略**：将问题分解为（a）母船路线段序列选择；（b）无人机-目标图分配；（c）时序可行性校验。
   - **迭代改进**：在（a）层用局部搜索调整母船停靠点顺序；在（b）层用匈牙利算法（或最小费用分配）重新分配无人机与目标图；（c）层用LP/MILP验证时序可行性并修复冲突。
5. **规模可扩展性**：精确模型适合小规模（≤10个目标图），matheuristic可处理中等规模（≤50个目标图）。

---

### 文献 5：Min-Max Multi-Trip Drone Location Arc Routing Problem（最小最大多行程无人机选址弧路由）

**来源**: Computers and Operations Research, Vol.174, 2025, 106894  
**作者**: Teresa Corberán, Isaac Plana, José María Sanchis  
**DOI**: 10.1016/j.cor.2024.106894

#### 问题变体场景描述

本文提出**MM-MT-dLARP**（Min-Max Multi-Trip Drone Location Arc Routing Problem），结合了位置选址（Location）、弧路由（Arc Routing）、多行程（Multi-Trip）和Min-Max目标：

- **联合选址与路由决策**：不仅决定无人机的巡检路线，还需同时确定无人机的**发射点（Launch Points）**位置（从候选集中选取有限个），每架无人机从被分配的发射点出发，完成多次飞行后返回。
- **多行程（Multi-Trip）**：每架无人机可从同一发射点出发，执行多次往返飞行（每次飞行距离不超过 $L$），每次飞行可覆盖若干条必服务线段（Required Lines）。
- **地面支撑车辆（Truck）协同**：每个发射点由一辆地面卡车负责运送无人机，卡车行驶路线由仓库出发，到达指定发射点后，无人机从该点执行多行程巡检。
- **Min-Max目标**：最小化**所有车辆（卡车行驶+无人机飞行）费用的最大值**，即平衡各卡车的工作负载（负载均衡）。
- **连续优化特性**：由于无人机可飞离路网直线飞至任意两点，必服务线段为折线链（Polygonal Chain），无人机的进出点不必局限于端点，形成连续优化问题。

#### 算法核心步骤描述

1. **离散化（Digitization）**：将每条必服务折线链离散为若干顶点和线段，并在所有顶点间构建完全非必要边图，将连续问题转化为离散的LC K-RPP（Length Constrained K-Rural Postman Problem）。
2. **MM-MT-LARP的整数规划模型**：引入二元变量 $x_{ij}^{dk}$ 表示"无人机 $d$ 在第 $k$ 次飞行中是否经过弧 $(i,j)$"，以及连续变量表示卡车行驶费用，建立含Min-Max目标的MILP。
3. **面描述（Polyhedral Study）**：
   - 证明多族有效不等式（Subtour Elimination、Connectivity Cuts、Capacity Cuts等）为关联多面体的面（Facets），这些割平面用于强化LP松弛。
4. **Branch-and-Cut（分支割）**：
   - 主循环：求解LP松弛 → 识别违反的有效不等式 → 添加割平面 → 分支。
   - 关键分离算法：连通性切割通过最小割（Min-Cut）识别，容量切割通过行舍入启发式识别。
5. **Matheuristic（数学启发式）**：
   - **聚类步骤**：将必服务线段按地理邻近性聚成 $D$ 个簇，确定各发射点位置。
   - **路线构造**：对每个簇，用路径扫描（Path-Scanning）构造初始无人机多行程飞行路线。
   - **改进步骤**：用Or-opt、2-opt*对路线进行局部搜索优化。
   - **选址重优化**：固定路线，用坐标下降法重新优化发射点位置（最小化欧氏距离和）。

---

### 文献 6：Solving the Length-Constrained K-Drones Rural Postman Problem（长度约束K无人机乡村邮递员）

**来源**: European Journal of Operational Research, Vol.292, 2021, pp.60–72  
**作者**: James F. Campbell, Ángel Corberán, Isaac Plana, José M. Sanchis, Paula Segura  
**DOI**: 10.1016/j.ejor.2020.10.024

#### 问题变体场景描述

本文研究**长度约束K无人机乡村邮递员问题**（LC K-DRPP），是首个系统研究多无人机弧路由的论文之一：

- **无人机飞离路网**：区别于传统车辆路由，无人机可在两点之间直线飞行，无需沿路网行驶，非必要"deadheading"段的费用是欧氏直线距离。
- **必服务折线（Required Lines）**：待巡检目标为一组折线链（如桥梁、管道、电力线），每条线有对应的服务费用（正比于长度）。K架无人机共同覆盖所有折线，每架的飞行总长度不超过 $L$（续航约束）。
- **最小化总费用**：目标为最小化所有无人机路线的**总服务费用**（而非平均或最大），因此需合理分配折线给各无人机，并优化进出点。
- **离散化后的LC K-RPP**：将每条折线链离散为若干分段（Segments），在顶点集上构造完全图（非必要边=欧氏直线距离），等价为离散弧路由问题。

#### 算法核心步骤描述

1. **图构造**：将连续LC K-DRPP离散化为LC K-RPP：每条折线链的顶点为节点，相邻顶点间的折线段为必要边，所有节点对之间添加非必要边（Euclidean距离）。
2. **整数规划模型**：提出包含二元变量（弧是否被某无人机经过）、流量守恒约束和长度约束 $\leq L$ 的IP，并加入以下有效不等式族：
   - **Subtour Elimination Constraints（SEC）**：防止产生不经仓库的子环。
   - **Connectivity Cuts**：确保每条必要边被至少一架无人机覆盖。
   - **Capacity Cuts（Blossom Inequalities）**：基于奇数集割的强化。
3. **Branch-and-Cut算法**：
   - LP松弛求解 → 识别违反的SEC/Connectivity Cuts（通过最小割算法）→ 添加切割 → 分支。
   - 采用强分支（Strong Branching）选择分支变量。
4. **Matheuristic**：
   - **初始解构造**：用改进的路径扫描（Path-Scanning）将折线段分配给K架无人机，确保每架总长度不超过 $L$。
   - **局部搜索**：用Or-opt和Lin-Kernighan式变换优化各无人机路线内部顺序。
   - **全局跨无人机交换**：在不同无人机之间交换折线段，进一步平衡负载并降低总费用。
5. **性能对比**：Branch-and-Cut可精确求解小规模（≤84条折线），Matheuristic在合理时间内求解中等规模，并与精确解对比分析间隙。

---

### 文献 7：Memetic Algorithm Based on Two_Arch2 for Multi-Depot Heterogeneous-Vehicle CARP（多目标多仓库异构车队CARP）

**来源**: Swarm and Evolutionary Computation, Vol.63, 2021, 100864  
**作者**: Bin Cao, Weizheng Zhang, Xuesong Wang, Jianwei Zhao, Yu Gu, Yan Zhang

#### 问题变体场景描述

本文研究**多目标、多仓库、异构车队容量约束弧路由问题**（MO-MDHV-CARP），应用于智能城市垃圾收集与道路维护场景：

- **多仓库（Multi-Depot）**：车队从多个不同仓库出发，每辆车必须返回其出发仓库（或任意一个仓库，取决于变体）。
- **异构车队（Heterogeneous Fleet）**：不同车辆有不同的容量（Capacity）和服务效率，车辆之间可在特定节点相互协作（协作服务同一弧段）。
- **双目标**：（1）最小化所有车辆的**总行程费用**（Total Travel Cost）；（2）最小化最大单辆车的行程时间（**Makespan**，即最长路线的时间）。两目标之间存在权衡（Pareto Front）。
- **协作任务（Collaborative Tasks）**：部分弧段由于体积或重量要求，需要两辆车共同服务，增加了协作约束的复杂性。

#### 算法核心步骤描述

1. **解编码（Solution Representation）**：将解编码为"路线-任务序列"格式，每辆车对应一个任务弧序列，多辆车的序列组成完整解。
2. **Two_Arch2多目标框架**：
   - 维护两个存档（Archives）：第一存档（Pareto Archive）保存当前已知的非支配解；第二存档（Diversity Archive）保存维持种群多样性的解。
   - 选择策略：从两个存档中以概率 $p$ 和 $1-p$ 分别选取父本。
3. **信息熵多样性度量**：用信息熵（Information Entropy）度量种群多样性，在熵值过低时触发"重启"机制（Restart），从精英解附近随机生成新个体加入种群。
4. **Memetic局部搜索（Local Search Operators）**：
   - **Route Improvement**：针对单条路线内部的任务交换（Task Swap）、插入（Insert）、逆序（Invert）操作。
   - **Cross-Route Improvement**：在不同路线/不同仓库的车辆之间移动任务弧，最大化Pareto改进。
5. **遗传操作**：
   - **SBX交叉（Simulated Binary Crossover）**：对路线进行部分映射交叉（PMX）或顺序交叉（OX），修复容量和任务覆盖约束。
   - **变异（Mutation）**：随机打乱一条路线内的任务顺序。
6. **约束修复**：若交叉/变异后产生容量违反，使用贪心重新分配（Greedy Reallocation）将超载任务移到其他车辆。

---

### 文献 8：GV-Drone Arc Routing for Urban Traffic Patrol（地面车辆-无人机协同城市巡逻弧路由）

**来源**: Swarm and Evolutionary Computation, Vol.77, 2023, 101246  
**作者**: Binjie Xu, Kexin Zhao, Qizhang Luo, Guohua Wu, Witold Pedrycz  
**DOI**: 10.1016/j.swevo.2023.101246

#### 问题变体场景描述

本文研究**地面车辆（GV）与多架无人机（Drones）协同的弧路由问题**（GVD-ARP），用于城市道路交通巡逻场景：

- **地面车辆作为无人机平台**：GV沿道路网络行驶，携带多架无人机；在路网节点处发射/回收无人机，GV同时充当无人机的充电站。
- **目标弧（Target Arcs）**：城市路网中有一组需要被巡逻的弧段（如高流量路段、事故多发路段），无人机负责对这些弧段进行监控，无方向限制（可顺行或逆行服务）。
- **无人机飞行时间约束**：每架无人机的单次飞行时长不超过 $P$（飞行时间上限），超出则须先返回GV充电。
- **GV与无人机均在路网上行驶**：不同于部分文献中无人机可飞离路网，本文中无人机也沿路网（或其捷径）行进，而非直线飞行——这简化了场景但更贴合某些电磁/视觉覆盖需求。
- **无人机可多次复用**：每架无人机可以被多次发射和回收。

#### 算法核心步骤描述

1. **问题形式化**：在有向图 $G=(V,A)$ 上，GV路线用关键节点序列 $R$ 表示，无人机的每次飞行由发射节点 $v_i$ 和回收节点 $v_j$（$i<j$）确定飞行段集合 $AL$。
2. **整数规划建模**：引入二元变量 $x_{im}$（GV第 $i$ 个节点是否为节点 $m$）、$\phi^T_{im}$（是否在此节点发射无人机）、$\phi^R_{im}$（是否在此节点回收无人机），建立以最小化总路程（GV行程+无人机飞行时间）为目标的IP。
3. **基于路由策略的遗传算法（Route-Policy-Based GA）**：
   - **编码**：染色体为GV关键节点序列 + 无人机发射/回收分配方案。
   - **交叉**：对GV路线部分进行顺序交叉（OX），对无人机分配部分进行单点交叉。
   - **变异**：随机交换GV路线中两个关键节点，或重新分配某次无人机飞行任务。
4. **无人机任务分配子问题**：给定GV路线，用贪心方法为目标弧分配最优无人机飞行段：优先选择使无人机飞行时间最短的（发射, 回收）点对，确保飞行时间 $\leq P$。
5. **可行性修复**：若某目标弧在当前分配下无法被覆盖（无合法发射/回收对），则在GV路线中插入额外停靠点以使该弧可达。
6. **实验验证**：在多个城市道路网络实例上测试，与单纯GV路由和单纯无人机路由基线对比，证明协同方案大幅降低总路程。

---

### 文献 9：Heuristic Algorithm for the Drone Rural Postman Problem（无人机乡村邮递员启发式）

**来源**: Journal of Industrial and Management Optimization, Vol.20, No.5, 2024, pp.1951–1966  
**作者**: Ailing Xie, Keigo Miyagawa, Wei Wu, Mutsunori Yagiura  
**DOI**: 10.3934/jimo.2023150

#### 问题变体场景描述

本文研究**无人机乡村邮递员问题**（DRPP, Drone Rural Postman Problem）：

- **无人机飞离路网**：与传统乡村邮递员问题（RPP，车辆需沿图中边行驶）不同，无人机可以在任意两点之间**直线飞行**（deadheading），不必沿图中的边行驶。
- **必服务边可被"切割"服务**：无人机可以从某条必服务边的**中间点**开始服务，也可以在中间暂停并在第二次飞行时继续服务剩余部分（Split Service），这是DRPP区别于传统RPP的关键特性——最优解可能比不允许切割更低。
- **单无人机、无容量/续航约束**：本文研究最基础的单无人机版本，不考虑能量约束（对应无限续航），重点分析连续优化的结构性质。
- **连续优化空间**：由于无人机可在折线上任意点进出，形成连续优化问题，理论分析上远比离散RPP复杂。

#### 算法核心步骤描述

1. **理论分析（Assumptions 3-5）**：证明对任意必服务边的切割点序列，旅行成本满足三角不等式（Assumption 5），服务成本满足对称性和累加性（Assumptions 3, 4），为启发式提供理论保证。
2. **图约减（Graph Reduction）**：
   - 识别并消除"冗余节点"（不影响最优解结构的中间折线顶点），减少离散化图的规模。
   - 识别一定覆盖条件下必须被访问的"强制节点"。
3. **两阶段启发式（Two-Phase Heuristic）**：
   - **第一阶段（图约减）**：对折线链上的折点进行剪枝，去除不改变最优解的冗余点，生成简化图。
   - **第二阶段（求解简化RPP）**：在约减后的图上构造RPP（传统车辆乡村邮递员），用标准RPP求解器（如Christofides启发式或精确算法）求解，得到无人机路线。
4. **近似比证明**：证明所提两阶段启发式的最坏情况近似比为 **2**（即结果不超过最优解的两倍），这是该问题首个有理论保证的近似算法。
5. **与竞品对比**：与Campbell等（文献19）提出的方法对比，证明两阶段启发式在解质量和计算时间上均具优势。

---

### 文献 10：Efficient Learning-based Solver for CARP（基于深度学习的CARP求解器）

**来源**: arXiv:2403.07028v1, 2024  
**作者**: Runze Guo, Feng Xue, Anlong Ming, Nicu Sebe  
（Beijing University of Posts and Telecommunications & University of Trento）

#### 问题变体场景描述

本文提出针对**标准容量约束弧路由问题（CARP）**的**深度学习（神经网络）求解器**：

- **标准CARP场景**：无向图中有一组必服务边（Required Edges），每条必服务边有需求量（Demand）和服务费用（Service Cost），仓库（Depot）为所有路线的起终点，每辆车容量为 $Q$，目标最小化总路程费用。
- **无向边处理**：无向边在决策时被分解为两条有向弧（两个方向），求解器直接对弧进行决策，避免了先前方法中需要额外判断方向的两阶段处理。
- **学习型求解器对比元启发式**：传统元启发式（MAENS、ILMA等）求解质量高但速度慢；神经网络求解器速度快但质量差。本文目标是设计与元启发式质量相当、但速度更快的学习型方法。

#### 算法核心步骤描述

1. **图预处理（MDS映射）**：用多维缩放（Multi-Dimensional Scaling, MDS）将输入图 $G$ 投影到 $d$ 维欧氏空间，为每条弧提取坐标特征（起始节点坐标 $mds_{start(i)}$，终止节点坐标 $mds_{end(i)}$），从而捕捉方向信息。
2. **方向感知注意力模型（Direction-aware Attention Model, DaAM）**：
   - 将弧的方向信息（由MDS坐标隐式编码）直接嵌入注意力计算，无需分离的方向判断步骤。
   - **编码器**：多层 Transformer Encoder，将每条弧的特征向量（是否为仓库弧、费用、需求、MDS坐标、最近已选弧信息）编码为高维嵌入。
   - **解码器（上下文注意力）**：基于当前路线末尾弧和剩余容量的"上下文向量"，通过注意力机制在所有候选弧上计算概率分布，选择下一条服务弧。
3. **Two-Phase Decision Making（两阶段决策）**：
   - **第一阶段（一次性转换）**：将无向图转为有向完全图 $G_0$，计算所有弧的初始嵌入（仅执行一次）。
   - **第二阶段（序列决策）**：逐步从 $G_0$ 中选择服务弧，更新当前路线状态，直至所有必服务弧被覆盖。
4. **训练策略**：采用强化学习（REINFORCE算法）训练，奖励函数为负总路程费用，通过基线（Baseline）估计方差降低。
5. **推理与集成**：推理时采用贪心或束搜索（Beam Search），并可将DaAM生成的解作为元启发式（如局部搜索）的初始解，实现与元启发式的互补集成。

---

### 文献 11：Novel Dual-Stage Algorithm for CARP with Time-Dependent Service Costs（时变服务费用CARP双阶段算法）

**来源**: arXiv:2406.15416v1, 2024  
**作者**: Qingya Li, Shengcai Liu, Juan Zou, Ke Tang  
（Southern University of Science and Technology; Xiangtan University）

#### 问题变体场景描述

本文研究**带时变服务费用的容量约束弧路由问题**（CARPTDSC, CARP with Time-Dependent Service Costs），以冬季撒盐除雪作业为主要应用场景：

- **时变服务费用（Time-Dependent Service Costs）**：同一条必服务弧，在不同时段执行服务的效果（和费用）不同。例如，深夜撒盐效果最好（费用最低），而交通高峰时段撒盐效果差（费用高）。因此，不仅要规划车辆路线，还需优化**车辆出发时间（Departure Time）**，以在时间窗内选择低服务费用时段执行服务。
- **双决策问题**：（1）为每辆车规划哪些弧段按何顺序服务（路线规划）；（2）为每辆车确定出发时间 $T_k$（出发时间优化），两者耦合。
- **约束**：每辆车容量 $Q$，所有路线均从仓库出发并返回，每条必服务弧恰好被服务一次，服务时间 $T(re^k_i)$ 不超过时间窗上限 $T$。

#### 算法核心步骤描述

1. **问题分解（Two-Stage Framework, MAENS-GN）**：将CARPTDSC分解为两个相互独立但联合优化的子问题：
   - **Stage 1（路线规划阶段）**：固定出发时间，采用进化算法（MAENS）优化路线结构。
   - **Stage 2（出发时间优化阶段）**：固定路线，用**梯度下降（Gradient Descent, GN）**对出发时间 $\{T_k\}$ 连续优化，最小化在当前路线结构下的总时变服务费用。
2. **MAENS路线优化**：
   - 继承经典MAENS（Memetic Algorithm with Extended Neighborhood Search）框架。
   - 邻域搜索：包括 Or-opt（单弧移动）、CROSS（两弧互换）、2-opt*（跨路线段交换）等操作。
   - 个体初始化：使用贪心最近邻构造（Greedy Nearest Neighbor Construction）为每辆车依次选择最近未服务弧。
3. **梯度下降出发时间优化**：
   - 目标函数关于 $T_k$ 可微（时变服务费用为连续函数）。
   - 计算 $\partial \text{TotalCost} / \partial T_k$，对各车出发时间执行梯度下降步。
   - 约束 $T_k \in [0, T_{\max}]$，用投影梯度法保证可行性。
4. **两阶段交替迭代**：路线优化与出发时间优化交替进行，直至收敛，兼顾解结构质量与时间调度效率。
5. **与现有方法对比**：与纯启发式（无时变）和小规模精确算法（CPLEX）对比，MAENS-GN在中大规模实例上取得最优解质量，且时间效率远优于精确方法。

---

### 文献 12：Novel Generalized Metaheuristic Framework for Dynamic CARP（动态CARP广义元启发式框架）

**来源**: GECCO'23 Companion, 2023  
**作者**: Hao Tong, Stefan Menzel, Bernhard Sendhoff, Leandro L. Minku, Xin Yao  
**DOI**: 10.1145/3583133.3595829

#### 问题变体场景描述

本文研究**动态容量约束弧路由问题**（DCARP, Dynamic CARP），针对现实中突发事件导致服务计划失效的场景：

- **动态变化事件（Dynamic Events）**：在车辆正在执行服务任务时，突发事件（如新增任务弧、车辆故障、道路封闭）打破当前服务计划，需要即时重新规划。
- **外部车辆（Outside Vehicles）**：与传统DCARP不同，本文考虑部分车辆已完成其当前路线段并停在某位置（称为"outside vehicle"），这些车辆仍有剩余容量，可以被重新分配以承接未完成任务。
- **虚拟任务策略（Virtual Task Strategy）**：为解决动态重规划时外部车辆的初始位置带来的非标准起点问题，将每辆外部车辆的当前位置定义为虚拟任务的"服务终点"，从而将DCARP统一转化为标准（静态）CARP格式，可直接套用任意静态CARP求解器。
- **广义框架（Generalized Framework）**：提出的框架不依赖某一特定元启发式，可集成任意静态CARP元启发式算法（如MAENS、ILMA、RTS等）作为底层求解器。

#### 算法核心步骤描述

1. **虚拟任务策略（Virtual Task Strategy）**：
   - 为每辆外部车辆创建一个"虚拟任务弧"，该弧的起点和终点均为外部车辆当前停靠位置，需求量为0，服务费用为0。
   - 将所有虚拟任务加入CARP实例的任务集合，并指定各虚拟任务必须由对应车辆服务（约束绑定），将DCARP转化为带有额外约束的CARP。
2. **静态CARP求解（集成任意元启发式）**：
   - 使用广义框架调用底层静态CARP元启发式（MAENS/ILMA/RTS），在虚拟任务转化后的实例上优化。
   - 比较"返回先行策略"（Return-First，先让外部车辆返回仓库再出发）与虚拟任务策略，证明后者更高效。
3. **初始化策略**：
   - **重启策略（Restart Strategy）**：在新动态事件发生后，完全随机初始化种群重新搜索。
   - **序列传输策略（Sequence Transfer Strategy）**：将旧解（事件发生前的部分路线）作为新实例的初始解，通过修复算法（删除已完成任务，保留未完成任务）快速生成可行初始解，利用旧解的信息加速收敛。
4. **实验验证**：在120个DCARP测试实例上测试，各种底层元启发式在广义框架下的性能均显著优于直接在DCARP上运行（无虚拟任务转化）的版本。

---

### 文献 13：Genetic Programming With Niching for Uncertain CARP（带小生境GP的不确定CARP）

**来源**: IEEE Transactions on Evolutionary Computation, Vol.26, No.1, 2022, pp.73–87  
**作者**: Shaolin Wang, Yi Mei, Mengjie Zhang, Xin Yao

#### 问题变体场景描述

本文研究**不确定容量约束弧路由问题**（UCARP, Uncertain CARP），其中任务需求和deadheading费用均为**随机变量**：

- **UCARP基本设置**：无向图 $G(V,E)$，每条任务边 $t \in T$ 有随机需求 $\bar{d}(t)$（实际值在服务该边时才揭示）和随机deadheading费用 $\bar{\varsigma}(e)$，目标最小化期望总费用 $E[C(S^\xi)]$。
- **四种不确定性来源**：（1）任务需求随机；（2）deadheading费用随机；（3）服务费用随机；（4）任务是否出现随机（即某些任务可能在实际场景中消失）。本文是首个同时考虑所有四种不确定性的工作。
- **路由策略（Routing Policy）而非固定路线**：由于实际情况在执行时才揭露，解不是预定路线，而是一个**决策策略**（Routing Policy） $h(\cdot)$，根据当前实际状态动态决定下一步行动。
- **GP超启发式（GP Hyper-heuristic）**：用遗传规划（GP）进化路由策略（以特征向量为输入的决策函数），而非直接进化路线。

#### 算法核心步骤描述

1. **路由策略表示**：GP将策略表示为一棵表达式树，输入为当前状态特征（剩余容量、当前位置、未服务任务集合的统计特征），输出为下一步应服务的任务评分，选分最高任务执行。
2. **小生境（Niching）机制**：
   - 使用基于行为多样性（Behavioral Diversity）的小生境：定义两个策略的"相似度"为在同一组样本上产生的解的相似程度。
   - 维护多个小生境（Niches），每个小生境维护一组相似策略，通过小生境竞争（Niche Competition）选择在小生境内适应度最高的个体，防止种群在极少数优势策略上收敛。
3. **GP进化流程**：
   - **初始化**：随机生成若干表达式树（策略），在一批样本（Samples）上评估期望总费用。
   - **选择（Tournament + Niche）**：结合锦标赛选择（Tournament Selection）和小生境惩罚（Niche Penalty），确保选出多样且优质的父本。
   - **交叉（Subtree Crossover）**：随机选择两棵树的子树互换，产生子代策略。
   - **变异（Subtree Mutation）**：随机替换树中某子树为新的随机子树。
4. **样本评估**：用蒙特卡罗采样（Monte Carlo Sampling）生成 $|\Xi|$ 个样本场景（不同的需求/费用实现），在每个样本上模拟路由策略的执行，计算平均总费用作为适应度。
5. **简化路由策略（Simplification）**：通过小生境机制和语义相似性剪枝，自动倾向于进化出更小、更可解释的策略树，提高策略实用性。

---

### 文献 14：Multidepot Drone General Routing Problem with Duration and Capacity Constraints（多仓库无人机一般路由）

**来源**: International Transactions in Operational Research, Vol.32, 2025, pp.3756–3779  
**作者**: Teresa Corberán, Isaac Plana, José M. Sanchis, Paula Segura  
**DOI**: 10.1111/itor.13457

#### 问题变体场景描述

本文研究**多仓库无人机一般路由问题（MDdGRP）**，是经典一般路由问题（GRP）在多仓库和无人机特性下的扩展：

- **一般路由问题（GRP）**：既需服务一组必服务弧（Arc Routing），又需访问一组必访问点（Node Routing），是CARP与TSP的泛化。
- **多仓库（Multiple Depots）**：无人机舰队分布在多个仓库，每架无人机从自己的仓库出发，完成任务后返回**任意**仓库（或特定仓库，取决于变体）。
- **续航与载荷约束**：每架无人机有最大飞行时间上限（Duration Constraint）和最大载荷（Capacity Constraint，用于送货任务），两者均不可超越。
- **无人机飞离路网**：无人机可在任意两点间直线飞行，非必要段的deadheading费用为欧氏直线距离，服务折线链（Line）时需沿线段飞行。
- **联合弧+点服务**：既要覆盖一组必服务折线段（类似RPP），又要访问若干必访问配送点（送货）。

#### 算法核心步骤描述

1. **离散化**：将连续折线链离散为顶点-线段结构，每条线段（弧）对应必服务任务，配送点为必访问节点。
2. **MDdGRP整数规划模型**：引入二元变量（无人机 $k$ 从仓库 $d$ 出发，经过弧/节点序列），目标最小化总费用，约束包括：多仓库出发/返回、每架无人机的续航约束（飞行时间 $\leq L$）、载荷约束（$\sum demand \leq Q$）、每段折线被至少一架无人机完整覆盖、每个配送点被恰好一架无人机访问。
3. **Branch-and-Cut精确算法**：
   - LP松弛 → 添加子环消除约束（Subtour Elimination）、连通性割（Connectivity Cuts）→ 分支。
   - 子环和连通性割通过最大流/最小割算法（Ford-Fulkerson）检测。
4. **Matheuristic算法1（Sequential Addition, SA）**：
   - 从空路线开始，每次迭代选择"代价增量最小"的未覆盖折线段或配送点，将其插入某条无人机路线中，直至所有任务被覆盖。
   - 约束修复：若插入后违反续航/载荷约束，则开辟新路线。
5. **Matheuristic算法2（Cluster-First Route-Second, CFRS）**：
   - **聚类阶段（Cluster-First）**：基于地理邻近性（Euclidean距离）将折线段和配送点聚成 $K$ 个簇，每簇分配给一组无人机。
   - **路线阶段（Route-Second）**：对每个簇，用近似TSP/RPP求解器规划无人机路线，满足续航和载荷约束。
6. **实验**：在新生成的MDdGRP基准实例集上测试，Branch-and-Cut可精确求解小规模，两个Matheuristic在大规模实例上快速给出高质量解，CFRS通常优于SA。

---

### 文献 15：Knowledge Transfer Genetic Programming with Auxiliary Population for UCARP（知识迁移GP辅助种群UCARP）

**来源**: IEEE Transactions on Evolutionary Computation, Vol.27, No.2, 2023, pp.311–325  
**作者**: Mazhar Ansari Ardeh, Yi Mei, Mengjie Zhang, Xin Yao

#### 问题变体场景描述

与文献13（GP-Niching UCARP）研究相同的UCARP框架，本文的创新在于引入**知识迁移（Knowledge Transfer）**机制：

- **跨问题知识迁移**：在解决一组相关UCARP实例时（例如同一道路网络在不同随机种子下的多个实例，或不同参数设置下的实例），利用**已求解实例**中学到的路由策略知识，加速求解**新实例**。
- **辅助种群（Auxiliary Population）**：来自已求解实例的GP策略树构成"辅助种群"，在进化新实例时，将辅助种群中的优质策略选择性地引入当前种群，提供有益多样性和良好初始点。
- **避免负迁移（Negative Transfer）**：若辅助种群策略与新实例不相关，强制引入反而有害（负迁移）。本文提出选择性迁移机制，仅引入与当前问题语义相似的辅助策略。

#### 算法核心步骤描述

1. **UCARP路由策略表示（与文献13相同）**：GP进化决策函数，以状态特征为输入，输出下一步服务任务的评分。
2. **辅助种群构建**：从已求解的 $m$ 个UCARP相关实例中，各保留 $K$ 个精英策略树，合并为辅助种群 $AP$。
3. **跨任务迁移相似性度量**：
   - **语义相似性（Semantic Similarity）**：在一批共同样本上评估辅助策略和当前种群个体产生的解的相似程度，以路由结果距离（Route Similarity）衡量。
   - **性能相似性（Performance Similarity）**：辅助策略在当前实例上的适应度与在其原始实例上的适应度之比。
4. **选择性引入（Selective Transfer）**：
   - 每次迭代，按相似性分数对辅助种群排序，仅选取相似性最高的 $k$ 个辅助策略加入当前种群（替换当前种群中最差的 $k$ 个个体）。
   - 相似性低于阈值 $\theta$ 的辅助策略被拒绝，避免负迁移。
5. **交叉与变异（同标准GP）**：子树交叉 + 子树变异，产生新策略树。
6. **实验**：在多组相关UCARP实例系列上测试，证明知识迁移GP（KT-GP）相比无迁移GP（Standard GP），收敛速度更快，最终解质量更高，且在负迁移风险较高的实例上也未见显著退化。

---

### 文献 16：Multi-Purpose K-Drones General Routing Problem（多用途K无人机一般路由）

**来源**: Networks, Vol.82, 2023  
**作者**: James Campbell, Ángel Corberán, Isaac Plana, José M. Sanchis, Paula Segura  
**DOI**: 10.1002/net.22176

#### 问题变体场景描述

本文提出**多用途K无人机一般路由问题**（MP K-DGRP），开创性地将**弧路由**（线性特征巡检）与**点路由**（配送任务）合并到同一无人机任务中：

- **多用途无人机（Multi-Purpose Drones）**：每架无人机在同一次飞行中既执行**感知（Sensing）**任务（沿线段飞行以提供覆盖），又执行**配送（Delivery）**任务（访问离散配送点）。
- **感知覆盖任务（Arc Component）**：待感知区域可以是二维面（转化为一组平行线段覆盖）或线状网络（如输电线、灌溉渠）。无人机沿线飞行以提供传感器覆盖（摄像头、热像仪等），覆盖宽度由传感器和飞行高度决定。
- **配送任务（Point Component）**：同时需要向若干地面目标点投递货物，目标点位置已知，每次配送消耗无人机载荷。
- **K架无人机**：无人机舰队共 $K$ 架，从同一仓库出发，需联合完成所有线段覆盖和所有配送任务，每架无人机有续航时间上限 $T$ 和载荷上限 $Q$。
- **应用场景**：洪灾区域搜救（覆盖洪区同时投递救援物资）、电力线巡检（沿线检测同时向维修点送工具）、农业喷洒（覆盖田地同时向局部补水站补给）。

#### 算法核心步骤描述

1. **问题建模（K-GRP格式）**：将MP K-DGRP建模为一般路由问题：节点集 = 仓库 + 所有折线段端点 + 所有配送点；必服务弧集 = 折线段（覆盖任务）；必访问节点集 = 配送点。
2. **整数规划（IP）模型**：
   - 二元变量 $x_e^k$（无人机 $k$ 是否经过线段/弧 $e$）和 $y_v^k$（无人机 $k$ 是否访问节点 $v$）。
   - 目标：最小化所有无人机路线的总飞行时间（或总费用）。
   - 约束：每条折线段被至少一架无人机覆盖；每个配送点被恰好一架无人机访问；每架无人机续航时间 $\leq T$，累计载荷 $\leq Q$；路线连通性（每架无人机的路线形成连通闭合回路）。
3. **Branch-and-Cut精确算法**：
   - LP松弛 → 添加SEC和Connectivity Cuts（通过最小割识别）→ 分支。
   - 用强分支策略（Strong Branching）提升分支质量。
4. **Matheuristic（MP K-DGRP的近似算法）**：
   - **初始解**：用路径扫描（Path-Scanning）为每架无人机分别构造覆盖折线段和配送点的路线草案。
   - **改进1（弧-点联合优化）**：用Or-opt在路线内部交换折线段和配送点的服务顺序，减少不必要的绕行。
   - **改进2（跨无人机重分配）**：在不同无人机间交换部分折线段或配送点，降低总时间，同时保证所有无人机的续航和载荷不超限。
5. **可行性保证**：对续航约束违反，将路线分段，开辟新无人机路线；对载荷违反，将配送任务转移至其他无人机。

---

### 文献 17：Drone Arc Routing Problems and Metaheuristic Solution Approach（无人机弧路由与元启发式求解）

**来源**: Drones, Vol.8, No.8, 2024, Article 373  
**作者**: Islam Altin, Aydin Sipahioglu  
（Eskisehir Osmangazi University, Turkey）

#### 问题变体场景描述

本文提出**带deadheading需求的无人机弧路由问题**（DARP-DD，Drone Arc Routing Problem with Deadheading Demand），是对经典DARP的重要扩展：

- **经典DARP（Drone ARP）**：无人机可在两点间直线飞行（不受路网约束），必须覆盖一组必服务弧段（Required Edges），目标最小化总路线费用。
- **Deadheading Demand（非服务飞行的能量消耗）**：与传统CARP不同，无人机在非服务飞行（Deadheading）时同样消耗电池能量，不仅服务飞行消耗电量。这使得能量约束比传统容量约束更为复杂：无人机即使不执行服务任务，在空载飞行期间也在耗电。
- **能量容量约束（Energy-Based Capacity）**：无人机的"容量"不是重量/体积，而是**电池电量**（Battery Capacity），服务飞行与非服务飞行均消耗电量，因此路线总电量消耗（服务+deadheading）不能超过电池上限。
- **多无人机版本**：在基础DARP基础上扩展至多架无人机协同覆盖，相当于带能量约束的CARP推广。
- **连续优化特性**：无人机飞行不局限于路网边，可在图外的欧氏空间直线飞行，引入连续位置决策。

#### 算法核心步骤描述

1. **DARP-DD问题形式化**：在带必服务线段的无向图上，定义电池容量 $Q_E$，每次服务弧 $e$ 消耗能量 $e_{service}(e)$，每次在两点间deadheading消耗能量 $e_{dh}(u,v) = \text{Euclidean}(u,v)$（与飞行距离成正比）。
2. **元启发式框架（Metaheuristic）**：
   - **初始解构造**：用贪心路径扫描（Path-Scanning）构造初始可行解，确保每架无人机电量不超限。
   - **邻域搜索（Neighbor Search Operators）**：
     - **Intra-Route Move**：在单架无人机路线内交换两个服务弧的服务顺序。
     - **Inter-Route Move**：在两架无人机之间转移一个服务弧，同时更新电量消耗验证可行性。
     - **Reverse Operator（新算子）**：对连续一段弧序列执行反向操作（改变服务方向），利用无人机弧路由的方向灵活性减少deadheading消耗。
     - **Merge/Split Operator（新算子）**：将两条相邻短路线合并为一条（若电量允许），或将超长路线拆分为两条，以优化电量使用效率。
3. **禁忌搜索框架（Tabu Search）**：将上述邻域操作嵌入禁忌搜索框架，维护禁忌列表（Tabu List）防止近期操作被立即逆转，设定禁忌期限（Tabu Tenure）。
4. **能量可行性修复**：每次邻域移动后，检查所有路线的总电量消耗，若违反约束则用贪心修复策略（将超量任务迁移至有余量的无人机）恢复可行性。
5. **实验**：在DARP和DARP-DD实例集上测试，证明新邻域算子（Reverse、Merge/Split）对求解质量有显著贡献；与已有DARP元启发式方法（Campbell等）对比，性能更优。

---

### 文献 18：Artificial Bee Colony Algorithm for Static and Dynamic CARP（蜜蜂群体算法求解静/动态CARP）

**来源**: Mathematics, Vol.10, No.13, 2022, Article 2205  
**作者**: Zsuzsanna Nagy, Ágnes Werner-Stark, Tibor Dulai  
（University of Pannonia, Hungary）

#### 问题变体场景描述

本文研究**静态CARP**和**动态CARP（DCARP）**，提出基于人工蜂群（Artificial Bee Colony, ABC）算法的统一求解框架：

- **标准静态CARP**：有向图上，车辆需覆盖所有必服务边，每辆车容量 $Q$，目标最小化所有路线的总费用（含服务+deadheading），所有信息已知且固定。
- **动态CARP（DCARP）**：在车辆执行任务过程中，运行时发生以下动态变化：（1）新的必服务边突然出现（New Tasks）；（2）已分配的任务被取消（Task Cancellation）；（3）道路状况变化导致费用更新（Cost Update）。系统需实时重新规划剩余任务。
- **统一框架**：静态模式下ABC直接优化完整解；动态模式下当事件发生时，提取当前车辆状态（已完成任务、当前位置、剩余容量），重新初始化ABC对剩余任务重规划，保持实时响应性。

#### 算法核心步骤描述

1. **解表示（Solution Representation）**：
   - 一个解表示为任务序列（Route Plans）的集合：$S = \{r_1, r_2, ..., r_{|S|}\}$，每条路线 $r_k = \langle t_0, t_{k,1}, ..., t_{k,l_k}, t_0 \rangle$（以仓库出发和返回）。
   - 相邻任务之间的deadheading路径由 Dijkstra 算法提前计算的最短路矩阵（MDC）填充。
2. **ABC算法三类蜂种**：
   - **Employed Bee（工蜂）**：维护一个当前解（Food Source），对其执行局部搜索改进，记录改进历史（Trial Counter）。
   - **Onlooker Bee（观察蜂）**：按照各工蜂解的适应度概率（Fitness-Proportional Selection）选择工蜂解跟随，施加跨路线优化操作。
   - **Scout Bee（侦察蜂）**：当某工蜂解经过 $limit$ 次迭代未改进时，放弃该解并随机生成新解（全局探索）。
3. **局部搜索操作**：
   - **2-opt**：在同一路线内交换两个非相邻任务节点之间的路段。
   - **Or-opt**：将1、2或3个连续任务从路线中提取出来，插入同一路线或另一路线中最优位置。
   - **Cross Exchange（跨路线）**：在两条路线间互换一段子序列，同时验证容量约束。
4. **动态响应机制**：
   - 事件发生时：（1）记录每辆车当前状态（位置、已完成任务、剩余容量）；（2）构建新的CARP实例（仅含剩余任务）；（3）将每辆车当前位置作为新实例的虚拟仓库起点；（4）重新运行ABC算法对新实例求解。
5. **实验**：在标准CARP基准（egl、gdb、val系列）和自构DCARP动态实例上测试，与MAENS、ILMA等主流算法对比，ABC在小到中等规模实例上取得竞争力结果。

---

### 文献 19：Polyhedral Analysis and New Algorithm for Length-Constrained K-Drones RPP（多边形分析与新算法）

**来源**: Computational Optimization and Applications, Vol.83, 2022, pp.67–109  
**作者**: James Campbell, Ángel Corberán, Isaac Plana, José M. Sanchis, Paula Segura  
**DOI**: 10.1007/s10589-022-00383-x

#### 问题变体场景描述

本文是文献6（LC K-DRPP初始研究）的深度扩展，专注于**多面体分析（Polyhedral Analysis）**与**更强的精确算法**：

- **LC K-DRPP问题同文献6**：K架无人机协同覆盖一组折线链，每架飞行长度 $\leq L$，目标最小化总服务费用，无人机可在两点间直线飞行（欧氏deadheading）。
- **离散化后的LC K-RPP**：将连续问题离散化为在图 $G=(V, E_R \cup E_{NR})$ 上的弧路由问题，$E_R$ 为必服务线段，$E_{NR}$ 为完全图（欧氏距离非必要边）。
- **本文核心贡献**：相比文献6，本文进行更深入的**多面体研究**，找到并证明更多更紧的有效不等式族，从而设计更强的Branch-and-Cut，大幅提升精确求解能力（能处理更大规模实例）。
- **并行优化LC K-RPP和LC K-DRPP**：Branch-and-Cut用于精确求解离散的LC K-RPP，然后用全局算法（Global Algorithm）将离散解转化为连续LC K-DRPP的解，优化折线上进出点位置。

#### 算法核心步骤描述

1. **LP松弛分析**：证明LP松弛的多面体具有特定的结构（高度，维度），为有效不等式的面证明奠定基础。
2. **新有效不等式族**：
   - **Generalized SEC（推广子环消除）**：比文献6中使用的SEC更紧，考虑K条路线的组合子环结构。
   - **Odd-k Inequalities（奇k不等式）**：基于K-RPP的奇切割结构，提供更紧的容量割。
   - **Configuration Inequalities（配置不等式）**：针对LC K-RPP中长度约束与路线结构的交互作用设计，是本文最重要的新贡献之一。
3. **高效分离算法（Separation Algorithms）**：
   - SEC类：用最大流（Max-Flow）/最小割（Min-Cut）在多项式时间内精确分离。
   - Odd-k类：用启发式方法近似分离（精确分离是NP难的）。
   - Configuration类：设计专用启发式分离过程。
4. **增强型Branch-and-Cut**：
   - 在根节点施加多轮切割（Root-Node Cutting Plane Rounds），再开始分支。
   - 节点处施加轻量分离（仅检查最可能违反的不等式）。
   - 对整数解验证LC约束，对违反者施加切割。
5. **全局算法（Global Algorithm for LC K-DRPP）**：
   - 给定LC K-RPP的离散解（折线进出点固定在顶点），在每条折线的连续区间内优化进出点位置（通过一维搜索），进一步降低总费用（利用无人机可在折线任意点进出的自由度）。
   - 与文献6中的Matheuristic相比，本文精确算法可求解更大规模实例（最多20条折线，每条30个中间点）。

---

### 文献 20：Coordinated Vehicle-Drone Arc Routing via Improved Adaptive Large Neighborhood Search（车辆-无人机协同弧路由IALNS）

**来源**: Sensors, Vol.22, No.10, 2022, Article 3702  
**作者**: Guohua Wu, Kexin Zhao, Jiaqi Cheng, Manhao Ma  
**DOI**: 10.3390/s22103702

#### 问题变体场景描述

本文研究**一辆地面车辆与多架无人机协同的弧路由问题**（VD-ARP，Vehicle-Drone Arc Routing Problem），用于城市交通巡逻场景：

- **车辆-无人机协同模式**：一辆地面车辆从仓库出发，携带多架无人机；车辆沿道路网络行驶，在路网节点处发射/回收无人机；无人机负责巡逻特定目标弧段（Target Edges）。
- **目标弧段必须由无人机访问**：某些目标边（如高架路段、快速路）**只能**由无人机覆盖（地面车辆无法访问），车辆负责运送无人机到达合适发射位置。
- **无人机电池更换（不是充电）**：无人机完成任务后返回车辆，由车辆**立即更换电池**（Battery Swap，而非充电等待），使得无人机可以被多次使用，减少等待时间。
- **车辆等待或继续行驶**：车辆在发射无人机后，可以（1）原地等待无人机返回，或（2）继续行驶到下一节点，再回收无人机或发射另一架无人机。
- **多架无人机并发飞行**：多架无人机可以同时在空中执行不同目标弧的巡逻任务，最大化并行效率。

#### 算法核心步骤描述

1. **问题建模（VD-ARP）**：在有向路网 $G=(V,A)$ 上，车辆路线为节点序列（选择经过的关键路口），每个节点可以是发射点、回收点、或两者兼具。无人机路线为从发射节点到若干目标弧段再到回收节点的子路线。
2. **改进自适应大邻域搜索（IALNS, Improved Adaptive Large Neighborhood Search）**：
   - **基础框架（ALNS）**：维护一组销毁（Destroy）和修复（Repair）算子，通过自适应权重（Adaptive Weights）动态选择表现好的算子。
   - **改进1（新销毁算子）**：
     - **目标弧重分配销毁（Task-Reallocation Destroy）**：随机选择若干目标弧从当前无人机路线中移除，留出空位供修复阶段重新分配。
     - **相邻弧段批量销毁（Cluster Destroy）**：移除地理位置相邻的一批目标弧（基于空间聚类），鼓励对相邻区域路线整体重优化。
   - **改进2（新修复算子）**：
     - **贪心最近邻插入（Greedy Nearest-Neighbor Insert）**：将待分配目标弧插入当前最近无人机的路线末尾，同时验证电量约束。
     - **最优位置插入（Best-Position Insert）**：枚举所有可行插入位置，选择使总飞行时间增量最小的位置插入。
3. **车辆路线与无人机路线联合优化**：
   - **车辆路线调整**：在IALNS迭代中，通过调整车辆停靠节点序列（插入/删除中间停靠点），为无人机创造更优的发射/回收机会。
   - **同步约束检查**：对每次销毁-修复操作后，验证车辆与无人机的时序同步性（确保无人机到达回收点时车辆已在场或即将到达）。
4. **初始解构造**：
   - 先用贪心路径扫描（Path-Scanning）为车辆规划一条经过所有发射/回收候选节点的基础路线。
   - 再用最近邻启发式将各目标弧分配给最近的无人机路线。
5. **算子权重自适应更新**：每隔固定迭代轮数，根据各算子历史改进率（improvement rate）更新轮盘赌选择权重，使表现好的算子被更频繁选用。
6. **实验**：在多个城市道路网络基准实例（不同规模、不同无人机数量）上测试，与单纯车辆路由（无无人机）和单纯无人机路由基线对比，以及与其他ALNS变体（原始ALNS、无自适应版本）对比，证明IALNS中联合优化和新算子的有效性。

---

## 横向研究趋势分析

### 1. 问题变体演化路径

#### 1.1 CARP→Drone ARP：飞离路网带来的连续优化新挑战
传统CARP（容量约束弧路由）要求车辆严格沿路网行驶，弧路由的核心特征是**服务弧（必服务边）**的存在，使其区别于TSP/VRP。无人机的引入打破了"沿路网行驶"的约束：

| 特征 | 传统CARP（车辆） | Drone ARP（无人机） |
|------|----------------|-------------------|
| 行驶约束 | 必须沿图中边 | 可直线飞行（欧氏距离） |
| 进出必服务边 | 只能从端点进出 | 可从折线上任意点进出（Split Service） |
| Deadheading费用 | 图中最短路 | 欧氏直线距离 |
| 能量约束 | 载重容量 | 飞行时间/电量（含deadheading消耗） |
| 问题性质 | 纯离散 | 混合连续-离散 |

这一变化由 **文献6、9、17、19** 系统研究（LC K-DRPP及其多边形分析版本），从单架到多架，从理论到算法，逐步建立了无人机弧路由的完整理论体系。

#### 1.2 单车→协同系统：Vehicle-Drone协同架构的多样化
以无人机作为地面车辆的"附属飞行工具"，形成Vehicle-Drone协同系统，是近年来最活跃的研究方向：

- **文献2/4（Amorosi等）**：母船+无人机，聚焦图状目标覆盖，母船在连续空间/折线/路网三种模式下行驶
- **文献8（Xu等）**：GV-Drone，强调地面车辆作为充电平台，在城市路网巡逻中实时发射/回收无人机
- **文献16（Campbell等）**：多用途无人机，同一次飞行既覆盖线段又完成配送，融合ARP与VRP
- **文献20（Wu等）**：VD-ARP，多无人机并行飞行，车辆即时电池更换，IALNS框架

协同系统的核心挑战在于：**车辆路线与无人机任务的时序同步（Synchronization）**，这需要联合优化两层决策，远比单层路由问题复杂。

#### 1.3 确定性→不确定性：随机环境下的鲁棒路由策略
**文献13/15（UCARP系列）** 系统研究随机任务需求和费用的弧路由问题。核心思想是：

- 不再寻找固定路线（Route），而是进化**路由策略（Routing Policy）**——一个能在运行时根据实际揭示信息动态决策的函数。
- GP超启发式（GP Hyper-Heuristic）将策略表示为可进化的决策树，在蒙特卡罗样本上评估期望费用。
- 文献13引入小生境（Niching）维持策略多样性；文献15引入知识迁移（Knowledge Transfer）跨问题复用策略。

#### 1.4 静态→动态：实时重规划框架
**文献12（DCARP广义框架）** 提出虚拟任务策略，将动态事件（突发新任务、车辆故障）转化为静态CARP格式，实现"即插即用"式动态响应。**文献11（CARPTDSC）** 则将时变服务费用与出发时间优化联合，是更细粒度的时变优化。**文献18（ABC for DCARP）** 提供了另一种基于人工蜂群的动态响应框架。

#### 1.5 优化→学习：深度学习求解CARP
**文献10（DaAM）** 代表最新研究趋势：用Transformer注意力机制直接学习CARP求解策略，通过强化学习训练，推理速度远超元启发式，质量与其相当，为大规模实时应用开辟了新方向。

---

### 2. 算法类型汇总对比

| 算法类别 | 代表文献 | 核心特点 | 适用规模 |
|---------|---------|----------|---------|
| Branch-and-Cut/Price | 1, 5, 6, 14, 16, 19 | 精确求解，多面体分析 | 小规模（<100任务） |
| Matheuristic（分解+精确） | 2, 4, 5, 6, 14, 16 | 精确子问题+启发式组装 | 中等规模 |
| Memetic Algorithm | 7, 11 | 进化+局部搜索混合 | 中大规模 |
| GP Hyper-Heuristic | 13, 15 | 策略进化，不确定环境 | 中等规模 |
| GRASP | 3 | 随机贪心构造+局部搜索 | 中大规模 |
| ABC算法 | 18 | 仿生群体算法 | 中等规模 |
| IALNS | 8, 20 | 自适应大邻域搜索 | 中大规模 |
| 深度学习（Transformer） | 10 | 端到端学习 | 大规模 |
| 两阶段启发式 | 9 | 图约减+RPP求解 | 中等规模 |
| 广义元启发式框架 | 12 | 动态适应，框架无关 | 中大规模 |

---

### 3. 未来研究方向

基于以上文献分析，道路网络巡检领域的主要研究缺口和未来方向包括：

1. **多无人机+多车辆协同的大规模优化**：现有工作多限于1辆车+多架无人机，真正的多车队协同仍有较大空白。
2. **实时动态与不确定性融合**：UCARP和DCARP目前分别研究，将随机需求与动态事件统一建模是重要方向。
3. **能量感知的精确模型**：现有无人机模型多用飞行距离/时间近似能量消耗，结合物理模型（旋翼无人机能耗公式）的更精确约束尚待建立。
4. **深度学习与元启发式的融合**：DaAM（文献10）已展示了学习型求解器的潜力，与局部搜索算子的混合（Hybrid Neural Metaheuristic）是自然的延伸。
5. **连续优化的理论突破**：折线链上的进出点优化（文献9、19）仍缺乏高效精确算法，尤其是多无人机版本的连续优化理论。
6. **多用途无人机任务规划**：文献16提出的感知+配送一体化无人机路由，在实际灾害响应、农业、基础设施检测等场景有巨大潜力，理论与算法均需进一步完善。

---

*文献综述由主agent汇总，每篇文献均由独立子agent直接读取原始PDF内容后分析，确保内容来源于第一手资料。*
