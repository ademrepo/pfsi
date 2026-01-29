import React from 'react';
import { Search } from 'lucide-react';

const SearchBar = ({ value, onChange, placeholder = "Rechercher..." }) => {
    return (
        <div className="search-bar">
            <Search size={18} className="search-icon" />
            <input 
                type="text" 
                placeholder={placeholder}
                value={value}
                onChange={(e) => onChange(e.target.value)}
            />
        </div>
    );
};

export default SearchBar;
