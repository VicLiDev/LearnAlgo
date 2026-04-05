# 泰勒公式和泰勒级数

## 泰勒公式

> ref: 《高等数学》上册 P140
### 推导过程

提出如下问题：设函数$f(x)$在含有$s_0$的开区间内具有直到$(n+1)$阶导数，试找出一个关于$(x-x_0)$的$n$次多项式
$$p_n(x) = a_0 + a_1 (x - x_0) + a_2(x - x_0)^2 + ... + a_n(x - x_0)^n$$
来近似表达$f(x)$，要求$p_n(x)$与$f(x)$之差是比$(x - x_0)$高阶的无穷小，并给出误差$|f(x) - p_n(x)|$的具体表达式

假设$p_n(x)$在$x_0$处的函数值及它的直到$n$阶导数在$x_0$处的值依次与$f(x_0)$，$f^{\prime}(x_0)$，...，$f^{(n)}(x_0)$相等，即满足
$$
\begin{cases}
p_n(x_0) = f(x_0), \\
p_n^{\prime}(x_0) = f^{\prime}(x_0), \\
p_n^{\prime \prime}(x_0) = f^{\prime \prime}(x_0), \\
... \\
p_n^{(n)}(x_0) = f^{(n)}(x_0), \\
\end{cases}
$$

按照这些等式来确定多项式$p_n(x)$的系数$a_0, a_1, a_2, ..., a_n$。为此，对 $p_n(x)$求各阶导数，然后分别带入以上等式得：
$$
\begin{cases}
a_0 = f(x_0) \\
1 * a_1 = f^{\prime}(x_0) \\
2! * a_2 = f^{\prime \prime}(x_0) \\
... \\
n! * a_n = f^{(n)}(x_0) \\
\end{cases}
$$

即得：
$$
\begin{cases}
a_0 = f(x_0) \\
a_1 = f^{\prime}(x_0) \\
a_2 = \frac{1}{2!} f^{\prime \prime}(x_0) \\
... \\
a_n = \frac{1}{n!} f^{(n)}(x_0) \\
\end{cases}
$$

将所求到的$a_0, a_1, a_2, ..., a_n$带入到 $p_n(x)$，得：
$$
p_n(x) = f(x_0) + f^{\prime}(x_0)(x - x_0) + \frac{f^{\prime \prime}(x_0)}{2!} (x - x_0)^2 + ... + \frac{f^{(n)}(x_0)}{n!} (x - x_0)^n
$$



**泰勒中值定理**：

如果函数$f(x)$在含有$x_0$的某个开区间$(a, b)$内具有直到$(n + 1)$阶的导数，则对任一$x \in (a, b)$，有
$$
p_n(x) = f(x_0) + f^{\prime}(x - x_0) + \frac{f^{\prime \prime}(x_0)}{2!} (x - x_0)^2 + ... + \frac{f^{(n)}(x_0)}{n!} (x - x_0)^n + R_n(x)
$$

其中
$$
R_n(x) = \frac{f^{(n+1)}(\xi)}{(n + 1)!} (x - x_0)^{(n + 1)}
$$
这里$\xi$是$x_0$与$x$之间的某个值，泰勒中值定理是拉格朗日中值定理的推广，证明暂且忽略，需要可以查看《高等数学》上册P141




## 泰勒级数

> ref: 《高等数学》下册 P278

泰勒级数（Taylor Series）的推导过程主要基于函数的无限次可微性（即光滑性）以及多项式逼近的思想。泰勒级数提供了一种将函数表示为无限项和（即级数）的方法，每一项都是函数在某点的导数乘以该点到该点的距离（或该点的幂）的乘积。

### 推导过程

经常会遇到问题：给定函数$f(x)$，要考虑他能否在某个区间内展开成幂级数，也就是说，是否能找到这样一个幂级数，他在某区间内收敛，且其恰好就是给定的函数$f(x)$，如果能找到这样的幂级数，我们就说，函数$f(x)$在该区间内能展开成幂级数，而这个幂级数在该区间内就表达了函数$f(x)$。

假设函数$f(x)$在点$x_0$的某邻域$U(x_0)$内能展开成幂级数，即有：
$$
f(x) = a_0 + a_1(x - x_0) + a_2(x - x_0)^2 + ... + a_n(x - x_0)^n + ..., x \in U(x_0)
$$
那么根据和函数的性质，可知$f(x)$在$U(x_0)$内应具有任意阶导数，且
$$
f^{(n)}(x) = n!a_n + (n+1)!a_{n+1}(x - x_0) + \frac{(n + 2)!}{2!}(x - x_0)^2 + ...,
$$
当$x=x_0$时，可得：
$$
f^{(n)}(x_0) = n! a_n
$$

于是
$$
	a_n = \frac{1}{n!} f^{n}(x_0) \quad (n = 0, 1, 2, ...)
$$

这就表明，如果函数$f(x)$有幂级数展开式，那么该幂级数的系数$a_n$由上式决定，该幂级数必定为：
$$
f(x_0) + f^{\prime}(x_0)(x - x_0) + ... + \frac{f^{(n)}(x_0)}{n!} (x - x_0)^n + ... = \sum_{n = 0}^{\infty} \frac{f^{(n)}(x_0)}{n!} (x - x_0)^n
$$

因此$f(x)$在$x_0$邻域内的展开式必定为：
$$
f(x) = \sum_{n = 0}^{\infty} \frac{f^n(x_0)}{n!}(x - x_0)^n, \quad x \in U(x_0)
$$

上式即为函数$f(x)$在点$x_0$处的泰勒级数

### 注意事项

- 泰勒级数的收敛性取决于函数f(x)的性质以及x与x0​之间的距离。
- 并非所有函数都有泰勒级数，或者其泰勒级数在整个定义域内都收敛。
- 泰勒级数在理论分析和数值计算中都有广泛应用，特别是在求解微分方程、近似计算等方面。


### 区别和联系

- **区别**：泰勒公式是一个有限项的和加上一个余项，用于近似计算；泰勒级数是一个无限项的和，用于表示函数或进行幂级数展开。
- **联系**：当泰勒公式的余项趋于0时，泰勒公式就变成了泰勒级数。在某些情况下，泰勒级数可以精确地表示函数，但在其他情况下可能只在某个区间内收敛。

因此，虽然泰勒公式和泰勒级数在形式上有相似之处，但它们是两个不同的概念，用于不同的数学分析和计算中。



## 欧拉公式

由于欧拉公式也是用了泰勒级数相关的内容，因此一并放到此章节

### 前备知识点

> ref: 《高等数学》下册P280

函数$f(x) = e^x$展开成$x$的幂级数为：$e^x = 1 + x + \frac{x^2}{2!} + ... + \frac{x^n}{n!} + ...,$

函数$f(x) = \sin{x}$展开成$x$的幂级数为：$x - \frac{x^3}{3!} + \frac{x^5}{5!} - (-1)^k\frac{x^{2k + 1}}{(2k + 1)!} + ... \quad (-\infty < x < + \infty)$，
更一般的可以写为：$\sin{x} = \sum_{k=0}^{\infty} \frac{(-1)^k}{(2k + 1)!}x^{2k + 1} \quad (-\infty < x < +\infty)$

对$\sin{x}$两边求导可得：$\cos{x} = \sum_{k=0}^{\infty} \frac{(-1)^k}{(2k)!}x^{2k} \quad (-\infty < x < +\infty)$

### 推导过程

> ref: 《高等数学》下册P291

设有复数项级数为
$$
(u_1 + iv_1) + (u_2 + iv_2) + ... + (u_n + iv_n) + ...,\quad \quad (1)
$$
其中$u_n, v_n, (n = 1, 2, 3, ...)$为实数或实函数，如果实部所成的级数
$$u_1 + u_2 + ... + u_n + ... \quad \quad (2)$$
收敛于和$u$，并且虚部所成的级数
$$v_1 + v_2 + ... + v_n + ... \quad \quad (3) $$
收敛于和$v$，那就说上式的级数收敛且其和为$u + iv$

如果式(1)各项的模所构成的级数$\sqrt{u_1^2 + v_1^2} + \sqrt{u_2^2 + v_2^2} + ... +  + \sqrt{u_n^2 + v_n^2} + ...$，收敛，则称式(1)绝对收敛

由于$|u_n| \leq \sqrt{u_n^2 + v_n^2}, \, |v_n| \leq \sqrt{u_n^2 + v_n^2} \, (n = 1, 2, 3, ...)$，那么级数(2)(3)绝对收敛，从而级数(1)绝对收敛

考察复数项级数：
$$
1 + z + \frac{1}{2!}z^2 + ... + \frac{1}{n!}z^n + ... \quad (z = x + iy) \quad \quad (4)
$$
可以证明级数(4)在整个复平面上是绝对收敛的。在$x$轴上$(z = x)$他表示指数函数$e^x$，在整个复平面上用它来定义复变量指数函数，记作$e^z$。于是$e^z$定义为
$$
e^z = 1 + z + \frac{1}{2!}z^2 + ... + \frac{1}{n!}z^n + ... \quad (|z| < \infty) \quad \quad (5)
$$
当$x = 0$时，$z$为纯虚数$iy$，式(5)成为：
$$
\begin{align}
e^{iy} &= 1 + iy + \frac{1}{2!}(iy)^2 + \frac{1}{3!}(iy)^3 + ... + \frac{1}{n!}(iy)^n + ... \\
&= 1 + iy - \frac{1}{2!}y^2 - i\frac{1}{3!}y^3 + \frac{1}{4!}y^4 + i\frac{1}{5!}y^5 - ...\\
&= (1 - \frac{1}{2!}y^2 + \frac{1}{4!}y^4 - ...) + (iy - i\frac{1}{3!}y^3 + i\frac{1}{5!}y^5 - ...)\\
\end{align}
$$

