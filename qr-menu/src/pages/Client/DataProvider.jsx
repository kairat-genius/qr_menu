import { useState, createContext, useEffect } from "react";
import axios from "axios";

export const DataContext = createContext();

export function DataProvider({ fetchUrl, children }) {
    const [data, setData] = useState();

    useEffect(() => {
        axios.get(fetchUrl)
            .then(response => {
                if (response.status === 200) {
                    const jsonData = response.data;
                    setData(jsonData);
                }
            })
            .catch(err => {
                console.error("Error fetching data:", err);
            });
    }, [fetchUrl]);

    return (
        <DataContext.Provider value={data}>
            {children}
        </DataContext.Provider>
    );
}
