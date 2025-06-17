import { ofetch } from "ofetch";

const LOCAL = "http://localhost:6060";
// const PRODUCTION = "http://119.3.226.59:6060";

const BASE_URL = LOCAL;

export const get = async (url: string, params?: any) => {
    const res = await ofetch(BASE_URL + url, {
        method: "GET",
        params,
    });
    return JSON.parse(res);
};

export const post = async (url: string, data?: any, params?: any) => {
    const payload = params
        ? {
              method: "POST",
              params,
              body: data,
          }
        : {
              method: "POST",
              body: data,
          };
    const res = await ofetch(BASE_URL + url, payload);
    return JSON.parse(res);
};
