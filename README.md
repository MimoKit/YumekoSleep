# YumekoSleep (梦境沉沦)

<p align="center">
  <img src="https://img.shields.io/badge/GsCore-Plugin-6b8afd?style=flat-square" alt="GsCore Plugin">
  <img src="https://img.shields.io/badge/Python-3.9+-3776ab?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/License-GPLv3-yellow?style=flat-square" alt="License">
</p>

<h1 align="center">🌙 YumekoSleep 梦境沉沦</h1>
<h4 align="center">✨ 基于 GsCore 框架的日系鸣潮风格「入梦·苏醒」早晚安打卡娱乐插件 ✨</h4>

<div align="center">
  <a href="https://github.com/Genshin-bots/gsuid_core">早柚核心 (GsCore)</a> &nbsp;·&nbsp;
  <a href="#丨指令说明">指令列表</a> &nbsp;·&nbsp;
  <a href="#丨配置说明">配置项</a> &nbsp;·&nbsp;
  <a href="#丨表情包集成">表情包后端</a>
</div>

<br/>

## 丨关于 YumekoSleep

> 「潮水退去，繁星低垂。卸下一整天在索拉里斯奔波的疲惫，漂泊者，今夜请安心入梦。」

**YumekoSleep** 是为 [GsCore (早柚核心)](https://github.com/Genshin-bots/gsuid_core) 量身定制的高性能、纯状态驱动的日系早晚安打卡插件。

- 🌊 **鸣潮沉浸式体验**：尊称用户为漂泊者，融合索拉里斯、流云、今汐、黑石平原与潮汐回响等丰富唯美寄语。
- ⏳ **无定时器轻量设计**：拒绝在后台启动轮询定时器与垃圾计时线程，完全由数据库精确时间戳驱动，零后台开销。
- 🌏 **双轨时区精准转换**：底层严格记录标准 UTC 国际时标，输出时自动感知部署机器系统时区，人性化输出年月日与时分秒。
- 🛡️ **每日入梦防刷锁**：同一自然日内打卡晚安后智能锁定，禁止贪睡重刷，防误触防刷屏。
- 🖼️ **鸣潮表情包联动**：无缝对接 `meme-generator` 后端，晚安时自动拾取用户高清头像独立下发 `kurogames_good_night` 晚安专属表情包。
- 📊 **Web 控制台即插即用**：基于 SQLModel 驱动，内置 GsAdminModel 控制台模型，支持在 GsCore 网页控制台实时检索用户打卡档案。

<br/>

## 丨安装部署

> [!NOTE]
> 本插件必须配合 [早柚核心 (gsuid_core)](https://github.com/Genshin-bots/gsuid_core) 框架运行，首次添加需重启 GsCore 即可自动建表并加载。

### 克隆安装
进入你的 GsCore 插件目录并克隆本仓库：

```bash
cd gsuid_core/gsuid_core/plugins
git clone https://github.com/MimoKit/YumekoSleep YumekoSleep
```

重启 GsCore，插件即会自动完成：
1. 注册 `[梦境沉沦/早晚安记录]` 业务服务
2. 创建 `goodnightrecord` 数据表与唯一索引
3. 挂载 Web 控制台管理卡片

<br/>

## 丨指令说明

触发前缀已设置为免前缀，直接在群聊或私聊中发送以下任意触发词即可：

| 功能 | 触发指令 | 触发说明 |
| :--- | :--- | :--- |
| **打卡入梦** | `晚安`、`睡觉啦`、`睡觉了`、`睡了`、`去睡了`、`安安`、`gn` | 记录入睡时间，回复鸣潮晚安寄语，并独立发送用户头像生成的晚安表情包 |
| **打卡苏醒** | `早安`、`起床啦`、`起床了`、`醒了`、`早呀`、`早上好`、`gm` | 计算并播报睡眠总时长，根据睡眠时间匹配鸣潮寄语；未打卡晚安则贴心提示 |

<br/>

## 丨文案赏析

### 🌙 晚安打卡
> **晚安，漂泊者～**  
> 今夜声骸平息，愿你的梦境如今汐大人的流云般宁静。  
> 入睡时间：2026年09月04日 23:30:15  
> *(随后单独发送一张带有漂泊者头像的鸣潮晚安表情包)*

### ☀️ 早安打卡
- **充实睡眠（4 ~ 11 小时）**：
  > **早安，漂泊者！**  
  > 你一共睡了 8小时15分钟。  
  > 清晨的潮汐带来全新的回响，今天的冒险也要全力以赴哦～  
  > 起床时间：2026年09月05日 07:45:30  
- **熬夜小猫（< 4 小时）**：
  > 才睡了这么一会儿呀，漂泊者要注意休息，别太勉强自己哦！
- **梦境长眠（> 11 小时）**：
  > 哇，睡了这么久，是陷入了时间的声骸回溯里了吗～
- **未曾入梦（无晚安记录）**：
  > 早上好，漂泊者！新的一天也要元气满满哦～昨晚没有找到你的入睡打卡记录呢。

<br/>

## 丨配置说明

在 GsCore 网页控制台的「插件配置」面板，或修改插件目录下的 `config.json`：

| 配置项键名 | 默认值 | 类型 | 说明 |
| :--- | :--- | :--- | :--- |
| `EnableMeme` | `true` | `bool` | 是否在晚安时生成并发送专属头像表情包 |
| `MemeApiUrl` | `http://127.0.0.1:2235` | `str` | Meme Generator 服务的访问接口根地址 |

<br/>

## 丨表情包集成

本插件原生适配 [meme-generator](https://github.com/MeetWq/meme-generator) 服务：
- **目标表情包 Key**：`kurogames_good_night`
- **支持接入方式**：
  - 本地直连：`http://127.0.0.1:2235`
  - 远程反代（推荐配置域名+SSL）：`https://meme.yourdomain.com:2234`
- 表情包将直接提取用户的当前高清头像（自动兼容 QQ 头像与平台头像），生成失败会自动降级仅发文本，不阻塞正常对话。

<br/>

## 丨致谢与开源协议

- 感谢 [GsCore (早柚核心)](https://github.com/Genshin-bots/gsuid_core) 框架提供的生态与基础设施支持。
- 感谢 [Meme-Generator](https://github.com/MeetWq/meme-generator) 提供的表情包渲染能力。
- 本项目采用 **[GNU General Public License v3.0 (GPLv3)](./LICENSE)** 协议开源。
