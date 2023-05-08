import { useState, useEffect } from 'react'
import OrderItem from '../components/OrderItem'
import { useGetIceCreamTubs, useGetFlavors, usePostOrder } from "../api/apiCall"

function OrderScreen() {
  const [orderItemCount, setOrderItemCount] = useState(0)
  const [isAddingItem, setIsAddingItem] = useState(false)
  const [isClickable, setIsClickable] = useState(false)
  const [orderId, setOrderId] = useState(null)
  const [email, setEmail] = useState('')
  const { data: iceCreamTubData, status: iceCreamStatus } = useGetIceCreamTubs()
  const { data: flavorData, status: flavorStatus } = useGetFlavors()
  const { mutate, isSuccess, isLoading, isError, error } = usePostOrder(setOrderId)

  const handleAddItemClick = () => {
    setOrderItemCount(orderItemCount + 1)
    setIsAddingItem(true)
  }
 
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
          <OrderItem key={index} icecream_tubs={iceCreamTubData} flavors={flavorData} orderId={orderId}/>
        ))
      )}
    </div>
  );
}

export default OrderScreen;