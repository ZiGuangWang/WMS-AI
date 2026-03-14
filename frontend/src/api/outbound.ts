import request from '@/utils/request'

export function getOutboundOrders(params: any) {
  return request({
    url: '/outbound/orders',
    method: 'get',
    params
  })
}

export function createOutboundOrder(data: any) {
  return request({
    url: '/outbound/orders',
    method: 'post',
    data
  })
}

export function updateOutboundOrder(id: string, data: any) {
  return request({
    url: `/outbound/orders/${id}`,
    method: 'put',
    data
  })
}

export function getOutboundOrderDetail(id: string) {
  return request({
    url: `/outbound/orders/${id}`,
    method: 'get'
  })
}

export function auditOutboundOrder(id: string) {
  return request({
    url: `/outbound/orders/${id}/audit`,
    method: 'post'
  })
}

export function getOutboundOrderList(params: any) {
  return request({
    url: '/outbound/orders',
    method: 'get',
    params
  })
}

export function reviewOutboundGoods(id: string, data: any) {
  return request({
    url: `/outbound/orders/${id}/review`,
    method: 'post',
    data: data.items
  })
}

export function shipOutboundGoods(id: string) {
  return request({
    url: `/outbound/orders/${id}/ship`,
    method: 'post'
  })
}
