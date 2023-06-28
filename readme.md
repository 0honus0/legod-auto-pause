# ·legod-auto-pause
雷神加速器时长自动暂停 docker 版本， 此为定时任务每天固定时间检查加速器是否暂停，没有暂停则自动暂停并发送推送信息(消息推送基于 https://github.com/Finb/Bark)


感谢 [@6yy66yy](https://github.com/6yy66yy) 无私提供的源码， 本项目基于 https://github.com/6yy66yy/legod-auto-pause 修改， 添加了dockerfile文件及优化了了一些代码

![image.png](https://s2.loli.net/2023/06/14/esAw4z1txnqpyO5.png)
![image.png](https://s2.loli.net/2023/06/14/hwTvfsIGEQZUXAK.png)

## 下载和教程
此项目部署到docker中，您可以修改文件并基于dockerfile本地编译，也可以使用在线拉取

1. 编译方式运行
```sh
git clone https://github.com/QuietBlade/legod-auto-pause.git
cd legod-auto-pause
docker build -t legod-auto-pause .
docker run -e UNAME=手机号 -e PASSWD=密码 legod-auto-pause:latest
# 第一次运行建议使用上面这行，确认无误之后 增加-d字段表示后台运行
docker run -d -e UNAME=手机号 -e PASSWD=密码 legod-auto-pause:latest
# 后台运行可以使用 docker logs 镜像代码 查看日志
```

2. 直接拉取运行

```sh
docker pull yuanzhangzcc/legod-auto-pause
docker run -d -e UNAME=手机号 -e PASSWD=密码 yuanzhangzcc/legod-auto-pause:latest
```

## 一、用前须知

此项目所有配置基于环境变量，请使用前务必设置为正确的信息

环境变量

| 变量名称 | 默认值 | 变量说明 | 
| -- | -- | -- |
|  TZ | `Asia/Shanghai` | docker时区设置，国内用户不建议更改 |
| TIME_STOP | `04:00` | 此变量为每日检查暂停的时间, 24小时制 |
| UNAME | Null | 账号/手机号，如果没有token则必填！ |
| PASSWD | Null | 密码，，如果没有token则必填！ |
| WEBHOOK |   | 消息推送服务，可以为空，使用Bark推送 |
| SLEEP | 3600 | 保活检测时间, 数字越小内存占用越大 |
| ACCOUNT_TOKEN |   | 账号token可以为空, 雷神官网查询 |

`token会过期，如果填入用户名密码会自动获取新的token`

### 消息推送

采用了bark消息推送，去brak申请地址，类似于 `https://api.day.app/xxxxxx/`
使用环境变量设置推送，建议为 `https://api.day.app/xxxxxx/雷神加速器/`

```
docker run -d -e WEBHOOK="https://api.day.app/xxxxxx/雷神加速器/" -e UNAME=手机号 -e PASSWD=密码 yuanzhangzcc/legod-auto-pause:latest
```


## 
本项目为仅为兴趣使然，边学边写，如有雷同，纯属巧合。
禁止商用！

    可以转载使用以及帮忙优化，发布时记得署名就好啦(●ˇ∀ˇ●)

## · 觉得好用给可以给原作者点个星星
https://github.com/6yy66yy/legod-auto-pause
