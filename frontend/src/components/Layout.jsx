import React, { useState } from 'react';
import Sidebar from './Sidebar';
import { Outlet } from 'react-router-dom';

const Layout = ({ user, onLogout }) => {
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
    return (
        <div className={`app-layout ${sidebarCollapsed ? 'app-layout--sidebar-collapsed' : ''}`}>
            <Sidebar user={user} onLogout={onLogout} collapsed={sidebarCollapsed} onToggle={() => setSidebarCollapsed((s) => !s)} />
            <main className="main-content">
                <Outlet />
            </main>
        </div>
    );
};

export default Layout;
