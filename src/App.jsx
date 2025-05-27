import React, { useState } from 'react';
import VoiceInput from './components/VoiceInput';
import Recommendation from './components/Recommendation';
import LoginPage from './components/LoginPage';
import LiveLocation from './components/LiveLocation'; // ✅ NEW

function App() {
  const [userId, setUserId] = useState(null);
  const [response, setResponse] = useState(null);

  if (!userId) {
    return <LoginPage setUserId={setUserId} />;
  }

  return (
    <div>
      <h1>Food Delivery App</h1>
      <VoiceInput userId={userId} setResponse={setResponse} />
      <LiveLocation userId={userId} /> {/* ✅ NEW */}
      {response && <Recommendation data={response} />}
    </div>
  );
}

export default App;
