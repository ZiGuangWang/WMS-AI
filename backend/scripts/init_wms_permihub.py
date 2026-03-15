import asyncio
from datetime import datetime
from typing import Dict, List, Optional
import os
import sys

import bcrypt
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings


SYSTEM_CODE = "wms"
SYSTEM_NAME = "WMS"
ADMIN_USERNAME = "wms_admin"
ADMIN_PASSWORD = "123456"
ROLE_CODE = "super_admin"
ROLE_NAME = "超级管理员"


def _now() -> datetime:
    return datetime.now()


def _hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=10)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


async def _upsert_system(db) -> dict:
    existing = await db["systems"].find_one({"code": SYSTEM_CODE})
    payload = {
        "name": SYSTEM_NAME,
        "code": SYSTEM_CODE,
        "description": "WMS-AI",
        "status": 1,
        "updatedAt": _now(),
    }
    if existing:
        await db["systems"].update_one({"_id": existing["_id"]}, {"$set": payload})
        return await db["systems"].find_one({"_id": existing["_id"]})
    payload["createdAt"] = _now()
    res = await db["systems"].insert_one(payload)
    return await db["systems"].find_one({"_id": res.inserted_id})


async def _upsert_account(db) -> dict:
    existing = await db["accounts"].find_one({"username": ADMIN_USERNAME})
    payload = {
        "username": ADMIN_USERNAME,
        "password": _hash_password(ADMIN_PASSWORD),
        "email": "",
        "phone": "",
        "status": 1,
        "updatedAt": _now(),
    }
    if existing:
        await db["accounts"].update_one({"_id": existing["_id"]}, {"$set": payload})
        return await db["accounts"].find_one({"_id": existing["_id"]})
    payload["createdAt"] = _now()
    res = await db["accounts"].insert_one(payload)
    return await db["accounts"].find_one({"_id": res.inserted_id})


