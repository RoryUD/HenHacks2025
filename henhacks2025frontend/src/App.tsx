import React from "react";
import logo from "./logo.svg";
import "./App.css";
import { appendFile } from "fs";

function App() {
	return (
		<div className="App">
			<header className="App-header">
				<img src={logo} className="App-logo" alt="logo" />
				<p>HenHacks 2025 Submission!</p>
			</header>
		</div>
	);
}

export default App;
