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






export const usePostOrder = () => {
  const { mutate: mutateOrderId } = useMutation(
    (id) =>
      axiosInstance.post(`${endpoint.post_order_id}/${id}/order_items`, {
        scoops_requested: 2,
        ice_cream_tub: 1,
      }),
    {
      onSuccess(response) {
        console.log("c'est genial !");
      },
      onError(error) {
        console.log(error);
      },
    }
  );

  return useMutation(
    (email) => axiosInstance.post(endpoint.post_order, { email }),
    {
      onSuccess(response) {
        mutateOrderId(response?.data?.id);

        ///

        // do something
      },
      onError(error) {
        console.log(error);
      },
    }
  );
};
