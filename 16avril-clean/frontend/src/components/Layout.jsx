import React from 'react';
import Sidebar from './Sidebar';
import { Outlet } from 'react-router-dom';

const Layout = ({ user, onLogout }) => {
    return (
        <div className="app-layout">
            <Sidebar user={user} onLogout={onLogout} />
            <main className="main-content">
                <Outlet />
            </main>
        </div>
    );
};

export default Layout;