def _permissions_def() -> List[Dict]:
    return [
        {"name": "认证", "code": "wms:auth:menu", "type": "menu", "parent": None, "sort": 0},
        {"name": "登录页", "code": "wms:auth:login:view", "type": "menu", "parent": "wms:auth:menu", "sort": 1},
        {"name": "登录", "code": "wms:auth:login:submit", "type": "button", "parent": "wms:auth:login:view", "sort": 1},
        {"name": "工作台", "code": "wms:dashboard:menu", "type": "menu", "parent": None, "sort": 1},
        {"name": "控制台首页", "code": "wms:dashboard:home:view", "type": "menu", "parent": "wms:dashboard:menu", "sort": 1},
        {"name": "快捷-入库单", "code": "wms:dashboard:home:go_inbound_order", "type": "button", "parent": "wms:dashboard:home:view", "sort": 2},
        {"name": "快捷-出库单", "code": "wms:dashboard:home:go_outbound_order", "type": "button", "parent": "wms:dashboard:home:view", "sort": 3},
        {"name": "快捷-库存查询", "code": "wms:dashboard:home:go_inventory_query", "type": "button", "parent": "wms:dashboard:home:view", "sort": 4},
        {"name": "快捷-货品导入", "code": "wms:dashboard:home:goods_import", "type": "button", "parent": "wms:dashboard:home:view", "sort": 5},
        {"name": "预警-查看全部", "code": "wms:dashboard:home:go_inventory_warning", "type": "button", "parent": "wms:dashboard:home:view", "sort": 6},
        {"name": "预警-调整", "code": "wms:dashboard:home:go_inventory_adjust", "type": "button", "parent": "wms:dashboard:home:view", "sort": 7},
        {"name": "基础数据管理", "code": "wms:basic:menu", "type": "menu", "parent": None, "sort": 2},
        {"name": "货品管理", "code": "wms:basic:goods:view", "type": "menu", "parent": "wms:basic:menu", "sort": 1},
        {"name": "货品-新增", "code": "wms:basic:goods:add", "type": "button", "parent": "wms:basic:goods:view", "sort": 1},
        {"name": "货品-导出", "code": "wms:basic:goods:export", "type": "button", "parent": "wms:basic:goods:view", "sort": 2},
        {"name": "货品-查询", "code": "wms:basic:goods:search", "type": "button", "parent": "wms:basic:goods:view", "sort": 3},
        {"name": "货品-重置", "code": "wms:basic:goods:reset", "type": "button", "parent": "wms:basic:goods:view", "sort": 4},
        {"name": "货品-编辑", "code": "wms:basic:goods:edit", "type": "button", "parent": "wms:basic:goods:view", "sort": 5},
        {"name": "货品-删除", "code": "wms:basic:goods:delete", "type": "button", "parent": "wms:basic:goods:view", "sort": 6},
        {"name": "货品-保存", "code": "wms:basic:goods:save", "type": "button", "parent": "wms:basic:goods:view", "sort": 7},
        {"name": "库位管理", "code": "wms:basic:location:view", "type": "menu", "parent": "wms:basic:menu", "sort": 2},
        {"name": "库位-新增", "code": "wms:basic:location:add", "type": "button", "parent": "wms:basic:location:view", "sort": 1},
        {"name": "库位-导入", "code": "wms:basic:location:import", "type": "button", "parent": "wms:basic:location:view", "sort": 2},
        {"name": "库位-导出", "code": "wms:basic:location:export", "type": "button", "parent": "wms:basic:location:view", "sort": 3},
        {"name": "库位-查询", "code": "wms:basic:location:search", "type": "button", "parent": "wms:basic:location:view", "sort": 4},
        {"name": "库位-重置", "code": "wms:basic:location:reset", "type": "button", "parent": "wms:basic:location:view", "sort": 5},
        {"name": "库位-编辑", "code": "wms:basic:location:edit", "type": "button", "parent": "wms:basic:location:view", "sort": 6},
        {"name": "库位-删除", "code": "wms:basic:location:delete", "type": "button", "parent": "wms:basic:location:view", "sort": 7},
        {"name": "库位-保存", "code": "wms:basic:location:save", "type": "button", "parent": "wms:basic:location:view", "sort": 8},
        {"name": "供应商管理", "code": "wms:basic:supplier:view", "type": "menu", "parent": "wms:basic:menu", "sort": 3},
        {"name": "供应商-新增", "code": "wms:basic:supplier:add", "type": "button", "parent": "wms:basic:supplier:view", "sort": 1},
        {"name": "供应商-导出", "code": "wms:basic:supplier:export", "type": "button", "parent": "wms:basic:supplier:view", "sort": 2},
        {"name": "供应商-查询", "code": "wms:basic:supplier:search", "type": "button", "parent": "wms:basic:supplier:view", "sort": 3},
        {"name": "供应商-重置", "code": "wms:basic:supplier:reset", "type": "button", "parent": "wms:basic:supplier:view", "sort": 4},
        {"name": "供应商-编辑", "code": "wms:basic:supplier:edit", "type": "button", "parent": "wms:basic:supplier:view", "sort": 5},
        {"name": "供应商-删除", "code": "wms:basic:supplier:delete", "type": "button", "parent": "wms:basic:supplier:view", "sort": 6},
        {"name": "供应商-保存", "code": "wms:basic:supplier:save", "type": "button", "parent": "wms:basic:supplier:view", "sort": 7},
        {"name": "入库管理", "code": "wms:inbound:menu", "type": "menu", "parent": None, "sort": 3},
        {"name": "入库单管理", "code": "wms:inbound:order:view", "type": "menu", "parent": "wms:inbound:menu", "sort": 1},
        {"name": "入库单-新增", "code": "wms:inbound:order:add", "type": "button", "parent": "wms:inbound:order:view", "sort": 1},
        {"name": "入库单-导出", "code": "wms:inbound:order:export", "type": "button", "parent": "wms:inbound:order:view", "sort": 2},
        {"name": "入库单-查询", "code": "wms:inbound:order:search", "type": "button", "parent": "wms:inbound:order:view", "sort": 3},
        {"name": "入库单-重置", "code": "wms:inbound:order:reset", "type": "button", "parent": "wms:inbound:order:view", "sort": 4},
        {"name": "入库单-去验收", "code": "wms:inbound:order:check_go", "type": "button", "parent": "wms:inbound:order:view", "sort": 5},
        {"name": "入库单-编辑", "code": "wms:inbound:order:edit", "type": "button", "parent": "wms:inbound:order:view", "sort": 6},
        {"name": "入库单-删除", "code": "wms:inbound:order:delete", "type": "button", "parent": "wms:inbound:order:view", "sort": 7},
        {"name": "入库单-审核", "code": "wms:inbound:order:audit", "type": "button", "parent": "wms:inbound:order:view", "sort": 8},
        {"name": "入库单-添加货品", "code": "wms:inbound:order:item_add", "type": "button", "parent": "wms:inbound:order:view", "sort": 9},
        {"name": "入库单-移除货品", "code": "wms:inbound:order:item_remove", "type": "button", "parent": "wms:inbound:order:view", "sort": 10},
        {"name": "入库单-保存", "code": "wms:inbound:order:save", "type": "button", "parent": "wms:inbound:order:view", "sort": 11},
        {"name": "货物验收", "code": "wms:inbound:check:view", "type": "menu", "parent": "wms:inbound:menu", "sort": 2},
        {"name": "验收-导出", "code": "wms:inbound:check:export", "type": "button", "parent": "wms:inbound:check:view", "sort": 1},
        {"name": "验收-打印", "code": "wms:inbound:check:print", "type": "button", "parent": "wms:inbound:check:view", "sort": 2},
        {"name": "验收-查询", "code": "wms:inbound:check:search", "type": "button", "parent": "wms:inbound:check:view", "sort": 3},
        {"name": "验收-重置", "code": "wms:inbound:check:reset", "type": "button", "parent": "wms:inbound:check:view", "sort": 4},
        {"name": "验收-打开验收弹窗", "code": "wms:inbound:check:check_open", "type": "button", "parent": "wms:inbound:check:view", "sort": 5},
        {"name": "验收-确认验收", "code": "wms:inbound:check:check_confirm", "type": "button", "parent": "wms:inbound:check:view", "sort": 6},
        {"name": "验收-打开上架弹窗", "code": "wms:inbound:check:shelve_open", "type": "button", "parent": "wms:inbound:check:view", "sort": 7},
        {"name": "验收-确认上架", "code": "wms:inbound:check:shelve_confirm", "type": "button", "parent": "wms:inbound:check:view", "sort": 8},
        {"name": "验收-详情", "code": "wms:inbound:check:detail", "type": "button", "parent": "wms:inbound:check:view", "sort": 9},
        {"name": "出库管理", "code": "wms:outbound:menu", "type": "menu", "parent": None, "sort": 4},
        {"name": "出库单管理", "code": "wms:outbound:order:view", "type": "menu", "parent": "wms:outbound:menu", "sort": 1},
        {"name": "出库单-新增", "code": "wms:outbound:order:add", "type": "button", "parent": "wms:outbound:order:view", "sort": 1},
        {"name": "出库单-导出", "code": "wms:outbound:order:export", "type": "button", "parent": "wms:outbound:order:view", "sort": 2},
        {"name": "出库单-查询", "code": "wms:outbound:order:search", "type": "button", "parent": "wms:outbound:order:view", "sort": 3},
        {"name": "出库单-重置", "code": "wms:outbound:order:reset", "type": "button", "parent": "wms:outbound:order:view", "sort": 4},
        {"name": "出库单-审核", "code": "wms:outbound:order:audit", "type": "button", "parent": "wms:outbound:order:view", "sort": 5},
        {"name": "出库单-去复核", "code": "wms:outbound:order:review_go", "type": "button", "parent": "wms:outbound:order:view", "sort": 6},
        {"name": "出库单-详情", "code": "wms:outbound:order:detail", "type": "button", "parent": "wms:outbound:order:view", "sort": 7},
        {"name": "出库单-编辑", "code": "wms:outbound:order:edit", "type": "button", "parent": "wms:outbound:order:view", "sort": 8},
        {"name": "出库单-删除", "code": "wms:outbound:order:delete", "type": "button", "parent": "wms:outbound:order:view", "sort": 9},
        {"name": "出库单-添加货品", "code": "wms:outbound:order:item_add", "type": "button", "parent": "wms:outbound:order:view", "sort": 10},
        {"name": "出库单-移除货品", "code": "wms:outbound:order:item_remove", "type": "button", "parent": "wms:outbound:order:view", "sort": 11},
        {"name": "出库单-保存", "code": "wms:outbound:order:save", "type": "button", "parent": "wms:outbound:order:view", "sort": 12},
        {"name": "货物复核", "code": "wms:outbound:review:view", "type": "menu", "parent": "wms:outbound:menu", "sort": 2},
        {"name": "复核-导出", "code": "wms:outbound:review:export", "type": "button", "parent": "wms:outbound:review:view", "sort": 1},
        {"name": "复核-打印", "code": "wms:outbound:review:print", "type": "button", "parent": "wms:outbound:review:view", "sort": 2},
        {"name": "复核-查询", "code": "wms:outbound:review:search", "type": "button", "parent": "wms:outbound:review:view", "sort": 3},
        {"name": "复核-重置", "code": "wms:outbound:review:reset", "type": "button", "parent": "wms:outbound:review:view", "sort": 4},
        {"name": "复核-打开复核弹窗", "code": "wms:outbound:review:review_open", "type": "button", "parent": "wms:outbound:review:view", "sort": 5},
        {"name": "复核-确认复核", "code": "wms:outbound:review:review_confirm", "type": "button", "parent": "wms:outbound:review:view", "sort": 6},
        {"name": "复核-确认发货", "code": "wms:outbound:review:ship_confirm", "type": "button", "parent": "wms:outbound:review:view", "sort": 7},
        {"name": "复核-详情", "code": "wms:outbound:review:detail", "type": "button", "parent": "wms:outbound:review:view", "sort": 8},
        {"name": "库存管理", "code": "wms:inventory:menu", "type": "menu", "parent": None, "sort": 5},
        {"name": "实时库存查询", "code": "wms:inventory:query:view", "type": "menu", "parent": "wms:inventory:menu", "sort": 1},
        {"name": "库存查询-导出", "code": "wms:inventory:query:export", "type": "button", "parent": "wms:inventory:query:view", "sort": 1},
        {"name": "库存查询-刷新", "code": "wms:inventory:query:refresh", "type": "button", "parent": "wms:inventory:query:view", "sort": 2},
        {"name": "库存查询-查询", "code": "wms:inventory:query:search", "type": "button", "parent": "wms:inventory:query:view", "sort": 3},
        {"name": "库存查询-重置", "code": "wms:inventory:query:reset", "type": "button", "parent": "wms:inventory:query:view", "sort": 4},
        {"name": "库存查询-流水", "code": "wms:inventory:query:history", "type": "button", "parent": "wms:inventory:query:view", "sort": 5},
        {"name": "库存预警", "code": "wms:inventory:warning:view", "type": "menu", "parent": "wms:inventory:menu", "sort": 2},
        {"name": "预警-导出", "code": "wms:inventory:warning:export", "type": "button", "parent": "wms:inventory:warning:view", "sort": 1},
        {"name": "预警-刷新", "code": "wms:inventory:warning:refresh", "type": "button", "parent": "wms:inventory:warning:view", "sort": 2},
        {"name": "预警-去补货", "code": "wms:inventory:warning:restock_go", "type": "button", "parent": "wms:inventory:warning:view", "sort": 3},
        {"name": "库存调整", "code": "wms:inventory:adjust:view", "type": "menu", "parent": "wms:inventory:menu", "sort": 3},
        {"name": "调整-新增", "code": "wms:inventory:adjust:add", "type": "button", "parent": "wms:inventory:adjust:view", "sort": 1},
        {"name": "调整-导出", "code": "wms:inventory:adjust:export", "type": "button", "parent": "wms:inventory:adjust:view", "sort": 2},
        {"name": "调整-查询", "code": "wms:inventory:adjust:search", "type": "button", "parent": "wms:inventory:adjust:view", "sort": 3},
        {"name": "调整-重置", "code": "wms:inventory:adjust:reset", "type": "button", "parent": "wms:inventory:adjust:view", "sort": 4},
        {"name": "调整-确认", "code": "wms:inventory:adjust:confirm", "type": "button", "parent": "wms:inventory:adjust:view", "sort": 5},
    ]


