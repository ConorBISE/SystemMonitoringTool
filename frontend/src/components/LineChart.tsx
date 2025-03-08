import { AxisOptions, Chart } from "react-charts";
import { Metric } from "../lib/api";
import { useMemo } from "react";

export default function LineChart({ data, metric }: {data: any[], metric: Metric}) {

    const dataWrapped = [{
        label: metric.name,
        data
    }]

    console.log(dataWrapped)

    const primaryAxis = useMemo(
        (): AxisOptions<any> => ({
            getValue: datum => new Date(datum.timestamp),
        }),
        []
    )

    const secondaryAxes = useMemo(
        (): AxisOptions<any>[] => [
            {
                getValue: datum => datum.value,
            },
        ],
        []
    )
    
    return (
        <div className="h-64">
            <Chart options={{
                data: dataWrapped,
                primaryAxis,
                secondaryAxes
            }} />
        </div>
    )
}