import React from 'react';
import Search from '@site/src/components/Search/Search';

const NavbarSearch = () => {
  return (
    <div className="navbar__search">
      <Search placeholder="Search..." />
    </div>
  );
};

export default NavbarSearch;