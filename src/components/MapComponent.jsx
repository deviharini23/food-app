import React from 'react';

function MapComponent({ location }) {
  return (
    <iframe
      width="100%"
      height="300"
      style={{ border: 0 }}
      loading="lazy"
      allowFullScreen
      src={`https://www.google.com/maps?q=${location}&output=embed`}
    />
  );
}

export default MapComponent;
