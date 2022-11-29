import React, { useState } from "react";
import styled from "styled-components";
import { TableLayout } from "../../components/Container/index";
import MenuBar from "../../components/MenuBar";
import InputBox from "../../components/InputBox";
import { api } from "../../api/api";
import { useNavigate } from "react-router-dom";
import { DefaultButton } from "../../components/Button";

const RegisterNotice = () => {
  const navigate = useNavigate();

  const [noticeTitle, setNoticeTitle] = useState("");
  const [noticeContent, setNoticeContent] = useState("");

  const titleHandler = ({ target }) => {
    setNoticeTitle(target.value);
  };
  const contentHandler = ({ target }) => {
    setNoticeContent(target.value);
  };

  const submitHandler = (e) => {
    let body = {
      title: noticeTitle,
      description: noticeContent,
    };
    e.preventDefault();
    if (noticeTitle === "") {
      alert("제목을 입력해주세요.");
      return;
    } else if (noticeContent === "") {
      alert("내용을 입력해주세요.");
      return;
    } else {
      try {
        const res = api.post("notice_insert", body);
        alert("공지사항이 등록되었습니다.");
        navigate("/notices");
      } catch (error) {
        console.log(error);
        console.log(error.response);
      }
    }
  };

  return (
    <>
      <MenuBar />
      <TableLayout>
        <InputBox
          labelText={"제목"}
          placeholder={"공지사항 제목을 입력하세요."}
          showButton={false}
          style={{ marginBottom: "30px" }}
          value={noticeTitle}
          onChange={titleHandler}
          className={"noticeTitle"}
        />
        <ContentLabel>내용</ContentLabel>
        <ContentArea
          value={noticeContent}
          onChange={contentHandler}
          placeholder="공지사항 내용을 입력하세요."
        ></ContentArea>
        <DefaultButton
          text={"등록"}
          style={{ float: "right", margin: "73px 0 50px" }}
          onClick={submitHandler}
        />
      </TableLayout>
    </>
  );
};

export default RegisterNotice;
const ContentLabel = styled.label`
  font-size: 14px;
`;
const ContentArea = styled.textarea`
  width: 100%;
  height: 603px;
  margin-top: 18px;
  padding: 25px 27px;
  border: 1px solid #c4c4c4;
  border-radius: 5px;
  resize: none;
  @media ${({ theme }) => theme.device.tablet} {
    height: 300px;
  }
`;
