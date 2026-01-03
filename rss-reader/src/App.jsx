import { useState } from 'react'
import './App.css'
import RssReader from './RssReader.jsx'

function App() {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = () => {
    console.log('Search for:', searchQuery);
    // Add your search logic here
  };

  console.log("App is rendering");

  return (
    <div className="App">
      <nav className='navbar'>
        <div className='search-box'>
          <input 
            type="text" 
            placeholder='Search news...'
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button onClick={handleSearch}>Search</button>
        </div>
      </nav>
      <h1>News Reader</h1>
      <div className='content'>
        <RssReader />
      </div>
    </div>
  )
}

export default App