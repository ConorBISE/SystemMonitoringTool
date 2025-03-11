import useSWR from "swr"
import { TimeseriesBound } from "./util"
const BASE_URL = "https://systemmonitortool.ddns.net/api"

export type Aggregator = {
    name: string
    uuid: string
}

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

export type Command = {
    command: string;
    data: string;
};

type ListResponse<T> = {
    items: T[]
    count: number
}

async function fetcher<T>(url: string): Promise<T> {
    return await (await fetch(BASE_URL + url)).json()
}

async function listItemFetcher<T>(url: string): Promise<T[]> {
    return (await fetcher<ListResponse<T>>(url)).items
}

export function useAggregators() {
    return useSWR<Aggregator[]>("/aggregator", listItemFetcher);
}

export function useAggregator(uuid: string) {
    return useSWR<Aggregator>(`/aggregator/${uuid}`, fetcher);
}


export function useMetrics() {
    return useSWR<Metric[]>("/metric", listItemFetcher);
}

export function useAggregatorMetrics(uuid: string) {
    return useSWR<Metric[]>(`/metric?aggregator_id=${uuid}`, listItemFetcher);
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

export async function postCommand(aggregatorId: string, command: Command): Promise<void> {
    await fetch(`${BASE_URL}/aggregator/${aggregatorId}/command`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(command)
    });
}
