import React, { Component } from 'react';
import PropTypes from 'prop-types';

import Paper from 'material-ui/Paper';
import TextField from 'material-ui/TextField';
import FlatButton from 'material-ui/FlatButton';
import Divider from 'material-ui/Divider';
import {orange500} from 'material-ui/styles/colors';


import {api} from './../utils/Api';

class ListContainer extends Component {
    
    constructor(props) {
        super(props);
        this.state={
            searchInput: '',
            searchInputError: false,
            notFound: false,
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
        this.setState({
            notFound: false,
        });
        this.searchSubmit();
    }

    searchSubmit = () =>{
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
                    console.log(response);
                })
        }
    }


    render(){
        return( 
            <div>
                <Paper className="listcontainer" zDepth={1} >
                    <h3 className="app-title">Stipo</h3>
                    <p className="app-desc">SPA, getting data from Yelp Fusion API</p>
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
                    <p className="app-desc">*Data is cached for 3 hours 
                    and list of people attending is updated at 5:00 a.m. (browser time).</p>
                    <Divider/>
                    {
                        this.state.notFound
                        ? (
                            <p className="search-notfound">Nothing was found for: <span>{this.state.searchInput}</span></p>
                        )
                        :(
                            <div></div>
                        )
                    }
                </Paper>
            </div>
        )
    }  
};

ListContainer.propTypes = {
    className: PropTypes.string,
    fetchingToken: PropTypes.bool,
};

export default ListContainer;
