import { useState } from "react";
import { useMetricReadings, Metric } from "../lib/api";
import LineChart from "./LineChart";
import { TimeseriesBound } from "../lib/util";
import { useInterval } from "usehooks-ts";

function lastHourInterval(): TimeseriesBound {
  return {
    min: new Date(Date.now() - 1000 * 60 * 60),
    max: new Date(),
  };
}

export default function MetricLineChart({ metric }: { metric: Metric }) {
  const [userHasZoomedChart, setUserHasZoomedChart] = useState(false);
  const [timeseriesBound, setTimeseriesBound] =
    useState<TimeseriesBound>(lastHourInterval());

  const { data: metricReadings, isLoading: metricReadingsLoading } =
    useMetricReadings(metric.uuid, timeseriesBound);

  useInterval(() => {
    if (!userHasZoomedChart) setTimeseriesBound(lastHourInterval());
  }, 1000 * 10);

  if (metricReadings === undefined) return <>Loading ...</>;

  const chartPoints = metricReadings.map((reading) => {
    return { x: new Date(reading.timestamp), y: reading.value };
  });

  return (
    <>
      <h1>{metric.name}</h1>

      <LineChart
        data={chartPoints}
        metric={metric}
        onTimeseriesBoundChange={(bound) => {
          setUserHasZoomedChart(true);
          setTimeseriesBound(bound);
        }}
        timeseriesBound={timeseriesBound}
        yaxisBound={
          metric.unit == "%" ? { min: 0, max: 100 } : { min: 10, max: 50 }
        }
      />

      {userHasZoomedChart && (
        <button
          className="ml-4 px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-700"
          onClick={() => {
            setTimeseriesBound(lastHourInterval());
            setUserHasZoomedChart(false);
          }}
        >
          Reset view
        </button>
      )}
    </>
  );
}
