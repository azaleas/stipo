import React from 'react';
import PropTypes from 'prop-types';

import {List, ListItem} from 'material-ui/List';
import Avatar from 'material-ui/Avatar';
import Divider from 'material-ui/Divider';

const ListComponent = (props) => {
    return (
        <div className="search-results">
            <List>
                {
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
