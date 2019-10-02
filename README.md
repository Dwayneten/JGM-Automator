# JGM Automator

> 这是基于 OpenCV 模板匹配和 Tesseract 文字识别的《家国梦》游戏自动化脚本。

## 主要功能

+ 定时收取金币
+ 自动运送货物
  * 指定运送货物的等级，可实现只给史诗建筑供货
+ 定时升级建筑
  * 策略1：按照配置文件优先升级高星建筑的对应buff建筑
  * 策略2：只升级指定建筑，适用于有主要产出建筑的情景

## 新增特性
+ 将硬编码部分配置文件化
+ 支持配置文件的热加载
+ 支持在命令行中以回车暂停/重启，以及优雅关闭，方便手动操作（如抽奖）
+ 修改火车货物对应的建筑：`prop.py` -> `BUILDING_2_GOODS` 
+ 新增火车货物：`target.py` & `target/`

## 导航

- [安装与运行](#安装与运行)
  * [环境](#环境)
  * [依赖](#依赖)
  * [运行](#运行)
- [操作说明](#操作说明)
- [开发说明](#开发说明)

## 安装与运行

### 环境

- [Python](https://www.python.org/downloads/)
- [ADB Kits](http://adbshell.com/downloads)
- [MuMu 模拟器](https://mumu.163.com/)

### 依赖

如果需要识别建筑等级则需要 Tesseract OCR
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

```bash
# 安装依赖
python -m pip install uiautomator2 opencv
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
+ 建筑位置编号
```
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
  "train_get_rank": 2                   // 自动供货的货物品质下限(包含) 0-普通/1-稀有/2-史诗
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

## 开发说明

+ Weditor

我们可以使用 Weditor 工具，获取屏幕坐标，以及在线编写自动化脚本。

```bash
# 安装依赖
python -m pip install --pre weditor

# 启动 Weditor
python -m weditor
```
