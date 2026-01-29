import React from 'react';
import SearchBar from './SearchBar';

const TopBar = ({ searchValue, onSearchChange, searchPlaceholder, actions }) => {
    return (
        <div className="top-bar">
            <SearchBar 
                value={searchValue}
                onChange={onSearchChange}
                placeholder={searchPlaceholder}
            />
            <div className="top-bar-actions">
                {actions}
            </div>
        </div>
    );
};

export default TopBar;