把$y$换成$x$，上式变为
$$
e^{ix} = \cos{x} + i \sin{x}
$$
这就是欧拉公式

### 推导过程_法2

欧拉公式的推导通常涉及泰勒级数（或称为幂级数）的展开。
1. **首先，考虑 $e^x$ 的泰勒级数展开**：
	$$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \cdots$$
2. **接着，考虑 $\cos x$ 和 $\sin x$ 的泰勒级数展开**：
	$$
	\cos x = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \cdots \\
	$$
	$$
	\sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \cdots \\
	$$
3. **将 $x$ 替换为 $ix$ 并代入 $e^x$ 的泰勒级数中**：
	 $$e^{ix} = 1 + ix + \frac{(ix)^2}{2!} + \frac{(ix)^3}{3!} + \frac{(ix)^4}{4!} + \cdots$$

4. **展开并合并同类项**：
	$$e^{ix} = 1 + ix - \frac{x^2}{2!} - \frac{ix^3}{3!} + \frac{x^4}{4!} + \frac{ix^5}{5!} - \frac{x^6}{6!} - \frac{ix^7}{7!} + \cdots$$

	注意到，这里的项可以分组为实部和虚部：
	 - 实部：$1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \cdots$，这正是 $\cos x$ 的泰勒级数。
	 - 虚部：$ix - \frac{ix^3}{3!} + \frac{ix^5}{5!} - \frac{ix^7}{7!} + \cdots$，这可以重写为 $i\left(x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \cdots\right)$，这正是 $i\sin x$ 的泰勒级数。


5. **因此，我们可以得出**：
	$$e^{ix} = \cos x + i\sin x$$
* **结论**

通过上述推导，我们证明了欧拉公式 $e^{ix} = \cos x + i\sin x$ 成立。这个公式在复变函数、电子学、量子力学等领域有着广泛的应用。



# 傅里叶变换

## 傅里叶级数

### 傅里叶级数的一般形式

#### 三角级数

以一般的形式表示正弦函数：
$$
y = A\sin{(wt + \phi)}
$$
其中：$A$: 振幅，$w$: 角频率，$\phi$: 初相

为了研究非正弦周期函数，使用幂展开的方式将周期函数展开成由简单的周期函数（例如三角函数）组成的级数，具体地说，将周期为$T( = \frac{2\pi}{w})$的周期函数用一系列用T为周期的正弦函数$A_n\sin{(nwt + \phi_n)}$组成的级数来表示，记为：
$$
f(t) = A_0 + \sum_{n = 1}^{\infty}A_n\sin{(nwt + \phi_n)}
$$

在电工学上，这种展开称为谐波分析，$A_0$被称为$f(t)$的直流分量；$A_1\sin(wt + \phi_1)$被称为一次谐波（又称为基波）；而$A_2\sin(wt + \phi_2)...$依次称为二次谐波，三次谐波等

为了方便起见，将公式展开：
$$
A_n\sin{(nwt + \phi_n) = A_n\sin{\phi_n\cos{nwt}} + A_n\cos{\phi_n\sin{nwt}}}
$$
令$\frac{a_0}{2} = A_0$，$a_n = A_n\sin{\phi_n}$，$b_n = A_n\cos{\phi_n}$，$w = \frac{\pi}{l}$（即 $T = 2l$），则上式可以改写为：
$$
\frac{a_0}{2} + \sum_{n = 1}^{\infty}(a_n\cos{\frac{n \pi t}{l}} + b_n\sin{\frac{n \pi t}{l}})
$$
形如上式的级数被称为**三角级数**

令$\frac{\pi t}{l} = x$，上式可以改为：
$$
\frac{a_0}{2} + \sum_{n = 1}^{\infty}(a_n\cos{nx} + b_n\sin{nx})
$$
这便是把以$2l$为周期的三角函数转换成了以$2\pi$为周期的三角函数

#### 三角级数的正交性

所谓三角函数系：
$$
1, \cos{x}, \sin{x}, \cos{2x}, \sin{2x}, ..., \cos{nx}, \sin{nx}
$$
在区间$[-\pi, \pi]$上正交，就是指三角函数系中任何不同的两个函数的乘积在趋近啊$[-\pi, \pi]$上的积分等于零，即：
$$
\begin{align}
&\int_{-\pi}^{\pi} \cos{nx}\, dx = 0 \quad (n = 1, 2, 3, ...), \\
&\int_{-\pi}^{\pi} \sin{nx}\, dx = 0 \quad (n = 1, 2, 3, ...), \\
&\int_{-\pi}^{\pi} \sin{kx} \cos{nx}\, dx = 0 \quad (k,n = 1, 2, 3, ..., k \neq n), \\
&\int_{-\pi}^{\pi} \cos{kx} \cos{nx}\, dx = 0 \quad (k,n = 1, 2, 3, ..., k \neq n), \\
&\int_{-\pi}^{\pi} \sin{kx} \sin{nx}\, dx = 0 \quad (k,n = 1, 2, 3, ..., k \neq n), \\
\end{align}
$$
证明：
利用三角函数中的和差化积公式：$\cos{kx}\cos{nx} = \frac{1}{2}[\cos{(k + n)}x + \cos{(k - n)}x]$，
当$k \neq n$时，有：
$$
\begin{align}
\int_{-\pi}^{\pi} \cos{kx}\cos{nx}\,dx &= \frac{1}{2} \int_{-\pi}^{\pi}[\cos{(k + n)}x + \cos{(k - n)}x]\,dx \\
&= \frac{1}{2} [\frac{\sin{(k + n)x}}{k + n} + \frac{\sin{(k - n)}x}{k - n}]_{-\pi}^{\pi} \\
&= 0 \quad (k,n = 1, 2, 3, ..., k \neq n)\\
\end{align}
$$

两个相同函数的乘积在区间$[-\pi, \pi]$上的积分不等于零，即：

$$
\begin{align}
&\int_{-\pi}^{\pi} 1^2 dx = 2\pi \\
&\int_{-\pi}^{\pi} \sin^2{nx} \, dx = \pi \\
&\int_{-\pi}^{\pi} \cos^2{nx} \, dx = \pi \\
\end{align}
$$
其中$n = 1, 2, 3 ...$


#### 推导过程

设$f(x)$是周期为$2\pi$的周期函数，且能展开成三角函数：
$$
f(x) = \frac{a_0}{2} + \sum_{k = 1}^{\infty}(a_k\cos{kx} + b_k\sin{kx})\quad \quad(1)
$$
假设上式中右端的级数可以逐项积分，先求$a_0$，对上式从$-\pi$到$\pi$进行积分，因此有：
$$
\int_{-\pi}^{\pi}f(x)\,dx = \int_{-\pi}^{\pi} \frac{a_0}{2}\,dx + \sum_{k=1}^{\infty}[a_k\int_{-\pi}^{\pi}\cos{kx}\,dx + b_k\int_{-\pi}^{\pi}\sin{kx}\,dx]
$$

根据三角函数系的正交性，等式右边除了第一项外，其余各项均为零，所以：
$$
\int_{-\pi}^{\pi}f(x)\,dx = \frac{a_0}{2} * 2\pi
$$
于是得
$$
a_0 = \frac{1}{\pi}\int_{-\pi}^{\pi} f(x)dx
$$

其次求$a_n$，用$\cos{nx}$乘式(1)两端，再从$-\pi$到$\pi$积分，得到：
$$
\int_{-\pi}^{\pi} f(x) \cos{nx}\,dx = \frac{a_0}{2} \int_{-\pi}^{\pi} {\cos{nx}}\,dx + \sum_{k=1}^{\infty}[a_k\int_{-\pi}^{\pi} \cos{kx} \cos{nx}\,dx + b_k\int_{-\pi}^{\pi}\sin{kx} \cos{nx}\,dx]
$$
根据三角函数系的正交性，等式右端出了$k=n$的一项外，其余各项均为零，所以
$$
\int_{-\pi}^{\pi}f(x)cos{nx}\,dx = a_n\int_{-\pi}^{\pi} \cos^2{nx}\,dx = a_n\pi
$$
于是得：
$$
a_n = \frac{1}{\pi}\int_{-\pi}^{\pi}f(x) \cos{nx}\,dx \quad (n = 1, 2, 3,...)
$$
类似的，用$\sin{x}$乘式(1)两端，再从${-\pi}$到$\pi$积分，可得：
$$
b_n = \frac{1}{\pi}\int_{-\pi}^{\pi}f(x) \sin{nx}\,dx \quad (n = 1, 2, 3,...)
$$

由于当$n=0$时，$a_n$的表达式正好给出$a_0$，因此，已得结果可以合并写成：
$$
\begin{cases}
a_n = \frac{1}{\pi}\int_{-\pi}^{\pi}f(x) \cos{nx}\,dx \quad (n = 1, 2, 3,...) \\
b_n = \frac{1}{\pi}\int_{-\pi}^{\pi}f(x) \sin{nx}\,dx \quad (n = 1, 2, 3,...) \\
\end{cases}
$$
如果上式中的$a_n$和$b_n$都存在，这时它们定出的系数$a_0, a_1, b_1,...$叫做函数$f(x)$的傅里叶系数，将这些系数带入式(1)右端，所得的三角级数
$$
f(x) = \frac{a_0}{2} + \sum_{k = 1}^{\infty}(a_k\cos{kx} + b_k\sin{kx})
$$
叫做傅里叶级数

