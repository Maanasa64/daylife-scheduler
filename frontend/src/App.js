import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    goals: '',
    constraints: '',
    wakeupTime: '8:00 AM',
    bedtime: '11:00 PM'
  });
  const [schedule, setSchedule] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const generateSchedule = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/generate-schedule', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          goals: formData.goals,
          constraints: formData.constraints,
          preferred_wakeup: formData.wakeupTime,
          preferred_bedtime: formData.bedtime
        }),
      });
  
      const data = await response.json();
      
      if (!response.ok) {
        const errorDetail = data.detail || 
          (data.error ? JSON.stringify(data.error) : 'Unknown error');
        throw new Error(`Server error: ${response.status} - ${errorDetail}`);
      }
      
      if (!data.schedule || !Array.isArray(data.schedule)) {
        throw new Error('Invalid schedule format received from server');
      }
      
      setSchedule(data.schedule);
      
    } catch (err) {
      setError(err.message);
      console.error('API Request Failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const exportToCalendar = async () => {
    try {
      const response = await fetch('http://localhost:8000/export-calendar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(schedule),
      });

      if (!response.ok) {
        throw new Error('Failed to generate calendar file');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'daily_schedule.ics';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      
    } catch (err) {
      setError(err.message);
      console.error('Calendar export failed:', err);
    }
  };

  return (
    <div className="container">
      <h1>DayLife Scheduler with Groq AI</h1>
      <p>Create your optimized daily schedule with Groq's ultra-fast AI</p>
      
      <div className="input-section">
        <div className="form-group">
          <label>Your Goals:</label>
          <textarea
            name="goals"
            value={formData.goals}
            onChange={handleChange}
            placeholder="e.g., Job applications, gym, LeetCode, project work"
            disabled={loading}
          />
        </div>
        
        <div className="form-group">
          <label>Constraints:</label>
          <textarea
            name="constraints"
            value={formData.constraints}
            onChange={handleChange}
            placeholder="e.g., CSE 150A class MWF 1-2pm"
            disabled={loading}
          />
        </div>
        
        <div className="time-preferences">
          <div className="form-group">
            <label>Wake Up Time:</label>
            <input
              type="text"
              name="wakeupTime"
              value={formData.wakeupTime}
              onChange={handleChange}
              disabled={loading}
            />
          </div>
          
          <div className="form-group">
            <label>Bedtime:</label>
            <input
              type="text"
              name="bedtime"
              value={formData.bedtime}
              onChange={handleChange}
              disabled={loading}
            />
          </div>
        </div>
        
        <button 
          onClick={generateSchedule} 
          disabled={loading || !formData.goals.trim()}
        >
          {loading ? 'Generating with Groq...' : 'Generate Schedule'}
        </button>
      </div>
      
      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {schedule.length > 0 && (
        <div className="schedule-results">
          <div className="schedule-header">
            <h2>Your AI-Generated Schedule</h2>
            <button 
              onClick={exportToCalendar}
              className="export-button"
              disabled={loading}
            >
              Export to Apple Calendar
            </button>
          </div>
          <div className="schedule-grid">
            {schedule.map((block, index) => (
              <div key={index} className={`schedule-block ${block.category}`}>
                <div className="time">{block.start_time} - {block.end_time}</div>
                <div className="activity">{block.activity}</div>
                <div className="category">{block.category}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;