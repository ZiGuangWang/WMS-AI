export function getPermissionCodes(): string[] {
  try {
    const raw = localStorage.getItem('permission_codes')
    if (!raw) return []
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

export function setPermissionCodes(codes: string[]) {
  localStorage.setItem('permission_codes', JSON.stringify(codes || []))
}

export function clearPermissionCodes() {
  localStorage.removeItem('permission_codes')
}

export function hasPermission(required: string | string[]): boolean {
  const codes = getPermissionCodes()
  if (!codes.length) return false
  const requiredList = Array.isArray(required) ? required : [required]
  return requiredList.every(code => codes.includes(code))
}

export function hasAnyPermission(required: string[]): boolean {
  const codes = getPermissionCodes()
  if (!codes.length) return false
  return required.some(code => codes.includes(code))
}