一个定义在$(-\infty, +\infty)$上周期为$2\pi$的函数$f(x)$，如果他在一个周期上可积，则一定可以做出$f(x)$的傅里叶级数。然而，函数$f(x)$的傅里叶级数是否一定收敛？如果它收敛，他是否一定收敛于函数$f(x)$？一般来说，这两个问题的答案都不是肯定的。那么，$f(x)$在怎样的条件下，他的傅里叶级数不仅收敛，而且收敛于$f(x)$？也就是说，$f(x)$满足什么条件可以展开成傅里叶级数？如下给出收敛定理

定理（收敛定理，狄利克雷（Dirichlet）充分条件） 设$f(x)$是周期为$2\pi$的周期函数，如果它满足：
1. 在一个周期内连续或只有有限个第一类时间点
2. 在一个周期内至多只有有限个极值点
则$f(x)$的傅里叶级数收敛，并且
* 当$x$是$f(x)$的连续点时，级数收敛于$f(x)$
* 当$x$是$f(x)$的间断点时，级数收敛于$\frac{1}{2}[f(x^-) + f(x^+)]$


**以上是以$2\pi$为周期的推导，如果以$T$为周期：**

$$ f(t) = \frac{a_0}{2} + \sum_{n=1}^{\infty} \left( a_n \cos\left(\frac{2\pi n t}{T}\right) + b_n \sin\left(\frac{2\pi n t}{T}\right) \right) $$

其中，系数$a_n$和$b_n$分别为：

$$ a_n = \frac{2}{T} \int_{t_0}^{t_0+T} f(t) \cos\left(\frac{2\pi n t}{T}\right) \, dt $$

$$ b_n = \frac{2}{T} \int_{t_0}^{t_0+T} f(t) \sin\left(\frac{2\pi n t}{T}\right) \, dt $$

这里$t_0$是任意实数。


**如果以$2l$为周期：**

$$ f(t) = \frac{a_0}{2} + \sum_{n=1}^{\infty} \left( a_n \cos\left(\frac{n\pi t}{l}\right) + b_n \sin\left(\frac{n\pi t}{l}\right) \right) $$

其中：

$$ a_n = \frac{1}{l} \int_{-l}^{l} f(t) \cos\left(\frac{n\pi t}{l}\right) \, dt \quad (n = 0, 1, 2, 3, \ldots) $$

$$ b_n = \frac{1}{l} \int_{-l}^{l} f(t) \sin\left(\frac{n\pi t}{l}\right) \, dt \quad (n = 1, 2, 3, \ldots) $$

证明：

做变量代换$z=\frac{\pi x}{l}$，于是区间$-l \leq x \leq l$就变换成$-\pi \leq z \leq \pi$。设函数$f(x)=f(\frac{lz}{\pi}) = F(z)$，从而$F(z)$是周期为$2\pi$的周期函数，并且它满足收敛定理的条件，将$F(z)$展开成傅里叶级数
$$
F(z) = \frac{a_0}{2} + \sum_{n=1}^{\infty} \left( a_n \cos\left(nz\right) + b_n \sin\left(nz\right) \right) 
$$
其中
$$
\begin{align}
a_n = \frac{1}{\pi}\int_{-\pi}^{\pi} F(z)\cos{(nz)}\,dz \\
b_n = \frac{1}{\pi}\int_{-\pi}^{\pi} F(z)\sin{(nz)}\,dz \\
\end{align}
$$
在上式中，零$z=\frac{\pi x}{l}$，并注意到$F(z) = f(x)$，于是有
$$
f(x) = \frac{a_0}{2} + \sum_{n=1}^{\infty} \left( a_n \cos\left(\frac{n\pi x}{l}\right) + b_n \sin\left(\frac{n\pi x}{l}\right) \right) 
$$
其中：
$$ a_n = \frac{1}{l} \int_{-l}^{l} f(x) \cos\left(\frac{n\pi x}{l}\right) \, dt \quad (n = 0, 1, 2, 3, \ldots) $$

$$ b_n = \frac{1}{l} \int_{-l}^{l} f(x) \sin\left(\frac{n\pi x}{l}\right) \, dt \quad (n = 1, 2, 3, \ldots) $$

### 傅里叶级数的复数形式

在周期为$2l$的傅里叶级数的基础上，利用欧拉公式 $\cos{t} = \frac{e^{it} + e^{-it}}{2}, \sin{t} = \frac{e^{it} - e^{-it}}{2i}$，可以把周期为$2l$的傅里叶级数化为：
$$
\begin{align}
f(x) &= \frac{a_0}{2} + \sum_{n=1}^{\infty} \left( a_n \cos\left(\frac{n\pi x}{l}\right) + b_n \sin\left(\frac{n\pi x}{l}\right) \right)  \\
&= \frac{a_0}{2} + \sum_{n = 1}^{\infty}[\frac{a_n - ib_n}{2} e^{i\frac{n \pi x}{l}} + \frac{a_n + ib_n}{2} e^{-i\frac{n \pi x}{l}}] \quad \quad (1)
\end{align}
$$
记
$$
\frac{a_0}{2} = c_0, \frac{a_n - ib_n}{2} = c_n, \frac{a_n + ib_n}{2} = c_{-n} \quad (n = 1, 2, 3,...) \quad \quad (2)
$$
则式(1)就可以表示为：

$$
\begin{align}
&c_0 + \sum_{n = 1}^{\infty}(c_ne^{i\frac{n \pi x}{l}} + c_{-n}e^{-i\frac{n \pi x}{l}}) \\
&=(c_ne^{i\frac{n \pi x}{l}})_{n=0} + \sum_{n = 1}^{\infty}(c_ne^{i\frac{n \pi x}{l}} + c_{-n}e^{-i\frac{n \pi x}{l}})
\end{align}
$$
即得傅里叶级数的复数形式为：
$$
\sum_{n = - \infty}^{\infty} c_n e^{i\frac{n \pi x}{l}}
$$
为了得出系数$c_n$的表达式，把$2l$周期的傅里叶级数带入到式(2)中，得：
$$
\begin{align}
c_0 &= \frac{a_0}{2} = \frac{1}{2l} \int_{-l}^{l}f(x)\,dx \\

c_n &= \frac{a_n - ib_n}{2} \\
&= \frac{1}{2}[\frac{1}{l}\int_{-l}^{l} f(x) \cos{\frac{n \pi x}{l}} \, dx - \frac{i}{l}\int_{-l}^{l}f(x) \sin{\frac{n \pi x}{l}} \, dx] \\
&= \frac{1}{2l}\int_{-l}^{l}f(x)(\cos {\frac{n \pi x}{l}} - i \sin{\frac{n \pi x}{l}}) \, dx \\
&= \frac{1}{2l}\int_{-l}^{l}f(x) e^{-i\frac{n \pi x}{l}}\,dx \quad \quad (n = 1, 2, 3,...) \\

c_{-n} &= \frac{a_n + ib_n}{2} \\
&= \frac{1}{2l}\int_{-l}^{l}f(x)e^{i\frac{n \pi x}{l}}\,dx \quad \quad (n = 1, 2, 3,...) \\
\end{align}
$$

将已得的结果合并写为：
$$
c_n = \frac{1}{2l}\int_{-l}^{l}f(x) e^{-i\frac{n \pi x}{l}}\,dx \quad \quad (n = 0, \pm1, \pm2,...)
$$





以$t$为变量，有复数形式的傅里叶级数如下：
$$ f(t) = \sum_{n = -\infty}^{\infty} C_n e ^{i \frac{n \pi t}{l}} $$

其中，
$$ Cn = \frac{1}{2l} \int_{-l}^{l} f(t) e^{-i \frac{n \pi t}{l}} \, d(t) \quad (n = \pm1, \pm2, \pm3, \ldots)$$


## 傅里叶(Fourier)变换

> ref：《积分变换》-- 东南大学数学系 张元林 编 P5

有复数形式的傅里叶级数如下：
$$ f(t)_{2l} = \sum_{n = -\infty}^{\infty} C_n e ^{i \frac{n \pi t}{l}} $$

其中，
$$ Cn = \frac{1}{2l} \int_{-l}^{l} f(t)_{2l} \, e^{-i \frac{n \pi t}{l}} \, dt \quad (n = \pm1, \pm2, \pm3, \ldots)$$

即：
$$ f(t)_{2l} = \frac{1}{2l} \sum_{n = -\infty}^{\infty} \int_{-l}^{l} f(\tau)_{2l} \, e^{-i \frac{n \pi \tau}{l}} \, d\tau \, e ^{i \frac{n \pi t}{l}} $$
由于$C_n$是一个常数，因此这里为了区分，将$C_n$得积分变量改为$\tau$

令$w= \frac{2\pi}{2l} = \frac{\pi}{l}$得：
$$ f(t)_{2l} = \frac{1}{2l} \sum_{n = -\infty}^{\infty} \int_{-l}^{l} f(\tau)_{2l} \, e^{-i n w \tau} \, d\tau \, e ^{i n w t} $$

令$w_n = nw \quad (n = 0, \pm1, \pm2,...)$得：
$$ f(t)_{2l} = \frac{1}{2l} \sum_{n = -\infty}^{\infty} \int_{-l}^{l} f(\tau)_{2l} \, e^{-i w_n \tau} \, d\tau \, e ^{i w_n t} $$

