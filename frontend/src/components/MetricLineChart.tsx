import { useEffect, useState } from "react";
import { getMetricReadings, Metric, MetricReading } from "../lib/api";
import LineChart from "./LineChart";
import { TimeseriesBound } from "../lib/util";
import { useInterval } from "usehooks-ts";

function useMetricReadings(metricId: string, timeseriesBound: TimeseriesBound) {
  const [readings, setReadings] = useState<MetricReading[]>([]);

  useEffect(() => {
    async function fetchData() {
      const data = await getMetricReadings(metricId, timeseriesBound);
      setReadings(data);
    }

    fetchData();
  }, [metricId, timeseriesBound]);

  return readings;
}

function lastHourInterval(): TimeseriesBound {
  return {
    min: new Date(Date.now() - 1000 * 60 * 60),
    max: new Date(),
  }
}

export default function MetricLineChart({ metric }: { metric: Metric }) {
  const [userHasZoomedChart, setUserHasZoomedChart] = useState(false);

  const [timeseriesBound, setTimeseriesBound] = useState<TimeseriesBound>(lastHourInterval());

  useInterval(() => {
    if (!userHasZoomedChart)
      setTimeseriesBound(lastHourInterval())
  }, 1000 * 10)

  const metricReadings = useMetricReadings(metric.uuid, timeseriesBound);

  const chartPoints = metricReadings.map((reading) => {
    return { x: new Date(reading.timestamp), y: reading.value };
  });

  return (
    <LineChart
      data={chartPoints}
      metric={metric}
      onTimeseriesBoundChange={(bound) => {
        setUserHasZoomedChart(true);
        setTimeseriesBound(bound);
      }}
      timeseriesBound={timeseriesBound}
      yaxisBound={
        metric.unit == "%" ? {min: 0, max: 100} : {min: 10, max: 50}
      }
    />
  );
}
