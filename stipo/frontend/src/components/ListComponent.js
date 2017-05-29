import React from 'react';
import PropTypes from 'prop-types';

import {api} from './../utils/Api';

import {List, ListItem} from 'material-ui/List';
import Avatar from 'material-ui/Avatar';
import Toggle from 'material-ui/Toggle';

const ListComponent = (props) => {
    return (
        <div className="search-results">
            <p>Search returns 20 results</p>
            <List>
                {
                    !api.isLoggedIn()
                    ?(
                        props.data.map((el, index) => (
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
                                     />
                                }
                                className="facility-infoblock"
                                secondaryText={
                                    <p className="facility-info">
                                        Total going: 
                                        <span className="facility-info--stat">
                                            {el.attends.length}
                                        </span>
                                        <br/>
                                        Rating: 
                                        <span className="facility-info--stat">
                                            {el.rating}
                                        </span>
                                    </p>
                                }
                            />
                        ))
                    )
                    :(
                        <p></p>
                    )
                }
            </List>
        </div>
    );
};

ListComponent.propTypes = {
    className: PropTypes.string,
    data: PropTypes.array,
};

export default ListComponent;
