<h1 align="center">
JGM Automator
</h1>

<p align="center">
<img alt="GitHub" src="https://img.shields.io/github/license/Dwayneten/JGM-Automator"> <a href="https://github.com/Dwayneten/JGM-Automator/releases"><img alt="GitHub tag (latest by date)" src="https://img.shields.io/github/v/tag/Dwayneten/JGM-Automator"></a> <img alt="家国梦支持版本" src="https://img.shields.io/badge/%E5%AE%B6%E5%9B%BD%E6%A2%A6-1.3.0-brightgreen"> <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Dwayneten/JGM-Automator"> <a href="https://www.codacy.com/manual/Dwayneten/JGM-Automator?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Dwayneten/JGM-Automator&amp;utm_campaign=Badge_Grade"><img src="https://api.codacy.com/project/badge/Grade/7542a731c7e741d19ab60340d2016507"/></a>
</p>

> 该项目为`Python`编写的基于 OpenCV 模板匹配和 Tesseract 文字识别的《家国梦》游戏自动化脚本。

## 主要功能

- :moneybag:定时收取金币
- :package:自动运送货物
  - 指定运送货物的等级，可实现只给史诗建筑供货
- :building_construction:定时升级建筑
  - 只升级指定建筑列表，适用于有主要产出建筑的情景
- :building_construction:主动升级建筑
  - 升至 x 级
  - 升级 x 次
- :love_letter:极速开红包相册
- :steam_locomotive:自动重启游戏刷新火车
  - 仅限 QQ 账号登陆

## 特性
- 将硬编码部分配置文件化
- 支持配置文件的热加载
- 支持在命令行中以回车暂停/重启，以及优雅关闭，方便手动操作（如抽奖）
- 支持在命令行输入特定命令来主动执行某些操作

## 更新

### [`v1.1.1`](https://github.com/Dwayneten/JGM-Automator/releases/tag/v1.1.1)

- 增加新版本4个货物图片和配置

- 更新一些货物图片以提升识别率

### [`v1.1.0`](https://github.com/Dwayneten/JGM-Automator/releases/tag/v1.1.0)

- 极速开红包/相册 大幅提升开红包/相册的速度

- 增加输出总结信息的命令

- 现在重启游戏约一分钟后仍未成功进入游戏界面则中止脚本

- 修改了一下代码格式

## 计算器

:computer:计算家国梦建筑最优摆放策略

