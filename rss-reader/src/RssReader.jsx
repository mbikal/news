import { useEffect, useState } from 'react';

function RssReader() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchRSS = () => {
    setLoading(true);
    setError(null);

    // Prevent caching
    const timestamp = new Date().getTime();
    const JSON_URL = `https://raw.githubusercontent.com/mbikal/news/main/rss/rss_feed.json?_=${timestamp}`;

    fetch(JSON_URL, { cache: 'no-cache' })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("RSS JSON:", data);

        if (data.items && data.items.length > 0) {
          setItems(data.items);
          setLastUpdated(new Date());
        } else {
          setError("RSS feed is empty");
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
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
        <h2>News Feed</h2>
        <div>
          <button onClick={fetchRSS} disabled={loading}>
            {loading ? 'Refreshing...' : '🔄 Refresh'}
          </button>
          {lastUpdated && (
            <div style={{ fontSize: '12px', color: '#666' }}>
              Last updated: {lastUpdated.toLocaleTimeString()}
            </div>
          )}
        </div>
      </div>

      {loading && <p>Loading news...</p>}

      {error && (
        <div style={{ color: 'red', marginBottom: '15px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {!loading && !error && items.length === 0 && <p>No news items found.</p>}

      {items.length > 0 && (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {items.map((item, index) => (
            <li key={index} style={{ marginBottom: '15px' }}>
              <a href={item.link} target="_blank" rel="noopener noreferrer">
                {item.title}
              </a>
              {item.published && (
                <div style={{ fontSize: '12px', color: '#666' }}>
                  📅 {new Date(item.published).toLocaleString()}
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default RssReader;
