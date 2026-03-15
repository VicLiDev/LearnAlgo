# 齐次坐标

欧氏空间（或者笛卡尔空间）描述2D/3D几何非常适合，但是这种方法却不适合处理透视空间
的问题（实际上，欧氏几何是透视几何的一个子集合）。

齐次坐标系：简而言之，齐次坐标系就是用$N+1$维来代表$N$维坐标，我们可以在2维笛卡尔
坐标末尾加上一个额外的变量$w$来形成$2D$齐次坐标，因此，一个点$(X,Y)$在齐次坐标里
变成了$(x,y,w)$，并且有$X = x/w$，$Y = y/w$。  
例如：笛卡尔坐标系下的$(1, 2)$的齐次坐标可以表示为$(1, 2, 1)$。如果$(1, 2)$移动到
无穷远处，在笛卡尔坐标下它变为$(-\infty, \infty)$，然后他的齐次坐标为$(1, 2, 0)$，
因为$(1 / 0, 2 / 0) = (-\infty, \infty)$，我们就可以不用“$\infty$“来表示一个无穷远
的点了

为何称为齐次坐标系？
我们把齐次坐标转化为笛卡尔坐标的方法是前$n-1$个坐标分量分别除以最后一个分量即可，
观察一下转化：
$$
\begin{align}
(1, 2, 3) \quad &\longrightarrow \quad (\frac{1}{3}, \frac{2}{3}) \\
(2, 4, 6) \quad &\longrightarrow \quad (\frac{2}{6}, \frac{4}{6}) = (\frac{1}{3}, \frac{2}{3}) \\
(4, 8, 12) \quad &\longrightarrow \quad (\frac{4}{12}, \frac{8}{12}) = (\frac{1}{3}, \frac{2}{3}) \\
... \quad \quad &\longrightarrow \quad \quad ... \\
(1a, 2a, 3a) \quad &\longrightarrow \quad (\frac{1a}{3a}, \frac{2a}{3a}) = (\frac{1}{3}, \frac{2}{3}) \\
\end{align}
$$
观察可知：这些点是齐次的，因为它们代表了笛卡尔坐标系里面的同一个点，换句话说，
齐次坐标有规模不变性。

齐次坐标的作用：
在笛卡尔坐标系中，同一平面的两条相互平行的直线永不相交，但却无法体现透视关系，
在齐次坐标系中可以体现透视关系，除此之外，齐次坐标在进行平移变换时，可以将加法
（在笛卡尔坐标系中平移一个向量是用相加的形式）转化为乘法。

证明：两条平行直线可以相交
考虑如下方程组：
$$
\begin{cases}
Ax + By + C = 0 \\
Ax + By + D = 0 \\
\end{cases}
$$
我们知道在笛卡尔坐标系里，该方程无解，因为$C \neq D$，如果$C = D$，两条直线就相同了

而在透视空间里，用齐次坐标$x/w$，$y/w$代替$x$，$y$
$$
\begin{cases}
A\frac{x}{w} + B\frac{y}{w} + C = 0 \\
A\frac{x}{w} + B\frac{y}{w} + D = 0 \\
\end{cases}

\longrightarrow

\begin{cases}
Ax + By + Cw = 0 \\
Ax + By + Dw = 0 \\
\end{cases}
$$
现在我们有一个解，$(x, y , 0)$两条直线相交于$(x, y, 0)$，这个点在无穷远处


# 坐标变换

$v' = Av$，其中$A$为变换矩阵，$v$为原始坐标。$v'$为变换后的坐标

平移：原始坐标$(x, y)$    平移量$(T_x, T_y)$    目标坐标$(x', y')$
$$
\left[
\begin{matrix}
x' \\
y' \\
1 \\
\end{matrix}
\right]
=
\left[
\begin{matrix}
1 & 0 & T_x \\
0 & 1 & T_y \\
0 & 0 & 1 \\
\end{matrix}
\right]
\left[
\begin{matrix}
x \\
y \\
1 \\
\end{matrix}
\right]
\quad
(齐次坐标形式)
$$

