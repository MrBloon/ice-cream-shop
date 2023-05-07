import React, { useState, useEffect } from 'react'
import axios from 'axios'

function OrderScreen() {
  const [flavors, setFlavors] = useState([]);
  console.log(flavors);
  useEffect(() => {
  axios.get('http://localhost:8000/flavors/')
    .then(response => {
      setFlavors(response.data);
    })
    .catch(error => {
      console.log(error);
    });
  }, [])

  return (
    <div>
      <h1>Enter your email</h1>
    </div>
  );
}

export default OrderScreen;