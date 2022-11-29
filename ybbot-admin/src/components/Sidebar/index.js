import React, { useState } from 'react';
import styled from 'styled-components';
import { SidebarData } from './data';
import SubMenu from './SubMenu';

const Sidebar = () => {
    const [selectNav, setSelectNav] = useState('');
    return (
        <SidebarNav>
            {SidebarData.map((item, index) => {
                return (
                    <SubMenu
                        item={item}
                        key={index}
                        selectNav={selectNav}
                        setSelectNav={setSelectNav}
                    />
                );
            })}
        </SidebarNav>
    );
};

export default Sidebar;

export const SidebarNav = styled.nav`
    min-height: ${({ theme }) =>
        `calc(100vh - ${theme.componentSize.NAVHEIGHT})`};
    min-width: ${({ theme }) => theme.componentSize.SIDEBARWIDTH};
    max-width: ${({ theme }) => theme.componentSize.SIDEBARWIDTH};
    background-color: ${({ theme }) => theme.colorTheme.MAIN};
    transition: 350ms;
    @media ${({ theme }) => theme.device.mobileL} {
        height: 100vh;
        min-width: 60vw;
        max-width: 60vw;
        min-width: 200px;
    }
`;
export const DropdownComponents = styled.div`
    width: ${({ theme }) => theme.componentSize.SIDEBARWIDTH};
    height: 50px;
    padding: 0px 36px;
    background-color: #5c6887;
    display: flex;
    align-items: center;
    justify-content: center;
    .MuiSelect-select {
        color: #fff !important;
    }
    .MuiInputBase-root {
        padding: 0;
    }
    @media ${({ theme }) => theme.device.mobileL} {
        width: 60vw;
        min-width: 200px;
        padding: 0px 1.7rem;
    }
`;
