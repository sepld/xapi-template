# X API 发帖程序

这是一个简单的Python程序，使用X API（原Twitter API）发布帖子。

## 前提条件

1. 你需要拥有X开发者账号并创建一个应用
2. 申请适当的API访问级别（Free, Basic, Pro或Enterprise）
3. 获取必要的OAuth凭证：
   - Consumer Key和Consumer Secret（应用凭证）
   - Access Token和Access Token Secret（用户凭证）

## 关于X API身份验证

X API的发布帖子功能只支持以下身份验证方式：
- OAuth 1.0a User Context（用户上下文）
- OAuth 2.0 User Context（用户上下文）

本程序使用OAuth 1.0a User Context进行身份验证，这是X API V2推荐的认证方式，提供更好的安全性和更现代的认证流程。

## 安装

1. 克隆此代码库
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
3. 配置认证信息（见下文）

## 使用方法

### 设置认证信息

通过环境变量提供OAuth凭证：

1. 复制环境变量模板文件：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入你的OAuth凭证：
   ```
   X_CONSUMER_KEY=你的应用Consumer Key
   X_CONSUMER_SECRET=你的应用Consumer Secret
   X_ACCESS_TOKEN=你的账户Access Token
   X_ACCESS_TOKEN_SECRET=你的账户Access Token Secret
   ```

### 运行程序

使用以下命令发布帖子：

```
python x_post.py --text "你的帖子内容" [--debug]
```

参数说明：
- `--text` 或 `-t`: 帖子内容
- `--debug` 或 `-d`: 启用调试模式，显示更详细的日志

### 调试工具

遇到认证问题时，可以使用以下工具进行诊断：

```
python debug_auth.py
```

这个工具会尝试获取当前用户信息，可以帮助检查OAuth认证是否正确配置。

## 获取OAuth凭证

1. 前往X开发者平台(https://developer.x.com)创建或登录账号
2. 创建一个项目和应用
3. 在应用设置页面中，找到"Keys and Tokens"标签
4. 生成Consumer Keys和Access Tokens
5. 确保你的应用有写入权限（Write）

## X API访问级别

根据X API文档，发布帖子的能力在不同访问级别有不同的限制：

- **Free**：仅限写操作和测试，应用级别限制每月500帖子
- **Basic**：用户级别限制每月3,000帖子，应用级别限制每月50,000帖子
- **Pro**：应用级别限制每月300,000帖子
- **Enterprise**：商业级访问，根据具体需求定制

## 常见问题

1. **401 Unauthorized错误**：
   - 检查OAuth凭证是否正确
   - 确认Access Token没有过期
   - 运行debug_auth.py诊断认证问题

2. **403 Forbidden错误**：
   - 确认你的应用有足够的权限
   - 确认OAuth类型正确（需要User Context）
   - 检查应用是否符合X的政策

## 注意事项

1. 确保遵守X的开发者政策和使用条款
2. 请妥善保管你的OAuth凭证，不要将其提交到公共代码库中
3. 根据[X API文档](https://docs.x.com/x-api/introduction)了解更多信息

## 进一步改进

这是一个基础实现，你可以根据需要扩展功能，例如：
- 添加媒体上传
- 实现线程回复
- 添加转发功能
- 集成用户查询等功能 