import { getToken } from './auth'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

async function apiRequest(method, endpoint, data = null, headers = {}) {
  const url = `${API_BASE_URL}${endpoint}`
  const token = getToken()
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  const options = { method, headers }
  if (data) {
    options.headers['Content-Type'] = 'application/json'
    options.body = JSON.stringify(data)
  }
  const response = await fetch(url, options)
  const json = await response.json()
  return { status: response.status, json }
}

export const apiGET = (endpoint, headers = {}) => apiRequest('GET', endpoint, null, headers)
export const apiPOST = (endpoint, data = {}, headers = {}) => apiRequest('POST', endpoint, data, headers)
export const apiPUT = (endpoint, data = {}, headers = {}) => apiRequest('PUT', endpoint, data, headers)
export const apiPATCH = (endpoint, data = {}, headers = {}) => apiRequest('PATCH', endpoint, data, headers)
export const apiDELETE = (endpoint, data = {}, headers = {}) => apiRequest('DELETE', endpoint, data, headers)

export const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
    headers: {
      'Authorization': `Bearer ${getToken()}`,
    }
  })
  const json = await response.json()
  return { status: response.status, json }
}

export const downloadFile = (fileId) => {
  const url = `${API_BASE_URL}/upload/${fileId}`
  return fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${getToken()}`,
    }
  })
}