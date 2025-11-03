---
tags:
  - "Numerical Optimization (2006, Springer)"
  - "Chapter 6"
  - "方法"
  - "中级"
前置知识: ""[[005-概念-优化算法概述]]""
---

# 知识点概述

BFGS方法是拟牛顿法中最流行和最有效的一种。它通过迭代更新Hessian矩阵的近似，来模拟牛顿法的行为，但避免了直接计算二阶导数。BFGS方法在计算成本、收敛速度和稳健性之间取得了出色的平衡，能够达到超线性收敛速度，并且其实现（特别是L-BFGS）非常适用于大规模问题。

# 教材原文

> The most popular quasi-Newton algorithm is the BFGS method, named for its discoverers Broyden, Fletcher, Goldfarb, and Shanno.
> The update formula for the inverse Hessian approximation $H_k$ is:
> $$(BFGS) \quad H_{k+1} = (I - \rho_k s_k y_k^T) H_k (I - \rho_k y_k s_k^T) + \rho_k s_k s_k^T, \tag{6.17}$$
> with
> $$\rho_k = \frac{1}{y_k^T s_k}, \quad s_k = x_{k+1}-x_k, \quad y_k = \nabla f_{k+1} - \nabla f_k.$$
> The update for the Hessian approximation $B_k$ is:
> $$B_{k+1} = B_k - \frac{B_k s_k s_k^T B_k}{s_k^T B_k s_k} + \frac{y_k y_k^T}{y_k^T s_k}. \tag{6.19}$$

# 详细解释

1.  **基本思想**
    *   BFGS方法属于拟牛顿法，它在每次迭代中都构造一个目标函数$f$的二次模型：
        $$m_k(p) = f_k + \nabla f_k^T p + \frac{1}{2} p^T B_k p$$
        其中$B_k$是Hessian矩阵$\nabla^2 f(x_k)$的一个近似。搜索方向$p_k$通过最小化该模型得到：$p_k = -B_k^{-1} \nabla f_k$。
    *   与牛顿法不同，BFGS不直接计算$B_k = \nabla^2 f(x_k)$，而是通过一个低秩（rank-two）的更新公式来迭代地逼近它。

2.  **割线方程 (Secant Equation)**
    *   更新的核心是满足**割线方程**: $B_{k+1}s_k = y_k$ (或等价地 $H_{k+1}y_k = s_k$) 。
    *   这个方程的意义是，要求新的Hessian近似$B_{k+1}$能够准确地反映上一步的梯度变化。它是在$s_k$方向上对$\nabla^2 f(x_{k+1})s_k \approx y_k$这个关系的一个近似。
    *   为了使更新有意义（特别是保证$B_{k+1}$正定），需要满足**曲率条件 (curvature condition)**: $s_k^T y_k > 0$。当采用满足Wolfe条件的线搜索时，这个条件自然成立。

3.  **BFGS 更新公式**
    *   BFGS更新是通过求解一个最小化问题导出的：在所有满足割线方程的对称矩阵中，寻找一个与当前Hessian近似$B_k$“最接近”的矩阵作为$B_{k+1}$。这里的“最接近”是通过一个加权的Frobenius范数来度量的。
    *   通常，算法直接更新Hessian的逆矩阵$H_k = B_k^{-1}$，因为这样计算搜索方向 $p_k = -H_k \nabla f_k$ 只需要矩阵-向量乘法，避免了求解线性方程组，计算成本为$O(n^2)$。
    *   $H_k$的更新公式见上述(6.17)，$B_k$的更新公式见(6.19)。两者是互为对偶的（通过交换$s_k \leftrightarrow y_k$和$B_k \leftrightarrow H_k$可以相互推导）。

4.  **算法框架 (Algorithm 6.1)**
    1.  给定初始点$x_0$，初始Hessian逆近似$H_0$（通常是单位阵$I$）。
    2.  **迭代**: 当$\nabla f_k \neq 0$时循环：
        a.  计算搜索方向: $p_k = -H_k \nabla f_k$。
        b.  执行线搜索，找到满足Wolfe条件的步长$\alpha_k$，并更新 $x_{k+1} = x_k + \alpha_k p_k$。
        c.  计算 $s_k = x_{k+1}-x_k$ 和 $y_k = \nabla f_{k+1} - \nabla f_k$。
        d.  使用公式(6.17)计算新的Hessian逆近似$H_{k+1}$。

5.  **重要性质**
    *   **正定性保持**: 如果初始近似$H_0$是正定的，并且线搜索满足$s_k^T y_k > 0$，那么后续所有的$H_k$都会保持正定。
    *   **自校正能力 (Self-Correcting Property)**: BFGS方法具有出色的自校正能力。即使$H_k$在某一步是一个很差的近似，只要线搜索足够精确，后续的更新会趋势性地修正这个近似，使其越来越准确。这是它比DFP等其他拟牛顿法更稳健的原因。
    *   **超线性收敛**: 在适当的条件下，BFGS方法具有Q-超线性收敛速度。

# 学习要点

-   掌握BFGS方法作为拟牛顿法的核心定位：用梯度信息近似Hessian。
-   理解割线方程$B_{k+1}s_k = y_k$和曲率条件$s_k^T y_k > 0$的中心作用。
-   熟记BFGS关于$H_k$（逆Hessian）的更新公式(6.17)。
-   了解BFGS算法的完整流程，特别是它与线搜索的结合。
-   知道BFGS方法最重要的优点：保持正定性、自校正能力和超线性收敛。

# 实践应用

-   BFGS是求解中小型无约束优化问题的**首选方法**之一。
-   对于大规模问题，其稠密的Hessian近似矩阵会带来巨大的内存开销。因此，**限制内存的BFGS (L-BFGS)** 方法被提出，它不存储完整的$H_k$矩阵，而是只保存最近的$m$个校正对$(s_i, y_i)$来隐式地表示$H_k$。L-BFGS是求解大规模无约束优化问题的标准算法。
-   在约束优化中，BFGS也被用来近似拉格朗日函数的Hessian矩阵，是SQP等方法的核心组成部分。

# 关联知识点

-   前置知识: [[005-概念-优化算法概述]], [[008-理论-收敛速度]]
-   后续知识: [[016-方法-SR1方法]], [[017-概念-Broyden族]], [[019-方法-限制内存的拟牛顿法]]
