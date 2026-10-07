const API_PREFIX = '/api'

export class ApiError extends Error {
  constructor(code, message, status) {
    super(message)
    this.name = 'ApiError'
    this.code = code
    this.status = status
  }
}

async function request(path, options = {}) {
  let response
  try {
    response = await fetch(`${API_PREFIX}${path}`, {
      ...options,
      headers: {
        Accept: 'application/json',
        ...(options.body ? { 'Content-Type': 'application/json' } : {}),
        ...options.headers,
      },
    })
  } catch (error) {
    if (error.name === 'AbortError') throw error
    throw new ApiError('API_UNAVAILABLE', 'Cannot reach the backend. Confirm that FastAPI is running on port 8000.', 0)
  }

  const payload = await response.json().catch(() => null)
  if (!response.ok) {
    const detail = payload?.error
    throw new ApiError(
      detail?.code || 'API_ERROR',
      detail?.message || `The backend returned HTTP ${response.status}.`,
      response.status,
    )
  }
  if (payload === null) {
    throw new ApiError('INVALID_RESPONSE', 'The backend response was not valid JSON.', response.status)
  }
  return payload
}

export function getHealth(signal) {
  return request('/health', { signal })
}

export function getEntities(signal) {
  return request('/entities', { signal })
}

export function getDatasetSummary(signal) {
  return request('/dataset/summary', { signal })
}

export function postAnalysis(payload) {
  return request('/analyze', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}