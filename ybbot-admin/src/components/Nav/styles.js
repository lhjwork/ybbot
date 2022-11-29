import styled from 'styled-components';

export const NavContainer = styled.div``;

export const TitleContainer = styled.div`
    position: fixed;
    height: ${({ theme }) => theme.componentSize.NAVHEIGHT};
    top: 0;
    background: #fff;
    width: 100%;
    z-index: 400;
    display: ${(props) => (props.isShow ? 'flex' : 'none')};
    align-items: center;
    justify-content: space-between;
    padding: 0px 46px 0px 32px;
    @media ${({ theme }) => theme.device.tablet} {
        padding: 0px 10px;
    }
    .hamburder {
        display: none;
        font-size: 25px;
        margin-left: 5px;
        cursor: pointer;
        color: ${({ theme }) => theme.colorTheme.Blue};
        @media ${({ theme }) => theme.device.tablet} {
            display: inline-block;
            margin-right: 5px;
            &:hover {
                transition: 0.1s;
                transform: scale(1.2);
            }
        }
    }
`;

export const TitleImg = styled.img`
    cursor: pointer;
    width: 208px;
    //height: ${({ theme }) => theme.componentSize.NAVHEIGHT};
    object-fit: contain;
    @media ${({ theme }) => theme.device.tablet} {
        width: 100px;
    }
`;

export const TouchAttendace = styled.div`
    font-size: 14px;
    line-height: 14px;
    font-weight: bold;
    margin-right: 10px;
    margin-left: 0px;
`;

export const TouchScreenShot = styled.img`
    width: 33px;
    object-fit: contain;
    cursor: pointer;
`;
export const Hamburger = styled.img``;
export const SidebarContainer = styled.div`
    display: none;
    position: fixed;
    min-height: 100vh;
    height: 100%;
    background-color: ${({ theme }) => theme.colorTheme.MAIN};
    //margin-top: 80px;
    transition: 0.5s;
    overflow-x: hidden;
    z-index: 1000;

    @media ${({ theme }) => theme.device.tablet} {
        display: ${(props) => (props.sideDrawerOpen ? 'block' : 'none')};
        margin-top: ${({ theme }) =>
            `calc(${theme.componentSize.NAVHEIGHT} * -1)`};
    } ;
`;
