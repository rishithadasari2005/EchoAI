import React, { useEffect, useState } from "react";
import axios from "axios";

export default function App() {
  const [buses, setBuses] = useState([]);
  const [location, setLocation] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:5000/schedule").then((res) => setBuses(res.data));
  }, []);

  const trackBus = async (busId) => {
    const res = await axios.get(`http://localhost:5000/track/${busId}`);
    setLocation(res.data);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">DTC Bus Schedule</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {buses.map((bus) => (
          <div key={bus.bus_id} className="p-4 border rounded shadow">
            <p><strong>Bus:</strong> {bus.bus_id}</p>
            <p><strong>Route:</strong> {bus.route}</p>
            <p><strong>Start Time:</strong> {new Date(bus.start_time).toLocaleTimeString()}</p>
            <p><strong>Status:</strong> {bus.status}</p>
            <button className="mt-2 px-3 py-1 bg-blue-500 text-white rounded" onClick={() => trackBus(bus.bus_id)}>
              Track
            </button>
          </div>
        ))}
      </div>

      {location && (
        <div className="mt-6 p-4 border-t">
          <h2 className="text-xl font-semibold">Tracking Result</h2>
          <p><strong>Bus ID:</strong> {location.bus_id}</p>
          <p><strong>Current Location:</strong> {location.location}</p>
          <p><strong>Coordinates:</strong> {location.coordinates.join(", ")}</p>
        </div>
      )}
    </div>
  );
}
