import * as React from "react";
import { createFileRoute } from "@tanstack/react-router";

import {
  useMetrics,
  Metric,
  useAggregatorMetrics,
  useAggregator,
} from "../lib/api";
import MetricLineChart from "../components/MetricLineChart";

export const Route = createFileRoute("/aggregator/$uuid")({
  component: AggregatorComponent,
});

function AggregatorComponent() {
  const { uuid } = Route.useParams();
  const { data: aggregator, isLoading: aggregatorLoading } = useAggregator(uuid);
  const { data: metrics, isLoading: metricsLoading } = useAggregatorMetrics(uuid);

  if (aggregator === undefined || metrics === undefined) {
    return <div>Loading ...</div>;
  }

  const charts = metrics.map((metric, i) => (
    <div className="py-2" key={i}>
      <h1>{metric.name}</h1>
      <MetricLineChart metric={metric} />
    </div>
  ));

  return (
    <div className="p-2">
      <h1 className="text-2xl font-bold mb-4">{aggregator.name}</h1>
      {charts}
    </div>
  );
}
