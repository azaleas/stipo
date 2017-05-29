import React, { Component } from 'react';
import PropTypes from 'prop-types';

import Link from 'react-router-dom/Link';

import Paper from 'material-ui/Paper';
import TextField from 'material-ui/TextField';
import FlatButton from 'material-ui/FlatButton';
import LinearProgress from 'material-ui/LinearProgress';
import Divider from 'material-ui/Divider';
import {orange500} from 'material-ui/styles/colors';


import {api} from './../utils/Api';

import ListComponent from './../components/ListComponent';

class ListContainer extends Component {
    
    constructor(props) {
        super(props);
        this.state={
            searchInput: '',
            searchInputError: false,
            notFound: false,
            noData: true,
            fetchingData: false,
            data: {},
        }
    }

    onSearchChange = (event) =>{
        if (this.state.notFound){
            this.setState({
                notFound: false,
            });
        }
        this.setState({
            searchInput: event.target.value,
            searchInputError: false, 
        });
    }

    handleKeyDown = (event) =>{
        if (event.key === "Enter"){
            this.searchSubmit();
        }
    }

    onSearchSubmit = (event) =>{
        this.searchSubmit();
    }

    searchSubmit = () =>{
        this.setState({
            notFound: false,
            noData: true,
            fetchingData: true,
        });
        if (!this.state.searchInput){
            this.setState({
                searchInputError: true,
            });
        }
        else{
            let searchInput = this.state.searchInput;
            api.searchLocation(searchInput)
                .then((response) => {
                    if (response === 404){
                        this.setState({
                            notFound: true,
                        });
                    }
                    else{
                        this.setState({
                            notFound: false,
                            data: response,
                            noData: false,
                            fetchingData: false,
                        })
                    }
                    console.log(response);
                })
        }
    }

    handletoggleAttend = (event, isInputChecked) =>{
        if (!api.isLoggedIn()){
            event.preventDefault();
            this.props.twitterLoginStart();
        }
    }


    render(){
        return( 
            <div>
                <Paper className="listcontainer" zDepth={1} >
                    <h3 className="app-title">Stipo</h3>
                    <p className="app-desc">
                        SPA, getting data from 
                        <a 
                            target="_blank"
                            href="https://www.yelp.com/developers/documentation/v3">
                                Yelp Fusion API
                        </a>
                    </p>
                    {
                        api.isLoggedIn()
                        ?(
                            <p className="app-user">Hello, {api.getUsername()}. 
                                <Link 
                                    to="/logout">
                                    Logout
                                </Link>
                            </p>
                        )
                        :(
                            <p></p>
                        )
                    }
                    <div className="app-searchblock">
                        <div className="app-searchblock--textinput">
                            <TextField
                                onChange={this.onSearchChange}
                                onKeyDown={this.handleKeyDown}
                                value={this.state.searchInput}
                                hintText={((this.state.searchInputError) ? "Can't be empty!.." : "Type in location...")}
                                underlineFocusStyle={{
                                    borderColor: orange500,
                                }}
                                underlineStyle={{
                                    borderColor: ((this.state.searchInputError) ? "red" : "#f1f1f1")
                                }}
                            />
                        </div>
                        <div className="app-searchblock--submit">
                            <FlatButton 
                                label="Search"
                                backgroundColor="#f1f1f1"
                                hoverColor={orange500}
                                onTouchTap={this.onSearchSubmit}
                            />
                        </div>
                    </div>
                    <p className="app-desc">*Data from Yelp API is cached for 24 hours 
                    and list of people attending is updated at 5:00 a.m. (browser time).</p>
                    <Divider/>
                    <div className="app-content">
                        {
                            this.state.notFound
                            ? (
                                <p className="search-notfound">Nothing was found for: <span>{this.state.searchInput}</span></p>
                            )
                            :(
                                !this.state.noData
                                ? (
                                    <ListComponent 
                                        data={this.state.data}
                                        toggleAttend={this.handletoggleAttend}
                                    />
                                )
                                :(
                                    this.state.fetchingData
                                    ?(
                                        <div className="search-progress">
                                            <LinearProgress 
                                                mode="indeterminate"
                                                color={orange500} />
                                            <p>Fetching the data...</p>
                                        </div>
                                    )
                                    :(
                                        <p></p>
                                    )
                                )
                            )
                        }
                    </div>
                </Paper>
            </div>
        )
    }  
};

ListContainer.propTypes = {
    className: PropTypes.string,
    fetchingToken: PropTypes.bool,
    twitterLoginStart: PropTypes.func,
};

export default ListContainer;
