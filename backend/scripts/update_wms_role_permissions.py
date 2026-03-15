import os
import re
from datetime import datetime, timezone
from typing import Dict, List, Tuple

from pymongo import MongoClient


def _connect() -> Tuple[MongoClient, str]:
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/permission_manager")
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    return client, uri


def _get_system(db) -> dict:
    sys_doc = db.systems.find_one({"code": "wms"}, {"_id": 1, "code": 1, "name": 1})
    if not sys_doc:
        raise SystemExit("未找到 systems.code=wms，请先运行 scripts/init_wms_permihub.py")
    return sys_doc


def _get_account(db, username: str) -> dict:
    u = username.strip()
    if not u:
        raise SystemExit("username 不能为空")
    acc = db.accounts.find_one(
        {"username": {"$regex": f"^{re.escape(u)}$", "$options": "i"}},
        {"_id": 1, "username": 1, "status": 1},
    )
    if not acc:
        raise SystemExit(f"未找到账号: {username}")
    return acc


def _get_bound_role(db, system_id, account_id) -> dict:
    acc_sys = db.accountsystems.find_one(
        {"accountId": account_id, "systemId": system_id}, {"roleId": 1}
    )
    if not acc_sys or not acc_sys.get("roleId"):
        raise SystemExit("未找到 accountsystems 绑定关系或 roleId")
    role = db.roles.find_one(
        {"_id": acc_sys["roleId"], "systemId": system_id},
        {"_id": 1, "code": 1, "name": 1, "systemId": 1, "permissions": 1},
    )
    if not role:
        raise SystemExit("未找到绑定的角色文档")
    return role


def _collect_permission_ids(db, system_id, modules: List[str]) -> Tuple[List, Dict[str, int]]:
    module_set = {m.strip() for m in modules if m and m.strip()}
    if not module_set:
        raise SystemExit("modules 不能为空")
    rx = "^wms:(" + "|".join(sorted(module_set)) + "):"
    perms = list(
        db.permissions.find(
            {"systemId": system_id, "status": 1, "code": {"$regex": rx}},
            {"_id": 1, "code": 1},
        ).sort("code", 1)
    )
    ids = [p["_id"] for p in perms]
    counts: Dict[str, int] = {}
    for m in sorted(module_set):
        prefix = f"wms:{m}:"
        counts[m] = sum(1 for p in perms if (p.get("code") or "").startswith(prefix))
    return ids, counts


def main() -> None:
    username = os.getenv("WMS_USERNAME", "wms_admin")
    modules_raw = os.getenv("WMS_MODULES", "dashboard,basic,inventory")
    modules = [m.strip() for m in modules_raw.split(",") if m.strip()]

    client, uri = _connect()
    db = client["permission_manager"]

    sys_doc = _get_system(db)
    acc = _get_account(db, username=username)
    role = _get_bound_role(db, system_id=sys_doc["_id"], account_id=acc["_id"])

    ids, counts = _collect_permission_ids(db, system_id=sys_doc["_id"], modules=modules)

    res = db.roles.update_one(
        {"_id": role["_id"]},
        {"$set": {"permissions": ids, "updatedAt": datetime.now(timezone.utc)}},
    )

    menu_codes = [f"wms:{m}:menu" for m in modules]
    view_codes = [
        "wms:dashboard:home:view",
        "wms:basic:goods:view",
        "wms:basic:location:view",
        "wms:basic:supplier:view",
        "wms:inventory:query:view",
        "wms:inventory:warning:view",
        "wms:inventory:adjust:view",
    ]
    codes = sorted(
        {
            p.get("code")
            for p in db.permissions.find(
                {"systemId": sys_doc["_id"], "status": 1, "_id": {"$in": ids}},
                {"code": 1},
            )
            if p.get("code")
        }
    )

    print("MONGODB_URI=", uri)
    print("system=", {"_id": str(sys_doc["_id"]), "code": sys_doc.get("code"), "name": sys_doc.get("name")})
    print("account=", {"_id": str(acc["_id"]), "username": acc.get("username"), "status": acc.get("status")})
    print("role=", {"_id": str(role["_id"]), "code": role.get("code"), "name": role.get("name")})
    print("update_modified=", res.modified_count)
    print("assigned_permissions=", len(ids))
    print("module_counts=", counts)
    print("menus_present=", {c: (c in codes) for c in menu_codes})
    print("views_present=", {c: (c in codes) for c in view_codes})


if __name__ == "__main__":
    main()