推荐 [lintx](https://github.com/lintx/) 写的 [家国梦计算器](https://lintx.github.io/jgm-calculator/index.html)

## 导航

- [安装与运行](#安装与运行)
  - [环境](#环境)
  - [依赖](#依赖)
  - [运行](#运行)
- [操作说明](#操作说明)
- [功能说明](#功能说明)
  - [主动升级建筑](#主动升级建筑)
  - [命令模式](#命令模式)
  - [自动开红包相册](#自动开红包相册)
- [开发说明](#开发说明)
- [开发计划](#开发计划)

## 安装与运行

### 环境

- [Python 3.7](https://www.python.org/downloads/)
- [ADB Kits](http://adbshell.com/downloads)
- [MuMu 模拟器](https://mumu.163.com/)

安装完后将`Python` 和 `ADB`的目录添加到系统环境变量`PATH`中，百度有教程

### 依赖

安装必须的 python 库

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple uiautomator2 opencv-python
```

如果需要使用以下命令则需要 [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) 并将其目录添加到系统环境变量`PATH`中

- `run upgrade_to x`

测试时使用的是`Tesseract OCR v5.0.0-alpha` [下载页面](https://github.com/UB-Mannheim/tesseract/wiki)

所有功能均在`Windows 10` `QQ 登陆` `MuMu 模拟器`的环境下测试

### 运行

```bash
# 打开 JGM-Automator 文件夹
# shift + 右键点空白处
# 选择“在此处打开 Powershell 窗口”或“在此处打开命令行窗口”
# 按以下步骤操作或输入命令

# 打开 MuMu 模拟器，确保屏幕大小为 1920（长） * 1080（宽）
# adb 连接
adb connect 127.0.0.1:7555

# 获取 device 名称,并填写至 main.py
# MuMu 模拟器忽略
adb devices

# 在已完成 adb 连接后，在手机安装 ATX 应用
# 此步骤仅第一次运行需要
python -m uiautomator2 init

# 按需求配置 config.json

# 打开模拟器中的 ATX ，点击“启动 UIAutomator”选项，确保 UIAutomator 是运行的。

# 进入游戏界面，启动自动脚本。
python main.py
```

## 操作说明

### 建筑位置编号
```bash
###7#8#9#
##4#5#6##
#1#2#3###
```

### 配置文件

- `config.json`

```JavaScript
{
  "swipe_interval_sec": 5,              // 收取金币最少间隔秒数
  "upgrade_interval_sec": 50,           // 升级建筑最少间隔秒数
  "building_pos": [
    ["零件厂", "人民石油", "企鹅机械"],
    ["商贸中心", "媒体之声", "民食斋"],
    ["花园洋房", "复兴公馆", "小型公寓"]
  ],                                    // 排布与游戏界面一致，修改为自己场上建筑名称
  "train_get_rank": [0, 1, 2]           // 要送货的货物品质 0-普通/1-稀有/2-史诗 只需送史诗则只留 [2]
  "debug_mode": false,                  // 调试模式 可无视
  "upgrade_building": true,             // 是否开启自动升级建筑 true/false
  "upgrade_building_list": [7, 9],      // 要升级的建筑位置编号 此例中先尝试升级 7 号再尝试升级 9 号
  "refresh_train": true,                // 是否开启自动刷新火车 true/false
  "detect_goods": true                  // 是否开启自动送货 每天送完货后可关闭 true/false
}
```

### 命令行操作  

```bash
# 启动
python main.py

# 暂停/重启（会有日志提示） 
[回车]

# 结束应用
end[回车]
```

以下命令均需暂停后输入才生效

```bash
# 进入命令模式
run command_mode on
# 退出命令模式
run command_mode off
# 将该建筑升至 x 级
run upgrade_to x
# 将该建筑升级 x 次
run upgrade_times x
# 开小/福气红包 x 次
run unpack s x
# 开中/多福红包 x 次
run unpack m x
# 开大/满福红包 x 次
run unpack l x
# 开相册 x 次
run album x
# 输出总结信息
run summary
```

## 功能说明

### 主动升级建筑

1. 脚本启动并正常运行后按回车进入暂停模式
2. 打开建筑中心并进入目标建筑的详细面板
   - 输入`run upgrade_to x`并回车将该建筑升至 x 级
   - 输入`run upgrade_times x`并回车将该建筑升级 x 次
3. 操作完成后将自动返回主界面并继续运行常规流程

### 命令模式

1. 脚本启动并正常运行后按回车进入暂停模式
2. 输入`run command_mode on` 进入暂停模式
3. 在命令模式下可以执行多次命令而不返回常规流程
4. 输入`run command_mode off` 退出暂停模式并返回游戏主界面

在需要对多个建筑进行升级时可以进入命令模式

例：主力建筑已经1000+级，想将其他建筑提升至925级以获取等级奖励

```bash
[回车]                // 进入暂停模式
run command_mode on  // 进入命令模式
// 手动在游戏内进入建筑中心并打开目标建筑的详细面板
run upgrade_to 925   // 将其升至 925 级 
// 等待升级完成后打开下一木匾建筑的详细面板
run upgrade_to 925   // 将其升至 925 级
// 升完想升的建筑后
run command_mode off // 退出命令模式自动返回主界面继续常规流程
```
### 自动开红包相册

1. 脚本启动并正常运行后按回车进入暂停模式
2. 打开商店面板
3. 输入`run unpack m x`自动开 x 个多福红包
4. 其他类型的红包或相册同样步骤

**注意**：为了保证开完一个红包会多点击几下，但不保证特殊情况下，如开满福红包三张卡都出史诗且三张卡同时升星时能点完这个红包

## 开发说明

- [Weditor](https://github.com/openatx/weditor)

我们可以使用 Weditor 工具，获取屏幕坐标，以及在线编写自动化脚本。

```bash
# 安装依赖
python -m pip install --pre weditor

# 启动 Weditor
python -m weditor
```

## 开发计划

- [ ] 自动升级所有建筑到 x 级以获取奖励

- [x] 开红包

- [x] 自动重启游戏刷新火车

- [ ] 供货阵容和产出阵容互换
