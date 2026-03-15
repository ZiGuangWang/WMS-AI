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

function getModuleMenuPermission(required: string): string {
  const code = (required || '').trim()
  if (!code) return ''
  if (!code.startsWith('wms:')) return ''
  if (!code.endsWith(':view')) return ''
  const parts = code.split(':')
  if (parts.length < 2) return ''
  return `wms:${parts[1]}:menu`
}

export function hasAccess(required: string | string[]): boolean {
  const requiredList = Array.isArray(required) ? required : [required]
  if (!requiredList.length) return true
  if (requiredList.every(code => !code)) return true
  if (hasPermission(requiredList)) return true

  const menus = requiredList
    .map(getModuleMenuPermission)
    .filter(Boolean)
  if (!menus.length) return false
  return menus.every(code => hasPermission(code))
}

export function hasAnyAccess(required: string[]): boolean {
  if (!required.length) return true
  return required.some(code => hasAccess(code))
}
