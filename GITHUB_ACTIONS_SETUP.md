# GitHub Actions 快速设置指南

## 📋 设置清单

### ✅ 步骤 1: 配置 GitHub Secrets

访问您的仓库：**Settings → Secrets and variables → Actions**

逐个添加以下 9 个 Secrets：

```
┌─────────────────────────────────────────────────────────┐
│  Secret 1: GAC_AUTH_TOKEN                               │
│  说明: GAC认证token（可留空，脚本会自动登录获取）        │
│  值:   留空或填入已有token                              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Secret 2: GAC_EMAIL                                    │
│  说明: GAC账号邮箱                                      │
│  值:   your_email@163.com                              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Secret 3: GAC_PASSWORD                                 │
│  说明: GAC账号密码                                      │
│  值:   your_gac_password                               │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Secret 4: SMTP_SERVER                                  │
│  说明: SMTP服务器地址                                   │
│  值:   smtp.163.com (163邮箱)                          │
│       smtp.gmail.com (Gmail)                           │
│       smtp.qq.com (QQ邮箱)                             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Secret 5: SMTP_PORT                                    │
│  说明: SMTP端口                                         │
│  值:   465 (163/QQ邮箱，SSL)                           │
│       587 (Gmail，STARTTLS)                            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Secret 6: SMTP_USER                                    │
│  说明: SMTP登录用户名（通常是邮箱地址）                  │
│  值:   your_email@163.com                              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Secret 7: SMTP_PASSWORD                                │
│  说明: SMTP密码（授权码，不是登录密码！）                │
│  值:   BWOQWYCZNFQFVNAZ (163授权码示例)                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Secret 8: FROM_EMAIL                                   │
│  说明: 发件人邮箱（通常与SMTP_USER相同）                 │
│  值:   your_email@163.com                              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Secret 9: TO_EMAIL                                     │
│  说明: 收件人邮箱（可以与FROM_EMAIL相同）                │
│  值:   your_email@163.com                              │
└─────────────────────────────────────────────────────────┘
```

---

## 🔑 获取 SMTP 授权码

### 163 邮箱

1. 登录 https://mail.163.com
2. 点击右上角 **设置** → **POP3/SMTP/IMAP**
3. 找到 **SMTP 服务**，点击 **开启**
4. 按提示发送短信验证
5. 获得 16 位授权码（类似：`BWOQWYCZNFQFVNAZ`）
6. **保存这个授权码**，用于 `SMTP_PASSWORD`

### QQ 邮箱

1. 登录 https://mail.qq.com
2. 点击 **设置** → **账户**
3. 找到 **POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务**
4. 开启 **SMTP 服务**
5. 按提示发送短信验证
6. 获得授权码
7. 用于 `SMTP_PASSWORD`

### Gmail

1. 访问 https://myaccount.google.com/security
2. 确保已启用 **两步验证**
3. 搜索 **应用专用密码**
4. 选择应用：**邮件**
5. 选择设备：**其他（自定义名称）**
6. 输入名称：`GAC Reset Tool`
7. 获得 16 位密码（类似：`abcd efgh ijkl mnop`）
8. 用于 `SMTP_PASSWORD`

---

## 📝 示例配置（163 邮箱）

```
GAC_AUTH_TOKEN:    (留空)
GAC_EMAIL:         your_gac_email@example.com
GAC_PASSWORD:      your_gac_password

SMTP_SERVER:       smtp.163.com
SMTP_PORT:         465
SMTP_USER:         youremail@example.com
SMTP_PASSWORD:     BWOQWYCZNFQFVNAZ
FROM_EMAIL:        youremail@example.com
TO_EMAIL:          youremail@example.com
```

---

## ✅ 步骤 2: 启用工作流

1. 将工作流文件提交到仓库：

```bash
git add .github/
git commit -m "Add GitHub Actions workflow"
git push
```

2. 访问仓库的 **Actions** 标签

3. 如果显示 "Workflows aren't being run on this repository"：
   - 点击 **I understand my workflows, go ahead and enable them**

---

## 🧪 步骤 3: 测试运行

### 手动触发测试

1. 进入 **Actions** 标签
2. 左侧选择 **GAC 自动重置积分**
3. 右侧点击 **Run workflow** 下拉菜单
4. 点击绿色的 **Run workflow** 按钮
5. 等待执行完成（约 1-2 分钟）

### 检查结果

**成功标志：**

- ✅ 所有步骤显示绿色勾号
- ✅ 收到邮件通知（根据配置）
- ✅ 日志中显示 "Credits have been reset successfully"

**失败处理：**

- ❌ 查看红色叉号的步骤
- 📝 点击步骤查看详细日志
- 📧 检查是否收到失败通知邮件
- 🔍 参考故障排查部分

---

## 🎯 配置验证清单

在测试运行前，请确认：

