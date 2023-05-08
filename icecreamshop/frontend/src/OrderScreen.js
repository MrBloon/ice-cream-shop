import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import axios from 'axios'
import OrderItem from './OrderItem'
import { useGetFlavors, usePostOrder } from "./api/apiCall"
import { useGetIceCreamTubs } from "./api/apiCall"

function OrderScreen() {
  const [orderItemCount, setOrderItemCount] = useState(0);
  const [isAddingItem, setIsAddingItem] = useState(false)
  const [isClickable, setIsClickable] = useState(false)
  const [orderId, setOrderId] = useState(null)
  const [email, setEmail] = useState('')
  const { data, status } = useGetIceCreamTubs()

  const handleAddItemClick = () => {
    setOrderItemCount(orderItemCount + 1)
    setIsAddingItem(true)
  }

  const createOrderMutation = useMutation((email) =>
    axios.post('http://localhost:8000/orders/', { email }),
    {
      onSuccess: (data) => {
        setIsClickable(true)
      },
    }
  )

  const addOrderItemMutation = useMutation((orderItem) =>
    axios.post(`http://localhost:8000/orders/${orderId}/order_items`, orderItem)
  )

  const handleEmailChange = (event) => {
    setEmail(event.target.value)
  }

  const handleCreateOrder = () => {
    email && createOrderMutation.mutate(email)
  }

  if (createOrderMutation.isLoading) {
    return <p>Creating order...</p>
  }

  if (createOrderMutation.isError) {
    const errorMessage = createOrderMutation.error.response.data.email;
    return <p>Error creating order: {errorMessage}</p>
  }

  return (
    <div>
      <label htmlFor="name">Email :</label>
      <input type="email" id="email" value={email} onChange={handleEmailChange} />
      <button onClick={handleCreateOrder} type="submit">Submit</button>
      <button disabled={!isClickable} onClick={handleAddItemClick}>Add item to order</button>
      {isAddingItem && (
        [...Array(orderItemCount)].map((_, index) => (
          <OrderItem key={index} icecream_tubs={data}/>
        ))
      )}
    </div>
  );
}

export default OrderScreen;