由于$Cn = \frac{1}{2l} \int_{-l}^{l} f(\tau)_{2l} \, e^{-i w_n \tau} \, d\tau \quad (n = \pm1, \pm2, \pm3, \ldots)$，对于固定的周期$2l$是一个常数，因此这里可以直接把它当成一个常数看待，当周期$2l \rightarrow \infty$，$w_0 = \frac{2\pi}{2l} = \frac{\pi}{l} \rightarrow 0 (\triangle w)$时，将$l = \frac{\pi}{w_0}$代入
$$
\begin{align}
f(t)_{2l} &= \frac{1}{2l} \sum_{n = -\infty}^{\infty} \int_{-l}^{l} f(\tau)_{2l} \, e^{-i w_n \tau} \, d\tau \, e ^{i w_n t} \\
&= \frac{2 \pi}{2l} * \frac{1}{2 \pi} \sum_{n = -\infty}^{\infty} \int_{-l}^{l} f(\tau)_{2l} \, e^{-i w_n \tau} \, d\tau \, e ^{i w_n t} \\
&= \frac{\pi}{l} * \frac{1}{2 \pi} \sum_{n = -\infty}^{\infty} \int_{-l}^{l} f(\tau)_{2l} \, e^{-i w_n \tau} \, d\tau \, e ^{i w_n t} \\
&= \triangle w * \frac{1}{2 \pi} \sum_{n = -\infty}^{\infty} \int_{-l}^{l} f(\tau)_{2l} \, e^{-i w_n \tau} \, d\tau \, e ^{i w_n t} \\
&= \frac{1}{2 \pi} \int_{-\infty}^{\infty} \int_{-l}^{l} f(\tau)_{2l} \, e^{-i w_n \tau} \, d\tau \, e ^{i w_n t} \, dw \\
&= \frac{1}{2 \pi} \int_{-\infty}^{\infty} \int_{-l}^{l} f(\tau)_{2l} \, e^{-i w_n \tau} \, d\tau \, e ^{i w_n t} \, dw \\
\end{align}
$$

又因为$\lim_{l \to \infty}$，$w_n$会趋于连续，因此有：
$$
\begin{align}
f(t) &= \frac{1}{2 \pi} \int_{-\infty}^{\infty} \int_{-l}^{l} f(\tau)_{2l} \, e^{-i w_n \tau} \, d\tau \, e ^{i w_n t} \, dw \\
&= \frac{1}{2 \pi} \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} f(\tau) \, e^{-i w \tau} \, d\tau \, e ^{i w t} \, dw \\
\end{align}
$$
上式称为傅里叶积分公式，其中间的积分为$F(w)$，即傅里叶变换：
$$
F(w) = \int_{-\infty}^{\infty} f(\tau) \, e^{-i w \tau} \, d\tau
$$
外边的积分为傅里叶反变换，即：
$$
f(t) = \frac{1}{2 \pi} \int_{-\infty}^{\infty} F(w) \, e ^{i w t} \, dw
$$

总结如下：
$$
\begin{cases}
f(t) = \frac{1}{2\pi} \int_{-\infty}^{+\infty} \int_{-\infty}^{+\infty} f(\tau) e^{-iw\tau} d\tau \, e^{iwt} dw, \quad 周期：\infty，中间的积分也即 F(w)\\
F(w) = \int_{-\infty}^{+\infty} f(t) e^{-iwt} dt, \quad 傅里叶变换(FT) \\
f(t) = \frac{1}{2\pi} \int_{-\infty}^{+\infty} F(w) e^{iwt} dw, \quad 傅里叶反变换(IFT)
\end{cases}
$$

对应傅里叶积分公式，给出傅里叶（Fourier）积分定理：
1. $f(t)$在任一有限区间上满足Dirichlet条件
2. $f(t)$在无限区间$(-\infty, \infty)$上绝对可积（即积分$\int_{-\infty}^{\infty}|f(t)|dt$收敛
则有：
$$
f(t) = \frac{1}{2 \pi} \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} f(\tau) \, e^{-i w_n \tau} \, d\tau \, e ^{i w_n t} \, dw \\
$$
成立，而左端的$f(t)$在他的间断点$t$处，应以$\frac{f(t + 0) +f(t - 0)}{2}$来代替。这个定理的条件是充分的，他的证明需要用到较多的理论基础，这里从略

## 傅里叶级数和傅里叶变换的区别与联系

1. 傅里叶级数对应的是周期信号，而傅立叶变换对应的是非周期信号
2. 傅里叶级数要求在一个周期内的能量是有限的，而傅立叶变换要求在整个周期内的能量是有限的
3. 傅里叶级数的系数是离散的，傅里叶变换是$w$的连续函数

由此可见，傅里叶级数与傅里叶变换的物理含义不同，量纲也不同，$X(j\Omega _0)$（傅里叶级数的系数）代表了周期信号$x(t)$第$k$次谐波幅度的大小，而$X(j\Omega)$（傅里叶变换的系数）是频谱密度的概念。为了说明这一点，我们可以将一个非周期信号视为周期$T$趋于无穷大的周期信号。由$\Omega _0 = \frac{2 \pi}{T}$可知，若$T \rightarrow \infty$，则必有$\Omega _0 \rightarrow 0$，$k \Omega _0 \rightarrow \Omega$，将傅里叶级数两边同乘上$T$(或$2l$)，并取$T \rightarrow \infty$时的极限，可得
$$
\lim_{T \to \infty} TX(k \Omega_0) = \lim_{\Omega_0 \to 0} \frac{2 \pi X(k \Omega_0)}{\Omega_0} = X(j\Omega)
$$
所以，从量纲上看，$X(j\Omega)$等于谐波幅度$X(k\Omega_0)$除以频率$\Omega_0$，显然，他是频谱密度的概念。

## 周期信号的傅里叶变换

先不考虑Dirichlet条件和能量有限的限制，直接求解周期信号的傅立叶变换。将傅里叶级数带入到傅里叶变换
$$
\begin{align}
F(w) &= \int_{-\infty}^{\infty} \left[ \frac{1}{2l} \sum_{n = -\infty}^{\infty} \int_{-l}^{l} f(\tau)_{2l} \, e^{-i \frac{n \pi \tau}{l}} \, d\tau \, e ^{i \frac{n \pi t}{l}} \right] \, e^{-i w t} \, dt \\
&= \int_{-\infty}^{\infty} \left[ \sum_{n = -\infty}^{\infty} C_n \, e ^{i \frac{n \pi t}{l}} \right] \, e^{-i w t} \, dt \\
&= \sum_{n = -\infty}^{\infty} C_n \, \int_{-\infty}^{\infty} \left[ e ^{i \frac{n \pi t}{l}} \right] \, e^{-i w t} \, dt \\
&= \sum_{n = -\infty}^{\infty} C_n \, \int_{-\infty}^{\infty} \left[ e ^{i w_n t} \right] \, e^{-i w t} \, dt \\
&= \sum_{n = -\infty}^{\infty} C_n \, \int_{-\infty}^{\infty} e ^{i w_n t} \, e^{-i w t} \, dt \\
&= \sum_{n = -\infty}^{\infty} C_n \, \int_{-\infty}^{\infty} \, e^{-i w t + i w_n t} \, dt \\
&= \sum_{n = -\infty}^{\infty} C_n \, \int_{-\infty}^{\infty} \, e^{i (w_n t - w t)} \, dt \\
\end{align}
$$
由积分：
$$
\int_{-\infty}^{\infty} e^{\pm jxy} dx = 2 \pi \delta(y)
$$
可得到周期信号傅立叶变换的表达式：
$$
F(w) = 2 \pi \sum_{k = -\infty}^{\infty} C_n \delta(w - w_n)
$$
上式表明，一个周期信号的傅立叶变换是由频率轴上间距为$w_0$的冲击序列(Drac函数)所组成，这些冲击序列的强度等于相应的傅立叶系数乘以$2\pi$。这样的离散频谱又称为“线谱”。由冲击函数的定义和频谱密度的物理概念可知，周期信号的频谱应理解为在无穷小的频率范围内取得了一个“无限大”的频谱密度。无限大是从冲击函数的角度来理解的。冲击函数的强度为$2\pi C_n$，单纯的从$C_n$来理解，它无密度的概念，它代表了在$w_n$出谐波的大小。

由此可以看出，本不具备傅里叶变换条件的周期信号，在引入了冲击信号后也可以做傅里叶变换。当然，变换的结果也应从冲击信号的角度来理解。这样由上式，我们就可以把傅里叶级数和傅里叶变换统一在一个理论框架下来进行讨论，并建立起二者的联系。

由上述的讨论，不难得出如下结论：时域连续的周期信号的傅里叶变换在频率是离散的、非周期的。

当$T\rightarrow\infty$时，上式中的离散频谱将变成连续谱，对应的是周期信号一个周期的傅里叶变换，但由于周期为无穷大，因此，他对应的实际上是非周期信号的傅里叶变换。由此可以得出结论：时域连续的非周期信号的傅里叶变换在频域上是连续的、非周期的。

## 傅立叶变换的进一步解释

傅里叶变换实际上是将信号$x(t)$和一组不同频率的复正弦作内积，即
$$
\begin{cases}
X(k\Omega_0) = <x(t), e^{jk\Omega_0t}> \quad 傅里叶级数 \\
X(k\Omega) = <x(t), e^{jk\Omega t}> \quad 傅里叶变换 \\
\end{cases}
$$
式中的复正弦即变换的基向量，而傅里叶系数或傅里叶变换是$x(t)$在这一组基向量上的投影。由于不同频率的正弦信号两两之间是正交的，因此傅里叶变换是正交变换。

将复杂信号分解为简单信号的组合是信号处理中最基本的方法，这样做一个是便于了解所要处理的信号的内涵，另一方面是便于提取信号的特征。那么傅里叶变换为什么要选择正弦信号作为分解的基向量呢？这是因为：
1. 正弦信号是最规则的信号，可由幅度、相位、频率这是哪个参数完全确定其时域波形。其频域也简单，只有一根谱线（复正弦）。将信号展开为正弦的组合，即可得到所有的谱线，从而得到信号的频谱分布。另外正弦信号处处可导，且有着无穷阶的导数，在信号处理的理论推导方面特别有用。为什么不选时域只取0和1的更简单的方波作为分解的基函数呢，因为但凡是信号在时域中有阶跃（或冲激）的成分，则都需要无穷多的频率成分才能合成这样的阶跃（或冲激）。另外方波的不可导也是一个重要原因。
2. 时间和频率是两个最重要也是最基本的物理量，而傅里叶变换正好把时间和频率联系了起来，使我们可以在时间和频率之间进行转换

