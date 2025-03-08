import * as React from "react";
import { createFileRoute } from "@tanstack/react-router";
import { useEffect } from "react";
import { useState } from "react";
import {
  getMetricReadings,
  getMetrics,
  Metric,
  MetricReading,
} from "../lib/api";
import LineChart from "../components/LineChart";

export const Route = createFileRoute("/")({
  component: HomeComponent,
});

function HomeComponent() {
  const [readings, setReadings] = useState<MetricReading[]>([]);
  const [metrics, setMetrics] = useState<Metric[]>([]);

  // TODO: *any* kind of fetching library to manage this
  useEffect(() => {
    async function inner() {
      setReadings(await getMetricReadings());
      setMetrics(await getMetrics());
    }

    inner();
  }, []);

  if (readings.length === 0 || metrics.length === 0) {
    return <div>Loading ...</div>;
  }

  const groupedByMetric = Object.groupBy(
    readings,
    (reading) => reading.metric.uuid
  );

  const readingsFiltered = Object.keys(groupedByMetric).map((key) =>
    groupedByMetric[key]?.map((reading) => ({
      y: reading.value,
      x: new Date(reading.timestamp),
    }))
  );

  const metricsByUuid = Object.groupBy(metrics, (metric) => metric.uuid);

  const metricsMeta = Object.keys(groupedByMetric).map(
    (uuid) => metricsByUuid[uuid][0]
  );

  const charts = readingsFiltered.map((readingArray, i) => (
    <div className="py-2">
      <h1>{metricsMeta[i].name}</h1>
      <LineChart data={readingArray || []} metric={metricsMeta[i]} />
    </div>
  ));

  return <div className="p-2">{charts}</div>;
}
