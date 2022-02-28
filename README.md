# vector_tools
自己写的一些 QGIS 矢量处理函数（processing algorithms）

## 安装
- 下载 zip 文件到本地，然后在 QGIS 中打开 `插件 -> 管理并安装插件 -> 从 ZIP 文件安装`

或者：

- 下载 zip 文件再解压缩到 QGIS 插件目录

## v0.1
创建第一个 "CreateLinksFromAPointLayer" 函数, 该函数输入一个 Point/MultiPoint 图层, 并按顺序在每两个点之间创建一条线段, 输出 LineString

![](/img/CreateLinksFromAPointLayer.png)