import Vue from 'vue'
import axios from "axios";


const request = async args => {
    const {
        method = 'GET',
        url,
        params = {},
        headers = {},
        body
    } = args

    const config = {
        url,
        method,
        params,
        headers,
        data: body
    }

    return axios(config)
}

const methods = {
    $get: async (url, params, headers) => {
        console.log("headers", headers)
        const response = await request({
            url,
            params,
            headers,
            method: 'GET'
        })

        return response.data
    }

    , $post : async (url, body, headers) => {
        const response = await request({
            url,
            headers,
            method: 'POST',
            body
        })
        return response.data
    }

    , $put : async (url, body, headers) => {
        const response = await request({
            url,
            headers,
            method: 'PUT',
            body
        })
        return response.data
    }

    , $patch : async (url, body, headers) => {
        const response = await request({
            url,
            headers,
            method: 'PATCH',
            body
        })
        return response.data
    },

    $deleteRequest : async (url, headers) => {
        const response = await request({
            url,
            headers,
            method: 'DELETE'
        })
        return response.data
    }
}


export const Request = {
    install(Vue) {
        for (let m in methods) {
            Vue.prototype[m] = methods[m];
        }
    }
}

Vue.use(Request);