# 版本更新说明 v1.2.2

## 🎉 新功能概述

本次更新（v1.2.2）添加了**邮件通知功能**，让您及时了解积分重置状态，无需手动检查日志。

---

## ✨ 主要更新

### 1. 邮件通知功能 📧

**智能邮件提醒，重要事件不错过**

脚本现在可以在关键事件发生时自动发送邮件通知：

- ✅ **重置成功** - 确认积分已重置
- ❌ **重置失败** - 及时发现问题
- 🔄 **Token刷新** - 了解认证状态
- ⚠️ **订阅异常** - 提醒续费
- 🌐 **网络错误** - 避免重复提交

#### 支持的邮件服务商

- Gmail
- 163邮箱
- QQ邮箱
- Outlook/Hotmail
- 其他支持SMTP的邮箱

#### 灵活的通知策略

可以单独控制每种场景是否发送邮件：

```json
{
  "on_failure": true,        // 失败时通知（推荐）
  "on_success": false,       // 成功时通知（可选）
  "on_token_refresh": true   // Token刷新时通知（推荐）
}
```

### 2. 邮件测试功能 🧪

**一键测试邮件配置**

新增命令行参数 `--test-email`，快速验证邮件配置：

```bash
python auto_reset_credits_advanced.py --test-email
```

测试邮件会包含：
- 当前积分信息
- 配置文件路径
- 测试时间戳

---

## 🔧 配置说明

### 完整配置示例

```json
{
  "auth_token": "",
  "email": "your_email@example.com",
  "password": "your_password",
  "base_url": "https://gaccode.com/api",
  "ticket_config": {
    "category_id": 3,
    "title": "重置积分",
    "description": "",
    "language": "zh"
  },
  "retry_config": {
    "max_retries": 3,
    "retry_delay": 2
  },
  "email_alerts": {
    "enabled": false,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "your_email@gmail.com",
    "smtp_password": "your_app_password",
    "from_email": "your_email@gmail.com",
    "to_email": "your_notification_email@example.com",
    "on_failure": true,
    "on_success": false,
    "on_token_refresh": true
  }
}
```

### 配置项详解

| 配置项 | 类型 | 说明 | 必填 |
|--------|------|------|------|
| `enabled` | boolean | 是否启用邮件通知 | 是 |
| `smtp_server` | string | SMTP服务器地址 | 是 |
| `smtp_port` | number | SMTP端口(587/465) | 是 |
| `smtp_user` | string | SMTP用户名 | 是 |
| `smtp_password` | string | SMTP密码/授权码 | 是 |
| `from_email` | string | 发件人邮箱 | 是 |
| `to_email` | string | 收件人邮箱 | 是 |
| `on_failure` | boolean | 失败时发送 | 否 |
| `on_success` | boolean | 成功时发送 | 否 |
| `on_token_refresh` | boolean | Token刷新时发送 | 否 |

---

## 📮 常见邮箱配置

### Gmail

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_user": "your_email@gmail.com",
  "smtp_password": "xxxx xxxx xxxx xxxx"
}
```

**重要：** 需要使用16位应用专用密码，不是账号密码！

**获取步骤：**
1. 访问 Google账户安全设置
2. 启用两步验证
3. 生成应用专用密码

### 163邮箱

```json
{
  "smtp_server": "smtp.163.com",
  "smtp_port": 465,
  "smtp_user": "your_email@163.com",
  "smtp_password": "授权码"
}
```

**获取授权码：**
1. 登录163邮箱
2. 设置 → POP3/SMTP/IMAP
3. 开启SMTP服务并获取授权码

### QQ邮箱

```json
{
  "smtp_server": "smtp.qq.com",
  "smtp_port": 465,
  "smtp_user": "your_email@qq.com",
  "smtp_password": "授权码"
}
```

---

## 🎯 使用场景

### 场景 1: 定时任务（推荐配置）

```json
{
  "email_alerts": {
    "enabled": true,
    "on_failure": true,
    "on_success": false,
    "on_token_refresh": true
  }
}
```

**特点：**
- 只在出错或Token刷新时通知
- 避免每天收到成功邮件
- 适合自动化运行

### 场景 2: 首次配置

```json
{
  "email_alerts": {
    "enabled": true,
    "on_failure": true,
    "on_success": true,
    "on_token_refresh": true
  }
}
```

**特点：**
- 所有事件都发送邮件
- 方便验证配置是否正确
- 测试完成后建议关闭成功通知

### 场景 3: 静默模式

```json
{
  "email_alerts": {
    "enabled": false
  }
}
```

**特点：**
- 完全禁用邮件通知
- 与v1.2.1版本行为一致

---

## 📨 邮件示例

### 成功通知

```
主题：[GAC积分重置工具] 积分重置成功 ✅

