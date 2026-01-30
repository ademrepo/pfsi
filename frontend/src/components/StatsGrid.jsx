import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

const StatCard = ({ label, value, badge, trend, icon: Icon, borderColor, valueColor }) => {
    return (
        <div
            className="stat-card"
            style={{
                borderLeft: borderColor ? `4px solid ${borderColor}` : undefined,
                height: '160px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
            }}
        >
            <div className="stat-card-header">
                <span
                    className="stat-card-label"
                    style={{
                        fontSize: '0.688rem',
                        letterSpacing: '0.15em',
                        fontWeight: '700'
                    }}
                >
                    {label}
                </span>
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
            <div
                className="stat-card-value"
                style={{
                    fontSize: '3rem',
                    fontWeight: '300',
                    letterSpacing: '-0.05em',
                    color: valueColor || 'var(--text-main)'
                }}
            >
                {value}
            </div>
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
