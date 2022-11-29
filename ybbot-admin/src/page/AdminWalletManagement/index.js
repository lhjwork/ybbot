import React from "react";
import styled from "styled-components";
import { FormLayout } from "../../components/Container/index";
import MenuBar from "../../components/MenuBar";
import { DefaultButton } from "../../components/Button";
import CustomTable from "../../components/CustomTable";
import { SmallButton } from "../../components/Button";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../../api/api";

const AdminWalletManagement = () => {
  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       const res = await api.get("notice_list");
  //       const noticeData = res.data;
  //     } catch (error) {
  //       console.log("err", error);
  //       console.log("err.res", error.response);
  //     }
  //   };
  //   fetchData();
  // }, []);

  return (
    <>
      <MenuBar />
      <FormLayout>
        <InputContainer>
          <Input
            type="text"
            placeholder="지갑주소를 입력해주세요."
            // onChange={tokenHandler}
          />
        </InputContainer>
        <Title style={{ marginTop: "20px" }}>현재 지갑주소 :</Title>
        <DefaultButton
          text={"등록"}
          style={{ marginTop: "50px" }}
          // onClick={submitHandler}
        />
      </FormLayout>
    </>
  );
};

export default AdminWalletManagement;
const Title = styled.p`
  font-size: 14px;
  line-height: 16px;
`;
const ButtonContainer = styled.div`
  & button {
    width: 150px;
    padding: 8.5px;
    float: right;
    margin-right: 36px;
    margin-top: -44px;
    position: relative;
    @media ${({ theme }) => theme.device.tablet} {
      width: 100px;
      margin-top: -55px;
      margin-right: 1rem;
      padding: 8px 0;
    }
  }
`;
const InputContainer = styled.div`
  width: 353px;
  max-width: 100%;
  margin-top: 20px;
  position: relative;
`;
const Input = styled.input`
  width: 100%;
  padding: 10px 35px 10px 12px;
  background: #ffffff;
  border: 1px solid #c4c4c4;
  border-radius: 5px;
`;
