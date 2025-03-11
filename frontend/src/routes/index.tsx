import * as React from "react";
import { createFileRoute } from "@tanstack/react-router";

import {
  useAggregators,
} from "../lib/api";

import { AggreagatorSummary } from "../components/AggregatorSummary";

export const Route = createFileRoute("/")({
  component: HomeComponent,
});

function HomeComponent() {
  const { data: aggregators, isLoading: aggregatorsLoading } = useAggregators();

  if (aggregatorsLoading || aggregators === undefined) {
    return <div>Loading ...</div>;
  }

  return (
    <div className="p-2">
      <h1 className="text-3xl font-bold mb-4">System Monitoring Tool</h1>
      <h2 className="text-xl font-semibold mb-6">Aggregators</h2>
      
      {aggregators.map(aggregator => (
        <AggreagatorSummary key={aggregator.uuid} aggregator={aggregator} />
      ))}
    </div>
  );
}