## 拉普拉斯(Laplace)变换

### 拉普拉斯正变换

> ref：《积分变换》-- 东南大学数学系 张元林 编 P90

傅里叶变换的绝对可积的条件是比较强的，许多函数即使是很简单的函数（例如单位阶跃函数、正弦、余弦函数以及线性函数等）都不满足这个条件，其次可以进行Fourier变换的函数必须在整个数轴上有定义，但在物理、无线电技术等实际应用中，许多以$t$作为自变量的函数往往在$t < 0$时是无意义的或者是不需要考虑的，像这样的函数都不能区Fourier变换。这就使得Fourier变换的应用范围受到相当大的限制。

对于任意一个函数$\phi(t)$，能否经过适当的改造使其进行Fourier变换时克服上述两个缺点呢？这就使我们想到前面讲过的单位阶跃函数$u(t)$和指数衰减函数$e^{-\beta t}(\beta > 0)$所具有的特点，用前者乘上$\phi(t)$可以使积分区间由$(-\infty, \infty)$换成$[0, \infty)$，用后者称$\phi(t)$就有可能使其变成绝对可积，因此，为了克服Fourier变换上述哦两个缺点，自然会想到用$u(t)e^{-\beta t}(\beta > 0)$来乘$\phi(t)$，即：
$$\phi(t)u(t)e^{-\beta t}(\beta > 0)$$
结果发现，只要$\beta$选得适当，一般来说，这个函数的Fourier变换总是存在的。对函数$\phi(t)$进行先乘$u(t)e^{-\beta t}(\beta > 0)$，再取Fourier变换的运算，这样就产生了 Laplace 变换。

对函数$\phi(t)u(t)e^{-\beta t}(\beta > 0)$取Fourier变换，可得：
$$
\begin{align}
G_{\beta}(w) &= \int_{-\infty}^{\infty} \phi(t)u(t)e^{-\beta t}e^{-iwt}dt \\
&= \int_{0}^{\infty} f(t) e^{-(\beta + iw)t} \, dt \\
&= \int_{0}^{\infty} f(t) e^{-st} \, dt \\
\end{align}
$$
其中
$$s = \beta + iw, \quad f(t) = \phi(t)u(t)$$
若再设$F(s) = G_{\beta}(\frac{s - \beta}{i})$，则得：
$$
\begin{align}
F(s) &= G_{\beta}(\frac{s - \beta}{i}) \\
&= \int_{0}^{\infty} f(t) e^{-(\beta + i \frac{s - \beta}{i}) t} \, dt \\
&= \int_{0}^{\infty} f(t) e^{-s t} \, dt \\
\end{align}
$$
这一步只是为了把自变量$w$换成$s$，上式被称为Laplace变换。

**定义**：

设函数$f(t)$当$t \geq 0$时有定义，而且积分
$\int_{0}^{+\infty} f(t) e^{-st} dt (s是一个复参量)$
在复平面$s$得某一区域内收敛，由此积分所确定的函数记为：
$$
F(s) = \int_{0}^{+\infty} f(t) e^{-st} dt
$$
则称上式为函数$f(t)$得Laplace变换式


**Laplace变换的存在定理**：

1. 在$t \geq 0$的任一有限区间上连续或分段连续
2. 当$t \rightarrow {+\infty}$时，$f(t)$的增长速度不超过某一指数函数，亦即存在常数$M > 0$及$c \geq 0$，使得$|f(t)| \leq Me^{ct}, \quad 0 \leq t < +\infty$成立（满足此条件的函数，称他的增大是不超过指数级的，$c$为他的增长指数）
则$f(t)$的Laplace变换
$$
F(s) = \int_{0}^{+\infty} f(t) e^{-st} dt
$$
在半平面$Re(s) > c$上一定存在，有短的积分在$Re(s) \geq c > c$上绝对收敛而且一致收敛，并且在$Re(s) > c$的半平面内，$F(s)$为解析函数


### 拉普拉斯逆变换

