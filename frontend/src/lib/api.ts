import useSWR from "swr"
import { TimeseriesBound } from "./util"
const BASE_URL = "https://systemmonitortool.ddns.net/api"

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

async function fetcher<T>(url: string): Promise<T> {
    return await (await fetch(BASE_URL + url)).json()
}


export function useMetrics() {
    return useSWR<Metric[]>("/metric", async (key: string) => (await fetcher<ListResponse<Metric>>(key)).items);
}

export function useMetricReadings(metricId: string, timeseriesBound?: TimeseriesBound) {
    const query = new URLSearchParams()
    query.set("metric_id", metricId)

    if (timeseriesBound) {
        query.set("timestamp_min", timeseriesBound.min.toISOString())
        query.set("timestamp_max", timeseriesBound.max.toISOString())
    }

    return useSWR<MetricReading[]>(`/metric_reading/${metricId}`, async (_key: string) => await fetcher<MetricReading[]>(`/metric_reading?${query.toString()}`))
}
