import {useState} from "react";
import { createFileRoute } from "@tanstack/react-router";

import {
  useAggregatorMetrics,
  useAggregator,
  useAggregatorDevices,
} from "../lib/api";
import MetricLineChart from "../components/MetricLineChart";

export const Route = createFileRoute("/aggregator/$uuid")({
  component: AggregatorComponent,
});

function AggregatorComponent() {
  const { uuid } = Route.useParams();
  const { data: aggregator, isLoading: aggregatorLoading } = useAggregator(uuid);
  const { data: aggregatorDevices, isLoading: aggregatorDevicesLoading } = useAggregatorDevices(uuid);
  const { data: aggregatorMetrics, isLoading: aggregatorMetricsLoading } = useAggregatorMetrics(uuid);

  const [selectedDevice, setSelectedDevice] = useState("all");

  if (aggregator === undefined || aggregatorDevices === undefined || aggregatorMetrics === undefined) {
    return <div>Loading ...</div>;
  }

  const handleDeviceChange = (event) => {
    setSelectedDevice(event.target.value);
  };

  const filteredMetrics = selectedDevice === "all"
    ? aggregatorMetrics
    : aggregatorMetrics.filter(metric => metric.device_id === selectedDevice);

  const charts = filteredMetrics.map((metric, i) => (
    <div className="py-2" key={i}>
      <MetricLineChart metric={metric} />
    </div>
  ));

  return (
    <div className="p-2">
      <h1 className="text-2xl font-bold mb-4">{aggregator.name}</h1>
      
      <select value={selectedDevice} onChange={handleDeviceChange} className="mb-4 p-2 border rounded">
        <option value="all">All Devices</option>
        {aggregatorDevices.map((device) => (
          <option key={device.uuid} value={device.uuid}>
            {device.name}
          </option>
        ))}
      </select>

      {charts}
    </div>
  );
}
