import React from 'react';

function Recommendation({ data }) {
  return (
    <div>
      <p><strong>You said:</strong> {data.order_text}</p>
      <p><strong>Suggested Dish:</strong> {data.suggestion}</p>
      <p><strong>Detected Location:</strong> {data.location}</p> {/* Add this line */}
    </div>
  );
}

export default Recommendation;
