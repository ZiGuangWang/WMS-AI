import request from '@/utils/request'

export function getInboundOrders(params: any) {
  return request({
    url: '/inbound/orders',
    method: 'get',
    params
  })
}

export function createInboundOrder(data: any) {
  return request({
    url: '/inbound/orders',
    method: 'post',
    data
  })
}

export function updateInboundOrder(id: string, data: any) {
  return request({
    url: `/inbound/orders/${id}`,
    method: 'put',
    data
  })
}

export function getInboundOrderDetail(id: string) {
  return request({
    url: `/inbound/orders/${id}`,
    method: 'get'
  })
}

export function auditInboundOrder(id: string) {
  return request({
    url: `/inbound/orders/${id}/audit`,
    method: 'post'
  })
}

export function getInboundOrderList(params: any) {
  return request({
    url: '/inbound/orders',
    method: 'get',
    params
  })
}

export function checkInboundGoods(id: string, data: any) {
  return request({
    url: `/inbound/orders/${id}/receive`,
    method: 'post',
    data: data.items
  })
}

export function shelveInboundGoods(id: string, data: any) {
  return request({
    url: `/inbound/orders/${id}/shelve`,
    method: 'post'
  })
}
