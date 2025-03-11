import * as React from "react";
import { createFileRoute } from "@tanstack/react-router";

import {
  useMetrics,
  Metric,
} from "../lib/api";
import MetricLineChart from "../components/MetricLineChart";

export const Route = createFileRoute("/")({
  component: HomeComponent,
});

function HomeComponent() {
  const { data: metrics, isLoading: metricsLoading } = useMetrics();

  if (metricsLoading || metrics === undefined) {
    return <div>Loading ...</div>;
  }

  const charts = metrics.map((metric, i) => (
    <div className="py-2" key={i}>
      <h1>{metric.name}</h1>
      <MetricLineChart metric={metric} />
    </div>
  ));

  return <div className="p-2">{charts}</div>;
}
