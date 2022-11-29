import styled from 'styled-components';
export const LoginContainer = styled.div`
    width: 645px;
    max-width: 95%;
    height: 383px;
    padding-top: 34px;
    background: #ffffff;
    box-shadow: 1px 1px 10px rgba(0, 0, 0, 0.15);
    border-radius: 20px;
    text-align: center;
`;
export const Title = styled.p`
    font-size: 32px;
    margin-bottom: 49px;
`;
export const LoginForm = styled.form``;
export const LoginInput = styled.input`
    width: 554px;
    height: 55px;
    max-width: 90%;
    padding: 17px 20px;
    background: #ffffff;
    border: 1px solid #c4c4c4;
    border-radius: 5px;
    &::placeholder {
        font-size: 18px;
        line-height: 21px;
    }
`;
