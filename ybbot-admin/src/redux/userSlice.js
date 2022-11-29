import { createSlice } from "@reduxjs/toolkit";
import { api } from "../api/api";

const config = {
  headers: {
    "Content-Type": "application/json",
  },
};
let initialStates = {
  loginId: null,
  sessionToken: null,
  isAdmin: null,
  id: null,
};
const userSlice = createSlice({
  name: "auth",
  initialState: initialStates,
  reducers: {
    LOGIN: (state, action) => {
      const { sessionToken, type, id, loginId, wallet } = action?.payload;
      state.sessionToken = sessionToken;
      state.loginId = loginId;
      state.isAdmin = type === "admin";
      state.id = id;
      state.wallet = wallet;
      // console.log("sessionToken", sessionToken);
      // console.log("type", type);
      // console.log("id", id);
      // console.log("loginId", loginId);
      // console.log("wallet", wallet);
      // api.defaults.headers.common['Authorization'] = 'sessionToken ' + sessionToken;
      // api.defaults.headers = {
      //     Authorization: `sessionToken ${sessionToken}`,
      //     'Content-Type': 'application/json',
      // };

      api.defaults.headers.common["Authorization"] = `Token ${sessionToken}`;
      api.defaults.headers.post["Content-Type"] = "application/json";
      // console.log(action?.payload);
    },

    LOGOUT: (state) => {
      return initialStates;
    },
    // SIGNUP: (state, action) => {
    //     const { user, sessionToken } = action.payload;
    //     state.user = user;
    //     state.sessionToken = sessionToken;
    //     // api.headers.common['Authorization'] = 'sessionToken ' + sessionToken;
    //     // api.defaults.headers.common['Authorization'] = 'sessionToken ' + sessionToken;
    // },

    // UpdateUserGym: (state, action) => {
    //     state.user.gym = action.payload;
    // },
  },
});

export const { LOGIN, LOGOUT, LOGINTYPE, UpdateUserGym, SIGNUP } =
  userSlice.actions;

export const connectLogin = (body) => async (dispatch) => {
  try {
    const { data } = await api.post("login", body);
    dispatch(
      LOGIN({
        sessionToken: data?.sessionToken,
        type: data?.type,
        id: data?.id,
        loginId: data?.login_id,
        wallet: data?.wallet,
      })
    );
    alert("로그인에 성공하였습니다");
  } catch (err) {
    console.log("err", err);
    console.log("err.res", err.response);
    let msg = "서버와 통신에 실패하였습니다.";
    const { data } = err.response;
    if (!data.ok && data.msg) {
      msg = data.msg;
    }
    alert(msg);
  }
};

// export const connectCenterSignUp =
//   (body, setUsingErrMessage, navigateBack) => async (dispatch) => {
//     try {
//       const { data } = await api.post("sign-up", body);
//       alert("회원가입에 성공하였습니다 \n관리자 승인 후 이용가능합니다");
//       navigateBack();
//     } catch (err) {
//       console.log("err", err?.response);
//       let msg = "서버와 통신에 실패하였습니다.";
//       const { data } = err?.response;

//       if (!data?.ok && data?.msg) {
//         msg = data?.msg;
//         setUsingErrMessage(data.msg);
//       }
//       alert(msg);
//       // alert(msg);
//     }
// };

export const centerUpdate = (body, id) => async (dispatch) => {
  try {
    const { data } = await api.patch(`gyms/${id}/`, body);
    console.log("업데이트", data);
    dispatch(UpdateUserGym(data));
    alert("적용되었습니다");
  } catch (err) {
    console.log("업데이트", err);
    let msg = "서버와 통신에 실패하였습니다";
    const { data } = err.response;
    if (!data.ok && data?.msg) {
      msg = data?.msg;
    }
    alert(msg);
  }
};
export const selectUser = (state) => state.user;
export default userSlice.reducer;
