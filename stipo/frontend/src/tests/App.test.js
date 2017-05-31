import React from 'react';
import { shallow } from 'enzyme';
import App from './../containers/App';
import {api} from './../utils/Api';

jest.mock('./../utils/Api');

describe('App', () => {
    let wrapper;

    beforeEach(() => {
        wrapper = shallow(<App />);
        wrapper.setState({loggedIn: false});
        wrapper.update();
    });

    afterEach(() => {
        api.handleTwitterLogin.mockClear();
    });
    
    it('renders without crashing', () => {
        wrapper;
    });

    it('should have the `div` with class ".container"', () => {
        expect(
            wrapper.find(".container").exists()
        ).toBe(true);
    });

    describe('Login', () => {
        beforeEach(() => {
            api.handleTwitterLogin.mockImplementation(() => {
                let response = new Promise((resolve, reject) =>{
                    resolve('success');
                });
                return response;
            });
            wrapper.update();
        });
        it('should login when `twitterLoginStart` is triggered', () => {
            wrapper.instance().twitterLoginStart();
            return api.handleTwitterLogin()
                .then((response) =>{
                    expect(response).toEqual('success');
                    expect(
                        wrapper.state().loggedIn
                    ).toEqual(true);
                });
        })
    });
})  