由Laplace变换的概念可知，函数$f(t)$的Laplace变换，实际上就是$F(t)u(t)e^{-\beta t}$的Fourier变换。于是，当$f(t)u(t)e^{-\beta t}$满足Fourier积分定理的条件时，按Fourier积分公式，在$f(t)$连续点处有：
$$
\begin{align}
f(t)u(t)e^{-\beta t} &= \frac{1}{2\pi} \int_{-\infty}^{+\infty} \left[\int_{-\infty}^{+\infty} f(\tau) u(\tau) e^{-\beta \tau} e^{-iw\tau} d\tau \right] \, e^{iwt} dw \\
&= \frac{1}{2\pi} \int_{-\infty}^{+\infty} \, e^{iwt} dw \left[\int_{0}^{+\infty} f(\tau) u(\tau) e^{-(\beta + iw)\tau} d\tau \right] \\
&= \frac{1}{2\pi} \int_{-\infty}^{+\infty} \, F(\beta + iw) e^{iwt} dw, \quad (t > 0) \\
\end{align}
$$
等式两边同乘$e^{\beta t}$并考虑到他与积分变量$w$无关，则
$$
f(t) = \frac{1}{2\pi} \int_{-\infty}^{+\infty} \, F(\beta + iw) e^{(\beta + iw)t} dw, \quad (t > 0) \\
$$
令$\beta + iw = s(即 w = \frac{s - \beta}{i}$，则有
$$
\begin{align}
f(t) &= \frac{1}{2\pi} \int_{\beta - i\infty}^{\beta + i\infty} \, F(s) e^{st} \frac{d[s - \beta]}{i} \\
&= \frac{1}{2\pi i} \int_{\beta - i\infty}^{\beta + i\infty} \, F(s) e^{st} ds \quad (t > 0)
\end{align}
$$
上式右边则称为 Laplace 反演积分，或 反变换


## 关系

$$
\begin{align}
&Fourier Series \quad \overset{周期 \to \infty}{\longrightarrow} \quad \quad Fourier Transform \\
&Fourier Transform \quad \overset{两边乘上 u(t) e^{-\beta t}}{\longrightarrow} \quad \quad Laplace Transform \\
\end{align}
$$

# 离散变换

## Z变换

### 前备知识点

> ref: 《数字信号处理》胡广书 P10

#### 单位抽样信号
$$
\delta(n) =
\begin{cases}
1 \quad n = 0 \\
0 \quad n \neq 0 \\
\end{cases}
$$
$\delta(n)$又称Kronecker函数。该信号在离散信号与离散系统的分析与综合中有重要作用，其地位犹如单位冲激信号对于连续时间信号与连续时间系统。但$\delta(n)$和$\delta(t)$的定义不同。$\delta(t)$是建立在积分的定义上，即
$$
\int_{-\infty}^{\infty} \delta(t) dt = 1
$$
且$t \neq 0$时，$\delta(t) = 0$。$\delta(t)$表示在极短的时间内所产生的巨大“冲激”，而$\delta(n)$在$t=0$时定义为1。$\delta(t)$又称Dirac函数

#### 脉冲串序列$p(n)$

将$\delta(n)$在时间轴上延迟$k$个采样周期，得$\delta(n-k)$，则
$$
\delta(n) =
\begin{cases}
1 \quad n = k \\
0 \quad n \neq k \\
\end{cases}
$$
在上式中，若$k$从$-\infty$变到$+\infty$，那么$\delta(n)$的所有移位可形成一个无限长的脉冲串序列$p(n)$，即
$$
p(n) = \sum_{k = -\infty}^{\infty} \delta(n - k)
$$
如果移位的不是$\delta(n)$而是单位冲激信号$\delta(t)$，那么可以得到冲激串序列$p(t)$，即：
$$
p(t) = \sum_{-\infty}^{\infty} \delta(t - nT_s)
$$
若将连续信号$x(t)$与$p(t)$相乘，可得到离散信号$x(nT_s)$或$x(n)$，即：
$$
x(nT_s) = x(n) = x(t)p(t) = x(t)\sum_{-\infty}^{\infty} \delta(t - nT_s)
$$
之所以使用$p(t)$乘以$x(t)$得到离散信号，而不是用$p(n)$和$x(t)$相乘，是因为$p(t)$有着积分性质，便于对上式做进一步的数学讨论

![](./pic.assets/1.jpg)
![](./pic.assets/2.jpg)

#### 单位阶跃序列

$$
u(n) =
\begin{cases}
1 \quad n \geq 0 \\
0 \quad n < 0
\end{cases}
$$
若序列$y(n) = x(n)u(n)$，那么$y(n)$的自变量$n$的取值就限定在$n \geq 0$的有半轴上

#### 正弦序列

$$
x(n) = A\sin{(2 \pi fnT_s + \phi)}
$$
式中$f$是频率，单位为$Hz$，令$\Omega = 2 \pi f$，则$\Omega$的单位为$rad/s$，$\Omega$是相对连续信号$x(t)$的连续角频率变量，当$f$由$-\infty$增至$+\infty$时，$\Omega$也由$-\infty$增至$\infty$，令：
$$
w = 2 \pi f T_s = 2 \pi \frac{f}{f_s}, \, f_s = \frac{1}{T_s}
$$
$f_s$又称抽样频率。显然，当$f$由0增至$f_s$时，$w$由0增至$2 \pi$，当$f$由0减至$-f_s$时，$w$由0变为$-2\pi$，当$f$再增加或再减少$f_s$的整数倍时，$w$重复$0 \sim \pm 2\pi$。$w$的单位是$rad$，我们称$w$为圆周频率或圆频率，他是相对离散信号$x(n)$的频率变量。由前边两式可知，正弦信号可以表示为：
$$
x(n) = A \sin{(wn + \phi)}
$$

#### 复正弦序列

$$
x(n) = e^{jwn} = \cos{(wn)} + j \sin{(wn)}
$$
上式即欧拉公式等式。复正弦$e^{jwn}$在数字信号处理中有着重要的应用，他不但是离散信号作傅里叶变换时的基函数，同时也可作为离散系统的特征函数

#### 指数序列

$$
x(n) = a^{|n|}
$$
式中，$a$为常数且$|a| < 1$

如果$a$为复数，我们可将$a$写$a = r e^{jw_0}$的形式，式中$r > 0, w_0 \neq 0, \pi$，这样，$x(n)$变成复值信号，即 $x(n) = r^{|n|}e^{jw_0|n|}$。若$r < 1$，则$x(n)$为衰减的复正弦，其实部和虚部分别为衰减的实余弦和衰减的实正弦

### 推导过程(利用拉普拉斯变换)

> ref: 《数字信号处理》胡广书 P54

$Z$变换的定义可以从两个方面引出，一是直接对离散信号给出定义，二是由抽样信号的拉普拉斯变换过渡到$Z$变换

给定一个离散信号$x(n)$，$n = -\infty ~ +\infty$，可直接给出$x(n)$的$Z$变换的定义
$$
X(z) = \sum_{n = -\infty}^{\infty} x(n) z^{-n}
$$
式中$z$为一复变量。由于$x(n)$的存在范围是$(-\infty, \infty)$，所以上式定义的$Z$变换称为双边$Z$变换。如果$x(n)$的存在范围是$[0, +\infty)$，那么上式应变成单边$Z$变换，即
$$
X(z) = \sum_{n = 0}^{\infty} x(n) z^{-n}
$$
由于因果性信号及因果系统的抽样响应$h(n)$在$n < 0$时恒为零，因此实际的物理信号对应的都是单边$Z$变换。

从拉普拉斯变换过渡到$Z$变换：

设连续信号$x(t)$抽样得到$x_s(nT_s)$，即
$$
x_s(nT_s) = x(t) \sum_{n = -\infty}^{\infty} \delta(t - nT_s) = \sum_n x(nT_s) \delta(t - nT_s)
$$
现在对$x_s(nT_s)$取拉普拉斯变换，得：
$$
\begin{align}
X(s) &= \int_{-\infty}^{\infty} x_s(nT_s)e^{-st} \, dt \\
&= \int_{-\infty}^{\infty} \left[ \sum_n x(nT_s) \delta(t - nT_s) \right] e^{-st} \, dt \\
&= \sum_n x(nT_s) \int_{-\infty}^{\infty} \delta(t - nT_s) e^{-st} \, dt \\
&= \sum_n x(nT_s) e^{-snT_s} \\
&= X(e^{sT_s}) \\
\end{align}
$$

这里用到了脉冲信号的筛选性质，简单可以理解，对 $\int_{-\infty}^{\infty} \delta(t - nT_s) e^{-st} \, dt$积分，由于$\delta(t - nT_s)$是一个时间点的信号，因此可以认为积分区域内$e^{-st} = e^{-snT_s}$，作为一个常数。

令 $z = e^{sT_s}$，这样，$x_s(nT_s)$得拉普拉斯变换式就可以变成另一复变量$z$的变换式，再次将$T_s$归一化为1，即将$x(nT_s)$简记为$x(n)$，那么上式变为
$$
X(z) = \sum_{n = -\infty}^{\infty} x(n) z^{-n}
$$
这和前边直接给出的定义是一样的

计算$Z$变换的逆变换通常有三种方法：幂级数法、部分分式法、留数法，这里不做介绍，可参考 《数字信号处理》胡广书 P66

总结：
$$
x(t) \overset{采样}{\longrightarrow} x_s(nT_s) \overset{Laplace Trans}{\longrightarrow} X(s) \overset{z = e^{sT_s}}{\longrightarrow} X(z)
$$

### 推导过程_2(利用拉普拉斯变换)

欧拉公式：$e^{i\theta} = \cos(\theta) + i\sin(\theta)$

T为采样周期
$$e(t) \overset{采样}{\longrightarrow} e^*(t) = \sum_{n=0}^{\infty} e(nT) \delta(t-nT) $$

拉氏变换：
$$
E^*(s) = \int_{-\infty}^{\infty} e^*(t)e^{-st} dt \\
= \int_{-\infty}^{\infty}[\sum_{n=0}^{\infty} e(nT) \delta(t-nT)]e^{-st}dt \\
= \sum_{n=0}^{\infty} e(nT) [\int_{-\infty}^{\infty} \delta(t-nT)e^{-st}dt]
$$

由脉冲信号筛选性质：$\int_{-\infty}^{\infty} \delta(t-nT)f(t)dt=f(nT)$

故：$E^*(s) = \sum_{n=0}^{\infty} e(nT) e^{-nsT}$

令 $z = e^{sT}$ 得 $E(z) = E^*(s)|_{s=\frac{1}{T}ln(z)} = \sum_{n=0}^{\infty}e(nT)z^{-n}$


## 离散傅里叶变换(DTFT)

### 推导过程(利用傅里叶变换)

> ref: 《数字信号处理》胡广书 P55

对于连续时间周期信号$x(t)$，若要求其离散傅里叶变换，可将其与冲激串序列$p(t) = p(t) = \sum_{-\infty}^{\infty} \delta(t - nT_s)$ 相乘，然后做傅里叶变换

$$
\begin{align}
\mathcal{F}[x(t)p_{T_s}{t}] &= \int_{-\infty}^{\infty} x(t) \sum_{n = -\infty}^{+\infty} \delta(t - nT_s) \, e^{-jwt} dt \\
&= \sum_{n = -\infty}^{+\infty} \int_{-\infty}^{\infty} x(t) \delta(t - nT_s) \, e^{-jwt} dt \\
&= \sum_{n = -\infty}^{+\infty} \int_{-\infty}^{\infty} x(nT_s) \delta(t - nT_s) \, e^{-jwnT_s} dt \\
&= \sum_{n = -\infty}^{+\infty} x(nT_s) e^{-jwnT_s} \int_{-\infty}^{\infty} \delta(t - nT_s) \, dt \\
&= \sum_{n = -\infty}^{+\infty} x(nT_s) e^{-jwnT_s} \\
\end{align}
$$
令$\Omega = wT_s$，则
$$
\begin{align}
\mathcal{F}[x(t)p_{T_s}{t}] &= \sum_{n = -\infty}^{+\infty} x(nT_s) e^{-jwnT_s} \\
&= \sum_{n = -\infty}^{+\infty} x(nT_s) e^{-j\Omega n} \\
\end{align}
$$

### 推导过程_法2(利用z变换)

> ref: 《数字信号处理》胡广书 P55

拉普拉斯复变量$s = \rho + j \Omega$，式中$\Omega = 2 \pi f$，是相对连续系统及连续信号的角频率，单位为$rad/s$。由$z = e^{sT_s}$得：
$$
z = e^{sT_s} = e^{(\rho + j \Omega)T_s = e^{\rho T_s} e^{j\Omega T_s}}
$$
令：
$$
\begin{cases}
r = e^{\rho T_s} \\
w = \Omega T_s \\
\end{cases}
$$
则
$$
z = re^{jw}
$$
$w$是相对离散系统和离散信号得圆周频率，单位为$rad$。将上式代入$Z$变换得：
$$
X(z) = \sum_{n = -\infty}^{\infty} x(n) (re^{jw})^{-n} = \sum_{n = -\infty}^{\infty} \left[ x(n)r^{-n} \right] e^{-jwn}
$$
这一结果说明，只要$x(n)r^{-n}$符合绝对可和的收敛条件，即$\sum_{n = -\infty}^{\infty} \left| x(n)r^{-n} \right| < \infty$，则$x(n)$的$Z$变换存在。这样，一个序列$x(n)$的$Z$变换，又可看成是该序列乘以一实加权序列$r^{-n}$后的傅立叶变换，即：
$$
X(z) = \mathcal{F}[x(n)r^{-n}]e^{-jwn}
$$
如果$r = 1$，则：
$$
X(z) |_{z = e^{jw}} = X(e^{jw}) = \sum_{n = -\infty}^{\infty}x(n)e^{-jwn}
$$
这时$Z$变换就演变为离散序列的傅里叶变换(DTFT)

### 推导过程_法3(LSI系统的频率响应)

若另输入信号$x(n) = \delta(n)$，那么，这时的输出$y(n)$是由单位抽样信号$\delta(n)$激励该系统所产生的响应，因此，我们称这时的$y(n)$为系统的单位抽样响应，并记为$h(n)$。$h(n)$反映了系统的固有特征，他是离散系统的一个重要参数。

* **线性**

设一个离散系统对$x_1(n)$的响应是$y_1(n)$，对$x_2(n)$的响应是$y_2(n)$，即：
$$
\begin{align}
y_1(n) = T[x_1(n)] \\
y_2(n) = T[x_2(n)] \\
\end{align}
$$
若该系统对$\alpha x_1(n) + \beta x_2(n)$的响应是$\ahpha y_1(n) + \beta y_2(n)，即
$$
\begin{align}
y(n) &= T[\alpha x_1(n) \beta x_2(n)] \\
&= \alpha T[x_1(n)] + \beta T[x_2(n)] \\
&= \alpha y_1(n) + \beta y_2(n) \\
\end{align}
$$
那么，我们说该系统是线性的，式子中$\alpha$，$\beta$是任意常数。显然，线性的含义是指该系统的输入、输出之间满足叠加原理。

* **移不变性**

设一个离散时间系统对$x(n)$的响应是$y(n)$，如果将$x(n)$延迟了$k$个抽样周期，输出$y(n)$也相应的延迟了$k$个抽样周期，那么，我们说该系统具有移不变性，即
$$
\begin{align}
& T[x(n)] = y(n) \\
& T[x(n - k)] = y(n - k) \\
\end{align}
$$
该性质的含义还可以直观的解释为：对给定的输入，系统的输出和输入施加的时间无关。即不论何时加上输入，只要输入信号一样，输出信号的形态就保持不变


同时具有线性和移不变性的离散时间系统称为线性移不变（linear shift invariant，LSI）离散时间系统。除非特别说明，一般研究的对象都认为是LSI系统。

* **LSI系统输入和输出的关系**

一个连续的线性时不变系统，其输入$x(t)$和输出$y(t)$之间的关系可以用一个常系数线性微分方程来描述，它反映了该系统的动态特征。与之相似，一个线性移不变离散时间系统可以用一个常系数线性查分方程来描述，即
$$
y(n) = -\sum_{k = 1}^{N} a(k) y(n-k) + \sum_{r = 0}^{M} b(r)x(n-r)
$$
式中$a(k)$，$b(r)$是方程的系数，其中$k = 1, \dots, N$，而$r = 0, \dots, M$。给定输入信号$x(n)$及系统的初始条件，可求出该查分方程的解$y(n)$，从而得到系统的输出。现利用讨论过的结果来导出LSI系统输入、输出之间的一个重要关系，即线性卷积（linear convolution）。

输入信号$x(n)$可以表示为$\delta(n)$及其移位的线性组合，即
$$
\begin{align}
x(n) &= \sum_{k = -\infty}^{\infty} x(k) \delta(n - k) \\
&= \dots + x(-1) \delta(n+1) + x(0) \delta(n) + x(1) \delta(n-1) + \dots
\end{align}
$$

当输入是$\delta(n)$时，输出$y(n) = h(n)$，由系统的LSI性质可得如下输入输出关系

| 输入                 | 输出                                     |
| ------------------ | -------------------------------------- |
| $x(0)\delta(n)$    | $x(0)h(n)$                             |
| $x(1)\delta(n-1)$  | $x(1)h(n-1)$，$h(n-1)$对应输入$\delta(n-1)$ |
| $x(-1)\delta(n+1)$ | $x(-1)h(n+1)$                          |
| $\dots$            | $\dots$                                |
| $x(k)\delta(n-k)$  | $x(k)h(n=k)$                           |

这样，系统对$x(n)$的响应$y(n)$是上面右边一系列的相加，即
$$
y(n) = \sum_{k = -\infty}^{\infty} x(k) h(n - k)
$$
此式称为LSI系统的线性卷积，可简记为$y(n) = x(n) * h(n)$。很容易证明（对于特定的$n$，重要的是$x$和$h$的对关系，只要相乘的对应值是对的就可以，相加是所有乘积的和，所以相加其实不影响），上式也可以表示为：
$$
y(n) = \sum_{k = -\infty}^{\infty} h(k) x(n - k)
$$
并有如下运算性质：
$$
y(n) = \left[x_1(n) + x_2(n)\right] * h(n) = x_1(x) * h(n) + x_2(x) * h(n)
$$

若$h(n)$对应的是因果系统，即$n < 0$时$h(n) \equiv 0$，那么线性卷积的公式可以写为：
$$
y(n) = \sum_{k = 0}^{\infty} h(k) x(n - k)
$$


* **LSI系统的频率响应**

如果另输入$x(n) = e^{jwn}$，其中$w$称为圆周率，其单位为$rad$。由欧拉恒等式，有
$$
e^{jwn} = \cos(wn) + j\sin(wn)
$$
同理
$$
\cos(wn) = (e^{jwn} + e^{-jwn}) / 2，\sin(wn) = (e^{jwn} - e^{-jwn}) / j2
$$
因此，称$x(n)$是一个复正弦。由$x(n)$所引起的输出：
$$
\begin{align}
y(n) &= \sum_{k = -\infty}^{\infty} h(k) x(n-k) \\
&= \sum_{k = -\infty}^{\infty} h(k)e^{j(n-k)w} \\
&= e^{jwn} \sum_{k = -\infty}^{\infty} h(k) e^{-jwk} \\
&= e^{jwn}H(e^{jw})
\end{align}
$$
这表明，输出$y(n)$也包含了同频率的复正弦信号，但它将受到一个复值函数$H(e^{jw})$的调制。由于这一原因，称复正弦函数$e^{jwn}$为系统的特征函数。定义
$$
H(e^{jwn}) = \sum_{n = -\infty}^{\infty} h(n) e^{-jwn}
$$
为系统的频率响应，又称系统的特征值。上式实际上是离散序列$h(n)$的傅立叶变换(discrete time Fourier transform, DTFT)。式中$h(n)$是离散的，但$H(e^{jw})$是$w$的连续函数，由于$e^{jw} = e^{j(w + 2k\pi)}$，所以$H(e^{jw})$又是$w$的周期函数，周期为$2\pi$。$h(n)$体现了系统的时域特征，而$H(e^{jw})$体现了系统的频域特征。因为$H(e^{jw})$是复值函数，所以又可以表示为：
$$
\begin{align}
H(e^{jw}) &= H_R(e^{jw}) + jH_I(e^{jw}) \\
H(e^{jw}) &= |H(e^{jw})|e^{j\phi(w)} \\
\end{align}
$$
$H_R(e^{jw})$，$H_I(e^{jw})$分别是$H(e^{jw})$的实部和虚部，$|H(e^{jw})|$是其幅度，$\phi(w)$是其相位，分别称为系统的幅频响应和相频响应。他们之间的相互关系是：
$$
\begin{align}
|H(e^{jw})| &= \left[H_R^2(e^{jw}) + H_I^2(e^{jw})\right]^{1/2} \\
\phi(w) &= \arctan{\frac{H_R(e^{jw})}{H_I(e^{jw})}} \\
\end{align}
$$
若令$x(n) = \cos(wn) = Re(e^{jwn})$，$Re(*)$表示取实部，那么
$$
y(n) = Re\{e^{jwn} H(e^{jwn})\} = |H(e^{jw})|\cos[wn + \phi(w)]
$$
再一次可以看到，系统的输出含有和输入同频率的正弦，其幅度要乘以$|H(e^{jw})|$，而相位移了$\phi(w)$。

若定义$z = e^{jw}$，$z$也是一个复变量，那么系统的特征值又可以写为
$$
H(z) = \sum_{n = -\infty}^{\infty} h(n) z^{-n}
$$
该式称为$h(n)$的$Z$变换，$H(z)$是系统的转移函数。$h(n)$，$H(e^{jw})$及$H(z)$是描述一个LSI系统的三个重要函数

### DTFT逆变换

用$e^{jwm}$乘以$X(e^{jw}) = \sum_{n = -\infty}^{\infty} x(n) e^{-jwn}$的两边，并在$-\pi ~ +\pi$内对$w$积分，有：
$$
\begin{align}
\int_{-\pi}^{\pi} X(e^{jw}) e^{jwm} dw
&= \int_{-\pi}^{\pi} \left[ \sum_{n = -\infty}^{\infty} x(n) e^{-jwn} \right] e^{jwm} dw \\
&= \sum_{n = -\infty}^{\infty} x(n) \int_{-\pi}^{\pi} e^{jw(m - n)} dw
\end{align}
$$
由于$\int_{-\pi}^{\pi} e^{jw(m - n)}$是复正弦信号在$-\pi ~ + \pi$内的积分，且$m$，$n$为整数，所以，不论$m$，$n$如何取值，只有$m = n$时该积分才不为零，且积分值为$2\pi$，即
$$
\int_{-\pi}^{\pi} e^{jw(n - n)} dw = 2 \pi \delta(m - n)
$$
所以
$$
x(n) = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{jw}) e^{jwn} dw
$$
这也是DTFT的反变换公式。

