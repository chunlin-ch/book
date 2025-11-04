---
tags:
  - "Numerical Optimization (2006, Springer)"
  - "Chapter 6"
  - "核心概念"
  - "高级"
前置知识:
  - "[[015-方法-BFGS方法]]"
  - "[[016-方法-SR1方法]]"
---

# 知识点概述

Broyden族是一类拟牛顿更新公式的统称，它是一个由单个参数$\phi_k$定义的线性组合，其成员包括了著名的BFGS和DFP方法。Broyden族中的所有方法都满足割线方程。通过研究Broyden族，可以从一个统一的视角来理解和分析不同拟牛顿法的性质，特别是它们在应用于二次函数时的行为。

# 教材原文

> The Broyden class is a family of updates specified by the following general formula:
> $$B_{k+1} = B_k - \frac{B_k s_k s_k^T B_k}{s_k^T B_k s_k} + \frac{y_k y_k^T}{y_k^T s_k} + \phi_k (s_k^T B_k s_k) v_k v_k^T, \tag{6.32}$$
> where $\phi_k$ is a scalar parameter and
> $$v_k = \left[ \frac{y_k}{y_k^T s_k} - \frac{B_k s_k}{s_k^T B_k s_k} \right]. \tag{6.33}$$
> We can rewrite (6.32) as a "linear combination" of these two methods, that is,
> $$B_{k+1} = (1-\phi_k)B_{k+1}^{\text{BFGS}} + \phi_k B_{k+1}^{\text{DFP}}.$$

# 详细解释

1.  **Broyden族的定义**
    *   如上公式(6.32)所示，Broyden族通过引入一个参数$\phi_k$来统一了一系列更新公式。
    *   当$\phi_k=0$时，公式退化为**BFGS**更新。
    *   当$\phi_k=1$时，公式退化为**DFP**更新。
    *   因此，Broyden族可以看作是BFGS和DFP更新的线性插值。

2.  **基本性质**
    *   **割线方程**: Broyden族中的所有成员都满足割线方程 $B_{k+1}s_k = y_k$，因为BFGS和DFP都满足此方程。
    *   **正定性保持**: 如果初始Hessian近似$B_0$是正定的，并且满足曲率条件$s_k^T y_k > 0$，那么当参数$\phi_k$满足 $\phi_k > \phi_k^c$ (其中$\phi_k^c \leq 0$是一个与$B_k, s_k, y_k$相关的临界值)时，新的近似$B_{k+1}$也将是正定的。特别地，当$\phi_k \in [0,1]$时（这个子集被称为**受限Broyden族 (restricted Broyden class)**），正定性一定能保持。

3.  **在二次函数上的性质 (Theorem 6.4)**
    *   当Broyden族方法应用于严格凸二次函数并采用**精确线搜索**时，它们表现出许多惊人的一致性：
        1.  **迭代点相同**: 对于所有满足$\phi_k \geq \phi_k^c$的$\phi_k$，算法产生的迭代点序列$\{x_k\}$是完全相同的，与$\phi_k$的取值无关。
        2.  **有限步终止**: 最多n步收敛到解。
        3.  **与共轭梯度法的关系**: 如果初始矩阵$B_0=I$，则产生的迭代点序列与共轭梯度法完全相同。
        4.  **精确Hessian**: 如果执行了n步，则$B_n=A$，即最终的Hessian近似等于二次函数的真实Hessian矩阵。

4.  **SR1方法与Broyden族**
    *   SR1方法也是Broyden族的一个成员，其对应的参数为：
        $$\phi_k = \frac{s_k^T y_k}{s_k^T y_k - s_k^T B_k s_k}$$
    *   这个$\phi_k$值可能不在$[0,1]$区间内，因此SR1不属于受限Broyden族，这也解释了为什么SR1不保证正定性。

# 学习要点

-   理解Broyden族是对BFGS和DFP等一系列拟牛顿更新的统一描述。
-   掌握Broyden族公式与参数$\phi_k$的关系，特别是$\phi_k=0$对应BFGS，$\phi_k=1$对应DFP。
-   了解受限Broyden族（$\phi_k \in [0,1]$）能够保持Hessian近似的正定性。
-   记住在二次函数和精确线搜索的理想条件下，Broyden族中的大部分方法（包括BFGS和DFP）产生完全相同的迭代点序列，并具有二次终止性。

# 实践应用

-   理论上，对二次函数和精确线搜索，Broyden族中$\phi_k \in [0,1]$的任何方法都等价。但在一般非线性函数和非精确线搜索的实际情况下，不同$\phi_k$的选择会导致算法性能的巨大差异。
-   大量的数值实验表明，BFGS方法（$\phi_k=0$）通常是Broyden族中最稳健和最高效的成员。DFP方法（$\phi_k=1$）在某些情况下表现不佳，因为它对非精确线搜索更敏感，且自校正能力不如BFGS。
-   对Broyden族的研究为理解各种拟牛顿法的共性和差异提供了理论框架，并最终指导了算法的选择，确立了BFGS的主导地位。

# 关联知识点

-   前置知识: [[015-方法-BFGS方法]], [[016-方法-SR1方法]]
-   后续知识: [[019-方法-限制内存的拟牛顿法]]
