import { useEffect, useState } from 'react';
import './App.css';

function RssReader() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const RSS_URL = "https://api.rss2json.com/v1/api.json?rss_url=https://mbikal.github.io/news/rss/rss.xml";

  useEffect(() => {
    fetch(RSS_URL)
      .then((res) => {
        console.log("Response status:", res.status);
        return res.json();
      })
      .then((data) => {
        console.log("Full RSS Data:", data);
        console.log("Status:", data.status);
        console.log("Items:", data.items);
        
        if (data.status === 'ok') {
          if (data.items && data.items.length > 0) {
            setItems(data.items);
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
  }, []);

  if (loading) return <p className="loading">Loading news...</p>;
  if (error) return <p className="loading">Error: {error}</p>;
  if (items.length === 0) return <p className="loading">No news items found.</p>;

  return (
    <div className="rss-container">
      <h2>News Feed</h2>
      <ul className="news-list">
        {items.map((item, index) => (
          <li key={index} className="news-item">
            <a href={item.link} target="_blank" rel="noopener noreferrer">
              {item.title}
            </a>
            <br />
            <small className="news-date">{new Date(item.pubDate).toLocaleString()}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RssReader;