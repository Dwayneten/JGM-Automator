# JGM Automator

> 这是基于 OpenCV 模板匹配的《家国梦》游戏自动化脚本。

## 安装与运行

```bash
# 安装依赖
python -m pip install uiautomator2 opencv

# adb 连接
# 使用 MuMu 模拟器，确保屏幕大小为 1920（长） * 1080（宽）
adb connect 127.0.0.1:7555

# 获取 device 名称,并填写至 main.py
adb devices

# 在已完成 adb 连接后，在手机安装 ATX 应用
python -m uiautomator2 init

# 打开 ATX ，点击“启动 UIAutomator”选项，确保 UIAutomator 是运行的。

# 进入游戏页面，启动自动脚本。
python main.py
```

## 定制
+ 修改火车货物对应的建筑：`prop.py` -> `BUILDING_2_GOODS` 
+ 新增火车货物：`target.py` & `target/`

## 新增特性
+ 定时升级房屋，策略：按照配置文件优先升级高星建筑的对应buff建筑
+ 将硬编码部分配置文件化
+ 支持配置文件的热加载
+ 支持在命令行中以回车暂停/重启，以及优雅关闭，方便手动操作（如抽奖）

## 说明

+ Weditor

我们可以使用 Weditor 工具，获取屏幕坐标，以及在线编写自动化脚本。

```bash
# 安装依赖
python -m pip install --pre weditor

# 启动 Weditor
python -m weditor
```

## 操作方法
+ 配置文件 - `config.json`
```json
{
  "swipe_interval_sec": 扫金币interval,
  "upgrade_interval_sec": 升级建筑interval,
  "upgrade_press_time_sec": 升级建筑时长按时间,
  "building_pos": [
    ["木材厂 4", "电厂 3", "钢铁厂 2"],
    ["便利店 3", "民食斋 1", "五金店 3"],
    ["钢结构房 4", "居民楼 3", "木屋 3"]
  ], // 排布与游戏界面一致，以"[建筑名称] [建筑星级]"为模版
  "train_get_rank": 火车货物收什么品质以上的(≥)，0-普通/1-稀有/2-史诗
}
```
+ 命令行操作  
`python3 main.py` 启动  
`[回车]` 暂停/重启（会有日志提示）  
`end[回车]` 结束应用  