$$
\left[
\begin{matrix}
x' \\
y' \\
\end{matrix}
\right]
=
\left[
\begin{matrix}
x \\
y \\
\end{matrix}
\right]
+
\left[
\begin{matrix}
T_x \\
T_y \\
\end{matrix}
\right]
\quad
(笛卡尔坐标形式)
$$
缩放：原始坐标$(x, y)$    缩放量$(S_x, S_y)$    目标坐标$(x', y')$

$$
\left[
\begin{matrix}
x' \\
y' \\
1 \\
\end{matrix}
\right]
=
\left[
\begin{matrix}
S_x & 0 & 0 \\
0 & S_y & 0 \\
0 & 0 & 1 \\
\end{matrix}
\right]
\left[
\begin{matrix}
x \\
y \\
1 \\
\end{matrix}
\right]
$$

2D旋转：原始坐标$(x, y)$    旋转量$\theta$    目标坐. $(x', y')$

$$
\left[
\begin{matrix}
x' \\
y' \\
1 \\
\end{matrix}
\right]
=
\left[
\begin{matrix}
\cos{\theta} & \sin{\theta} & 0 \\
-\sin{\theta} & \cos{\theta} & 0 \\
0 & 0 & 1 \\
\end{matrix}
\right]
\left[
\begin{matrix}
x \\
y \\
1 \\
\end{matrix}
\right]
\quad
(顺时针旋转)
$$
证明：
![](./pic/1.excalidraw.md)

逆时针旋转：
$$
\begin{cases}
x' = r \cos{(\alpha + \beta)} = r \cos{\alpha} \cos{\beta} - r \sin{\alpha} \sin{\beta} \\
y' = r \sin{(\alpha + \beta)} = r \sin{\alpha} \cos{\beta} + r \sin{\beta} \cos{\alpha} \\
\end{cases}
$$
又因：
$$
\begin{cases}
x = r \cos{\beta} \\
y = r \sin{\beta} \\
\end{cases}
$$
所以：
$$
\begin{cases}
x' = x \cos{\alpha} - y \sin{\alpha} \\
y' = x \sin{\alpha} + y \cos{\alpha} \\
\end{cases}
$$

顺时针旋转：
$$
\begin{cases}
x' = r \cos{(\beta - \alpha)} = r \cos{\beta} \cos{\alpha} + r \sin{\beta} \sin{\alpha} \\
y' = r \sin{(\beta - \alpha)} = r \sin{\beta} \cos{\alpha} - r \sin{\alpha} \cos{\beta} \\
\end{cases}
$$
又因：
$$
\begin{cases}
x = r \cos{\beta} \\
y = r \sin{\beta} \\
\end{cases}
$$
所以：
$$
\begin{cases}
x' = x \cos{\alpha} + y \sin{\alpha} \\
y' = - x \sin{\alpha} + y \cos{\alpha} \\
\end{cases}
$$


3D旋转：在三维空间中，旋转可以围绕任意轴进行。但为简单起见，我们通常讨论围绕
x、y 或 z 轴的旋转。

- **绕 Z 轴旋转 $\theta$ 角度**：
$$
\begin{pmatrix}
x' \\
y' \\
z' \\
\end{pmatrix}
=
\begin{pmatrix}
\cos \theta & -\sin \theta & 0 \\
\sin \theta & \cos \theta & 0 \\
0 & 0 & 1 \\
\end{pmatrix}
\begin{pmatrix}
x \\
y \\
z \\
\end{pmatrix}
$$

- **绕 Y 轴旋转 $\theta$ 角度**：
$$
\begin{pmatrix}
x' \\
y' \\
z' \\
\end{pmatrix}
=
\begin{pmatrix}
\cos \theta & 0 & \sin \theta \\
0 & 1 & 0 \\
-\sin \theta & 0 & \cos \theta \\
\end{pmatrix}
\begin{pmatrix}
x \\
y \\
z \\
\end{pmatrix}
$$

