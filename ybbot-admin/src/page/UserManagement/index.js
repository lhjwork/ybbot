import React, { useEffect, useState } from "react";
import { api } from "../../api/api";
import { TableLayout } from "../../components/Container/index";
import MenuBar from "../../components/MenuBar";
import InputBox from "../../components/InputBox";
import CustomTable from "../../components/CustomTable";
import { SmallButton } from "../../components/Button";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";

const UserManagement = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [searchPost, setSearchPost] = useState([]);
  const [posts, setPosts] = useState(TableBodyData);
  const [searchContent, setSearchContent] = useState("");
  const [transactionPosts, setTransactionPosts] = useState(TableBodyData);
  const [transactionInfoDisplay, setTransactionInfoDisplay] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get("user_list");
        const userData = res.data;
        userArrayHanlder(userData);
      } catch (error) {
        console.log("err", error);
        console.log("err.res", error.response);
      }
    };
    fetchData();
  }, []);

  const userArrayHanlder = (data) => {
    const post = [];
    data.result
      .sort((a, b) => a.id - b.id)
      .forEach((item, i) => {
        post.unshift([
          item.id,
          item.username,
          item.phone,
          item.email,
          item.apikey,
          item.start_active ? "활동중" : "",
          <SmallButton
            text={"확인하기"}
            style={{ width: "auto" }}
            // onClick={() => userTransactionHandler(item.id)}
            onClick={() => onClickTransaction(item.id)}
          />,
        ]);
      });
    setPosts(post);
  };

  const onClickTransaction = (userId) => {
    return navigate(`/users/userTransactions/${userId}`, {
      state: userId,
    });
  };

  const searchHandler = ({ target: { value } }) => {
    setSearchContent(value);
  };

  const onClickSearch = () => {
    let newData = [];
    posts.forEach((item) => {
      if (
        item[1]?.includes(searchContent) ||
        item[2]?.includes(searchContent) ||
        item[3]?.includes(searchContent) ||
        item[4]?.includes(searchContent) ||
        item[5]?.includes(searchContent)
      ) {
        newData.push(item);
      }
    });
    if (newData.length === 0) {
      alert("해당 검색결과가 없습니다");
      setSearchPost(posts);
    } else {
      setSearchPost(newData);
    }
  };

  const userTransactionHandler = (userId) => {
    let body = {
      user_id: userId,
    };
    dispatch(userAlarm(body));
    setTransactionInfoDisplay(true);
  };
  const userAlarm = (body) => async (dispatch) => {
    try {
      const { data } = await api.post("transcation_list", body);
      console.log(data);
      const post = [];
      post.unshift([
        data.result.market,
        data.result.side,
        data.result.volume,
        data.result.price,
        data.result.work_time,
      ]);
      setTransactionPosts(post);
    } catch (err) {
      // alert("알림 정보가 없습니다.");
      console.log("err", err);
      console.log("err.res", err.response);
    }
  };

  return (
    <>
      <MenuBar />
      <TableLayout>
        <InputBox
          labelText={"제목"}
          placeholder={"검색어를 입력하세요."}
          showButton={true}
          onChange={searchHandler}
          onClick={onClickSearch}
        />
        <CustomTable
          //page
          style={{ marginTop: "36px" }}
          startSearch={false}
          tableHeader={HeaderData}
          tableHeaderStyle={{}}
          tableBodyTextRightColumn={[]}
          tableBodyTextLeftColumn={[0, 1, 2, 3, 4]}
          tableHeaderRightColumn={[]}
          tableHeaderLeftColumn={[0, 1, 2, 3, 4]}
          tableBody={searchPost.length !== 0 ? searchPost : posts}
          columnColor={null}
          CheckBoxStyle={{}}
          columnFunctions={{}}
          colorIncludeColumns={[]}
          selectedList={null} //index or id를 통해서 위치알아올수 있도록함.
          setSelectedList={null}
          isFullScreen={true}
          hasCheckBox={false}
          isShownPagenation={true}
          isFullTable={false}
          MAXPAGESIZE={10} //페이지네이션 보여지는 post 수
        />
      </TableLayout>
    </>
  );
};
let HeaderData = [
  "이름",
  "휴대폰",
  "이메일",
  "API 키",
  "bot 활동여부",
  "자동매매 거래내역",
];
let TableBodyData = [];

export default UserManagement;
