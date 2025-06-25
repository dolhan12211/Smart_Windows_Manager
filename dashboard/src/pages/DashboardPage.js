import React, { useState, useEffect } from 'react';
import WindowCard from '../components/WindowCard';

function DashboardPage() {
  const [windowsData, setWindowsData] = useState([]);

  useEffect(() => {
        const fetchData = async () => {
          try {
            
            const response = await fetch('http://4.233.221.95:8000/get_data');
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
        const result = await response.json();
        console.log("Fetched data:", result);
        setWindowsData(result);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 1000); 
    return () => clearInterval(intervalId);
  }, []); 

  return (
    <div className="min-h-screen bg-gray-800 text-gray-100 p-6">
      <header className="text-center mb-8">
        <h1 className="text-4xl font-bold text-blue-400">Smart Windows Manager Dashboard</h1>
      </header>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Window Cards */}
        <div className="flex-1 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {windowsData.length > 0 ? (
            windowsData.map(window => (
              <WindowCard key={window.window_id} windowData={window} window_open={window.window_open} />
            ))
          ) : (
            <p className="text-center text-gray-400 col-span-full">Waiting for windows data...</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;
