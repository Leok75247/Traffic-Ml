import { useEffect, useState } from 'react'
import { AlertCircle, LoaderCircle, RefreshCw } from 'lucide-react'
import { ApiError, getDatasetSummary, getEntities, getHealth, postAnalysis } from './api.js'
import { Dashboard } from './components/Dashboard.jsx'

const DEFAULT_WINDOW = 48

function messageForAnalysisError(error) {
  if (error.code === 'ENTITY_NOT_FOUND') {
    return {
      state: 'invalid-entity',
      title: 'Sensor not found',
      message: 'The selected sensor index is not available in the loaded dataset. Choose an index from the entity list and try again.',
    }
  }
  if (error.code === 'INSUFFICIENT_OBSERVATIONS') {
    return {
      state: 'insufficient-sequence',
      title: 'Sequence is too short',
      message: error.message || 'The selected sensor does not have enough valid observations for this window.',
    }
  }
  return {
    state: 'api-error',
    title: 'Analysis could not be completed',
    message: error.message || 'The API returned an unexpected response. Try again shortly.',
  }
}

function App() {
  const [apiState, setApiState] = useState('loading')
  const [apiError, setApiError] = useState(null)
  const [health, setHealth] = useState(null)
  const [entities, setEntities] = useState([])
  const [summary, setSummary] = useState(null)
  const [entityId, setEntityId] = useState('')
  const [windowSize, setWindowSize] = useState(DEFAULT_WINDOW)
  const [analysisState, setAnalysisState] = useState('initial')
  const [analysisError, setAnalysisError] = useState(null)
  const [analysis, setAnalysis] = useState(null)

  async function loadDataset(signal, showLoading = true) {
    if (showLoading) {
      setApiState('loading')
      setApiError(null)
    }
    try {
      const [healthResponse, entityResponse, summaryResponse] = await Promise.all([
        getHealth(signal),
        getEntities(signal),
        getDatasetSummary(signal),
      ])
      if (healthResponse.status !== 'ok') {
        throw new ApiError('API_UNAVAILABLE', 'The backend health check did not return a ready status.', 503)
      }
      if (!entityResponse.entities?.length) {
        throw new ApiError('NO_ENTITIES', 'The dataset did not return any selectable sensor indices.', 503)
      }
      if (signal?.aborted) return
      setHealth(healthResponse)
      setEntities(entityResponse.entities)
      setSummary(summaryResponse)
      setEntityId((selected) => entityResponse.entities.includes(selected) ? selected : entityResponse.entities[0])
      setApiState('ready')
    } catch (error) {
      if (signal?.aborted) return
      setApiError(error)
      setApiState('error')
    }
  }

  useEffect(() => {
    const controller = new AbortController()
    queueMicrotask(() => {
      if (!controller.signal.aborted) loadDataset(controller.signal, false)
    })
    return () => controller.abort()
  }, [])

  async function handleAnalyze() {
    if (apiState !== 'ready' || !entities.includes(entityId)) {
      if (entityId && !entities.includes(entityId)) {
        setAnalysisState('invalid-entity')
        setAnalysisError({
          title: 'Sensor not found',
          message: 'Choose a sensor index from the entity list returned by the backend.',
        })
      }
      return
    }
    setAnalysisState('loading')
    setAnalysisError(null)
    setAnalysis(null)
    try {
      const result = await postAnalysis({ entity_id: entityId, window_size: windowSize })
      setAnalysis(result)
      setAnalysisState('success')
    } catch (error) {
      const mapped = messageForAnalysisError(error)
      setAnalysisState(mapped.state)
      setAnalysisError(mapped)
    }
  }

  function resetAnalysis() {
    setAnalysis(null)
    setAnalysisError(null)
    setAnalysisState('initial')
  }

  function handleEntityChange(value) {
    setEntityId(value)
    resetAnalysis()
  }

  function handleWindowChange(value) {
    setWindowSize(Number(value))
    resetAnalysis()
  }

  return (
    <>
      {apiState === 'loading' && (
        <div className="connection-ribbon" role="status">
          <LoaderCircle className="spin" size={14} />
          Connecting to the traffic analysis service
        </div>
      )}
      {apiState === 'error' && (
        <div className="connection-ribbon connection-ribbon--error" role="alert">
          <AlertCircle size={14} />
          <span>{apiError?.message || 'The traffic analysis service is unavailable.'}</span>
          <button className="ribbon-retry" type="button" onClick={() => loadDataset()}>
            <RefreshCw size={13} /> Retry
          </button>
        </div>
      )}
      <Dashboard
        apiState={apiState}
        analysis={analysis}
        analysisError={analysisError}
        analysisState={analysisState}
        entityId={entityId}
        entities={entities}
        health={health}
        onAnalyze={handleAnalyze}
        onEntityChange={handleEntityChange}
        onWindowChange={handleWindowChange}
        summary={summary}
        windowSize={windowSize}
      />
    </>
  )
}

export default App
