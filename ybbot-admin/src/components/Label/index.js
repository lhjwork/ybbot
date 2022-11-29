import styled from 'styled-components';

export const LabelTitle = ({ style, text }) => {
    return <Label style={style}>{text}</Label>;
};

const Label = styled.p`
    font-weight: 700;
    font-size: 14px;
    line-height: 16px;
`;
