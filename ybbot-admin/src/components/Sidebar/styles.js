import styled from "styled-components";
import { Link } from "react-router-dom";
export const SidebarLink = styled.div`
  display: flex;
  color: #ffffff;
  justify-content: space-between;
  align-items: center;
  list-style: none;
  height: 48px;
  text-decoration: none;
  font-size: 18px;
  cursor: pointer;
  margin-top: 0px;
  margin-bottom: 0px;
  padding: 0 25px;

  font-weight: bold;
  @media ${({ theme }) => theme.device.tablet} {
    padding: 0 1.5rem;
  }
`;

export const SidebarLabel = styled.span`
  //margin-left: 16px;
  width: 145px;
  display: block;
  font-size: 14px;
  line-height: 14px;
`;
export const InSidebarLabel = styled.span`
  //margin-left: 16px;
  display: block;
  font-size: 14px;
  line-height: 14px;
  margin-left: 31px;
  @media ${({ theme }) => theme.device.tablet} {
    margin-left: 15px;
  }
`;
export const DropdownLink = styled(Link)`
  font-style: normal;
  font-weight: 400;
  font-size: 12px;
  line-height: 12px;

  @keyframes growDown {
    0% {
      transform: scaleY(0);
    }
    80% {
      transform: scaleY(1.1);
    }
    100% {
      transform: scaleY(1);
    }
  }
  transition: all 0.3s ease-in-out 0s, visibility 0s linear 0.3s,
    z-index 0s linear 0.01s;

  animation: growDown 300ms ease-in-out forwards;
  transform-origin: top center;
  background-color: ${(props) =>
    props.locations === "true"
      ? props.theme.colorTheme.LIGHTBLUE
      : props.theme.colorTheme.MAIN};
  color: ${(props) => (props.locations === "true" ? "#3D4563" : "#fff")};

  padding-left: 44px;
  height: 35px;
  display: flex;
  align-items: center;
  text-decoration: none;
  cursor: pointer;
  &:hover {
    cursor: pointer;
    opacity: 0.7;
  }
  @media ${({ theme }) => theme.device.tablet} {
    padding-left: 35px;
  }
`;

export const ArrowSize = styled.div`
  color: rgba(153, 153, 153, 1);
  //margin-right: 34px;
`;

export const TopSideBar = styled.div`
  width: 280px;
  outline: none;
  height: 1px;
  font-size: 15px;
  line-height: 10px;
  border-right: 0;
  border-left: 0;
  border-top: 0;
`;

export const Container = styled.div`
  @keyframes growDown {
    0% {
      transform: scaleY(0);
    }
    80% {
      transform: scaleY(1.1);
    }
    100% {
      transform: scaleY(1);
    }
  }
  transition: all 0.3s ease-in-out 0s, visibility 0s linear 0.3s,
    z-index 0s linear 0.01s;

  animation: growDown 300ms ease-in-out forwards;
  transform-origin: top center;
`;