### 其它

有其他认为重要的内容：

1. 信号截短对DTFT的影响：参考 : 《数字信号处理》胡广书 P114
2. 频谱的周期延拓：将连续信号$x_a(t)$经抽样变成$x(nTs)$后，$x(nT_s)$的频谱将变成周期的。相对频率$\Omega$，周期为$\Omega_s = 2\pi/T_s = 2\pi f_s$，相对圆周率$w$，周期为$2\pi$。变成周期的方法是将$X_a(j\Omega)$在频率轴上以$\Omega_s$为周期移位后再叠加，并除以$T_s$。这种现象又称为频谱的周期延拓。参考 : 《数字信号处理》胡广书 P119
3. 周期延拓的同时，可能会带来周期的混叠，更多内容参考 : 《数字信号处理》胡广书 P119

## 离散时间周期信号的傅里叶级数(DFS)

设$\tilde{x}(nT_s)$是周期信号$\tilde{x}(t)$的抽样，$\tilde{x}(t)$的周期为$T$，每个周期内抽N个点，即$T = NT_s$。这样，$\tilde{x}(nT_s)$也是周期的，周期为$NT_s$或$N$。由连续周期的傅立叶级数$x(t) = \sum_{k = -\infty}^{\infty} X(k\Omega_0) e^{jk\Omega_0t}$，将$\tilde{x}(t)$展成傅立叶级数，得
$$
\tilde{x}(t) = \sum_{k = -\infty}^{\infty} X(k\Omega_0) e^{jk\Omega_0t}
$$
$X(k\Omega_0)$是$\tilde{x}(t)$的傅立叶系数，所以他是离散的且是非周期的，式中$k = 0, \pm1, \dots, \pm\infty$，而$\Omega_0 = 2\pi / T = 2\pi / NT_s$。现对上式的$\tilde{x}(t)$抽样，得
$$
\begin{align}
\tilde{x}(nT_s) &= \tilde{x}(t)|_{t = nT_s} \\
&= \sum_{k} \tilde{X}(k\Omega_0)exp(jk \frac{2\pi}{NT_s} nT_s) \\
&= \sum_{k} \tilde{X}(k\Omega_0)exp(j \frac{2\pi}{N} nk) \\
\end{align}
$$
由之前的讨论可知，离散信号的频谱应该是周期的，周期为$\Omega_s$，所以上式中已将$X(k\Omega_0)$改记为$\tilde{X}(k\Omega_0)$。

