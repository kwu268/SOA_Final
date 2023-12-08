import React from "react";
import { Nav, NavLink, NavMenu } from "./NavbarElements";

const Navbar = () => {
    return (
        <>
            <Nav>
                <NavMenu>
                    <NavLink to="/">
                        Home
                    </NavLink>
                    <NavLink to="/search">
                        Search
                    </NavLink>
                </NavMenu>
            </Nav>
        </>
    );
};
 
export default Navbar;