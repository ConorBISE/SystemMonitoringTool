import * as React from "react";
import { createFileRoute } from "@tanstack/react-router";
import { AxisOptions, Chart } from "react-charts";
import { useEffect } from "react";
import { useState } from "react";
import { getMetricReadings, getMetrics, Metric, MetricReading } from "../lib/api";
import LineChart from "../components/LineChart";

export const Route = createFileRoute("/")({
  component: HomeComponent,
});

type MyDatum = { x: number; y: number };

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
      value: reading.value,
      timestamp: reading.timestamp,
    }))
  )

  const metricsByUuid = Object.groupBy(metrics, (metric) => metric.uuid)

  const metricsMeta = Object.keys(groupedByMetric).map(uuid => metricsByUuid[uuid][0]);

  console.log(readingsFiltered[0])
  return (
    <div className="p-2">
      <LineChart data={readingsFiltered[2] || []} metric={metricsMeta[2]} />
    </div>
  );

  // const data = [
  //   {
  //     label: 'React Charts',
  //     data: [
  //       {
  //         x: 1,
  //         y: 1,
  //       },
  //       {
  //         x: 2,
  //         y: 2,
  //       },
  //       {
  //         x: 3,
  //         y: 3,
  //       },
  //     ],
  //   },
  // ]

  // const primaryAxis = React.useMemo(
  //   (): AxisOptions<MyDatum> => ({
  //     getValue: datum => datum.x,
  //   }),
  //   []
  // )

  // const secondaryAxes = React.useMemo(
  //   (): AxisOptions<MyDatum>[] => [
  //     {
  //       getValue: datum => datum.y,
  //     },
  //   ],
  //   []
  // )

  // return (
  //   <div className="p-2 h-64">
  //     <Chart options={{
  //       data,
  //       primaryAxis,
  //       secondaryAxes,
  //      }}></Chart>
  //    </div>
  // )
}
