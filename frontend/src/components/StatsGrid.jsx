import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

const StatCard = ({ label, value, badge, trend, icon: Icon }) => {
    return (
        <div className="stat-card">
            <div className="stat-card-header">
                <span className="stat-card-label">{label}</span>
                {Icon && (
                    <div style={{ 
                        width: '40px', 
                        height: '40px', 
                        background: 'var(--bg-page)', 
                        borderRadius: '10px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'var(--primary)'
                    }}>
                        <Icon size={20} />
                    </div>
                )}
            </div>
            <div className="stat-card-value">{value}</div>
            <div className="stat-card-meta">
                {trend && (
                    <span className="badge-increase">
                        {trend > 0 ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                        {Math.abs(trend)}%
                    </span>
                )}
                {badge && badge}
            </div>
        </div>
    );
};

const StatsGrid = ({ stats }) => {
    return (
        <div className="stats-grid">
            {stats.map((stat, index) => (
                <StatCard key={index} {...stat} />
            ))}
        </div>
    );
};

export { StatCard, StatsGrid };
export default StatsGrid;
