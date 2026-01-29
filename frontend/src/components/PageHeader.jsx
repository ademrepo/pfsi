import React from 'react';

const PageHeader = ({ title, subtitle, actions }) => {
    return (
        <div className="page-header">
            <div>
                <h1>{title}</h1>
                {subtitle && <p className="page-subtitle">{subtitle}</p>}
            </div>
            {actions && (
                <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1rem' }}>
                    {actions}
                </div>
            )}
        </div>
    );
};

export default PageHeader;
