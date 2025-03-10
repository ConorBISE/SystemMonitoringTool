import { TimeseriesBound } from "./util"

const BASE_URL = "http://systemmonitortool.ddns.net/api"

export type Metric = {
    name: string
    unit: string
    uuid: string   
}

export type MetricReading = {
    metric_id: string
    device_id: string
    value: number
    timestamp: string
}

type ListResponse<T> = {
    items: T[]
    count: number
}

export async function getMetrics() {
    const res: ListResponse<Metric> = await (await fetch(`${BASE_URL}/metric`)).json()
    return res.items
}

export async function getMetricReadings(metricId: string, timeseriesBound?: TimeseriesBound) {
    const query = new URLSearchParams()
    query.set("metric_id", metricId)

    if (timeseriesBound) {
        query.set("timestamp_min", timeseriesBound.min.toISOString())
        query.set("timestamp_max", timeseriesBound.max.toISOString())
    }
        
    const res: MetricReading[] = await (await fetch(`${BASE_URL}/metric_reading?${query.toString()}`)).json()
    return res
}
