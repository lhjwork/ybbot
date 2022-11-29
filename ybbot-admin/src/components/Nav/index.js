import React, { useEffect, useState } from "react";
import { TitleContainer, SidebarContainer, NavContainer } from "./styles";
import Sidebar from "../../components/Sidebar";
import { useNavigate } from "react-router-dom";
import { FaPowerOff } from "react-icons/fa";
import styled from "styled-components";
import { LOGOUT } from "../../redux/userSlice";
import { useDispatch, useSelector } from "react-redux";
import { HiMenu } from "react-icons/hi";
const Nav = () => {
  const user = useSelector((state) => state.auth.loginId);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const hamburgerRef = React.createRef(); // 1. ref 를 만들어주고
  const [sideDrawerOpen, setSideDrawerOpen] = useState(false);

  function useOutsideAlerter(ref) {
    useEffect(() => {
      function handleClickOutside(event) {
        if (ref.current && !ref.current.contains(event.target)) {
          setSideDrawerOpen(false);
        }
      }

      document.addEventListener("mousedown", handleClickOutside);
      return () => {
        document.removeEventListener("mousedown", handleClickOutside);
      };
    }, [ref]);
  }
  useOutsideAlerter(hamburgerRef);
  return (
    <div>
      <BackBlur sideDrawerOpen={sideDrawerOpen} />
      <NavContainer ref={hamburgerRef}>
        <TitleContainer
          isShow={true}
          // isShow={auth && !location.includes('TouchAttendance')}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
            }}
          >
            <HiMenu
              className={"hamburder"}
              onClick={(e) => {
                setSideDrawerOpen(true);
              }}
            />
            YB BOT
            {/* <TitleImg
                            src={require('../../assets/navbar/logo.png')}
                            alt='logo'
                            onClick={(e) => {
                                e.preventDefault();
                                navigate('/UserManagement');
                            }}
                        /> */}
          </div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
            }}
          >
            {user && (
              <LogOutContain>
                <Logout
                  onClick={() => {
                    if (window.confirm("로그아웃 하시겠습니까?")) {
                      dispatch(LOGOUT());
                      navigate("/login");
                      return alert("로그아웃 되었습니다.");
                    }
                  }}
                >
                  <LogOut>로그아웃</LogOut>
                  <FaPowerOff className={"icons"} size={18} />
                </Logout>
              </LogOutContain>
            )}
          </div>
        </TitleContainer>
        <SidebarContainer sideDrawerOpen={sideDrawerOpen}>
          <Sidebar />
        </SidebarContainer>
      </NavContainer>
    </div>
  );
};

export default Nav;
const BackBlur = styled.div`
  position: absolute;
  background: rgba(0, 0, 0, 0.4);
  width: 100%;
  height: 100%;
  z-index: 401;
  margin-top: ${({ theme }) => `calc(${theme.componentSize.NAVHEIGHT} * -1)`};
  display: none;
  @media ${({ theme }) => theme.device.tablet} {
    display: ${(props) => (props.sideDrawerOpen ? "block" : "none")};
  }
`;
const LogOutContain = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  align-content: center;
  @media ${({ theme }) => theme.device.tablet} {
    margin-right: 1rem;
  }
`;
export const LogOut = styled.p`
  margin-right: 13px;
  font-size: 14px;
  @media ${({ theme }) => theme.device.tablet} {
    margin-right: 5px;
    & + svg {
      width: 12px;
    }
  }
`;

const Logout = styled.span`
  font-size: 14px;
  line-height: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-weight: bold;
  font-family: "Roboto";
`;
