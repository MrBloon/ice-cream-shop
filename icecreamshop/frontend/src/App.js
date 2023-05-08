import './App.css'
import React from 'react'
import { HashRouter as Router, Routes, Route } from 'react-router-dom'
import OrderScreen from './OrderScreen'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<OrderScreen/>} />
      </Routes>
    </Router>
  )
}

export default App;
