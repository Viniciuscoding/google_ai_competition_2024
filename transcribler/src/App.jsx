// import { useState } from 'react'
import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router-dom';

/* component routes */ 
import Home from './components/Home';

function App() {
  return (
    <>
      <main>
        <BrowserRouter>
          <Routes>
            <Route>
              <Route path="/" element={<Home />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </main>
    </>
  )
}

export default App
