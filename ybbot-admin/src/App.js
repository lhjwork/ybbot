import theme from "./theme";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import { useSelector } from "react-redux";
import React from "react";
import styled, { createGlobalStyle, ThemeProvider } from "styled-components";
import Sidebar from "./components/Sidebar";
import Nav from "./components/Nav";
import Login from "./page/Login";
import UserManagement from "./page/UserManagement";
import UserTransaction from "./page/UserManagement/UserTransaction";
import Notice from "./page/Notice";
import RegisterNotice from "./page/Notice/RegisterNotice";
import UpdateNotice from "./page/Notice/UpdateNotice";
import Faq from "./page/Faq";
import RegisterFaq from "./page/Faq/RegisterFaq";
import UpdateFaq from "./page/Faq/UpdateFaq";
import PaymentManagement from "./page/PaymentManagement";
import AdminWalletManagement from "./page/AdminWalletManagement";
import AdminPasswordManagement from "./page/AdminPasswordManagement";

function App() {
  const user = useSelector((state) => state.auth.loginId);
  const GlobalStyle = createGlobalStyle`
    * {
        box-sizing: border-box;
    }
      body {
        font-family: 'Robot', sans-serif;
        font-weight: 400;
        font-style: normal;
        color: ${({ theme }) => theme.colorTheme.BLACK};
        margin: 0;
        height: 100%;
        background-color: #FBFBFB;
      }

      div, p, span {

        margin: 0;
        word-break: keep-all;
        -ms-overflow-style: none;

        ::-webkit-scrollbar {
          display: none;
        }
      }

      table td, table th {
        -webkit-box-sizing: border-box;
        box-sizing: border-box;
      }

      input[type='text'],
      input[type='password'],
      textarea {
        font-family: 'Robot', sans-serif;
        background: #ffffff;
        border: 1px solid #c4c4c4;
        font-size: 14px;
        &::placeholder {
            font-size: 14px;
            line-height: 16px;
            color: #c4c4c4;
        }
        &:read-only:focus {
            outline: none;
            cursor: default;
        }
      }
      input[type='radio'] {
        -webkit-appearance: none;
        cursor: pointer;
      }
      button {
          cursor: pointer;
      }
    `;

  const Center = styled.div`
    height: 100%;
    display: flex;
    flex: 1;
    flex-direction: row;
    margin-top: ${(props) =>
      props?.isLogin ? props.theme.componentSize.NAVHEIGHT : "0px"};
  `;
  const SideBarBox = styled.div`
    display: flex;
    min-height: ${({ theme }) =>
      `calc(100vh - ${theme.componentSize.NAVHEIGHT})`};
    @media ${({ theme }) => theme.device.tablet} {
      display: none;
    }
  `;
  const Container = styled.div`
    display: flex;
    flex-direction: column;
    flex: 1;
    overflow: scroll;
    //height: 100%;
    height: ${(props) =>
      props.isLogin
        ? "100vh"
        : `calc(100vh - ${props.theme.componentSize.NAVHEIGHT})`};
  `;
  const LoginContainer = styled.div`
    display: flex;
    height: 100vh;
    justify-content: center;
    align-items: center;
  `;

  let { isAdmin } = useSelector((state) => state.auth);

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />

      <Router>
        {user && <Nav />}
        {isAdmin !== null ? (
          <Center isLogin={true}>
            {user && (
              <SideBarBox>
                <Sidebar />
              </SideBarBox>
            )}
            <Container isLogin={false}>
              <Routes>
                <>
                  <Route path="*" element={<Navigate to="/users" />} />
                  <Route path="/users" element={<UserManagement />} />
                  <Route
                    path="/users/userTransactions"
                    element={<UserTransaction />}
                  >
                    <Route path=":id" element={<UserTransaction />} />
                  </Route>
                  <Route path="/notices" element={<Notice />} />
                  <Route
                    path="/notices/registerNotice"
                    element={<RegisterNotice />}
                  />
                  <Route
                    path="/notices/updateNotice"
                    element={<UpdateNotice />}
                  >
                    <Route path=":id" element={<UpdateNotice />} />
                  </Route>
                  <Route path="/faqs" element={<Faq />} />
                  <Route
                    path="/faqs/registerFaq"
                    element={<RegisterNotice />}
                  />
                  <Route path="/faqs/updateFaq" element={<UpdateFaq />}>
                    <Route path=":id" element={<UpdateFaq />} />
                  </Route>
                  <Route path="/payments" element={<PaymentManagement />} />
                  <Route
                    path="/adminWalletManagement"
                    element={<AdminWalletManagement />}
                  />
                  <Route
                    path="/adminPasswordManagement"
                    element={<AdminPasswordManagement />}
                  />
                </>
              </Routes>
            </Container>
          </Center>
        ) : (
          <LoginContainer>
            <Routes>
              <Route path="*" element={<Navigate to="/Login" />} />
              <Route path="/Login" element={<Login />} />
            </Routes>
          </LoginContainer>
        )}
      </Router>
    </ThemeProvider>
  );
}

export default App;
