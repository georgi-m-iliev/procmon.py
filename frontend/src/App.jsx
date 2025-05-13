import { Navbar, NavbarBrand, TextInput, DarkThemeToggle } from "flowbite-react";

import ProcessTable from "./ProcessTable.jsx";
import { useState } from "react";

export default function App() {
    const [refreshRate, setRefreshRate] = useState(5000);
    const [filter, setFilter] = useState("");


    return (
        <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white transition-colors">
            <Navbar fluid rounded className="border-b dark:border-gray-700">
                <NavbarBrand href="#">
                    <h1 className="text-2xl font-bold">Process Monitor</h1>
                </NavbarBrand>
                <div className="flex md:order-2">
                    <div className="flex flex-col w-full max-w-sm mx-5">
                        <label htmlFor="refreshRate" className="font-medium mb-1">
                            Refresh Rate: {refreshRate} ms
                        </label>
                        <input
                            id="refreshRate"
                            type="range"
                            min="500"
                            max="10000"
                            step="100"
                            value={refreshRate}
                            onChange={(e) => setRefreshRate(parseInt(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                        />
                    </div>
                    <DarkThemeToggle />
                    {/*<NavbarToggle />*/}
                </div>
                {/*<NavbarCollapse>*/}
                {/*    /!* Add Nav links here if needed *!/*/}
                {/*</NavbarCollapse>*/}
            </Navbar>
            <main className="p-6">
                <div className="flex flex-col md:flex-row md:h-[calc(100vh-8rem)] p-4 gap-4 box-border">
                    <div className="flex-1 overflow-hidden">
                        <div className="h-full overflow-y-auto border rounded-lg p-2">
                            <div className="flex justify-between items-center p-2" >
                                <h2 className="text-lg font-semibold mb-2">Processes</h2>
                                <TextInput
                                    className=""
                                    placeholder="process name..."
                                    onChange={(e) => setFilter(e.target.value)}
                                />
                            </div>
                            <ProcessTable endpoint="http://localhost:8000/api/processes"
                                          refreshRate={refreshRate}
                                          filter={filter}
                                          hasSort
                            />
                        </div>
                    </div>
                    <div className="md:w-2/5 flex flex-col gap-4">
                        <div className="flex-1 min-h-0 overflow-hidden">
                            <div className="h-full overflow-y-auto border rounded-lg p-2">
                                <h2 className="text-lg font-semibold mb-2 ml-2">Detected CPU Usage Anomalies</h2>
                                <ProcessTable endpoint="http://localhost:8000/api/anomaly"
                                              refreshRate={refreshRate}
                                              anomaly="cpu"
                                />
                            </div>
                        </div>
                        <div className="flex-1 min-h-0 overflow-hidden">
                            <div className="h-full overflow-y-auto border rounded-lg p-2">
                                <h2 className="text-lg font-semibold mb-2 ml-2">Detected Memory Usage Anomalies</h2>
                                <ProcessTable endpoint="http://localhost:8000/api/anomaly"
                                              refreshRate={refreshRate}
                                              anomaly="memory"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
