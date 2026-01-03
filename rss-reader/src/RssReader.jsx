import { useEffect, useState } from 'react';

function RssReader() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  
  const fetchRSS = () => {
    setLoading(true);
    setError(null);
    
    // Add timestamp to prevent caching
    const timestamp = new Date().getTime();
    const RSS_URL = `https://api.rss2json.com/v1/api.json?rss_url=https://raw.githubusercontent.com/mbikal/news/main/rss/rss.xml&_=${timestamp}`;
    
    fetch(RSS_URL, {
      cache: 'no-cache',
      headers: {
        'Cache-Control': 'no-cache'
      }
    })
      .then((res) => {
        console.log("Response status:", res.status);
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("Full RSS Data:", data);
        console.log("Status:", data.status);
        console.log("Items:", data.items);
        
        if (data.status === 'ok') {
          if (data.items && data.items.length > 0) {
            setItems(data.items);
            setLastUpdated(new Date());
          } else {
            setError("RSS feed is empty - no items found");
          }
        } else {
          setError(`RSS API Error: ${data.message || 'Unknown error'}`);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load RSS", err);
        setError(`Network error: ${err.message}`);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchRSS();
  }, []);

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', borderBottom: '2px solid #333', paddingBottom: '10px' }}>
        <h2 style={{ margin: 0 }}>News Feed</h2>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '5px' }}>
          <button 
            onClick={fetchRSS} 
            disabled={loading}
            style={{
              padding: '8px 16px',
              background: loading ? '#ccc' : '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontSize: '14px',
              fontWeight: '500'
            }}
          >
            {loading ? 'Refreshing...' : '🔄 Refresh'}
          </button>
          {lastUpdated && (
            <small style={{ color: '#666', fontSize: '12px' }}>
              Last updated: {lastUpdated.toLocaleTimeString()}
            </small>
          )}
        </div>
      </div>

      {loading && items.length === 0 && (
        <p style={{ textAlign: 'center', color: '#666', padding: '40px' }}>
          Loading news...
        </p>
      )}
      
      {error && (
        <div style={{ 
          padding: '15px', 
          background: '#fee', 
          border: '1px solid #fcc', 
          borderRadius: '4px',
          color: '#c00',
          marginBottom: '20px'
        }}>
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {!loading && !error && items.length === 0 && (
        <p style={{ textAlign: 'center', color: '#666', padding: '40px' }}>
          No news items found.
        </p>
      )}

      {items.length > 0 && (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {items.map((item, index) => (
            <li 
              key={index} 
              style={{
                padding: '15px',
                marginBottom: '10px',
                background: '#f9f9f9',
                borderRadius: '6px',
                borderLeft: '4px solid #007bff'
              }}
            >
              <a 
                href={item.link} 
                target="_blank" 
                rel="noopener noreferrer"
                style={{
                  color: '#007bff',
                  textDecoration: 'none',
                  fontSize: '16px',
                  fontWeight: '500',
                  display: 'block',
                  marginBottom: '8px'
                }}
                onMouseOver={(e) => e.target.style.textDecoration = 'underline'}
                onMouseOut={(e) => e.target.style.textDecoration = 'none'}
              >
                {item.title}
              </a>
              <small style={{ color: '#666', fontSize: '13px' }}>
                📅 {new Date(item.pubDate).toLocaleString()}
              </small>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default RssReader;