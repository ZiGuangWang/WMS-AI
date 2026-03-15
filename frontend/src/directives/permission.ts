import type { Directive } from 'vue'
import { hasAccess } from '@/utils/permission'

export const permissionDirective: Directive = {
  mounted(el, binding) {
    const required = binding.value
    if (!required) return
    if (!hasAccess(required)) {
      el.style.display = 'none'
    }
  },
  updated(el, binding) {
    const required = binding.value
    if (!required) return
    el.style.display = hasAccess(required) ? '' : 'none'
  }
}
