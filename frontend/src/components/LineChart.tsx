import ReactApexChart from "react-apexcharts";
import { Metric } from "../lib/api";
import { TimeseriesBound } from "../lib/util";

export type ChartPoint = {
    x: Date,
    y: number
}

export type YAxisBounds = {
  min: number,
  max: number
}

export default function LineChart({
  data,
  metric,
  timeseriesBound,
  yaxisBound,
  onTimeseriesBoundChange
}: {
  data: ChartPoint[];
  metric: Metric;
  timeseriesBound: TimeseriesBound;
  yaxisBound: YAxisBounds;
  onTimeseriesBoundChange?: (bound: TimeseriesBound) => void;
}) {
  const onChartEvent = (chart: any, axes: any) => {
    onTimeseriesBoundChange && onTimeseriesBoundChange({
      min: new Date(axes.xaxis.min),
      max: new Date(Math.min(axes.xaxis.max, Date.now() ))
    })
  };

  return (
    <ReactApexChart
      options={{
        chart: {
          type: "line",
          zoom: {
            enabled: true,
            allowMouseWheelZoom: false
          },
          events: {
            zoomed: onChartEvent,
            scrolled: onChartEvent
          },
          toolbar: {
            tools: {
              reset: false
            }
          },
          animations: {
            enabled: false
          }
        },
        xaxis: {
          type: "datetime",
          title: {
            text: "Timestamp",
          },
          min: timeseriesBound.min.getTime(),
          max: timeseriesBound.max.getTime()
        },
        yaxis: {
          title: {
            text: `${metric.name} (${metric.unit})`,
          },
          decimalsInFloat: 2,
          min: yaxisBound.min,
          max: yaxisBound.max
        },
      }}
      series={[{ name: metric.name, data }]}
      height={350}
    />
  );
}
