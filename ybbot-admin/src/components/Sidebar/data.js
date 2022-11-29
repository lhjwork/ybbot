import React from "react";
import * as MdIcons from "react-icons/md";
let ICONSIZE = "1.4rem";
let COLOR = "#FFFFFF";
export const SidebarData = [
  {
    title: "사용자 관리",
    icon: <MdIcons.MdWifi size={ICONSIZE} color={COLOR} />,
    path: "/users",
  },
  {
    title: "공지사항",
    icon: <MdIcons.MdOutlineHeadset size={ICONSIZE} color={COLOR} />,
    path: "/notices",
  },
  {
    title: "자주묻는질문",
    icon: <MdIcons.MdOutlineHeadset size={ICONSIZE} color={COLOR} />,
    path: "/faqs",
  },
  // {
  //   title: "결제",
  //   icon: <MdIcons.MdPayment size={ICONSIZE} color={COLOR} />,
  //   path: "/payments",
  // },
  // {
  //   title: "유저 자동매매 거래내역",
  //   icon: <MdIcons.MdOutlineHeadset size={ICONSIZE} color={COLOR} />,
  //   path: "/userTransactionManagement",
  // },
  {
    title: "어드민 지갑 등록 및 수정",
    icon: <MdIcons.MdCardGiftcard size={ICONSIZE} color={COLOR} />,
    path: "/adminWalletManagement",
  },
  {
    title: "어드민 비밀번호 수정",
    icon: <MdIcons.MdOutlineSettings size={ICONSIZE} color={COLOR} />,
    path: "/adminPasswordManagement",
  },
];