GAC积分重置工具通知

时间: 2025-11-12 15:30:45
类型: success

积分已成功重置！

工单ID: 902875
响应消息: 🎉 恭喜！您的积分充值申请已自动批准。您的积分已重置！✅
完成时间: 2025-11-12 15:30:45
当前积分: 100

---
此邮件由GAC积分重置工具自动发送
配置文件: config.json
```

### 失败通知

```
主题：[GAC积分重置工具] 网络错误 - 无法验证重置状态

GAC积分重置工具通知

时间: 2025-11-12 15:30:45
类型: error

无法验证今天是否已经重置积分（网络连接失败）。
为避免重复提交，已终止执行。
请检查网络连接后重试。

---
此邮件由GAC积分重置工具自动发送
配置文件: config.json
```

---

## 🚀 快速开始

### 1. 更新配置文件

编辑 `config.json`，添加 `email_alerts` 配置块：

```json
{
  "email_alerts": {
    "enabled": true,
    "smtp_server": "smtp.163.com",
    "smtp_port": 465,
    "smtp_user": "your_email@163.com",
    "smtp_password": "your_auth_code",
    "from_email": "your_email@163.com",
    "to_email": "your_email@163.com",
    "on_failure": true,
    "on_success": false,
    "on_token_refresh": true
  }
}
```

### 2. 测试邮件配置

```bash
python auto_reset_credits_advanced.py --test-email
```

**预期输出：**
```
============================================================
Email Notification Test Mode
============================================================
Config: config.json
------------------------------------------------------------
[INFO] Credit balance:
  - Balance: 100
[INFO] Sending email: 邮件功能测试
[SUCCESS] Email sent successfully: 邮件功能测试
------------------------------------------------------------
Test complete. Please check your inbox.
============================================================
```

### 3. 正常运行

```bash
python auto_reset_credits_advanced.py
```

邮件会在配置的场景自动发送！

---

## 🔄 从v1.2.1升级

### 升级步骤

1. **备份配置**
```bash
cp config.json config.json.backup
```

2. **更新脚本**
```bash
# 下载或复制新版 auto_reset_credits_advanced.py
```

3. **添加邮件配置（可选）**

在 `config.json` 中添加 `email_alerts` 配置块。

如果不添加，脚本会使用默认配置（邮件通知禁用）。

4. **测试邮件功能**
```bash
python auto_reset_credits_advanced.py --test-email
```

5. **正常使用**
```bash
python auto_reset_credits_advanced.py
```

### 向后兼容性

✅ **完全兼容** v1.2.1 配置  
✅ 不添加 `email_alerts` 配置时，邮件功能自动禁用  
✅ 所有现有功能保持不变

---

## ❓ 常见问题

### Q1: 邮件功能是否必须启用？

**A:** 不是。`email_alerts.enabled` 默认为 `false`，完全可选。

### Q2: 如何获取Gmail应用专用密码？

**A:** 
1. 访问 https://myaccount.google.com/security
2. 启用两步验证
3. 搜索"应用专用密码"
4. 生成新密码

### Q3: 163/QQ邮箱为什么发送失败？

**A:** 需要使用**授权码**，不是登录密码。在邮箱设置中开启SMTP服务并生成授权码。

### Q4: 端口587和465有什么区别？

**A:** 
- 587: STARTTLS (推荐)
- 465: SSL/TLS
- 脚本会自动选择正确的连接方式

### Q5: 可以发送到多个邮箱吗？

**A:** 当前版本仅支持单个收件人。如需多个收件人，可以设置邮件转发规则。

### Q6: 邮件中包含完整token吗？

**A:** 不包含。出于安全考虑，只显示前50个字符。

---

## 🔐 安全建议

### 1. 保护配置文件

```bash
# Linux/macOS
chmod 600 config.json

