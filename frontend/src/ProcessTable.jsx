import React, { useEffect, useState } from "react";

import {
    Table,
    TableHead,
    TableRow,
    TableHeadCell,
    TableBody,
    TableCell,
    TextInput,
    DarkThemeToggle
} from "flowbite-react";
import axios from "axios";

export default function ProcessTable(props) {
    const [data, setData] = useState([]);
    const [sortBy, setSortBy] = useState("pid");
    const [sortOrder, setSortOrder] = useState("asc");

    const columnNames = {
        "pid": "PID",
        "name": "Name",
        "cpu_usage": "CPU Usage (%)",
        "memory_usage": "Memory Usage (%)"
    }

    useEffect(() => {
        const fetchProcessData = () => {
            let baseUrl = props.endpoint;
            if (props.filter) {
                baseUrl += "/" + props.filter;
            }
            else if (props.hasSort) {
                baseUrl += `?order_by=${sortBy}&order=${sortOrder}`;
            }
            else if (props.anomaly) {
                baseUrl += "/" + props.anomaly;
            }

            axios
                .get(baseUrl)
                .then((res) => setData(res.data))
                .catch((err) => console.error("Failed to fetch processes:", err));
        };

        fetchProcessData();
        const interval = setInterval(fetchProcessData, props.refreshRate);
        return () => clearInterval(interval);
    }, [sortBy, sortOrder, props.filter, props.refreshRate, props.endpoint, props.hasSort, props.anomaly]);

    const handleSort = (column) => {
        if (sortBy === column && sortOrder !== column) {
            setSortOrder(sortOrder === "asc" ? "desc" : "asc");
        } else {
            setSortBy(column);
        }
    };

    return (
        <Table>
            <TableHead>
                <TableRow>
                    {data?.["columns"]?.map((col) => (
                        <TableHeadCell
                            key={col}

                            onClick={() => props.hasSort && handleSort(col)}
                            className={`cursor-pointer ${props.hasSort && sortBy === col ? "font-bold text-red-600" : "font-bold"}`}
                            data-key={col["key"]}
                        >
                            {columnNames[col]}
                        </TableHeadCell>
                    ))}
                </TableRow>
            </TableHead>
            <TableBody className="divide-y">
                {data?.["processes"]?.map((proc) => (
                    <TableRow key={proc["pid"]} className="hover:bg-gray-100">
                        <TableCell>{proc["pid"]}</TableCell>
                        <TableCell>{proc["name"]}</TableCell>
                        <TableCell>{parseFloat(proc["cpu_usage"]).toFixed(2)}</TableCell>
                        <TableCell>{parseFloat(proc["memory_usage"]).toFixed(2)}</TableCell>
                    </TableRow>
                ))}
                {data?.size === 0 && (
                    <TableRow>
                        <TableCell colSpan="4" className="text-center">No data available</TableCell>
                    </TableRow>
                )}
            </TableBody>
        </Table>
    );
}