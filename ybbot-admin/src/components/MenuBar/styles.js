import styled from 'styled-components';
export const Container = styled.div`
    display: flex;
    background: #ffffff;
    box-shadow: inset 2px 2px 2px rgba(0, 0, 0, 0.1),
        inset 2px -2px 2px rgba(0, 0, 0, 0.1);
    min-height: 50px;
    align-items: center;
    padding: 0 38px;
    @media ${({ theme }) => theme.device.tablet} {
        padding: 0 1rem;
        margin-bottom: 12px;
    }

    position: relative;
`;

export const Title = styled.span`
    font-family: Roboto;
    font-style: normal;
    font-size: 14px;
    line-height: 16px;
    color: #000;
`;
export const PageName = styled.span`
    font-family: Roboto;
    font-size: 14px;
    line-height: 16px;
    color: #3d4563;
`;
export const Arrow = styled.img`
    width: 8px;
    height: 15px;
    object-fit: contain;
    margin: 0 28px;
    @media ${({ theme }) => theme.device.tablet} {
        width: 5px;
        height: 10px;
        margin: 0 1rem;
    }
`;
export const Icons = styled.img`
    object-fit: contain;
    width: 14px;
    height: 14px;
    margin-left: 26px;
    @media ${({ theme }) => theme.device.tablet} {
        margin-left: 0px;
    }
`;
export const RightContainer = styled.div`
    display: flex;
    flex: 1;
    justify-content: flex-end;

    @media ${({ theme }) => theme.device.tablet} {
        display: none;
    }
`;
export const Menutitle = styled.span`
    font-style: normal;
    font-weight: bold;
    line-height: 14px;
    color: #555555;
    margin-left: 7px;
`;
export const Division = styled.div`
    border: 1px solid #e3e5e5;
    margin-left: 24px;
`;

export const SubMenu = styled.span`
    font-style: normal;
    font-weight: bold;
    line-height: 14px;
    color: #555555;
    margin-left: 17px;
    &:hover {
        cursor: ${(props) => (props.isOneSelect ? 'not-allowed' : 'pointer')};
        transform: ${(props) =>
            props.isOneSelect ? ' scale(1.0)' : ' scale(1.2)'};
        transition: 0.1s;
    }
    @media ${({ theme }) => theme.device.tablet} {
        margin-left: 0px;
        padding: 0px 10px;
        text-align: left;
    }
`;
export const MenuBox = styled.div`
    align-items: center;
    display: flex;
    &:hover {
        cursor: ${(props) => (props.isOneSelect ? 'not-allowed' : 'pointer')};
        transform: ${(props) =>
            props.isOneSelect ? 'not-allowed' : 'scale(1.2)'};
        transition: 0.1s;
    }
    @media ${({ theme }) => theme.device.tablet} {
        margin-left: 0px;
        padding: 0px 10px;
        text-align: left;
    }
`;
