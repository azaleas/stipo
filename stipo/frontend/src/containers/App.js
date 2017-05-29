import React, { Component } from 'react';
import PropTypes from 'prop-types';

import Route from 'react-router-dom/Route';
import Switch from 'react-router-dom/Switch';

import injectTapEventPlugin from 'react-tap-event-plugin';
injectTapEventPlugin();

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';


import {api} from './../utils/Api';
import VARIABLES from './../utils/variables';

import ListContainer from './../containers/ListContainer';

import LoginTwitter from './../containers/LoginTwitter';
import Logout from './../containers/Logout';

import NotFound from './../components/NotFound';

import './../styles/App.css';

class App extends Component {
    
    constructor(props) {
        super(props);
        this.state = {
            fetchingToken: false,
        }
    }

    twitterLoginStart = (event) => {

        localStorage.removeItem('oath_token');
        localStorage.removeItem('oauth_secret');
        localStorage.removeItem('user');
            
        // http://stackoverflow.com/questions/4068373/center-a-popup-window-on-screen
        let dualScreenLeft = window.screenLeft !== undefined ? window.screenLeft : screen.left;
        let dualScreenTop = window.screenTop !== undefined ? window.screenTop : screen.top;

        let width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
        let height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

        let left = ((width / 2) - (570 / 2)) + dualScreenLeft;
        let top = ((height / 2) - (520 / 2)) + dualScreenTop;
        window.open(
            VARIABLES.TWITTER_LOGIN_URL, 
            '_blank', 
            'location=yes,height=400,width=400,scrollbars=yes,status=yes,top=' + top + ',left=' + left + ''
        );
        this.twitterLogin();
    }

    twitterLogin(){
        /*Remove login text while loggging in is in process*/
        let user = localStorage.getItem('user');
        if(user !== '' && typeof user !== 'undefined' && user !== null){
            this.setState({
                fetchingToken: true,
            });
        }
        api.handleTwitterLogin()
            .then((response) =>{
                if(response === 'error'){
                    setTimeout(() => {
                        this.twitterLogin();
                    }, 50);
                }
                else if(response === 'success'){
                    this.setState({
                        fetchingToken: false,
                    });
                }
            })
    }

    render(){
        return(
            <div className="container">
                <MuiThemeProvider>
                    <Switch>
                        <Route 
                            exact path="/" 
                            render={props => 
                                <ListContainer fetchingToken={this.state.fetchingToken} {...props} />
                            } />
                        <Route path="/twitter_logged_in/" component={LoginTwitter} />
                        <Route path="/logout" component={Logout} />
                        <Route path="*" component={NotFound} />
                    </Switch>
                </MuiThemeProvider>
            </div>
        )
    }    
};

App.propTypes = {
    className: PropTypes.string,
};

export default App;