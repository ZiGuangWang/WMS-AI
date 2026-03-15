# WMS-AI 仓库管理系统

基于 Vue3 + TypeScript + Vite 和 Python FastAPI + MongoDB 开发的轻量级 Web 端仓库管理系统。

## 目录结构

- `frontend/`: Vue3 前端应用
- `backend/`: Python FastAPI 后端应用

## 核心功能

1. **基础数据管理**: 货品、库位、供应商管理。
2. **入库管理**: 入库单、验收、上架、库存更新。
3. **出库管理**: 出库单、复核、发货、库存扣减。
4. **库存管理**: 查询、预警、调整、批次管理。

## 快速开始

## 1. 环境预要求 (Prerequisites)

如果您的电脑尚未安装 Python，请务必先按照以下步骤操作：

### **第一步：安装 Python**
1. **下载**: 访问 [Python 官网](https://www.python.org/downloads/windows/)，下载 **"Windows installer (64-bit)"** (推荐 3.11 或 3.12 版本)。
2. **安装 (关键)**: 运行安装包，**务必勾选底部的 "Add Python to PATH"**。
3. **完成**: 点击 "Install Now" 直至完成。

### **第二步：解决 Windows 别名冲突**
Windows 自带的 `python.exe` 别名会干扰真实环境，必须关闭：
1. 点击 Windows **开始菜单**，搜索并打开 **"管理应用执行别名"** (Manage app execution aliases)。
2. 在列表中找到 **"python.exe"** 和 **"python3.exe"**，将它们的开关全部设为 **"关" (Off)**。

---

## 2. 后端启动 (Backend Setup)

1. **进入目录**: `cd backend`
2. **创建虚拟环境**:
   ```bash
   python -m venv .venv
   ```
3. **激活虚拟环境**:
   - **Git Bash (推荐)**: `source .venv/Scripts/activate`
   - **PowerShell**: `.\.venv\Scripts\activate`
4. **安装依赖**:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. **初始化权限系统数据（首次启动必做）**:
   - 该项目的登录与接口鉴权依赖 MongoDB 中 `permission_manager` 库的 RBAC 数据；若未初始化，后端会报“权限系统未初始化”。
   - 可选：先配置环境变量 `MONGODB_URI` 指向你的 MongoDB（默认 `mongodb://localhost:27017/permission_manager`）。
   - 在 `backend` 目录执行：
     ```bash
     python scripts/init_wms_permihub.py
     ```
   - 脚本会创建/更新 `wms` 系统、默认管理员账号、权限树与 `super_admin` 角色；默认账号：`wms_admin`，默认密码：`123456`（建议初始化后尽快修改）。
6. **启动服务**:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

## 3. 前端启动 (Frontend Setup)

1. 进入 `frontend` 目录
2. 安装依赖: `npm install`
3. 启动项目: `npm run dev`

## 权限联动（PermiHub-AI）

- 本项目的账号、角色、权限数据来自 MongoDB 的 `permission_manager`，与 PermiHub-AI 共用同一套 RBAC 数据。
- 在 PermiHub-AI 给角色“分配权限”时，WMS-AI 的页面访问与菜单显示主要依赖 `wms:xxx:yyy:view`（页面权限）；仅勾选模块节点但未包含页面 `view` 时，WMS-AI 会提示无权限或看不到菜单入口。
- 修改角色权限后，需要在 WMS-AI 重新登录（或清理本地 `token/permission_codes`）以刷新权限缓存。

## 技术栈

- 前端: Vue3, TS, Vite, Element Plus, Pinia, Vue Router
- 后端: Python, FastAPI, Motor (Async MongoDB), Pydantic
- 数据库: MongoDB (与 PermiHub-AI 共用)
