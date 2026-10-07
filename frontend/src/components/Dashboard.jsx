import {
  Activity,
  ArrowRight,
  ArrowUpRight,
  CircleAlert,
  Clock3,
  Database,
  LoaderCircle,
  RefreshCw,
  Signal,
  TriangleAlert,
} from 'lucide-react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

const WINDOW_OPTIONS = [24, 48, 96, 288, 576, 1440]
const STATE_COLORS = {
  low: '#64745b',
  medium: '#8e724b',
  high: '#744a41',
  unknown: '#77766c',
}
const CHART_STATE_VALUES = {
  'Low Traffic': 0,
  'Medium Traffic': 1,
  'High Traffic': 2,
}

function stateTone(label = '') {
  if (label.toLowerCase().includes('low')) return 'low'
  if (label.toLowerCase().includes('medium')) return 'medium'
  if (label.toLowerCase().includes('high')) return 'high'
  return 'unknown'
}

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`
}

function formatNumber(value, digits = 2) {
  return new Intl.NumberFormat('en-US', { maximumFractionDigits: digits }).format(value)
}

function formatTimestamp(value, includeDate = false) {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return new Intl.DateTimeFormat('en-GB', {
    ...(includeDate ? { day: '2-digit', month: 'short' } : {}),
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC',
    hourCycle: 'h23',
  }).format(date)
}

function shortDate(value) {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return new Intl.DateTimeFormat('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    timeZone: 'UTC',
  }).format(date)
}

function Header({ apiState, health, summary }) {
  const ready = apiState === 'ready' && health?.status === 'ok'
  return (
    <header className="masthead">
      <div className="masthead-copy">
        <p className="eyebrow">Emergency traffic intelligence</p>
        <h1>Ambulance Traffic Intelligence</h1>
        <p className="masthead-subtitle">HMM-Based Traffic Congestion State Analysis</p>
      </div>
      <div className={`service-status ${ready ? 'is-ready' : ''}`} aria-live="polite">
        <span className="status-dot" />
        <span>{ready ? 'MODEL READY' : apiState === 'loading' ? 'CONNECTING' : 'SERVICE UNAVAILABLE'}</span>
        {ready && summary?.dataset_label && <span className="status-divider">/</span>}
        {ready && summary?.dataset_label && <span className="dataset-name">{summary.dataset_label}</span>}
      </div>
    </header>
  )
}

function ControlBar({ apiState, entityId, entities, isLoading, onAnalyze, onEntityChange, onWindowChange, windowSize, summary }) {
  return (
    <section className="control-bar" aria-label="Analysis controls">
      <div className="control-group control-group--entity">
        <label htmlFor="entity-select">Entity</label>
        <select
          id="entity-select"
          value={entityId}
          disabled={apiState !== 'ready'}
          onChange={(event) => onEntityChange(event.target.value)}
        >
          {entities.map((entity) => <option key={entity} value={entity}>Sensor {entity}</option>)}
        </select>
      </div>
      <div className="control-group control-group--window">
        <label htmlFor="window-select">Window</label>
        <select
          id="window-select"
          value={windowSize}
          disabled={apiState !== 'ready'}
          onChange={(event) => onWindowChange(event.target.value)}
        >
          {WINDOW_OPTIONS.map((size) => (
            <option key={size} value={size}>{size} observations</option>
          ))}
        </select>
      </div>
      <div className="control-spacer" />
      <div className="dataset-chip" title={summary?.dataset_source || ''}>
        <Database size={13} strokeWidth={1.7} />
        <span>{summary?.dataset_label || 'Dataset'}</span>
      </div>
      <button
        className="analyze-button"
        type="button"
        onClick={onAnalyze}
        disabled={apiState !== 'ready' || isLoading || !entityId}
      >
        {isLoading ? <LoaderCircle className="spin" size={15} /> : <Activity size={15} strokeWidth={1.8} />}
        <span>{isLoading ? 'Analyzing' : 'Analyze'}</span>
      </button>
    </section>
  )
}

function MetricCard({ label, value, support, tone, icon: Icon }) {
  const isPending = !value
  return (
    <article className="metric-card">
      <div className="metric-topline">
        <p className="metric-label">{label}</p>
        <span className={`metric-mark ${tone || ''}`}><Icon size={13} strokeWidth={1.8} /></span>
      </div>
      <p className={`metric-value ${tone || ''} ${isPending ? 'metric-value--pending' : ''}`}>
        {value || 'Awaiting analysis'}
      </p>
      <p className="metric-support">{support}</p>
    </article>
  )
}

function KeyResults({ analysis, analysisState }) {
  const success = analysisState === 'success' && analysis
  const leadingState = success
    ? Object.entries(analysis.state_probabilities).sort((a, b) => b[1] - a[1])[0]
    : null
  const nextProbability = success ? analysis.next_state_probabilities[analysis.next_state] : null
  const latestObservation = success ? analysis.viterbi_sequence.at(-1) : null

  return (
    <section className="key-results" aria-label="Analysis results">
      <MetricCard
        label="Current state"
        value={success ? analysis.current_state.replace(' Traffic', '').toUpperCase() : null}
        support={success && latestObservation
          ? `Latest inferred condition · ${formatTimestamp(latestObservation.timestamp)}`
          : 'Latest inferred traffic condition'}
        tone={success ? stateTone(analysis.current_state) : 'medium'}
        icon={Activity}
      />
      <MetricCard
        label="Next predicted state"
        value={success ? analysis.next_state.replace(' Traffic', '').toUpperCase() : null}
        support={success && nextProbability != null
          ? `One-step probability · ${formatPercent(nextProbability)}`
          : 'Most likely next hidden state'}
        tone={success ? stateTone(analysis.next_state) : 'high'}
        icon={ArrowUpRight}
      />
      <MetricCard
        label="Top state probability"
        value={success && leadingState ? formatPercent(leadingState[1]) : null}
        support={success && leadingState
          ? `${leadingState[0]} in the current distribution`
          : 'Probability from current state distribution'}
        tone="neutral"
        icon={Signal}
      />
    </section>
  )
}

function PanelHeading({ title, subtitle, trailing }) {
  return (
    <div className="panel-heading">
      <div>
        <h2>{title}</h2>
        {subtitle && <p>{subtitle}</p>}
      </div>
      {trailing && <div className="panel-trailing">{trailing}</div>}
    </div>
  )
}

function EmptyAnalysis({ analysisState, error, onRetry }) {
  if (analysisState === 'loading') {
    return (
      <div className="empty-analysis empty-analysis--loading" role="status">
        <LoaderCircle className="spin" size={24} />
        <div>
          <strong>Analysing the selected sequence</strong>
          <p>Training the HMM and calculating the state path.</p>
        </div>
      </div>
    )
  }
  if (analysisState === 'invalid-entity' || analysisState === 'insufficient-sequence' || analysisState === 'api-error') {
    return (
      <div className="empty-analysis empty-analysis--error" role="alert">
        {analysisState === 'insufficient-sequence'
          ? <TriangleAlert size={22} />
          : analysisState === 'invalid-entity'
            ? <CircleAlert size={22} />
            : <RefreshCw size={22} />}
        <div>
          <strong>{error?.title || 'Analysis unavailable'}</strong>
          <p>{error?.message || 'The request could not be completed.'}</p>
          {onRetry && <button className="text-action" type="button" onClick={onRetry}>Try analysis again <ArrowRight size={14} /></button>}
        </div>
      </div>
    )
  }
  return (
    <div className="empty-analysis" role="status">
      <Activity size={22} />
      <div>
        <strong>Analysis not run</strong>
        <p>Select a sensor and window, then analyze to see its computed traffic states.</p>
      </div>
    </div>
  )
}

function TimelineTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const observation = payload[0].payload
  return (
    <div className="chart-tooltip">
      <span className={`tooltip-state-dot ${stateTone(observation.state)}`} />
      <div>
        <strong>{observation.state}</strong>
        <p>{formatTimestamp(observation.timestamp, true)} UTC</p>
      </div>
    </div>
  )
}

function StateDot({ cx, cy, payload }) {
  if (cx == null || cy == null) return null
  return <circle cx={cx} cy={cy} r={3.5} fill={STATE_COLORS[stateTone(payload.state)]} stroke="#fefdf9" strokeWidth={1.5} />
}

function TrafficTimeline({ analysis, analysisState, error, onRetry }) {
  const rows = analysis?.viterbi_sequence.map((item, index) => ({
    index,
    timestamp: item.timestamp,
    time: new Date(item.timestamp).getTime(),
    state: item.state,
    level: CHART_STATE_VALUES[item.state],
  })) || []
  const first = rows[0]?.time
  const last = rows.at(-1)?.time

  return (
    <section className="panel timeline-panel">
      <PanelHeading
        title="Traffic State Timeline"
        subtitle="Recent hidden-state sequence inferred by Viterbi"
        trailing={analysis ? <span className="observations-tag">{analysis.viterbi_sequence.length} observations</span> : null}
      />
      {analysisState === 'success' && rows.length > 0 ? (
        <div className="timeline-chart" role="img" aria-label={`Viterbi traffic state timeline for ${analysis.entity_id}`}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={rows} margin={{ top: 14, right: 20, bottom: 0, left: 4 }}>
              <CartesianGrid vertical={false} stroke="#e7e3da" strokeDasharray="2 4" />
              <XAxis
                type="number"
                dataKey="time"
                domain={[first, last]}
                tickCount={5}
                tickFormatter={(value) => formatTimestamp(value, true)}
                tick={{ fill: '#858378', fontSize: 10 }}
                axisLine={{ stroke: '#d8d3c8' }}
                tickLine={false}
                minTickGap={18}
              />
              <YAxis
                type="number"
                domain={[0, 2]}
                ticks={[2, 1, 0]}
                tickFormatter={(value) => ['Low', 'Medium', 'High'][value]}
                tick={{ fill: '#77766c', fontSize: 10, fontWeight: 600 }}
                axisLine={false}
                tickLine={false}
                width={54}
              />
              <Tooltip content={<TimelineTooltip />} />
              {last != null && <ReferenceLine x={last} stroke="#a6a193" strokeDasharray="3 4" label={{ value: 'LATEST', position: 'insideTopRight', fill: '#77766c', fontSize: 9 }} />}
              <Line
                type="stepAfter"
                dataKey="level"
                name="Inferred state"
                stroke="#8e724b"
                strokeWidth={2.2}
                activeDot={{ r: 5, stroke: '#fefdf9', strokeWidth: 2 }}
                dot={<StateDot />}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      ) : <EmptyAnalysis analysisState={analysisState} error={error} onRetry={onRetry} />}
      {analysisState === 'success' && rows.length > 0 && (
        <div className="timeline-range">
          <span>{formatTimestamp(rows[0].timestamp, true)} UTC</span>
          <span>Sensor {analysis.entity_id}</span>
          <span>{formatTimestamp(rows.at(-1).timestamp, true)} UTC</span>
        </div>
      )}
    </section>
  )
}

function SensorNetworkContext({ entities, entityId, summary, onEntityChange }) {
  const visibleEntities = entities.slice(0, 7)
  if (entityId && !visibleEntities.includes(entityId)) {
    if (visibleEntities.length >= 7) visibleEntities[visibleEntities.length - 1] = entityId
    else visibleEntities.push(entityId)
  }
  const positions = ['node-north', 'node-west', 'node-center', 'node-east', 'node-southwest', 'node-south', 'node-southeast']

  return (
    <section className="panel context-panel">
      <PanelHeading title="SENSOR NETWORK CONTEXT" subtitle="Index-only view · not geographic" />
      <div className="sensor-schematic" aria-label="Schematic arrangement of available sensor indices; not a map">
        <div className="schematic-grid" aria-hidden="true" />
        <svg className="schematic-links" viewBox="0 0 420 220" preserveAspectRatio="none" aria-hidden="true">
          <path d="M79 62 L167 90 L252 64 L338 99 M85 163 L167 125 L252 158 L338 99 M167 90 L167 125 M252 64 L252 158" />
        </svg>
        {visibleEntities.map((id, index) => (
          <button
            className={`sensor-node ${positions[index]} ${id === entityId ? 'is-selected' : ''}`}
            key={id}
            type="button"
            onClick={() => onEntityChange(id)}
            aria-pressed={id === entityId}
            title={`Select sensor ${id}`}
          >
            <span className="node-indicator" />
            <span className="node-label">SENSOR</span>
            <strong>{id}</strong>
          </button>
        ))}
        {entityId && <span className="selected-note"><span /> Selected · {entityId}</span>}
      </div>
      <div className="context-footer">
        <div className="state-legend" aria-label="Traffic state colors">
          {Object.entries(STATE_COLORS).filter(([key]) => key !== 'unknown').map(([key, color]) => (
            <span key={key}><i style={{ backgroundColor: color }} />{key}</span>
          ))}
        </div>
        <span className="schematic-caption">Positions are illustrative</span>
      </div>
      <div className="context-metadata">
        <span><Signal size={13} /> {summary ? formatNumber(summary.entity_count, 0) : '—'} indexed sensors</span>
        <span><Clock3 size={13} /> {summary ? `${formatNumber(summary.sampling_interval_seconds / 60, 0)} min interval` : '—'}</span>
      </div>
    </section>
  )
}

function ProbabilityChart({ analysis, analysisState, error }) {
  const data = analysis
    ? Object.entries(analysis.state_probabilities).map(([state, probability]) => ({ state, probability }))
    : []
  return (
    <section className="panel probability-panel">
      <PanelHeading title="State Probabilities" subtitle="Current state distribution" />
      {analysisState === 'success' && data.length > 0 ? (
        <div className="probability-chart" role="img" aria-label="Current state probabilities returned by the analysis API">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart layout="vertical" data={data} margin={{ top: 12, right: 22, bottom: 6, left: 0 }}>
              <CartesianGrid horizontal={false} stroke="#ebe7de" />
              <XAxis
                type="number"
                domain={[0, 1]}
                tickFormatter={(value) => `${Math.round(value * 100)}%`}
                tick={{ fill: '#858378', fontSize: 10 }}
                axisLine={{ stroke: '#d8d3c8' }}
                tickLine={false}
              />
              <YAxis
                type="category"
                dataKey="state"
                width={100}
                tick={{ fill: '#48483f', fontSize: 11, fontWeight: 500 }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                formatter={(value) => [formatPercent(Number(value)), 'Probability']}
                cursor={{ fill: '#f4f2eb', opacity: 0.7 }}
                contentStyle={{ border: '1px solid #dbd6ca', borderRadius: 8, fontSize: 12, background: '#fefdf9' }}
              />
              <Bar dataKey="probability" barSize={13} radius={[0, 4, 4, 0]}>
                {data.map((entry) => <Cell key={entry.state} fill={STATE_COLORS[stateTone(entry.state)]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      ) : <EmptyAnalysis analysisState={analysisState} error={error} />}
      {analysisState === 'success' && <p className="chart-footnote">Filtered posterior at the latest observation</p>}
    </section>
  )
}

function TransitionMatrix({ analysis, analysisState, error }) {
  const labels = analysis ? Object.keys(analysis.state_probabilities) : []
  return (
    <section className="panel matrix-panel">
      <PanelHeading title="HMM Transition Matrix" subtitle="Estimated state-to-state movement" />
      {analysisState === 'success' && analysis?.transition_matrix ? (
        <div className="matrix-wrap">
          <table className="transition-table">
            <caption className="sr-only">Transition probabilities from each traffic state to the next</caption>
            <thead>
              <tr>
                <th scope="col">From / To</th>
                {labels.map((label) => <th scope="col" key={label}>{label.replace(' Traffic', '')}</th>)}
              </tr>
            </thead>
            <tbody>
              {analysis.transition_matrix.map((row, rowIndex) => (
                <tr key={labels[rowIndex]}>
                  <th scope="row">{labels[rowIndex].replace(' Traffic', '')}</th>
                  {row.map((probability, columnIndex) => (
                    <td key={`${rowIndex}-${columnIndex}`}>
                      <span
                        className={`matrix-value ${rowIndex === columnIndex ? 'is-diagonal' : ''}`}
                        style={{ '--cell-strength': 0.05 + probability * 0.28 }}
                        title={`${labels[rowIndex]} to ${labels[columnIndex]}: ${probability}`}
                      >
                        {probability.toFixed(3)}
                      </span>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          <p className="matrix-note">Rows are origin states; columns are next states.</p>
        </div>
      ) : <EmptyAnalysis analysisState={analysisState} error={error} />}
    </section>
  )
}

function ModelStatistics({ analysis, analysisState, error }) {
  if (analysisState !== 'success' || !analysis) {
    return (
      <section className="panel stats-panel">
        <PanelHeading title="Model Statistics" subtitle="Training and inference snapshot" />
        <EmptyAnalysis analysisState={analysisState} error={error} />
      </section>
    )
  }
  const training = analysis.training
  const stats = [
    { label: 'Forward log probability', value: formatNumber(analysis.forward_log_probability, 3) },
    { label: 'Baum-Welch iterations', value: formatNumber(training.iterations, 0) },
    { label: 'Converged', value: training.converged ? 'Yes' : 'No', tone: training.converged ? 'low' : 'medium' },
    { label: 'Sequence length', value: `${formatNumber(analysis.viterbi_sequence.length, 0)} observations` },
  ]
  return (
    <section className="panel stats-panel">
      <PanelHeading title="Model Statistics" subtitle="Training and inference snapshot" />
      <dl className="stats-list">
        {stats.map((item) => (
          <div className="stats-row" key={item.label}>
            <dt>{item.label}</dt>
            <dd className={item.tone ? `state-text ${item.tone}` : ''}>{item.value}</dd>
          </div>
        ))}
      </dl>
      <p className="algorithm-label" title={training.algorithm}>{training.algorithm}</p>
    </section>
  )
}

function FutureStates({ states }) {
  if (!states?.length) return null
  return (
    <div className="future-outlook">
      <span className="future-label">Short outlook</span>
      <div className="future-items">
        {states.map((item, index) => (
          <span className={`future-item ${stateTone(item.state)}`} key={`${item.step}-${item.state}`}>
            <span className="future-step">+{item.step}</span>
            <strong>{item.state.replace(' Traffic', '')}</strong>
            <small>{formatPercent(item.state_probabilities[item.state])}</small>
            {index < states.length - 1 && <ArrowRight className="future-arrow" size={12} />}
          </span>
        ))}
      </div>
    </div>
  )
}

function ViterbiSequence({ analysis, analysisState, error, onRetry }) {
  if (analysisState !== 'success' || !analysis) {
    return (
      <section className="sequence-panel sequence-panel--empty">
        <div className="sequence-empty-copy">
          <p className="sequence-kicker">Viterbi sequence</p>
          <strong>{analysisState === 'initial' ? 'The inferred path will appear here' : error?.title || 'Sequence unavailable'}</strong>
          <p>{analysisState === 'initial' ? 'A state label will be shown for each observation in the selected window.' : error?.message}</p>
          {analysisState === 'api-error' && onRetry && <button className="sequence-retry" type="button" onClick={onRetry}>Retry analysis <RefreshCw size={13} /></button>}
        </div>
        <div className="sequence-symbol" aria-hidden="true"><Activity size={28} /></div>
      </section>
    )
  }

  const currentProbabilities = analysis.state_probabilities
  const highestCurrent = Object.entries(currentProbabilities).sort((a, b) => b[1] - a[1])[0]
  const predictedProbability = analysis.next_state_probabilities[analysis.next_state]
  const finalViterbi = analysis.viterbi_sequence.at(-1)

  return (
    <section className="sequence-panel">
      <div className="sequence-main">
        <div className="sequence-heading-row">
          <p className="sequence-kicker">Viterbi sequence</p>
          <span className="sequence-count">{formatNumber(analysis.viterbi_sequence.length, 0)} observations</span>
        </div>
        <div className="sequence-track" role="list" aria-label={`Viterbi sequence for sensor ${analysis.entity_id}`}>
          {analysis.viterbi_sequence.map((item, index) => (
            <span
              className={`sequence-point ${stateTone(item.state)}`}
              key={`${item.timestamp}-${index}`}
              role="listitem"
              title={`${formatTimestamp(item.timestamp, true)} UTC · ${item.state}`}
              aria-label={`${item.state}, ${formatTimestamp(item.timestamp, true)} UTC`}
            >
              {item.state.replace(' Traffic', '').slice(0, 1)}
            </span>
          ))}
        </div>
        <div className="sequence-legend">
          <span><i className="low" />Low</span>
          <span><i className="medium" />Medium</span>
          <span><i className="high" />High</span>
          {finalViterbi && <span className="sequence-last">Latest Viterbi state · {finalViterbi.state}</span>}
        </div>
      </div>
      <div className="result-explanation">
        <p className="sequence-kicker">Why this result</p>
        <p className="explanation-copy">
          The latest filtered distribution favors <strong>{highestCurrent[0]}</strong> ({formatPercent(highestCurrent[1])});
          the model assigns <strong>{formatPercent(predictedProbability)}</strong> to <strong>{analysis.next_state}</strong> for the next step.
        </p>
        <FutureStates states={analysis.future_state_sequence} />
      </div>
    </section>
  )
}

function DatasetFootnote({ summary }) {
  if (!summary) return null
  return (
    <footer className="dataset-footnote">
      <span>{summary.dataset_label} · {formatNumber(summary.entity_count, 0)} indexed sensors</span>
      <span>{shortDate(summary.start_time)} – {shortDate(summary.end_time)} · {formatNumber(summary.sampling_interval_seconds / 60, 0)}-minute sampling</span>
      <span>{summary.geographic_metadata_available ? 'Geographic metadata available' : 'No geographic metadata'}</span>
    </footer>
  )
}

export function Dashboard({
  apiState,
  analysis,
  analysisError,
  analysisState,
  entityId,
  entities,
  health,
  onAnalyze,
  onEntityChange,
  onWindowChange,
  summary,
  windowSize,
}) {
  const retryAnalysis = analysisState === 'api-error' ? onAnalyze : null
  const isAnalyzing = analysisState === 'loading'
  return (
    <main className="dashboard-shell">
      <Header apiState={apiState} health={health} summary={summary} />
      <ControlBar
        apiState={apiState}
        entityId={entityId}
        entities={entities}
        isLoading={isAnalyzing}
        onAnalyze={onAnalyze}
        onEntityChange={onEntityChange}
        onWindowChange={onWindowChange}
        summary={summary}
        windowSize={windowSize}
      />
      <KeyResults analysis={analysis} analysisState={analysisState} />
      <div className="analysis-grid">
        <TrafficTimeline analysis={analysis} analysisState={analysisState} error={analysisError} onRetry={retryAnalysis} />
        <SensorNetworkContext entities={entities} entityId={entityId} summary={summary} onEntityChange={onEntityChange} />
      </div>
      <div className="model-grid">
        <ProbabilityChart analysis={analysis} analysisState={analysisState} error={analysisError} />
        <TransitionMatrix analysis={analysis} analysisState={analysisState} error={analysisError} />
        <ModelStatistics analysis={analysis} analysisState={analysisState} error={analysisError} />
      </div>
      <ViterbiSequence analysis={analysis} analysisState={analysisState} error={analysisError} onRetry={retryAnalysis} />
      <DatasetFootnote summary={summary} />
      <span className="sr-only" aria-live="polite">
        {analysisState === 'loading' ? 'Analysis in progress' : analysisState === 'success' ? 'Analysis results loaded' : ''}
      </span>
    </main>
  )
}