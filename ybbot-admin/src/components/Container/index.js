import React from 'react';
import styled from 'styled-components';

export const TableLayout = ({ children, style }) => {
    return (
        <TableLayoutContainer style={style}>{children}</TableLayoutContainer>
    );
};
export const FormLayout = ({ children, style }) => {
    return (
        <InputLayoutContainer style={style}>{children}</InputLayoutContainer>
    );
};
const TableLayoutContainer = styled.div`
    position: relative;
    margin: 36px 36px 0 41px;
    @media ${({ theme }) => theme.device.tablet} {
        margin: 20px 5vw;
    }
`;
const InputLayoutContainer = styled.div`
    position: relative;
    margin: 38px 52px;
    @media ${({ theme }) => theme.device.tablet} {
        margin: 20px 5vw;
    }
`;
