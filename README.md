# Antirattan / 反藤甲

Antirattan 是一款简单便捷的分函数代码查重工具，适用于函数较多（如 DS 题）的分函数查重。

目前支持 Windows 和 Linux（在 NOI Linux（Ubuntu 的一个衍生版本）经过测试），尚不明确是否支持其他操作系统。

## 安装依赖(Windows)

首先你需要安装 MinGW 和 Python，并且将其放到环境变量中。

然后在命令行，项目文件目录下运行：

```
mingw32-make install
```

运行命令时请保证网络畅通。

## 安装依赖(Linux)

首先你需要安装 G++,Make 和 Python 3。在 NOI Linux 中默认都安装了。

然后在命令行，项目文件目录下运行：

```
make install_linux
```

运行命令时请保证网络畅通。

## 使用

在 `1.cpp` 中放置题解，在 `2.cpp` 中放置待判断的代码，在 `1.in` 中放置一组数据输入（尽可能大，如果过小可能重复率会偏大）。

尽量格式化 `1.cpp` 和 `2.cpp` 以提高准确率。

然后运行下面的命令以查看报告：

**Windows**

```
mingw32-make run
```

**Linux**

```
make run_linux
```

运行命令时请保证网络畅通，程序需要访问 Compiler Exploer 以获取简化后的汇编代码信息。

报告中，列表示 `1.cpp` 中的函数，行表示 `2.cpp` 中的函数。可以通过命令行输出的颜色来判断抄袭的可能性。

## 原理

首先通过 Compiler Exploer 分离函数代码，然后计算出第 $i$ 个函数与第 $j$ 个函数之间的汇编代码相似度（使用 Jaccard 算法） $a_{i,j}$。

然后通过 gcov 找出每一行执行次数，然后计算出第 $i$ 个函数与第 $j$ 个函数之间代码的执行次数的 LCS 与平均长度之比 $b_{i,j}$。

然后 $i,j$ 两函数的答案为 $0.8b_{i,j}+0.2a_{i,j}$。
