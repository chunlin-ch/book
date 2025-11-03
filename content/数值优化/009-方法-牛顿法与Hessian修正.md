---
tags:
  - "Numerical Optimization (2006, Springer)"
  - "Chapter 3"
  - "方法"
  - "中级"
前置知识: ""[[008-理论-收敛速度]]""
---

# 知识点概述

纯牛顿法在迭代点远离解时，其Hessian矩阵 $\nabla^2 f(x_k)$ 可能不是正定的，导致牛顿方向 $p_k^N = -(\nabla^2 f_k)^{-1} \nabla f_k$ 可能不是下降方向。为了保证算法的全局收敛性，需要对Hessian矩阵进行修正，以确保生成一个有效的下降方向。常用的修正策略包括特征值修正、单位矩阵倍数加成和修正的Cholesky分解。

# 教材原文

> Away from the solution, the Hessian matrix $\nabla^2 f(x)$ may not be positive definite, so the Newton direction ... may not be a descent direction. We now describe an approach to overcome this difficulty ... This approach obtains the step $p_k$ from a linear system identical to (3.38), except that the coefficient matrix is replaced with a positive definite approximation, formed before or during the solution process. The modified Hessian is obtained by adding either a positive diagonal matrix or a full matrix to the true Hessian $\nabla^2 f(x_k)$.

# 详细解释

**动机**: 保证线搜索牛顿法的全局收敛性。当Hessian矩阵 $\nabla^2 f_k$ 非正定时，牛顿步可能指向函数值增加的方向。通过修正Hessian，我们构造一个新的正定矩阵$B_k$，并用它来计算搜索方向 $p_k = -B_k^{-1} \nabla f_k$，从而保证$p_k$是一个下降方向。

**修正策略**: 

1.  **特征值修正 (Eigenvalue Modification)**
    *   **思想**: 对Hessian矩阵进行谱分解（$A = Q \Lambda Q^T$），然后替换掉所有负的或不够大的正特征值。例如，将所有小于某个正阈值$\delta$的特征值$\\lambda_i$替换为$\\delta$。
    *   **优点**: 理论上清晰，可以进行最优修正（在Frobenius范数意义下）。
    *   **缺点**: 计算矩阵的完整谱分解成本极高（$O(n^3)$），在实际中不可行。

2.  **单位矩阵倍数加成 (Adding a Multiple of the Identity)**
    *   **思想**: 构造修正矩阵 $B_k = \nabla^2 f(x_k) + \tau I$，其中 $\\tau > 0$ 是一个标量，其大小要足以保证$B_k$是正定的。这相当于将原Hessian的所有特征值都增加了$\\tau$。
    *   **优点**: 实现简单。
    *   **缺点**: 这种方法“一刀切”，改变了所有的特征值，可能丢失了原Hessian矩阵中有效的曲率信息。确定合适的$\\tau$值可能需要多次尝试和矩阵分解，成本较高。

3.  **修正的Cholesky分解 (Modified Cholesky Factorization)**
    *   **思想**: 在尝试对Hessian矩阵进行Cholesky分解（$A=LDL^T$）的过程中，动态地修正矩阵。如果分解过程中遇到非正的对角元$d_j$，就将其增加到一个足够大的正数，以保证分解可以继续并最终得到一个正定矩阵。
    *   **优点**: 是一种非常实用和高效的策略。它只在必要时进行修正，如果原Hessian已经是“足够正定”的，则不进行任何修改，从而保留了牛顿法的快速收敛特性。许多优化软件都采用了这种或类似的策略。
    *   **实现**: 算法在计算$LDL^T$分解的第j列时，会计算对角元$d_j$。如果$d_j$小于某个阈值，就将其增加，例如 $d_j = \max(|c_{jj}|, (\theta_j/\beta)^2, \delta)$。

4.  **修正的对称不定分解 (Modified Symmetric Indefinite Factorization)**
    *   **思想**: 首先计算Hessian的对称不定分解 $PAP^T = LBL^T$，其中B是块对角矩阵（含1x1和2x2块）。然后修正B的特征值，得到$B+F$，最终的修正是通过 $A+E = P^T L(B+F)L^T P$ 得到的。
    *   **优点**: 能够处理不定Hessian，并且修正的目标性更强。

# 学习要点

-   理解纯牛顿法在全局收敛上的局限性以及Hessian修正的必要性。
-   掌握不同Hessian修正策略的基本思想、优缺点和适用场景。
-   认识到修正的Cholesky分解是目前最实用、最高效的方法之一。
-   修正的目标是在保证下降方向的同时，尽可能少地改变原始Hessian矩阵的二阶信息。

# 实践应用

-   在开发或使用基于牛顿法的优化求解器时，Hessian修正是一个核心的全局化技术。
-   信赖域方法（见Chapter 4）提供了另一种处理非正定Hessian的有效途径，它通过限制步长来处理负曲率，而不是直接修改Hessian矩阵。
-   在许多大型优化问题中，精确计算Hessian矩阵本身就不可行，此时会采用拟牛顿法（如BFGS）或不精确牛顿法（如Newton-CG），这些方法也内含了处理非正定性的机制。

# 关联知识点

-   前置知识: [[008-理论-收敛速度]], [[004-理论-最优性条件]]
-   后续知识: [[010-方法-信赖域方法概述]], [[018-方法-不精确牛顿法]]
