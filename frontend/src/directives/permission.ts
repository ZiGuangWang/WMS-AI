import type { Directive } from 'vue'
import { hasPermission } from '@/utils/permission'

export const permissionDirective: Directive = {
  mounted(el, binding) {
    const required = binding.value
    if (!required) return
    if (!hasPermission(required)) {
      el.style.display = 'none'
    }
  },
  updated(el, binding) {
    const required = binding.value
    if (!required) return
    el.style.display = hasPermission(required) ? '' : 'none'
  }
}

