# YumekoSleep

<h1 align="center">YumekoSleep</h1>
<h4 align="center">✨ 基于 GsCore 框架的日系鸣潮风格「入梦·苏醒」早晚安打卡娱乐插件 ✨</h4>

<div align="center">
  <a href="https://github.com/Genshin-bots/gsuid_core">早柚核心</a> &nbsp;·&nbsp;
  <a href="https://github.com/MimoKit/YumekoSleep/issues">问题反馈</a>
</div>

<br/>

## 丨安装提醒

> 该插件为 [早柚核心 (gsuid_core)](https://github.com/Genshin-bots/gsuid_core) 的扩展插件，必须先部署好 GsCore 框架才能使用。首次安装需重启 GsCore 才能完全应用。

<br/>

## 丨如何安装

进入 GsCore 插件目录并克隆本仓库：

```bash
cd gsuid_core/gsuid_core/plugins
git clone https://github.com/MimoKit/YumekoSleep YumekoSleep
```

重启 GsCore 即可自动加载并初始化数据表。

<br/>

## 丨指令列表

插件默认免前缀触发，支持在群聊或私聊直接使用：

| 指令 | 说明 |
| :--- | :--- |
| `晚安`、`睡觉啦`、`睡觉了`、`睡了`、`去睡了`、`安安`、`gn` | 记录入睡时间，发送鸣潮晚安寄语，并根据配置独立下发头像晚安表情包 |
| `早安`、`起床啦`、`起床了`、`醒了`、`早呀`、`早上好`、`gm` | 计算并播报睡眠时长与鸣潮早安寄语；若昨晚未打卡则进行友好提示 |

<br/>

## 丨功能特性

- **鸣潮风格寄语**：尊称用户为漂泊者，根据入梦打卡与苏醒时长动态匹配鸣潮世界观文案。
- **无定时器纯状态驱动**：不开启任何后台轮询计时任务，完全依托 GsCore 数据库时间戳比对计算。
- **本地系统时间自动换算**：底层记录精确标准时间，回复自动按部署机器当前系统时区输出年月日与时分秒。
- **同日入梦防重限制**：同一自然日内已打卡入睡的用户再次发送晚安将被拦截并提示，防止重复刷屏。
- **表情包联动支持**：可选对接 Meme Generator 服务的 `kurogames_good_night` 表情包，使用用户高清头像生成并独立发送。
- **Web 控制台支持**：基于 SQLModel 实现，自动在 GsCore 网页控制台注册管理面板。

<br/>

## 丨配置说明

插件支持在 GsCore 网页控制台的「插件配置」页面进行可视化配置，或直接修改插件目录下的 `config.json`：

| 配置项 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `EnableMeme` | `bool` | `true` | 是否在晚安时生成并发送头像表情包 |
| `MemeApiUrl` | `str` | `http://127.0.0.1:2235` | 表情包后端服务接口地址 |

<br/>

## 丨致谢与开源声明

- 感谢 [GsCore (早柚核心)](https://github.com/Genshin-bots/gsuid_core) 提供的机器人框架与底层支持。
- 感谢 [Meme-Generator](https://github.com/MeetWq/meme-generator) 提供的表情包生成支持。
- 本项目采用 **[GNU General Public License v3.0 (GPLv3)](./LICENSE)** 协议开源。
