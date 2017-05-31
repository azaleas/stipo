import React from 'react';
import { shallow } from 'enzyme';
import ListContainer from './../containers/ListContainer';
import ListComponent from './../components/ListComponent';
import {api} from './../utils/Api';


jest.mock('./../utils/Api');

const data = [
    {
        "id": 18,
        "name": "Arendsnest",
        "location": "Amsterdam",
        "rating": "4.5",
        "url": "https://www.yelp.com/biz/arendsnest-amsterdam-2?adjust_creative=jos-y9cCoGyrA2dE3OOVrg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=jos-y9cCoGyrA2dE3OOVrg",
        "image_url": "https://s3-media1.fl.yelpcdn.com/bphoto/FurcfTuqaYBv_q34bGTK5g/o.jpg",
        "attends": [
            {
                "user": 3,
                "is_going": true,
                "time": 1496205599000.0
            },
            {
                "user": 4,
                "is_going": false,
                "time": 1496205150000.0
            },
        ]
    },
]

describe('ListContainer', () => {
    let wrapper;

    let pathname = {
        pathname: '/',
    }

    beforeEach(() => {
        wrapper = shallow(<ListContainer location={pathname} />);
        api.isLoggedIn.mockImplementation(() => true);
        api.searchLocation.mockImplementation(() => {
            let response = new Promise((resolve, reject) =>{
                resolve(data);
            });
            return response;
        });

        api.attendLocation.mockImplementation(() => {
            let response = new Promise((resolve, reject) =>{
                resolve('saved');
            });
            return response;
        });
    });
    

    afterEach(() => {
        api.searchLocation.mockClear();
        api.attendLocation.mockClear();
        api.isLoggedIn.mockClear();
    });

    it('renders without crashing', () => {
        wrapper;
    });

    it('should have `LinearProgress` element when fetching data', () => {
        wrapper.setState({
            fetchingData: true,
            noData: true,
            notFound: false,
        });
        expect(
            wrapper.find('LinearProgress').exists()
        ).toBe(true);   
    });

    it('should have `ListComponent` element when data is returned', () => {
        wrapper.setState({
            noData: false,
            searchInput: 'Amsterdam',
        });
        wrapper.instance().searchSubmit();
        return api.searchLocation()
            .then((response) =>{
                expect(response).toEqual(data);
                expect(
                    wrapper.state().data
                ).toEqual(data);
                expect(
                    wrapper.find('ListComponent').exists()
                ).toBe(true);  
            });  
    });

    it('should have `.search-notfound` element when nothing found', () => {
        wrapper.setState({
            notFound: true,
        });
        expect(
            wrapper.find('.search-notfound').exists()
        ).toBe(true);   
    });

    it('should have `.app-user` element when user Logged In', () => {
        api.isLoggedIn();
        expect(
            wrapper.find('.app-user').exists()
        ).toBe(true);   
    });

    describe('ListComponent Component', ()=> {
        let list;
        beforeEach(() => { 
            wrapper.setState({
                data: data,
            });           
            wrapper.update();
            list = shallow(
                    <ListComponent 
                        data={wrapper.state().data}
                        toggleAttend={wrapper.instance().handletoggleAttend}
                        totalGoing={wrapper.state().totalGoing}
                          />
            );
        });
        
        it('renders without crashing', () => {
            list;
        });
    });
})  
