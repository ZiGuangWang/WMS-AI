import request from '@/utils/request'

// Goods
export function getGoodsList(params: any) {
  return request({
    url: '/basic/goods',
    method: 'get',
    params
  })
}

export function createGoods(data: any) {
  return request({
    url: '/basic/goods',
    method: 'post',
    data
  })
}

export function updateGoods(id: string, data: any) {
  return request({
    url: `/basic/goods/${id}`,
    method: 'put',
    data
  })
}

export function deleteGoods(id: string) {
  return request({
    url: `/basic/goods/${id}`,
    method: 'delete'
  })
}

// Locations
export function getLocationList(params: any) {
  return request({
    url: '/basic/locations',
    method: 'get',
    params
  })
}

export function createLocation(data: any) {
  return request({
    url: '/basic/locations',
    method: 'post',
    data
  })
}

export function updateLocation(id: string, data: any) {
  return request({
    url: `/basic/locations/${id}`,
    method: 'put',
    data
  })
}

export function deleteLocation(id: string) {
  return request({
    url: `/basic/locations/${id}`,
    method: 'delete'
  })
}

// Suppliers
export function getSupplierList(params: any) {
  return request({
    url: '/basic/suppliers',
    method: 'get',
    params
  })
}

export function createSupplier(data: any) {
  return request({
    url: '/basic/suppliers',
    method: 'post',
    data
  })
}

export function updateSupplier(id: string, data: any) {
  return request({
    url: `/basic/suppliers/${id}`,
    method: 'put',
    data
  })
}

export function deleteSupplier(id: string) {
  return request({
    url: `/basic/suppliers/${id}`,
    method: 'delete'
  })
}
