# YumekoSleep

<p align="center">
  <a href="https://github.com/MimoKit/YumekoSleep"><img src="./ICON.png" width="160" alt="YumekoSleep ICON"></a>
</p>

<h1 align="center">YumekoSleep 0.1.0</h1>

<h4 align="center">✨基于<a href="https://github.com/Genshin-bots/gsuid_core" target="_blank">GsCore</a>的日系鸣潮风格「入梦·苏醒」早晚安打卡娱乐插件✨</h4>

<div align="center">
  <a href="https://docs.sayu-bot.com/" target="_blank">安装文档</a> &nbsp; · &nbsp;
  <a href="https://github.com/Genshin-bots/gsuid_core" target="_blank">gsuid_core</a> &nbsp; · &nbsp;
  <a href="https://github.com/MimoKit/YumekoSleep/issues" target="_blank">问题反馈</a>
</div>

<div align="center">
  <a href="https://count.getloli.com/"><img src="https://count.getloli.com/get/@YumekoSleep?theme=booru-lewd" alt="YumekoSleep 访问计数"></a>
</div>

<br/>

## 丨安装提醒

> **注意：该插件为 [早柚核心 (gsuid_core)](https://github.com/Genshin-bots/gsuid_core) 的扩展，具体安装方式可参考上方安装文档**
>
> **运行环境要求 Python `3.10+`**
>
> **如果是最新版本的 `gsuid_core`，可以直接对 bot 发送 `core安装插件YumekoSleep`，然后重启 Core 以应用安装**

<br/>

## 丨我该如何安装该插件？

- 前提：你已经部署好 [gsuid_core](https://github.com/Genshin-bots/gsuid_core)。
- 将本仓库克隆到 GsCore 插件目录并重启：

```bash
cd gsuid_core/gsuid_core/plugins
git clone https://github.com/MimoKit/YumekoSleep YumekoSleep
```

- 重启 GsCore 后插件自动加载并初始化数据表。

<br/>

## 丨指令列表

| 指令 | 说明 |
|------|------|
| `晚安`、`睡觉啦`、`睡觉了`、`睡了`、`去睡了`、`安安`、`gn` | 记录入睡时间，发送鸣潮晚安寄语，并根据配置独立下发头像晚安表情包 |
| `早安`、`起床啦`、`起床了`、`醒了`、`早呀`、`早上好`、`gm` | 计算并播报睡眠时长与鸣潮早安寄语；若昨晚未打卡则进行友好提示 |

<br/>

## 丨配置说明

可在 **GsCore 网页控制台**「插件配置」页面进行可视化配置，或直接修改插件目录下的 `config.json`：

| 配置项 | 类型 | 默认值 | 说明 |
|:---|:---|:---|:---|
| `EnableMeme` | `bool` | `true` | 是否在晚安时生成并发送头像表情包 |
| `MemeApiUrl` | `str` | `http://127.0.0.1:2235` | Meme Generator 服务的访问接口根地址 |

<br/>

## 丨使用限制

> [!CAUTION]
> 本项目仅供学习与交流使用，严禁用于任何商业用途。

<br/>

## Star History

<a href="https://www.star-history.com/?repos=MimoKit%2FYumekoSleep&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=MimoKit/YumekoSleep&type=date&theme=dark&legend=top-left&sealed_token=kYkSb6pkJH90d_uxGRTxHLowiWKuZa-t0m0cnPffvVAy71Y_KfjJ2LbGN0uE4m5ZFYTstQTonrMRxxwlimfwVZLNof1fhDDjUr1-4fKvVrZWTNFP2IJTuKrON1lBlIXYW-C02fNQ8k14QX0QXn_AOzxYXKDBQU2f1CIiPGkUcc-S8cojFrzKVJry3Mh3" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=MimoKit/YumekoSleep&type=date&legend=top-left&sealed_token=kYkSb6pkJH90d_uxGRTxHLowiWKuZa-t0m0cnPffvVAy71Y_KfjJ2LbGN0uE4m5ZFYTstQTonrMRxxwlimfwVZLNof1fhDDjUr1-4fKvVrZWTNFP2IJTuKrON1lBlIXYW-C02fNQ8k14QX0QXn_AOzxYXKDBQU2f1CIiPGkUcc-S8cojFrzKVJry3Mh3" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=MimoKit/YumekoSleep&type=date&legend=top-left&sealed_token=kYkSb6pkJH90d_uxGRTxHLowiWKuZa-t0m0cnPffvVAy71Y_KfjJ2LbGN0uE4m5ZFYTstQTonrMRxxwlimfwVZLNof1fhDDjUr1-4fKvVrZWTNFP2IJTuKrON1lBlIXYW-C02fNQ8k14QX0QXn_AOzxYXKDBQU2f1CIiPGkUcc-S8cojFrzKVJry3Mh3" />
 </picture>
</a>

<br/>

## 丨致谢

- [GsCore (早柚核心)](https://github.com/Genshin-bots/gsuid_core)
- [Meme-Generator](https://github.com/MeetWq/meme-generator)
- [Wuyi 无疑](https://github.com/KimigaiiWuyi)
- [fzmandy 伐竹猫](https://github.com/MeowAndy)
