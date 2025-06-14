import { ofetch } from "ofetch";

const BASE_URL = "http://localhost:6060";

export const get = async (url: string, params?: any) => {
    const res = await ofetch(BASE_URL + url, {
        method: "GET",
        params,
    });
    return JSON.parse(res);
};

export const post = async (url: string, data?: any) => {
    const res = await ofetch(BASE_URL + url, {
        method: "POST",
        body: data,
    });
    return JSON.parse(res);
};
