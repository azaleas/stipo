import React from 'react';
import PropTypes from 'prop-types';

const moment = require('moment');

import {api} from './../utils/Api';

import {List, ListItem} from 'material-ui/List';
import Avatar from 'material-ui/Avatar';
import Toggle from 'material-ui/Toggle';

const ListComponent = (props) => {
    let user_id;
    /*get only attends until 5 a.m. (convert the time to utc) */
    let currentTime = moment();
    let updateTime = moment().set({
        'hour': 5, 
        'minute': 0,
        'second': 0,
        'millisecond': 0,
    });
    if (currentTime < updateTime){
        updateTime = moment().subtract(1, 'days').set({
            'hour': 5, 
            'minute': 0,
            'second': 0,
            'millisecond': 0,
        });
    }
    if (api.isLoggedIn()){
        user_id = api.getUserId();
    }
    updateTime = moment.utc(updateTime);
    return (
        <div className="search-results">
            <List>
                {
                    !api.isLoggedIn()
                    ?(
                        props.data.map((el, index) => {
                            let totalGoing = 0;
                            if (el.attends.length !== 0){
                                el.attends.forEach((el, index) => {
                                    let attendTime = new Date(el.time);
                                    if (attendTime >= updateTime && el.is_going === true){
                                        totalGoing++;
                                    }
                                });
                            }
                            return (
                                <ListItem
                                    key={el.id}
                                    leftAvatar={<Avatar src={el.image_url} />}
                                    primaryText={
                                        <p className="facility-info--title">
                                            {el.name} | <a href={el.url} target="_blank">Yelp Link</a>
                                        </p>
                                    }
                                    secondaryTextLines={2}
                                    disabled
                                    rightToggle={
                                        <Toggle
                                            thumbStyle={{
                                                backgroundColor: "rgb(245, 216, 162)",
                                            }}
                                            thumbSwitchedStyle={{
                                                backgroundColor: "orange",
                                            }}
                                            trackStyle={{
                                                backgroundColor: "rgba(255, 165, 0, 0.5)",
                                            }}
                                            trackSwitchedStyle={{
                                                backgroundColor: "rgb(245, 216, 162)",
                                            }}
                                            onToggle={props.toggleAttend}
                                         />
                                    }
                                    className="facility-infoblock"
                                    secondaryText={
                                        <p className="facility-info">
                                            Total going: 
                                            <span className="facility-info--stat">
                                                {totalGoing}
                                            </span>
                                            <br/>
                                            Rating: 
                                            <span className="facility-info--stat">
                                                {el.rating}
                                            </span>
                                        </p>
                                    }
                                />
                            )
                        })
                    )
                    :(
                        props.data.map((el, index) => {
                            let totalGoing = 0;
                            let userGoing = false;
                            if (el.attends.length !== 0){
                                el.attends.forEach((el, index) => {
                                    let attendTime = new Date(el.time);
                                    if (attendTime >= updateTime && el.is_going === true){
                                        totalGoing++;
                                        if(parseInt(user_id, 10) === parseInt(el.user, 10)){
                                            userGoing = true;
                                        }
                                    }
                                });
                            }
                            if(props.totalGoing[el.id] >= 0){
                                totalGoing = props.totalGoing[el.id];
                            }
                            return(
                                <ListItem
                                    key={el.id}
                                    leftAvatar={<Avatar src={el.image_url} />}
                                    primaryText={
                                        <p className="facility-info--title">
                                            {el.name} | <a href={el.url} target="_blank">Yelp Link</a>
                                        </p>
                                    }
                                    secondaryTextLines={2}
                                    disabled
                                    rightToggle={
                                        <Toggle
                                            thumbStyle={{
                                                backgroundColor: "rgb(245, 216, 162)",
                                            }}
                                            thumbSwitchedStyle={{
                                                backgroundColor: "orange",
                                            }}
                                            trackStyle={{
                                                backgroundColor: "rgba(255, 165, 0, 0.5)",
                                            }}
                                            trackSwitchedStyle={{
                                                backgroundColor: "rgb(245, 216, 162)",
                                            }}
                                            defaultToggled={userGoing ? true : false}
                                            onToggle={(event, isInputChecked) => {
                                                props.toggleAttend(el.id, isInputChecked, totalGoing);
                                            }}
                                         />
                                    }
                                    className="facility-infoblock"
                                    secondaryText={
                                        <p className="facility-info">
                                            Total going: 
                                            <span className="facility-info--stat">
                                                {totalGoing}
                                            </span>
                                            <br/>
                                            Rating: 
                                            <span className="facility-info--stat">
                                                {el.rating}
                                            </span>
                                        </p>
                                    }
                                />
                            )
                        })
                    )
                }
            </List>
        </div>
    );
};

ListComponent.propTypes = {
    className: PropTypes.string,
    data: PropTypes.array,
    toggleAttend: PropTypes.func,
    totalGoing: PropTypes.object,
};

export default ListComponent;
