import request from '@/utils/request'

export function getInventoryQuery(params: any) {
  return request({
    url: '/inventory/query',
    method: 'get',
    params
  })
}

export function getInventoryWarning() {
  return request({
    url: '/inventory/warning',
    method: 'get'
  })
}

export function adjustInventory(data: any) {
  return request({
    url: '/inventory/adjust',
    method: 'post',
    params: data
  })
}

export function getInventoryLogs(params: any) {
  return request({
    url: '/inventory/logs',
    method: 'get',
    params
  })
}