由以下两式：
$$
\begin{align}
X(k\Omega_0) = \frac{1}{T} \int_{-T/2}^{T/2} x(t) e^{-jk\Omega_0 t} dt \\
X(n) = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{jw}) e^{jwn} dw \\
\end{align}
$$
可知，对周期信号的求和或者积分应在一个周期内进行，因此前边$\tilde{x}(nT_s)$，的求和也应在$X(k\Omega_0)$的一个周期内进行。现分析一下$X(k\Omega_0)$的周期是多少。

由于$\Omega_s = 2\pi/T_s = 2\pi N/T = N\Omega_0$，$\Omega_0$是$\tilde{x}(t)$的基波频率，因此，在$\tilde{X}(k\Omega_0)$的一个周期内应有$N$个点，也即其周期是$N$。取其一个周期，并简记为$X(k)$。又由于
$$
exp(j\frac{2\pi}{N}nk) = exp \left[ j\frac{2\pi}{N}n(k + lN) \right]
$$
式中$l$为任意整数，所以$\tilde{x}(nT_s)$可以表示为
$$
\tilde{x}(nT_s) = \sum_{k = 0}^{N - 1} X(k) exp(j\frac{2\pi}{N}nk)
$$
当$n = 0, 1, \dots , N - 1$和$n = N, \dots , 2N - 1$时，上式所求出的结果时一样的，即此式只能计算出$N$个$\tilde{x}(nT_s)$的值。这$N$个值即$\tilde{x}(nT_s)$的一个周期，记为$x(n), n = 0, 1, \dots , N - 1$。这样 上式左边的$\tilde{x}(nT_s)$可换成$x(nT_s)$。现对上式两边做如下运算：
$$
\begin{align}
\sum_{n = 0}^{N - 1} x(n) exp(-j \frac{2\pi}{N}ln) &= \sum_{n = 0}^{N - 1} \left[ \sum_{k = 0}^{N - 1} X(k) exp(j\frac{2\pi}{N}nk) \right] exp(-j\frac{2\pi}{N}nl ) \\
&= \sum_{k = 0}^{N - 1} X(k) \sum_{n = 0}^{N - 1} exp \left[j\frac{2\pi}{N}(k - l)n \right]
\end{align}
$$
由于
$$
\sum_{n = 0}^{N - 1} exp \left[j\frac{2\pi}{N}(k - l)n \right] =
\begin{cases}
N \quad \quad k - l = 0, N, 2N, \dots \\
0 \quad \quad 其它
\end{cases}
$$
故，上式的右边等于$NX(k)$，于是有
$$
X(k) = \frac{1}{N} \sum_{n = 0}^{N - 1} x(n) exp(-j \frac{2\pi}{N} nk)
$$
习惯上将定标因子$N$移到反变换中。这样，总结上述的讨论，对离散周期信号，可以得到如下两组变换式：
<一个周期>
$$
\begin{cases}
X(k) &= \sum_{n = 0}^{N - 1} x(n) exp(-j\frac{2\pi}{N}nk) \quad \quad \quad k = 0, 1, \dots, N - 1  \\
x(n) &= \frac{1}{N} \sum_{k = 0}^{N - 1} X(k) exp(j\frac{2\pi}{N}nk) \quad \quad n = 0, 1, \dots, N - 1 \\
\end{cases}
$$
和
<所有周期>
$$
\begin{cases}
\tilde{X}(k) &= \sum_{n = 0}^{N - 1} \tilde{x}(n) exp(-j\frac{2\pi}{N}nk) \quad \quad \quad k = -\infty \sim +\infty  \\
\tilde{x}(n) &= \frac{1}{N} \sum_{k = 0}^{N - 1} \tilde{X}(k) exp(j\frac{2\pi}{N}nk) \quad \quad n = -\infty \sim +\infty \\
\end{cases}
$$
上式称为离散周期序列的傅立叶级数（DFS），尽管式中标注的$n$，$k$都是从$-\infty$至$+\infty$，实际上，只能算出$N$个独立的值。DFS在时域、频域都是周期的，而且是离散的

## 离散傅里叶变换(DFT)

在计算机上实现信号的频谱分析及其他方面的处理工作时，对信号的要求是：在时域和频域都是离散的，而且是有限长，前边讲过的变换，只有DFS在时域和频域都是离散的，但$\tilde{x}(nT_s)$和$\tilde{X}(k\Omega_0)$都是无限长的。由于$exp(\pm j \frac{2\pi}{N} nk)$相对$n$和$k$都是以$N$为周期的，所以只要保证$\tilde{x}$是以$N$点为周期的，那么$\tilde{X}(k\Omega_0)$也是以$N$点为周期的。而且由$\tilde{X}(k\Omega_0)$在一个周期内取反变换得到的$\tilde{x}(nT_s)$也能保证是以$N$点为周期的。这一极好的性质导出DFS章节一个周期的DFS变换对，即DFT。对其重写则有：
$$
\begin{cases}
X(k) = \sum_{n = 0}^{N - 1} exp(-j\frac{2\pi}{N}nk) = \sum_{n = 0}^{N - 1} x(n) W_N^{nk} \quad \quad k = 0, 1, \dots, N - 1 \\
x(n) = \frac{1}{N} \sum_{k = 0}^{N - 1} X(k) exp(j \frac{2\pi}{N} nk) = \frac{1}{N}\sum_{k = 0}^{N - 1} X(k) W_N^{-nk} \quad \quad n = 0, 1, \dots, N - 1 \\
\end{cases}
$$
式中$x(n)$，$X(k)$分别是$\tilde{x}(nT_s)$和$\tilde{X}(k\Omega_0)$的一个周期，此处把$T_s$，$\Omega_0$都归一化为1；而$W_N = exp(-j\frac{2\pi}{N})$。DFT对应的是在时域、频域都是有限长，且又都是离散的一类变换。

显然DFT并不是一个新的傅立叶变换形式，实际上它来自于DFS，只不过仅在时域、频域各取一个周期而已。由这一个周期做延拓，可得到整个的$\tilde{x}(nT_s)$和$\tilde{X}(k\Omega_0)$。

在实际的工作中常常遇到的是非周期序列，他们可能是有限长，也可能是无限长，对这样的序列做傅立叶变换，理论上应是做DTFT，得到周期的连续频谱$X(e^{jw})$。然后$X(e^{jw})$不能直接在计算机上做数字运算，那么如何应用DFT变换求$x(n)$的傅立叶变换呢？具体做法如下：若$x(n)$是有限长序列，我们令其长度为$N$，若$x(n)$是无限长序列，我们是说$\tilde{x}(n)$是由$x(n)$做周期延拓所形成的。对$\tilde{x}(n)$，按所有周期的DFS，求变换，得到的$\tilde{X}(k)$也是以$N$为周期的序列，其一个周期为$X(k)$，$k = 0, 1, \dots, N - 1$。由DFS及DFT的导出过程可知，$X(k)$将是$x(n)$的傅立叶变换或是其傅立叶变换的某种程度上的近似。

这样对任意有限长序列$x(n)$，都可按照DFS变换在计算机上求其频谱。但需要记住，只要使用DFS的变换公式，不管$x(n)$本身是否来自周期序列，都应把他看作某一周期序列的一个周期。DFT的这一特点决定了他的许多特殊性质。


## 关系

$Z$变换与DTFT变换有着密切的联系，可以详细阅读前边的推导过程

四种形式的傅里叶变换：

|                       | 时域     |                                                                          | 频域     |                                                                                  |
| --------------------- | ------ | ------------------------------------------------------------------------ | ------ | -------------------------------------------------------------------------------- |
| FT(Fourier Transform) | 连续 非周期 | $X(j\Omega) = \int_{-\infty}^{\infty} x(t) e^{-j\Omega t}dt$             | 连续 非周期 | $x(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} X(j\Omega) e^{j\Omega t} d\Omega$ |
| FS(Fourier Series)    | 连续 周期  | $X(k\Omega_0) = \frac{1}{T} \int_{-T/2}^{T/2} x(t) e^{-jk\Omega_0 t} dt$ | 离散 非周期 | $x(t) = \sum_{k = -\infty}^{\infty} X(k\Omega_0) e^{jk\Omega_0 t}$               |
| DTFT                  | 离散 非周期 | $X(e^{jw}) = \sum_{n = -\infty}^{\infty} x(n) e^{-jwn}$                  | 连续 周期  | $x(n) = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{jw}) e^{jwn} dw$                   |
| DFS                   | 离散 周期  | $X(k) = \sum_{n = 0}^{N-1} x(n) e^{j \frac{2\pi}{N} nk}$                 | 离散 周期  | $x(n) = \frac{1}{N} \sum_{k = 0}^{N-1} X(k) e^{j \frac{2\pi}{N} nk}$             |
| DFT(取DFS的一个周期)        |        |                                                                          |        |                                                                                  |

由时域到频率的对应关系：

| 时域  | 频域  |
| --- | --- |
| 连续  | 非周期 |
| 离散  | 周期  |
| 非周期 | 连续  |
| 周期  | 离散  |
