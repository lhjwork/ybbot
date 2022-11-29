import styled from "styled-components";
import { DefaultButton } from "../Button/index";

const InputBox = ({
  labelText,
  placeholder,
  showButton,
  style,
  inputStyle,
  onChange,
  onClick,
  value,
  className,
  readOnly,
}) => {
  return (
    <InputContainer style={style} className={className}>
      <Label>{labelText}</Label>
      <Input
        placeholder={placeholder}
        type="text"
        onChange={onChange}
        value={value}
        style={inputStyle}
        readOnly={readOnly}
      />
      {showButton && (
        <DefaultButton
          text={"검색"}
          style={{ float: "right" }}
          onClick={onClick}
        />
      )}
    </InputContainer>
  );
};

export default InputBox;

const InputContainer = styled.div`
  @media ${({ theme }) => theme.device.tablet} {
    &.noticeTitle input {
      width: 100%;
      margin-top: 18px;
    }
  }
`;
const Label = styled.label`
  margin-right: 34px;
  font-size: 14px;
  @media ${({ theme }) => theme.device.tablet} {
    margin-right: 20px;
  }
`;
const Input = styled.input`
  width: calc(100% - 300px);
  max-width: 725px;
  padding: 9.75px 13px;
  border-radius: 5px;
  @media ${({ theme }) => theme.device.tablet} {
    width: calc(100% - 160px);
  }
`;
