import { apiRequest } from "./client";
const options=(token)=>({token});
export const getFavorites=(token)=>apiRequest("/api/v1/favorites",options(token));
export const addFavorite=(token,placeId)=>apiRequest(`/api/v1/favorites/${placeId}`,{...options(token),method:"POST",successMessage:"Добавлено в избранное"});
export const removeFavorite=(token,placeId)=>apiRequest(`/api/v1/favorites/${placeId}`,{...options(token),method:"DELETE",successMessage:"Удалено из избранного"});
