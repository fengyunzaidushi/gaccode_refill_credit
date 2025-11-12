# 快速开始指南

## 5 分钟快速配置

### 步骤 1: 安装 Python（如果还没有）

**Windows:**

- 访问 https://www.python.org/downloads/
- 下载并安装 Python 3.8 或更高版本
- 安装时勾选 "Add Python to PATH"

**Linux/macOS:**

```bash
# 通常已预装，检查版本
python3 --version
```

### 步骤 2: 安装依赖

```bash
pip install requests
```

### 步骤 3: 配置脚本（推荐方式 - 无需手动获取 Token）

**方法 A: 使用 Email 和 Password（最简单，推荐）✨**

```bash
# 1. 复制配置文件
cp config.json.example config.json

# 2. 编辑 config.json，填入你的邮箱和密码
{
  "auth_token": "",
  "email": "your_email@example.com",
  "password": "your_password"
}
```

**脚本会自动登录并保存 token，无需手动获取！**

**方法 B: 手动获取 Token（传统方式）**

如果你想手动配置 token：

1. 打开浏览器访问 https://gaccode.com 并登录
2. 按 `F12` 打开开发者工具
3. 点击 "Network" 标签
4. 刷新页面
5. 随便点击一个请求
6. 在 "Request Headers" 中找到 `Authorization`
7. 复制 `Bearer` 后面的长字符串
8. 填入 config.json 的 `auth_token` 字段

### 步骤 4: 运行脚本

**直接运行 Python 脚本（推荐）:**

```bash
# Windows
python auto_reset_credits_advanced.py

# Linux/macOS/Git Bash
python3 auto_reset_credits_advanced.py
```

**首次运行输出示例:**

```
[STEP -2] No valid auth token found, attempting to login...
[INFO] Attempting to login and get authentication token...
[SUCCESS] Login successful!
[SUCCESS] Configuration saved to config.json
[INFO] ✓ Authentication token obtained and saved!
```

### 步骤 5: 查看结果

如果成功，你会看到：

```
===========================================================
[SUCCESS] Credits have been reset successfully! ✅
===========================================================
```

## 常用命令

```bash
# 基本运行
python auto_reset_credits_advanced.py

# 查看积分余额
python auto_reset_credits_advanced.py --check-balance

# 测试连接（不创建工单）
python auto_reset_credits_advanced.py --dry-run

# 使用自定义配置文件
python auto_reset_credits_advanced.py --config my_config.json

# 命令行直接传 token（不使用配置文件）
python auto_reset_credits_advanced.py --token "YOUR_TOKEN_HERE"
```

## 一键运行脚本

**Linux/macOS/Git Bash:**

```bash
./run_reset.sh                    # 基本运行
./run_reset.sh --check-balance    # 查看余额
./run_reset.sh --dry-run          # 测试模式
```

**Windows:**

```cmd
run_reset.bat                     REM 基本运行
run_reset.bat --check-balance     REM 查看余额
run_reset.bat --dry-run          REM 测试模式
```

## 疑难解答

### 问题: ModuleNotFoundError: No module named 'requests'

**解决:**

```bash
pip install requests
# 或
python -m pip install requests
```

### 问题: 认证失败 (401 Unauthorized)

**解决:**

- Token 可能已过期，重新获取
- 检查 Token 是否完整复制（包括开头和结尾）
- 确保 Token 前面没有 "Bearer " 文字（只复制 token 本身）

### 问题: 达到每日限额

**解决:**

- 每天最多 1 次重置
- 等待第二天再试

### 问题: config.json not found

**解决:**

```bash
cp config.json.example config.json
# 然后编辑 config.json 填入你的 token
```

### 问题: 需要 reCAPTCHA 验证

**解决:**

- 手动访问网站完成一次验证
- 然后再运行脚本

## 自动化运行（可选）

### Windows 计划任务

1. Win + R，输入 `taskschd.msc`
2. 创建基本任务
3. 触发器：每天
4. 操作：启动程序 → 浏览到 `run_reset.bat`

### Linux/macOS Cron

```bash
# 编辑 crontab
crontab -e

# 每天早上 9 点运行
0 9 * * * cd /path/to/script && python3 auto_reset_credits_advanced.py

# 或使用 shell 脚本
0 9 * * * /path/to/script/run_reset.sh
```

## 安全提示

⚠️ **重要：不要分享你的 Token！**

- Token 等同于你的账号密码
- 不要将包含 token 的文件提交到 Git
- 不要在聊天或论坛中发布你的 token
- 如果 token 泄露，立即重新登录以刷新 token

## 需要帮助？

查看完整文档：`README_AUTO_RESET.md`

---

**就是这么简单！享受自动化吧！** 🎉
