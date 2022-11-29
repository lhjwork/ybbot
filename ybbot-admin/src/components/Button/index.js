import styled from "styled-components";

export const DefaultButton = ({ style, text, onClick }) => {
  return (
    <DefaultButtonstyle onClick={onClick} style={style}>
      {text}
    </DefaultButtonstyle>
  );
};

export const SmallButton = ({ style, text, onClick }) => {
  return (
    <SmallButtonStyle onClick={onClick} style={style}>
      {text}
    </SmallButtonStyle>
  );
};

const DefaultButtonstyle = styled.button`
  width: 206px;
  padding: 9.5px;
  background: #adccef;
  border: 0;
  border-radius: 10px;
  font-size: 16px;
  color: #fff;
  font-weight: 700;
  line-height: 19px;
  @media ${({ theme }) => theme.device.tablet} {
    width: 100px;
  }
`;
const SmallButtonStyle = styled.button`
  width: 70px;
  height: 32px;
  background-color: #fff;
  border: 1px solid #458bff;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  line-height: 16px;
  color: #458bff;
  @media ${({ theme }) => theme.device.tablet} {
    width: 50px;
    height: 30px;
  }
`;
