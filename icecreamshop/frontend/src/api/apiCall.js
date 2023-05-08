import { useMutation, useQuery } from "@tanstack/react-query"
import { axiosInstance } from "./config"
import { endpoint } from "./endpoint"

export const useGetFlavors = () => {
  const getFlavors = async () => {
    const { data } = await axiosInstance.get(endpoint.get_flavors)
    return data;
  };

  return useQuery([endpoint.get_flavors], getFlavors);
}

export const useGetIceCreamTubs = () => {
  const getIceCreamTubs = async () => {
    const { data } = await axiosInstance.get(endpoint.get_icecream_tubs)
    return data
  };

  return useQuery([endpoint.get_icecream_tubs], getIceCreamTubs);
}

export const usePostOrder = (setOrderId) => {
  return useMutation((email) => axiosInstance.post(endpoint.post_order, { email }), {
    onSuccess: (data) => { 
      setOrderId(data.data.id)
    }
  })
}

export const usePostOrderItem = () => {
  return useMutation(({scoopsRequested, selectedIceCreamTub, orderId}) => axiosInstance.post(`${endpoint.post_order}${orderId}/order_items/`, { scoopsRequested, selectedIceCreamTub }), {
    onSuccess: (data) => { 
      console.log(data.data)
    }, 
    onError: (error) => { 
      console.log(error)
    },  
  })
}