- [ ] 所有 9 个 Secrets 都已添加
- [ ] Secret 名称完全一致（区分大小写）
- [ ] SMTP_PASSWORD 使用的是授权码，不是登录密码
- [ ] 邮箱已开启 SMTP 服务
- [ ] GAC_EMAIL 和 GAC_PASSWORD 正确
- [ ] 工作流文件已推送到仓库
- [ ] 仓库已启用 Actions

---

## ⏰ 运行时间说明

### 定时运行

工作流将在每天 **北京时间 23:57** 自动运行。

**时区转换：**

- 北京时间 23:57 = UTC 15:57
- Cron 表达式：`57 15 * * *`

### 首次自动运行

- 提交工作流后
- 等待到下一个 23:57（北京时间）
- 工作流自动触发

**注意：** GitHub Actions 可能有 5-10 分钟的延迟。

---

## 📊 监控运行状态

### 查看执行历史

1. 进入 **Actions** 标签
2. 查看工作流运行记录：
   - 🟢 绿色勾号 = 成功
   - 🔴 红色叉号 = 失败
   - 🟡 黄色圆圈 = 运行中

### 查看详细日志

1. 点击任意运行记录
2. 查看各步骤的执行情况
3. 点击步骤名称查看详细日志
4. 下载日志文件（右上角 ⋮ 菜单）

---

## 🔍 常见错误和解决方案

### 错误 1: "Error: Process completed with exit code 1"

**原因：** 脚本执行失败

**检查：**

```
查看 "运行积分重置" 步骤的日志
查找具体错误信息：
- [ERROR] 开头的行
- 异常堆栈信息
```

**常见原因：**

- GAC 账号密码错误
- 今日已重置
- 网络问题
- 订阅过期

### 错误 2: "Error: Secrets cannot be found"

**原因：** Secrets 未配置或名称错误

**解决：**

1. 检查 Secrets 名称是否完全一致
2. 确认 Secrets 在正确的仓库中
3. 重新创建 Secrets

### 错误 3: "发送失败通知邮件出错: SMTPAuthenticationError"

**原因：** SMTP 认证失败

**解决：**

1. 确认使用的是授权码，不是登录密码
2. 检查 SMTP_USER 和 SMTP_PASSWORD 是否正确
3. 确认邮箱 SMTP 服务已开启

### 错误 4: "已经重置过了"

**现象：**

```
[INFO] ⚠️  Already reset today!
```

**说明：**

- 这是正常情况
- 脚本检测到今天已经重置
- 自动跳过，等待明天

---

## 💡 高级配置

### 修改运行时间

编辑 `.github/workflows/auto-reset-credits.yml`：

```yaml
schedule:
  - cron: "0 12 * * *" # 改为北京时间 20:00
```

**时间计算：** 北京时间 - 8 = UTC 时间

### 只在工作日运行

```yaml
schedule:
  - cron: "57 15 * * 1-5" # 周一到周五
```

### 添加多个时间点

```yaml
schedule:
  - cron: "57 15 * * *" # 23:57
  - cron: "0 12 * * *" # 20:00
```

---

## 📧 邮件通知配置

### 通知策略

工作流配置的通知策略：

```json
"on_failure": true,        // 失败时通知 ✅
"on_success": false,       // 成功时不通知
"on_token_refresh": true   // Token刷新时通知 ✅
```

### 修改通知策略

如果想收到成功通知，需要在工作流的配置生成部分修改：

```yaml
"on_success": true, # 改为 true
```

---

## 🔐 安全建议

### 1. 使用私有仓库

如果担心安全问题，建议将仓库设为私有：

- Settings → Danger Zone → Change visibility → Make private

### 2. 定期更换密码

- 每 3 个月更换一次 GAC 密码
- 每 3 个月重新生成 SMTP 授权码
- 更新后记得更新 Secrets

### 3. 限制 Actions 权限

在仓库设置中限制 Actions 权限：

- Settings → Actions → General
- Workflow permissions → Read repository contents

### 4. 监控运行记录

定期检查 Actions 执行记录，发现异常及时处理。

---

## 📚 相关文档

- `GITHUB_ACTIONS_GUIDE.md` - 完整的 GitHub Actions 指南
- `EMAIL_NOTIFICATION_GUIDE.md` - 邮件通知配置指南
- `AUTO_LOGIN_GUIDE.md` - 自动登录功能说明
- `QUICKSTART.md` - 快速开始指南

---

## ✅ 完成确认

配置完成后，您应该：

- ✅ 已添加所有 9 个 Secrets
- ✅ 工作流文件已提交到仓库
- ✅ 手动测试运行成功
- ✅ 收到测试邮件
- ✅ 了解如何查看日志
- ✅ 知道如何处理常见错误

---

**恭喜！自动化配置完成！** 🎉

现在您的积分将在每天 **北京时间 23:57** 自动重置，并通过邮件接收通知。

**下一步：**

- 等待今晚 23:57 首次自动运行
- 检查邮件通知
- 查看 Actions 运行记录

---

**版本：** v1.0.0  
**更新日期：** 2025-11-12
