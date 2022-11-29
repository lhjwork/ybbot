import React, { useEffect, useState } from "react";
import { api } from "../../api/api";
import { TableLayout } from "../../components/Container/index";
import MenuBar from "../../components/MenuBar";
import InputBox from "../../components/InputBox";
import CustomTable from "../../components/CustomTable";
import { useLocation, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";

const UserManagement = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const dispatch = useDispatch();
  const [searchPost, setSearchPost] = useState([]);
  const [posts, setPosts] = useState(TableBodyData);
  const [searchContent, setSearchContent] = useState("");
  const [transactionInfoDisplay, setTransactionInfoDisplay] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        let body = {
          user_id: location.state,
        };
        dispatch(userAlarm(body));
        setTransactionInfoDisplay(true);
      } catch (error) {
        console.log("err", error);
        console.log("err.res", error.response);
      }
    };
    fetchData();
  }, []);

  const userAlarm = (body) => async (dispatch) => {
    try {
      const { data } = await api.post("transcation_list", body);
      const post = [];
      data.result
        .sort((a, b) => new Date(a.work_time) - new Date(b.work_time))
        .forEach((item) => {
          post.unshift([
            "",
            item.market,
            item.volume,
            item.side == "bid" ? "매수" : "매도",
            item.price,
            item.work_time,
          ]);
        });
      setPosts(post);
    } catch (err) {
      console.log("err", err);
      console.log("err.res", err.response);
    }
  };

  const searchHandler = ({ target: { value } }) => {
    setSearchContent(value);
  };

  const onClickSearch = () => {
    let newData = [];
    console.log(posts);
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
          tableBodyTextLeftColumn={[]}
          tableHeaderRightColumn={[]}
          tableHeaderLeftColumn={[]}
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
let HeaderData = ["코인명", "코인수량", "매수/매도 여부", "금액", "매매시간"];
let TableBodyData = [];

export default UserManagement;
