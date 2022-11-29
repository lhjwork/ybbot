import styled from 'styled-components';
export const TD = styled.td`
    min-width: 40px;
    height: 40px;
    padding: 0px 0.8rem;
    background-color: #fff;
    border: 0.5px solid #eaeaea;
    font-size: 14px;
    line-height: 16px;
    font-family: Roboto;
    text-align: ${(props) => props.textAlign};
    position: relative;
    white-space: ${(props) => (props.isFullScreen ? 'pre' : 'nowrap')};
    &:hover {
        text-decoration: ${(props) => (props.hover ? 'underline' : 'none')};
    }
    @media ${({ theme }) => theme.device.tablet} {
        padding: ${(props) => (props.isFullScreen ? '0px 0.8rem' : '5px 15px')};
    }
`;
export const TableContainer = styled.div`
    display: flex;
    width: 100%;
    flex: 1;
    overflow: auto;
    /* @media ${({ theme }) => theme.device.tablet} {
        margin: 0 1rem;
    } */
`;
export const TDHeader = styled.td`
    background: #f9f8f9;
    font-weight: bold;
    font-size: 14px;
    line-height: 16px;
    text-align: ${(props) => props.textAlign};
    position: relative;
    border: 0.5px solid #eaeaea;
    padding: 0px 0.8rem;
    min-width: 40px;
    height: 47px;
    max-height: 47px;
    white-space: ${(props) => (props.isFullScreen ? 'pre' : 'nowrap')};
    @media ${({ theme }) => theme.device.tablet} {
        line-height: 10px;
        padding: 0px 0.8rem;
        height: 37px;
        max-height: 37px;
    }
`;
export const CheckBox = styled.td`
    height: 18px;
    width: auto;
    min-width: 40px;
    background-color: #fff;
    border: 0.5px solid #eaeaea;
    /* background: #f9f8f9; */
    text-align: center;
`;

export const CheckBoxImage = styled.img`
    width: 13px;
    height: 13px;
    object-fit: contain;
    cursor: pointer;
`;
export const TR = styled.tr`
    background: ${(props) =>
        props.isSelected ? 'rgba(0,0,0,0.05)' : 'default'};
    transition: 300ms linear;
`;