- **绕 X 轴旋转 $\theta$ 角度**：
$$
\begin{pmatrix}
x' \\
y' \\
z' \\
\end{pmatrix}
=
\begin{pmatrix}
1 & 0 & 0 \\
0 & \cos \theta & -\sin \theta \\
0 & \sin \theta & \cos \theta \\
\end{pmatrix}
\begin{pmatrix}
x \\
y \\
z \\
\end{pmatrix}
$$

在进行三维坐标变换时，经常会用到欧拉角，欧拉角是一种基于三种较简单旋转运动
（称为俯仰、滚动、偏航）创建一般旋转的机制，想象驾驶飞机前进：
* 俯仰角：以飞机翅膀为轴（一般朝右边，作为z轴），绕z轴滚动，称为俯仰角
* 滚动角：以飞机前进方向为轴（一般朝前边，作为x轴），绕x轴旋转，称为滚动角
* 偏航角：垂直地面穿过飞机为轴（一般朝上，作为y轴），绕y轴旋转，称为偏航角


# 坐标系变换的原理详解

坐标系变换的核心是**描述一个坐标系（局部坐标系）如何通过平移、旋转、缩放等操作，
映射到另一个坐标系（世界坐标系）**。齐次坐标和变换矩阵是实现这一过程的数学工具。
以下是分步原理说明：

使用齐次坐标的作用：
- 统一平移、旋转、缩放为矩阵乘法。
- 区分点和向量（点的 $w=1$，向量的 $w=0$）。

坐标系变换的数学表达：  
设世界坐标系为 $A$，局部坐标系为 $B$。  
坐标系 $B$的基向量和原点在 $A$ 中的表示，可以通过一个齐次变换矩阵 $M_{A\to B}$ 描述：

$$\mathbf{P}_A = M_{A\to B} \cdot \mathbf{P}_B$$

其中：
- $\mathbf{P}_B$ 是点在 $B$ 中的坐标。
- $\mathbf{P}_A$ 是点在 $A$ 中的坐标。
- $M_{A\to B}$ 是 $4 \times 4$ 的齐次变换矩阵。

变换矩阵的分解：
变换矩阵 $M$ 可分解为平移 $T$、旋转 $R$、缩放 $S$ 的组合：

$M = T \cdot R \cdot S$

这里的平移、旋转、缩放矩阵，如前文所述


**变换顺序的重要性**  
矩阵乘法不满足交换律，因此变换顺序直接影响结果：  
- **先旋转后平移**：旋转局部坐标系的基向量，再移动原点。  
  $M = T \cdot R$
- **先平移后旋转**：会以世界坐标系的原点为中心旋转，导致非预期结果。


# 世界坐标系/相机坐标系/图像坐标系/像素坐标系

## 坐标系转换概述

1. **世界坐标系（World Coordinate System, WCS）**：这是一个三维的、绝对的坐标系，
   用于描述物体在真实世界中的位置。
2. **相机坐标系（Camera Coordinate System, CCS）**：这也是一个三维坐标系，但其
   原点位于相机的光心，Z轴与相机的光轴重合，X轴和Y轴分别与图像平面的两边平行。
3. **图像坐标系（Image Coordinate System, ICS）**：这是一个二维坐标系，其原点
   位于图像平面的中心（通常是光轴与图像平面的交点），X轴和Y轴分别与图像的两个
   边平行。
4. **像素坐标系（Pixel Coordinate System, PCS）**：这是一个二维的、以像素为单位的
   坐标系，其原点位于图像的左上角，X轴和Y轴分别与图像的列和行平行。

## 转换关系

- **世界坐标系到相机坐标系**：通过旋转矩阵R和平移向量t进行转换。
- **相机坐标系到图像坐标系**：利用透视投影进行转换，通常使用相机的内参矩阵K（包括
  焦距和光心位置）。
- **图像坐标系到像素坐标系**：通过缩放和平移进行转换，这通常是一个简单的线性变换。