async def _upsert_permissions(db, system_id: ObjectId) -> List[ObjectId]:
    defs = _permissions_def()
    code_to_id: Dict[str, ObjectId] = {}

    for p in defs:
        if p["parent"] is None:
            existing = await db["permissions"].find_one({"systemId": system_id, "code": p["code"]})
            payload = {
                "systemId": system_id,
                "name": p["name"],
                "code": p["code"],
                "type": p["type"],
                "parentId": None,
                "sort": p["sort"],
                "status": 1,
                "updatedAt": _now(),
            }
            if existing:
                await db["permissions"].update_one({"_id": existing["_id"]}, {"$set": payload})
                code_to_id[p["code"]] = existing["_id"]
            else:
                payload["createdAt"] = _now()
                res = await db["permissions"].insert_one(payload)
                code_to_id[p["code"]] = res.inserted_id

    pending = [p for p in defs if p["parent"] is not None]
    for _ in range(10):
        if not pending:
            break
        next_pending = []
        for p in pending:
            parent_code = p["parent"]
            parent_id = code_to_id.get(parent_code)
            if not parent_id:
                next_pending.append(p)
                continue
            existing = await db["permissions"].find_one({"systemId": system_id, "code": p["code"]})
            payload = {
                "systemId": system_id,
                "name": p["name"],
                "code": p["code"],
                "type": p["type"],
                "parentId": parent_id,
                "sort": p["sort"],
                "status": 1,
                "updatedAt": _now(),
            }
            if existing:
                await db["permissions"].update_one({"_id": existing["_id"]}, {"$set": payload})
                code_to_id[p["code"]] = existing["_id"]
            else:
                payload["createdAt"] = _now()
                res = await db["permissions"].insert_one(payload)
                code_to_id[p["code"]] = res.inserted_id
        pending = next_pending

    all_ids = list(code_to_id.values())
    return all_ids


