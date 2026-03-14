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

### 后端启动

1. 进入 `backend` 目录
2. 安装依赖: `pip install -r requirements.txt`
3. 启动服务: `uvicorn app.main:app --reload`

### 前端启动

1. 进入 `frontend` 目录
2. 安装依赖: `npm install`
3. 启动项目: `npm run dev`

## 技术栈

- 前端: Vue3, TS, Vite, Element Plus, Pinia, Vue Router
- 后端: Python, FastAPI, Motor (Async MongoDB), Pydantic
- 数据库: MongoDB (与 PermiHub-AI 共用)
