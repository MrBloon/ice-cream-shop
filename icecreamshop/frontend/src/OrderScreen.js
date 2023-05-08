import { useState, useEffect } from 'react'
import { useMutation } from '@tanstack/react-query'
import axios from 'axios'
import OrderItem from './OrderItem'
import { useGetIceCreamTubs, useGetFlavors, usePostOrder } from "./api/apiCall"

function OrderScreen() {
  const [orderItems, setOrderItems] = useState([
    {
      "scoops_requested": 2,
      "ice_cream_tub": 1
    }
  ]);
  const [orderItemCount, setOrderItemCount] = useState(0);
  const [isAddingItem, setIsAddingItem] = useState(false)
  const [isClickable, setIsClickable] = useState(false)
  const [orderId, setOrderId] = useState(null)
  const [email, setEmail] = useState('')
  const { data: iceCreamTubData, status: iceCreamStatus } = useGetIceCreamTubs();
  const { data: flavorData, status: flavorStatus } = useGetFlavors();
  const { mutate, isSuccess, isLoading, isError, error } = usePostOrder()

  const onAddItem = (orderItem) => {
    setOrderItems(prev => ({...prev, orderItem}) )
  }
  

  const handleAddItemClick = () => {
    setOrderItemCount(orderItemCount + 1)
    setIsAddingItem(true)
  }
 
  const addOrderItemMutation = useMutation((orderItem) =>
    axios.post(`http://localhost:8000/orders/${orderId}/order_items`, orderItem)
  )

  const handleEmailChange = (event) => {
    setEmail(event.target.value)
  }

  const handleCreateOrder = () => {
    email && mutate(email)
  }

  useEffect(() => {
    if (isSuccess) {
      setIsClickable(true);
    }
  }, [isSuccess])

  if (isLoading) {
    return <p>Creating order...</p>
  }

  if (isError) {
    const errorMessage = error.response.data.email;
    return <p>Error creating order: {errorMessage}</p>
  }

  return (
    <div className="form-container">
      <label className="label" htmlFor="email">Email:</label>
      <input
        className="input"
        type="email"
        id="email"
        value={email}
        onChange={handleEmailChange}
      />
      <button className="button submit" onClick={handleCreateOrder} type="submit">
        Create Order
      </button>
      <button
        className={`button ${isClickable ? "clickable" : "not-clickable"}`}
        onClick={handleAddItemClick}
        disabled={!isClickable}
      >
        Add item to order
      </button>
      {isAddingItem && (
        [...Array(orderItemCount)].map((_, index) => (
          <OrderItem key={index} icecream_tubs={iceCreamTubData} flavors={flavorData}/>
        ))
      )}
    </div>
  );
}

export default OrderScreen;