# 添加到.gitignore
echo "config.json" >> .gitignore
```

### 2. 使用应用专用密码

- ✅ 使用应用专用密码/授权码
- ❌ 避免使用账号密码
- 🔄 定期更换密码

### 3. 独立通知邮箱

建议使用专门的邮箱用于通知，避免与个人邮箱混合。

### 4. 邮件内容安全

- Token只显示前50字符
- 不包含完整密码
- 敏感信息自动隐藏

---

## 📊 功能对比

| 功能 | v1.2.1 | v1.2.2 |
|------|--------|--------|
| 自动登录 | ✅ | ✅ |
| Token自动保存 | ✅ | ✅ |
| Token自动刷新 | ✅ | ✅ |
| 订阅检查 | ✅ | ✅ |
| 网络异常处理 | ✅ | ✅ |
| **邮件通知** | ❌ | ✅ |
| **邮件测试** | ❌ | ✅ |
| **多场景通知** | ❌ | ✅ |

---

## 📝 新增文档

### EMAIL_NOTIFICATION_GUIDE.md

详细的邮件通知配置指南，包含：

- 📧 完整配置说明
- 🔧 常见邮箱配置
- 🧪 测试方法
- 🔍 故障排查
- 💡 最佳实践

---

## 🎓 高级用法

### 定时任务配置

**Linux/macOS (crontab):**

```bash
# 每天早上9点自动运行，失败时发送邮件
0 9 * * * cd /path/to/script && python3 auto_reset_credits_advanced.py >> /tmp/gac_reset.log 2>&1
```

**Windows (任务计划程序):**

1. 创建基本任务
2. 触发器：每天 09:00
3. 操作：运行 `python auto_reset_credits_advanced.py`
4. 失败时会收到邮件通知

### 邮件过滤规则

在邮箱中设置过滤规则：

**主题包含：** `[GAC积分重置工具]`  
**操作：** 移动到专用文件夹

---

## 🐛 故障排查

### 邮件发送失败

**症状：**
```
[ERROR] Failed to send email: SMTPAuthenticationError
```

**解决方案：**
1. 检查SMTP用户名和密码
2. 确认使用应用专用密码（不是账号密码）
3. 检查邮箱是否开启SMTP服务

### 连接超时

**症状：**
```
[ERROR] Failed to send email: TimeoutError
```

**解决方案：**
1. 检查网络连接
2. 确认SMTP服务器地址和端口
3. 检查防火墙设置

### 配置不完整

**症状：**
```
[WARNING] Email configuration incomplete, missing: ['smtp_password']
```

**解决方案：**
确保所有必填字段都已填写。

---

## 📈 性能影响

### 新增操作耗时

| 操作 | 耗时 | 触发条件 |
|------|------|---------|
| 发送邮件 | ~2-5s | 配置的场景发生时 |

**总体影响：** 
- 大部分情况下可忽略
- 仅在需要发送邮件时产生延迟
- 邮件发送失败不影响主流程

---

## 🚀 未来计划

- [ ] 支持多个收件人
- [ ] HTML格式邮件
- [ ] 邮件模板自定义
- [ ] 微信/钉钉通知
- [ ] Webhook支持

---

## 📝 版本信息

- **版本号**: v1.2.2
- **发布日期**: 2025-11-12
- **更新类型**: 功能增强
- **向后兼容**: ✅ 完全兼容v1.2.1
- **测试状态**: ✅ 已测试

---

## 🙏 致谢

感谢 PVE Checkin工具的邮件通知实现提供的参考！

---

**更新完成，享受邮件通知的便利！** 📧

---

## 相关文档

- `EMAIL_NOTIFICATION_GUIDE.md` - 邮件通知详细指南
- `AUTO_LOGIN_GUIDE.md` - 自动登录指南
- `QUICKSTART.md` - 快速开始
- `docs/CHANGELOG.md` - 完整更新日志

