import styled from 'styled-components';

export const Normal20Title = ({ style, text }) => {
    return <Normal20Font style={style}>{text}</Normal20Font>;
};

const Normal20Font = styled.p`
    font-size: 20px;
    line-height: 23px;
    @media ${({ theme }) => theme.device.tablet} {
        font-size: 14px;
    }
`;
