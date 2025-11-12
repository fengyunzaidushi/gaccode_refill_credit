# GitHub Actions 自动化部署指南

## 📋 目录

- [功能概述](#功能概述)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [运行时间](#运行时间)
- [测试工作流](#测试工作流)
- [故障排查](#故障排查)

---

## 🎯 功能概述

GitHub Actions 工作流每天自动运行积分重置脚本，并通过邮件发送通知。

### 特性

- ⏰ **定时执行**：每天北京时间 23:57 自动运行
- 📧 **邮件通知**：成功/失败/Token 刷新自动发送邮件
- 🔐 **安全存储**：敏感信息使用 GitHub Secrets 保护
- 🔄 **手动触发**：支持手动运行工作流
- 📝 **日志记录**：保留 7 天的执行日志

---

## 🚀 快速开始

### 步骤 1: 配置 GitHub Secrets

进入您的 GitHub 仓库：

**Settings → Secrets and variables → Actions → New repository secret**

添加以下 Secrets：

| Secret 名称      | 说明                     | 示例值               |
| ---------------- | ------------------------ | -------------------- |
| `GAC_AUTH_TOKEN` | GAC 认证 token（可为空） | `eyJhbGciOi...`      |
| `GAC_EMAIL`      | GAC 账号邮箱             | `your_email@163.com` |
| `GAC_PASSWORD`   | GAC 账号密码             | `your_password`      |
| `SMTP_SERVER`    | SMTP 服务器              | `smtp.163.com`       |
| `SMTP_PORT`      | SMTP 端口                | `465`                |
| `SMTP_USER`      | SMTP 用户名              | `your_email@163.com` |
| `SMTP_PASSWORD`  | SMTP 授权码              | `BWOQWYCZNFQFVNAZ`   |
| `FROM_EMAIL`     | 发件邮箱                 | `your_email@163.com` |
| `TO_EMAIL`       | 收件邮箱                 | `your_email@163.com` |

### 步骤 2: 启用工作流

1. 提交工作流文件到仓库
2. 进入仓库的 **Actions** 标签
3. 如果显示"Workflows aren't being run"，点击启用

### 步骤 3: 手动测试

1. 进入 **Actions** 标签
2. 选择 **GAC 自动重置积分** 工作流
3. 点击 **Run workflow** → **Run workflow**
4. 查看执行结果

---

## 🔧 配置说明

### GitHub Secrets 详细说明

#### 1. GAC 账号配置

```
GAC_AUTH_TOKEN: 可以留空，脚本会自动登录获取
GAC_EMAIL:      您的gaccode.com邮箱
GAC_PASSWORD:   您的gaccode.com密码
```

#### 2. 邮件配置（163 邮箱示例）

```
SMTP_SERVER:    smtp.163.com
SMTP_PORT:      465
SMTP_USER:      your_email@163.com
SMTP_PASSWORD:  授权码（不是登录密码！）
FROM_EMAIL:     your_email@163.com
TO_EMAIL:       your_email@163.com
```

**获取 163 邮箱授权码：**

1. 登录 163 邮箱
2. 设置 → POP3/SMTP/IMAP
3. 开启 SMTP 服务
4. 生成授权码（16 位）

#### 3. Gmail 配置

```
SMTP_SERVER:    smtp.gmail.com
SMTP_PORT:      587
SMTP_USER:      your_email@gmail.com
SMTP_PASSWORD:  应用专用密码（16位）
FROM_EMAIL:     your_email@gmail.com
TO_EMAIL:       your_email@gmail.com
```

**获取 Gmail 应用专用密码：**

1. 访问 https://myaccount.google.com/security
2. 启用两步验证
3. 生成应用专用密码

---

## ⏰ 运行时间

### 默认时间

- **北京时间**：每天 23:57
- **UTC 时间**：每天 15:57
- **Cron 表达式**：`57 15 * * *`

### 时间转换参考

| 北京时间  | UTC 时间  | Cron 表达式       |
| --------- | --------- | ----------------- |
| 08:00     | 00:00     | `0 0 * * *`       |
| 12:00     | 04:00     | `0 4 * * *`       |
| 18:00     | 10:00     | `0 10 * * *`      |
| 23:00     | 15:00     | `0 15 * * *`      |
| **23:57** | **15:57** | **`57 15 * * *`** |

### 修改运行时间

编辑 `.github/workflows/auto-reset-credits.yml`：

```yaml
schedule:
  - cron: "57 15 * * *" # 修改这里
```

**公式：** 北京时间 - 8 小时 = UTC 时间

---

## 🧪 测试工作流

### 方法 1: 手动触发

1. 进入仓库的 **Actions** 标签
2. 选择 **GAC 自动重置积分**
3. 点击 **Run workflow**
4. 选择分支并运行

### 方法 2: 推送代码触发

添加 push 触发器（仅用于测试）：

```yaml
on:
  push:
    branches: [main]
  schedule:
    - cron: "57 15 * * *"
  workflow_dispatch:
```

**注意：** 测试完成后记得删除 push 触发器！

---

## 📧 邮件通知说明

### 自动发送的邮件

工作流会在以下情况发送邮件：

1. **脚本内置通知**（来自脚本）：

   - ❌ 重置失败
   - 🔄 Token 刷新
   - ⚠️ 订阅异常
   - 🌐 网络错误

2. **GitHub Actions 失败通知**（来自工作流）：
   - ❌ 工作流执行失败
   - 包含日志链接

### 邮件示例

**成功邮件（脚本发送）：**

```
主题: [GAC积分重置工具] 积分重置成功 ✅
内容: 积分已成功重置！
```

**失败邮件（工作流发送）：**

```
主题: [GAC积分重置工具] ❌ GitHub Actions 执行失败
内容: GitHub Actions 任务执行失败！
      请检查详细日志: [链接]
```

---

## 🔍 查看执行日志

### 在线查看

1. 进入 **Actions** 标签
2. 选择对应的工作流运行记录
3. 点击查看各步骤的详细日志

### 下载日志

1. 进入工作流运行记录
2. 滚动到底部
3. 下载 **reset-logs-[运行 ID]** 附件

---

## ❓ 故障排查

### 问题 1: 工作流未运行

**症状：**

- 定时任务未触发
- Actions 标签无记录

**解决方案：**

1. 确认工作流文件路径正确：`.github/workflows/auto-reset-credits.yml`
2. 检查仓库是否启用了 Actions
3. 确认分支是默认分支（main/master）
4. GitHub Actions 可能延迟 5-10 分钟

### 问题 2: Secrets 未生效

**症状：**

```
[ERROR] Email and password are required
```

**解决方案：**

1. 检查 Secrets 名称是否完全一致（区分大小写）
2. 重新创建 Secrets
3. 确认 Secrets 在正确的仓库中

### 问题 3: 邮件发送失败

**症状：**

```
[ERROR] Failed to send email: SMTPAuthenticationError
```

**解决方案：**

1. 确认使用的是授权码，不是登录密码
2. 检查 SMTP 服务器和端口是否正确
3. 163 邮箱确认 SMTP 服务已开启

### 问题 4: 今日已重置

**症状：**

```
[INFO] ⚠️  Already reset today!
```

**解决方案：**

- 这是正常情况，说明今天已经重置过了
- 脚本会自动跳过，等待明天再运行
- 无需手动处理

### 问题 5: Token 过期

**症状：**

```
[WARNING] Token appears to be invalid (401 Unauthorized)
```

**解决方案：**

- 脚本会自动重新登录获取新 token
- 检查 GAC_EMAIL 和 GAC_PASSWORD 是否正确
- 新 token 会自动保存（但不会更新到 Secrets）

---

## 🔐 安全最佳实践

### 1. 保护 Secrets

- ✅ 使用 GitHub Secrets 存储敏感信息
- ✅ 定期更换密码和授权码
- ❌ 不要在代码中硬编码密码
- ❌ 不要在公共仓库使用真实凭证

### 2. 限制权限

```yaml
permissions:
  contents: read # 只读权限
```

### 3. 私有仓库

建议将包含自动化脚本的仓库设为私有：

- Settings → Danger Zone → Change visibility → Make private

### 4. 清理临时文件

工作流会自动清理生成的配置文件：

```yaml
- name: 清理敏感配置文件
  if: always()
  run: rm -f config_github_actions.json
```

---

## 📊 工作流执行流程

```
定时触发 (23:57 北京时间)
    ↓
检查代码
    ↓
安装 Python 3.11
    ↓
安装依赖 (requests)
    ↓
创建临时配置文件 (使用Secrets)
    ↓
运行积分重置脚本
    ├─ 成功：脚本发送成功邮件 (如果配置)
    └─ 失败：发送失败邮件
    ↓
清理临时配置文件
    ↓
上传日志 (保留7天)
    ↓
完成 ✅
```

---

## 🎓 高级配置

### 1. 仅工作日运行

```yaml
schedule:
  - cron: "57 15 * * 1-5" # 周一到周五
```

### 2. 多次运行

```yaml
schedule:
  - cron: "57 15 * * *" # 23:57
  - cron: "0 12 * * *" # 20:00
```

### 3. 添加通知到其他渠道

在工作流中添加额外的通知步骤：

```yaml
- name: 发送企业微信通知
  if: failure()
  run: |
    curl -X POST "https://qyapi.weixin.qq.com/..." \
      -d '{"msgtype":"text","text":{"content":"积分重置失败"}}'
```

### 4. 条件执行

```yaml
- name: 运行积分重置
  if: github.event_name == 'schedule' # 仅定时触发时运行
  run: python auto_reset_credits_advanced.py
```

---

## 📝 工作流文件说明

### 文件结构

```
.github/
├── workflows/
│   └── auto-reset-credits.yml    # 工作流定义
└── config.json.example            # 配置示例
```

### 关键步骤

| 步骤        | 说明                | 失败处理   |
| ----------- | ------------------- | ---------- |
| 检查代码    | 拉取最新代码        | 终止工作流 |
| 安装 Python | 设置 Python 环境    | 终止工作流 |
| 安装依赖    | 安装 requests 库    | 终止工作流 |
| 创建配置    | 从 Secrets 生成配置 | 终止工作流 |
| 运行脚本    | 执行重置逻辑        | 继续执行   |
| 清理文件    | 删除敏感配置        | 始终执行   |
| 发送邮件    | 失败时通知          | 仅失败时   |
| 上传日志    | 保存执行记录        | 始终执行   |

---

## 💡 常见问题

### Q1: 为什么选择 23:57 而不是 00:00？

**A:** 避开高峰期：

- 00:00 是常见的定时任务时间
- GitHub Actions 可能延迟
- 23:57 确保在当天结束前执行

### Q2: 工作流会消耗多少 GitHub Actions 时间？

**A:** 每次运行约 1-2 分钟：

- 免费账户：2000 分钟/月
- 每天运行：约 30-60 分钟/月
- 完全够用 ✅

### Q3: 可以在私有仓库使用吗？

**A:** 可以：

- 私有仓库也支持 GitHub Actions
- 但会消耗私有仓库的 Actions 时间配额

### Q4: 如何禁用自动运行？

**A:** 三种方法：

1. 删除 `.github/workflows/auto-reset-credits.yml`
2. 在 Actions 标签禁用工作流
3. 注释掉 schedule 部分

### Q5: 收不到邮件怎么办？

**A:** 检查以下几点：

1. 查看工作流日志确认是否发送
2. 检查垃圾邮件文件夹
3. 确认邮箱配置正确
4. 测试 SMTP 连接

---

## 🔄 更新工作流

### 更新步骤

1. 修改 `.github/workflows/auto-reset-credits.yml`
2. 提交并推送到仓库
3. 工作流自动更新，无需额外操作

### 版本管理

建议在提交信息中注明版本：

```bash
git add .github/workflows/auto-reset-credits.yml
git commit -m "Update workflow: add email retry logic (v1.0.1)"
git push
```

---

## 📞 获取帮助

### 相关文档

- `EMAIL_NOTIFICATION_GUIDE.md` - 邮件通知配置
- `AUTO_LOGIN_GUIDE.md` - 自动登录功能
- `QUICKSTART.md` - 快速开始
- [GitHub Actions 文档](https://docs.github.com/en/actions)

### 调试技巧

1. **启用详细日志**

```yaml
- name: 运行积分重置
  run: python auto_reset_credits_advanced.py --config config_github_actions.json
  env:
    ACTIONS_STEP_DEBUG: true
```

2. **输出调试信息**

```yaml
- name: 调试信息
  run: |
    echo "Python版本: $(python --version)"
    echo "工作目录: $(pwd)"
    echo "文件列表: $(ls -la)"
```

---

**版本：** v1.0.0  
**更新日期：** 2025-11-12  
**状态：** ✅ 已测试

---

**享受自动化带来的便利！** 🚀
