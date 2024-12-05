import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const NAV_LINKS = [
  { path: "/", label: "Home" },
  { path: "/about", label: "About" },
  { path: "/services", label: "Services" },
  { path: "/contact", label: "Contact" },
];

const Header = () => (
  <header className="header">
    <div className="logo">
      <Link to="/">MetaSpace</Link>
    </div>
    <nav className="navbar">
      <ul>
        {NAV_LINKS.map((link) => (
          <li key={link.path}>
            <Link to={link.path}>{link.label}</Link>
          </li>
        ))}
      </ul>
    </nav>
  </header>
);

export default Header;