import { Aggregator, postCommand } from "../lib/api";
import { Link } from "@tanstack/react-router";

export function AggreagatorSummary({ aggregator }: { aggregator: Aggregator }) {

    const onIdentifyAggregator = async () => {
        await postCommand(aggregator.uuid, {
            command: "open_browser",
            data: "https://google.com"
        });
    };

    return (
        <div className="bg-white shadow-md rounded-lg p-4 mb-4">
            <h2 className="text-xl font-semibold mb-4">{aggregator.name}</h2>
            <div className="flex gap-4">
                <Link 
                    to="/aggregator/$uuid"
                    params={{ uuid: aggregator.uuid }}
                    className="flex-1 bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded transition-colors text-center"
                >
                    View Metrics
                </Link>
                <button 
                    className="flex-1 bg-green-500 hover:bg-green-600 text-white font-medium py-2 px-4 rounded transition-colors"
                    onClick={onIdentifyAggregator}
                >
                    Identify Aggregator
                </button>
            </div>
        </div>
    )
}