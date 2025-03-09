import * as React from "react";
import { createFileRoute } from "@tanstack/react-router";
import { useEffect } from "react";
import { useState } from "react";
import {
  getMetrics,
  Metric,
} from "../lib/api";
import MetricLineChart from "../components/MetricLineChart";

export const Route = createFileRoute("/")({
  component: HomeComponent,
});

function HomeComponent() {
  const [metrics, setMetrics] = useState<Metric[]>([]);

  // TODO: *any* kind of fetching library to manage this
  useEffect(() => {
    async function inner() {
      setMetrics(await getMetrics());
    }

    inner();
  }, []);

  if (metrics.length === 0) {
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
