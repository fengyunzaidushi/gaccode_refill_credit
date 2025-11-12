# GitHub Actions 自动化部署

## 🎯 快速开始（3步完成）

### 1️⃣ 配置 Secrets

进入仓库 **Settings → Secrets and variables → Actions**，添加9个Secrets：

| Secret | 说明 | 示例 |
|--------|------|------|
| `GAC_AUTH_TOKEN` | 认证token（可空） | 留空 |
| `GAC_EMAIL` | GAC邮箱 | `your@163.com` |
| `GAC_PASSWORD` | GAC密码 | `password` |
| `SMTP_SERVER` | SMTP服务器 | `smtp.163.com` |
| `SMTP_PORT` | SMTP端口 | `465` |
| `SMTP_USER` | SMTP用户 | `your@163.com` |
| `SMTP_PASSWORD` | SMTP授权码 | `AUTH_CODE` |
| `FROM_EMAIL` | 发件邮箱 | `your@163.com` |
| `TO_EMAIL` | 收件邮箱 | `your@163.com` |

### 2️⃣ 推送代码

```bash
git add .github/
git commit -m "Add GitHub Actions workflow"
git push
```

### 3️⃣ 启用并测试

1. 访问仓库 **Actions** 标签
2. 点击 **GAC 自动重置积分**
3. 点击 **Run workflow** 测试

✅ **完成！** 每天23:57自动运行

---

## ⏰ 运行时间

- **定时运行**：每天北京时间 23:57
- **Cron表达式**：`57 15 * * *`
- **手动触发**：随时可在Actions页面触发

---

## 📧 邮件通知

自动发送邮件的场景：
- ✅ 重置成功（可选）
- ❌ 重置失败
- 🔄 Token刷新
- ⚠️ 订阅异常
- 🌐 网络错误

---

## 📚 详细文档

- **[GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)** - 详细设置步骤
- **[GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md)** - 完整使用指南
- **[EMAIL_NOTIFICATION_GUIDE.md](EMAIL_NOTIFICATION_GUIDE.md)** - 邮件配置说明

---

## 🔍 常见问题

**Q: 如何获取163邮箱授权码？**  
A: 登录163邮箱 → 设置 → POP3/SMTP/IMAP → 开启SMTP → 获取授权码

**Q: 为什么没有自动运行？**  
A: 检查是否已启用Actions，定时任务可能延迟5-10分钟

**Q: 如何查看执行日志？**  
A: 进入Actions标签 → 点击任意运行记录 → 查看步骤日志

---

## 🔐 安全提示

- ✅ 敏感信息使用GitHub Secrets存储
- ✅ 临时配置文件自动清理
- ✅ 建议使用私有仓库
- ✅ 定期更换密码和授权码

---

**版本：** v1.3.0  
**更新日期：** 2025-11-12

