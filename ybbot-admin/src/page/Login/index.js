import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { LoginContainer, Title, LoginInput, LoginForm } from "./styles";
import { DefaultButton } from "../../components/Button";
import { connectLogin } from "../../redux/userSlice";

const Login = () => {
  const dispatch = useDispatch();

  const [userId, setUserId] = useState("");
  const [userPassword, setUserPassword] = useState("");

  const handleOnClick = (e) => {
    e.preventDefault();
    if (userId === "") {
      alert("아이디를 입력해주세요.");
      return;
    } else if (userPassword === "") {
      alert("비밀번호를 입력해주세요.");
      return;
    }

    let body = {
      loginId: userId,
      password: userPassword,
    };
    dispatch(connectLogin(body));
    // navigate('/UserManagement');
  };

  const idHandler = ({ target }) => {
    setUserId(target.value);
  };

  const passwordHandler = ({ target }) => {
    setUserPassword(target.value);
  };
  return (
    <LoginContainer>
      <Title>로그인</Title>
      <LoginForm>
        <LoginInput
          type="text"
          placeholder="아이디"
          value={userId}
          onChange={idHandler}
        />
        <LoginInput
          type="password"
          placeholder="비밀번호"
          value={userPassword}
          onChange={passwordHandler}
          style={{ marginTop: "12px" }}
        />
        <DefaultButton
          type="submit"
          text={"로그인"}
          onClick={(e) => handleOnClick(e)}
          style={{
            width: "206px",
            padding: "9.5px",
            marginTop: "38px",
            fontSize: "14px",
          }}
        />
      </LoginForm>
    </LoginContainer>
  );
};

export default Login;
