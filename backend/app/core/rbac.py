from typing import List, Optional, Set, Union
import re
import jwt
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import settings
from app.db.mongodb import get_perm_database


_bearer = HTTPBearer(auto_error=False)


def _decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录或登录已失效",
            headers={"WWW-Authenticate": "Bearer"},
        )
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录或登录已失效",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return str(sub)


async def get_current_username(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
) -> str:
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录或登录已失效",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return _decode_token(credentials.credentials)


async def get_wms_system_id(
    db: AsyncIOMotorDatabase = Depends(get_perm_database),
    system_code: str = "wms",
) -> ObjectId:
    sys = await db["systems"].find_one({"code": system_code})
    if not sys:
        raise HTTPException(status_code=500, detail="权限系统未初始化")
    return sys["_id"]


async def get_account_by_username(
    username: str,
    db: AsyncIOMotorDatabase,
) -> Optional[dict]:
    u = username.strip()
    if not u:
        return None
    return await db["accounts"].find_one(
        {"username": {"$regex": f"^{re.escape(u)}$", "$options": "i"}}
    )


async def get_permission_codes(
    db: AsyncIOMotorDatabase,
    username: str,
    system_code: str = "wms",
) -> List[str]:
    system_id = await get_wms_system_id(db=db, system_code=system_code)  # type: ignore
    account = await get_account_by_username(username=username, db=db)
    if not account:
        return []

    acc_sys = await db["accountsystems"].find_one(
        {"accountId": account["_id"], "systemId": system_id}
    )
    if not acc_sys:
        return []

    role_perm_ids: List[ObjectId] = []
    role_id = acc_sys.get("roleId")
    if role_id:
        role = await db["roles"].find_one({"_id": role_id, "systemId": system_id})
        if role and role.get("permissions"):
            role_perm_ids = list(role["permissions"])

    extra_ids = list(acc_sys.get("extraPermissions") or [])
    denied_ids = set(acc_sys.get("deniedPermissions") or [])

    union_ids: Set[ObjectId] = set(role_perm_ids) | set(extra_ids)
    final_ids: List[ObjectId] = [pid for pid in union_ids if pid not in denied_ids]

    if not final_ids:
        return []

    perms = await db["permissions"].find(
        {"_id": {"$in": final_ids}, "systemId": system_id, "status": 1},
        {"code": 1},
    ).to_list(length=2000)
    return sorted({p["code"] for p in perms if p.get("code")})


async def get_current_permission_codes(
    username: str = Depends(get_current_username),
    db: AsyncIOMotorDatabase = Depends(get_perm_database),
) -> List[str]:
    return await get_permission_codes(db=db, username=username, system_code="wms")


def require_permissions(required: Union[str, List[str]]):
    required_list = [required] if isinstance(required, str) else list(required)

    async def _checker(perms: List[str] = Depends(get_current_permission_codes)) -> None:
        if not required_list:
            return
        if not set(required_list).issubset(set(perms)):
            raise HTTPException(status_code=403, detail="无权限")

    return _checker

