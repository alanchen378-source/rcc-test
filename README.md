# 人型检测 / 人脸管理系统（骨架版）

本仓库提供基于 FastAPI + SQLAlchemy 的人型检测与人脸管理系统骨架，实现了配置拆分、基础数据库模型以及房间与人员的 CRUD 示例，方便按需扩展 YOLO、ByteTrack、InsightFace 等核心能力。

## 目录结构
- `app/`：后端源代码
  - `main.py`：FastAPI 入口，自动创建数据库表并注册路由
  - `config.py`：加载三份 YAML 配置
  - `models.py`：数据库实体模型定义（房间、人员、访客、路人、RTSP 流、ROI、事件、轨迹、特征等）
  - `routers/`：REST API 路由（目前包含房间与人员）
  - `db/session.py`：数据库连接、Session 工厂
  - `schemas/`：Pydantic 模型
- `config_env.yml`：环境配置（数据库、日志）
- `config_app.yml`：应用配置（YOLO、ByteTrack、InsightFace、业务阈值等）
- `config_rtsp.yml`：RTSP 与 ROI 配置示例
- `install`：一键安装脚本（创建虚拟环境、安装依赖、初始化数据表）
- `run.sh`：一键启动脚本
- `requirements.txt`：Python 依赖

## 快速开始
1. 安装依赖并初始化数据库：
   ```bash
   ./install
   ```
2. 启动 API 服务：
   ```bash
   ./run.sh
   ```
3. 访问接口与管理界面：
   - 根路径健康检查：`GET /`
   - 房间 CRUD：`/rooms`
   - 人员 CRUD：`/people`
   - Web 管理后台：`GET /admin`（内置房间、人员的表单式管理界面）

默认数据库地址来自 `config_env.yml`，请按需修改为实际的 PostgreSQL 连接信息。
