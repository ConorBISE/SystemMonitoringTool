import ReactApexChart from "react-apexcharts";
import { Metric } from "../lib/api";

export type ChartPoint = {
    x: Date,
    y: number
}

export default function LineChart({
  data,
  metric,
}: {
  data: ChartPoint[];
  metric: Metric;
}) {
  return (
    <ReactApexChart
      options={{
        chart: {
          type: "line",
          zoom: {
            enabled: true,
            allowMouseWheelZoom: false
          }
        },
        xaxis: {
          type: "datetime",
          title: {
            text: "Timestamp",
          },
        },
        yaxis: {
          title: {
            text: `${metric.name} (${metric.unit})`,
          },
          decimalsInFloat: 2
        },
      }}
      series={[{ name: metric.name, data }]}
      height={350}
    />
  );
}
