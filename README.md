# JGM Automator

> 这是基于 OpenCV 模板匹配和 Tesseract 文字识别的《家国梦》游戏自动化脚本。

## 主要功能

- 定时收取金币
- 自动运送货物
  - 指定运送货物的等级，可实现只给史诗建筑供货
- 定时升级建筑
  - 策略1：按照配置文件优先升级高星建筑的对应buff建筑
  - 策略2：只升级指定建筑，适用于有主要产出建筑的情景
- :star:**New** 主动升级建筑
  - 升至 x 级
  - 升级 x 次
- :star:**New** 自动开红包/相册
- :star:**New** 自动重启游戏刷新火车
  - 配置文件已修改，请注意确认

## 新增特性
- 将硬编码部分配置文件化
- 支持配置文件的热加载
- 支持在命令行中以回车暂停/重启，以及优雅关闭，方便手动操作（如抽奖）
- 支持在命令行输入特定命令来主动执行某些操作

## 导航

- [安装与运行](#安装与运行)
  - [环境](#环境)
  - [依赖](#依赖)
  - [运行](#运行)
- [操作说明](#操作说明)
- [功能说明](#功能说明)
  - [主动升级建筑](#主动升级建筑)
  - [命令模式](#命令模式)
  - [自动开红包/相册](#自动开红包/相册)
- [开发说明](#开发说明)
- [开发计划](#开发计划)

## 安装与运行

### 环境

- [Python](https://www.python.org/downloads/)
- [ADB Kits](http://adbshell.com/downloads)
- [MuMu 模拟器](https://mumu.163.com/)

安装完后将`Python` 和 `ADB`的目录添加到系统环境变量`PATH`中，百度有教程

### 依赖

如果需要识别建筑等级则需要 Tesseract OCR 并将其目录添加到系统环境变量`PATH`中
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

```bash
# 安装依赖
python -m pip install uiautomator2 opencv-python
```

### 运行

```bash
# adb 连接
# 使用 MuMu 模拟器，确保屏幕大小为 1920（长） * 1080（宽）
adb connect 127.0.0.1:7555

# 获取 device 名称,并填写至 main.py
adb devices

# 在已完成 adb 连接后，在手机安装 ATX 应用
python -m uiautomator2 init

# 按需求配置 config.json

# 打开 ATX ，点击“启动 UIAutomator”选项，确保 UIAutomator 是运行的。
# 进入游戏页面，启动自动脚本。
python main.py
```

## 操作说明

- 建筑位置编号
```bash
###7#8#9#
##4#5#6##
#1#2#3###
```

+ 配置文件 - `config.json`

```JavaScript
{
  "swipe_interval_sec": 5,              // 收取金币间隔秒数
  "upgrade_interval_sec": 50,           // 升级建筑间隔秒数
  "upgrade_press_time_sec": 1,          // 升级建筑时长按升级按钮的秒数
  "upgrade_type_is_assign": true,       // 为 true 时只自动升级指定位置的建筑
  "assigned_building_pos": 7,           // 指定自动升级建筑的位置
  "building_pos": [
    ["木材厂 4", "电厂 3", "钢铁厂 2"],
    ["便利店 3", "民食斋 1", "五金店 3"],
    ["钢结构房 4", "居民楼 3", "木屋 3"]
  ],                                    // 排布与游戏界面一致，以"[建筑名称] [建筑星级]"为模版
  "train_get_rank": [0, 1, 2]           // 要送货的货物品质 0-普通/1-稀有/2-史诗 只需送史诗则只留 [2]
  "debug_mode": false,                  // 调试模式 可无视
  "refresh_train": true,                // 是否开启自动刷新火车 true/false
  "detect_goods": true                  // 是否开启自动送货 每天送完货后可关闭 true/false
}
```

+ 命令行操作  

```bash
# 启动
python3 main.py

# 暂停/重启（会有日志提示） 
[回车]

# 结束应用
end[回车]
```

以下命令均需暂停后输入才生效

- 进入命令模式

`run command_mode on`

- 退出命令模式

`run command_mode off`

- 将该建筑升至 x 级

`run upgrade_to x`

- 将该建筑升级 x 次

`run upgrade_times x`

- 开小/福气红包 x 次

`run unpack s x`

- 开中/多福红包 x 次

`run unpack m x`

- 开大/满福红包 x 次

`run unpack l x`

- 开相册 x 次

`run album x`


## 功能说明

### 主动升级建筑

1. 脚本启动并正常运行后按回车进入暂停模式
1. 打开建筑中心并进入目标建筑的详细面板
   - 输入`run upgrade_to x`并回车将该建筑升至 x 级
   - 输入`run upgrade_times x`并回车将该建筑升级 x 次
1. 操作完成后将自动返回主界面并继续运行常规流程

### 命令模式

1. 脚本启动并正常运行后按回车进入暂停模式
1. 输入`run command_mode on` 进入暂停模式
1. 在命令模式下可以执行多次命令而不返回常规流程
1. 输入`run command_mode off` 退出暂停模式并返回游戏主界面

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
### 自动开红包/相册

1. 脚本启动并正常运行后按回车进入暂停模式
1. 打开商店面板
1. 输入`run unpack m x`自动开 x 个多福红包
1. 其他类型的红包或相册同样步骤

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
