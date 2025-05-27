import React, { useEffect } from 'react';
import axios from 'axios';

function LiveLocation({ userId }) {
  useEffect(() => {
    const updateLocation = (position) => {
      const { latitude, longitude } = position.coords;
      axios.post("http://localhost:8000/update_location", {
        user_id: userId,
        latitude,
        longitude
      }).catch(err => {
        console.error("Location update failed:", err.message);
      });
    };

    const errorHandler = (err) => {
      console.error("Geolocation error:", err.message);
    };

    const watchId = navigator.geolocation.watchPosition(updateLocation, errorHandler, {
      enableHighAccuracy: true,
      maximumAge: 10000,
      timeout: 5000
    });

    return () => navigator.geolocation.clearWatch(watchId);
  }, [userId]);

  return <p>📍 Tracking your live location...</p>;
}

export default LiveLocation;
