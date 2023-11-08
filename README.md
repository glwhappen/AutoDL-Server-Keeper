# AutoDL Server Keeper

这个仓库包含了一个 Python 脚本，它的作用是定期唤醒 [AutoDL](https://www.autodl.com/) 的服务器实例，以避免在不活跃14天后被自动销毁。

## 功能

- 定时触发服务器实例的电源操作，确保服务器不会因长时间不活跃而被销毁。
- 自动登录并发送 HTTP 请求来管理服务器电源状态。
- 日志记录每次操作的状态，便于追踪和调试。

## 使用方法

在开始使用之前，你需要配置几个环境变量。这些环境变量将用于脚本中，以确保你的认证信息安全。

创建一个 `.env` 文件，并填写你的 `AUTHORIZATION` token：

```plaintext
# .env 文件内容
AUTHORIZATION=你的认证token
```

**注意：** 切记不要将 `.env` 文件推送到你的公开仓库。

## 如何使用

1. 克隆此仓库到你的本地或服务器上。
2. 安装必要的依赖：

```bash
pip install -r requirements.txt
```


3. 运行 `main.py` 脚本：

```bash
python main.py
```

4. 脚本会开始按照预设的间隔时间唤醒和关闭指定的服务器实例。

## 配置

- 确保你的 `main.py` 文件中的 `headers` 和 `manage_power` 函数里的参数配置正确。
- 你可以修改调度器 `scheduler` 的时间间隔，来设置唤醒服务器的频率。


## 自动化保活工作流

为了防止 [AutoDL](https://www.autodl.com/) 服务器在不活跃14天后自动销毁，本仓库配置了一个自动化的 GitHub Actions 工作流，该工作流会定时执行一个简单的 Python 脚本来启动服务器。

### 工作流描述

- **名称**: AutoDL Keep Alive
- **触发时间**: 每天北京时间早上4点
- **工作流任务**:
  1. 检出仓库代码
  2. 设置 Python 环境
  3. 安装所需依赖
  4. 执行 `main.py` 中的 `change` 函数，触发服务器的启动和关闭操作

### 安全性说明

为了保护敏感信息，如 `authorization` 令牌，我们不将其直接存储在代码或工作流文件中。相反，我们使用 GitHub 仓库的 Secrets 功能来安全地存储并在工作流中引用这些值。

在创建了这个工作流文件之后，你需要在 GitHub 仓库的 Settings -> Secrets 部分添加名为 AUTHORIZATION 的 secret。这个 secret 应该包含你的授权令牌，它会在工作流运行时被设置为环境变量。

![](https://raw.githubusercontent.com/glwhappen/images/main/img/202311081933806.png)

## 安全和隐私

- 确保你的 `authorization` 令牌安全，不要公开在互联网上。
- 不要在任何地方公开你的个人密钥和敏感数据。

## 贡献

如果你有任何改进建议或功能请求，请创建一个 Issue 或者提交一个 Pull Request。