async def _upsert_role(db, system_id: ObjectId, permission_ids: List[ObjectId]) -> dict:
    existing = await db["roles"].find_one({"systemId": system_id, "code": ROLE_CODE})
    payload = {
        "systemId": system_id,
        "name": ROLE_NAME,
        "code": ROLE_CODE,
        "description": "WMS-AI 超级管理员",
        "permissions": permission_ids,
        "status": 1,
        "updatedAt": _now(),
    }
    if existing:
        await db["roles"].update_one({"_id": existing["_id"]}, {"$set": payload})
        return await db["roles"].find_one({"_id": existing["_id"]})
    payload["createdAt"] = _now()
    res = await db["roles"].insert_one(payload)
    return await db["roles"].find_one({"_id": res.inserted_id})


async def _upsert_account_system(db, account_id: ObjectId, system_id: ObjectId, role_id: ObjectId) -> dict:
    existing = await db["accountsystems"].find_one({"accountId": account_id, "systemId": system_id})
    payload = {
        "accountId": account_id,
        "systemId": system_id,
        "roleId": role_id,
        "extraPermissions": [],
        "deniedPermissions": [],
        "updatedAt": _now(),
    }
    if existing:
        await db["accountsystems"].update_one({"_id": existing["_id"]}, {"$set": payload})
        return await db["accountsystems"].find_one({"_id": existing["_id"]})
    payload["createdAt"] = _now()
    res = await db["accountsystems"].insert_one(payload)
    return await db["accountsystems"].find_one({"_id": res.inserted_id})


async def main():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client["permission_manager"]

    system = await _upsert_system(db)
    system_id = system["_id"]

    account = await _upsert_account(db)
    account_id = account["_id"]

    permission_ids = await _upsert_permissions(db, system_id=system_id)
    role = await _upsert_role(db, system_id=system_id, permission_ids=permission_ids)
    role_id = role["_id"]

    await _upsert_account_system(db, account_id=account_id, system_id=system_id, role_id=role_id)

    client.close()
    print("初始化完成")


if __name__ == "__main__":
    asyncio.run(main())
