import React from 'react';
import PropTypes from 'prop-types';

const ListComponent = ({ className }) => {
    return (
        <div>Hello</div>
    );
};

ListComponent.propTypes = {
    className: PropTypes.string,
    data: PropTypes.array,
};

export default ListComponent;
