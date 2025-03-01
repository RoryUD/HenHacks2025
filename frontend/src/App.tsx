import React, { useEffect, useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import {
	Chart as ChartJS,
	ChartOptions,
	ChartData,
	TooltipItem,
} from "chart.js/auto";
import "./App.css";

function App() {
	// Define the GraphData interface to type the state
	interface GraphData {
		labels: string[];
		data: number[];
	}

	// Use GraphData or an empty array for initial state to avoid null
	const [graphData, setGraphData] = useState<GraphData>({
		labels: [],
		data: [],
	});

	useEffect(() => {
		// Fetch graph data from the Flask API
		axios.get("http://127.0.0.1:5000/api/graph-data")
			.then((response) => {
				console.log("Graph Data:", response.data); // Log the response data
				setGraphData(response.data);
			})
			.catch((error) => {
				console.error(
					"There was an error fetching the graph data!",
					error
				);
			});
	}, []);

	// Type for chart options
	const chartOptions: ChartOptions<"line"> = {
		responsive: true,
		plugins: {
			legend: {
				position: "top", // 'top' position does not need `as const`
			},
			tooltip: {
				callbacks: {
					label: function (tooltipItem: TooltipItem<"line">) {
						// Assert the type of tooltipItem.raw as number
						const value = tooltipItem.raw as number;
						return `Disasters: ${value}`;
					},
				},
			},
		},
	};

	// Explicitly type chartData as ChartData<'line'>
	const chartData: ChartData<"line"> = {
		labels: graphData.labels,
		datasets: [
			{
				label: "Number of Disasters",
				data: graphData.data,
				borderColor: "rgba(75, 192, 192, 1)",
				backgroundColor: "rgba(75, 192, 192, 0.2)",
				borderWidth: 1,
			},
		],
	};

	return (
		<div className="App">
			<div className="App-header">Waffle House Disaster Tracker</div>
			<div className="App-body">
				{graphData.labels.length > 0 ? (
					<div>
						<h2>Disaster Frequency per Location</h2>
						<Line data={chartData} options={chartOptions} />
					</div>
				) : (
					<p>Loading graph data...</p>
				)}
			</div>
			<div className="App-footer">
				<p>Made By:</p>
				<p>
					<a href="https://github.com/aghoy9">Alex Hoy</a> ,
					<a href="https://github.com/Dtrieu728">
						Dustine Trieu
					</a>{" "}
					, and{" "}
					<a href="https://github.com/RoryUD">Rory Jordan</a>
				</p>
			</div>
		</div>
	);
}

export default App;
