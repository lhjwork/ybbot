import React from "react";
import { Container, Title } from "./styles";
import { useLocation } from "react-router-dom";
const MenuBar = () => {
  const location = useLocation().pathname;

  const ReturnName = (index) => {
    try {
      const menuLocationNameSplit = location.split("/");
      if (!isNaN(menuLocationNameSplit[menuLocationNameSplit.length - 1])) {
        return MenuLocationName[
          location.split("/")[menuLocationNameSplit.length - 2]
        ][index];
      } else {
        return MenuLocationName[
          location.split("/")[menuLocationNameSplit.length - 1]
        ][index];
      }
    } catch (e) {
      return "페이지를 찾을 수 없습니다";
    }
  };

  return (
    <Container>
      <Title>{ReturnName(0)}</Title>
    </Container>
  );
};

export default MenuBar;

let MenuLocationName = {
  users: ["사용자 관리"],
  userTransactions: ["자동매매 거래내역"],
  notices: ["공지사항"],
  faqs: ["자주묻는질문"],
  // payments: ["결제"],
  userTransactionManagement: ["유저 자동매매 거래내역"],
  adminWalletManagement: ["어드민 지갑 등록 및 수정"],
  adminPasswordManagement: ["어드민 비밀번호 수정"],
};
