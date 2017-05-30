import axios from 'axios';
// import Cookies from 'universal-cookie';

const API_STEM = '/api/v1';
const API_STEM_AUTH = '/rest-auth';

class Api{

    constructor() {
        if(localStorage.getItem('token') === null){
            this.token = null;
        }
        else{
            this.token = localStorage.getItem('token');
        }
    }

    searchLocation(location){
        let URL = `${API_STEM}/places/searchplaces/`;

        return axios.post(
                URL, 
                {
                    location,
                }
            )
            .then((response) => {
                return response.data;
            })
            .catch((error) => {
                if (error.response.status === 404){
                    return error.response.status;
                }
                else{
                    console.warn(error);
                }
            })
    }

    attendLocation(facilityId, toggleValue){
        let URL = `${API_STEM}/places/${facilityId}/attend/`;
        let config = {
            headers: {"Authorization": "Token " + this.token},
        };
        return axios.post(
                URL, 
                {
                    "is_going": toggleValue,
                },
                config
            )
            .then((response) => {
                return response.data;
            })
            .catch((error) => {
                console.warn(error.response);
            })
    }

    handleTwitterLogin(){
        let URL = `${API_STEM_AUTH}/twitter/`;

        let access_token = localStorage.getItem('oath_token');
        let token_secret = localStorage.getItem('oauth_secret');
        if(access_token && token_secret){
            return axios.post(
                    URL, 
                    {
                        access_token,
                        token_secret
                    },
                )
                .then((response) => {
                    let token = response.data.key;
                    localStorage.setItem('token', token);
                    this.token = token;
                    localStorage.removeItem('oath_token');
                    localStorage.removeItem('oauth_secret');

                    return 'success';
                })
                .catch((error) => {
                    console.warn(error.response);
                })
        }
        else{
            let promise = new Promise((resolve, reject) =>{
                resolve('error');
            });
            return promise;
        }
    }

    saveTwitterTokens(oath_token, oauth_secret, user, user_id){
        localStorage.removeItem('oath_token');
        localStorage.removeItem('oauth_secret');
        localStorage.removeItem('user');
        localStorage.removeItem('user_id');
        localStorage.setItem('oath_token', oath_token);
        localStorage.setItem('oauth_secret', oauth_secret);
        localStorage.setItem('user', user);
        localStorage.setItem('user_id', user_id);
    }

    handleLogout(){
        localStorage.removeItem('oath_token');
        localStorage.removeItem('oauth_secret');
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('user_id');
        this.token = null;
        let URL = `${API_STEM_AUTH}/logout/`;
        let config = {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        };
        axios.post(
            URL,
            config
        )
        .catch((error) => {
            console.warn(error.response);
        })
    }

    isLoggedIn(){
        return !!this.token;
    }

    getUsername(){
        return localStorage.getItem('user');
    }
    getUserId(){
        return localStorage.getItem('user_id');
    }
}

export const api = new Api();