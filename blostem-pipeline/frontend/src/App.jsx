import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Pipeline from './pages/Pipeline';
import ActivationTracker from './pages/ActivationTracker';
import SequenceViewer from './pages/SequenceViewer';
import ActivityFeedPage from './pages/ActivityFeedPage';
import EmailHistoryPage from './pages/EmailHistoryPage';

export default function App() {
  return (
    <Router>
      <div className="flex">
        <Sidebar />
        <Routes>
          <Route path="/" element={<Pipeline />} />
          <Route path="/activation" element={<ActivationTracker />} />
          <Route path="/sequences" element={<SequenceViewer />} />
          <Route path="/activity" element={<ActivityFeedPage />} />
          <Route path="/email-history" element={<EmailHistoryPage />} />
        </Routes>
      </div>
    </Router>
  );
}
