
export type Metric = {
    name: string
    unit: string
    uuid: string   
}

export type MetricReading = {
    metric: Metric
    value: number
    timestamp: string
}

type ListResponse<T> = {
    items: T[]
    count: number
}

export async function getMetrics() {
    const res: ListResponse<Metric> = await (await fetch("http://localhost:8000/api/metric")).json()
    return res.items
}

export async function getMetricReadings() {
    const res: ListResponse<MetricReading> = await (await fetch("http://localhost:8000/api/metric_reading")).json()
    return res.items
}
