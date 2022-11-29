import React from "react";
import styled from "styled-components";
import { TableLayout } from "../../components/Container/index";
import MenuBar from "../../components/MenuBar";
import InputBox from "../../components/InputBox";
import CustomTable from "../../components/CustomTable";
import { SmallButton } from "../../components/Button";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../../api/api";

const FaqList = () => {
  const navigate = useNavigate();

  const [selectedList, setSelectedList] = useState([]);
  const [searchPost, setSearchPost] = useState([]);
  const [posts, setPosts] = useState(TableBodyData);
  const [searchContent, setSearchContent] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get("question_list");
        const faqData = res.data;
        faqArrayHanlder(faqData);
      } catch (error) {
        console.log("err", error);
        console.log("err.res", error.response);
      }
    };
    fetchData();
  }, []);

  const faqArrayHanlder = (data) => {
    const post = [];
    data.result
      .sort((a, b) => a.q_id - b.q_id)
      .forEach((item, i) => {
        post.unshift([
          "", //체크박스
          item.q_id, //id
          item.title, //제목
          item.updateTime, //등록일
          item.description, //내용
        ]);
      });
    setPosts(post);
  };
  const onClickUpdate = (e) => {
    if (selectedList.length > 1) {
      alert("수정할 질문을 하나만 선택해주세요.");
      return;
    } else if (selectedList.length == 0) {
      alert("수정할 질문을 선택해주세요.");
      return;
    }
    const selectedFaqObj = selectedList[0];
    return navigate(`/faqs/updateFaq/${selectedFaqObj[1]}`, {
      state: selectedFaqObj,
    });
  };
  const onClickDelete = async (e) => {
    if (selectedList.length == 0) {
      alert("삭제할 질문을 선택해주세요.");
    } else {
      try {
        const selectedFaqId = [];
        selectedList.forEach((item) => selectedFaqId.push(item[1]));
        await api.post(`question_delete`, {
          q_id: selectedFaqId,
        });
        setSelectedList([]);
        setPosts(posts.filter((post) => !selectedList.includes(post)));
      } catch (error) {
        console.log("err", error);
        console.log("err.res", error.response);
      }
    }
  };

  const searchHandler = ({ target: { value } }) => {
    setSearchContent(value);
  };

  const onClickSearch = () => {
    let newData = [];
    posts.forEach((item) => {
      if (item[2]?.includes(searchContent)) {
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
          labelText={"검색"}
          placeholder={"검색어를 입력하세요."}
          showButton={true}
          onClick={onClickSearch}
          value={searchContent}
          onChange={searchHandler}
        />
        <ButtonContainer>
          <SmallButton
            text={"등록"}
            style={{
              backgroundColor: "#458BFF",
              color: "#fff",
            }}
            onClick={(e) => {
              navigate(`/faqs/registerFaq`);
            }}
          />
          <SmallButton
            text={"수정"}
            style={{
              marginLeft: "9px",
            }}
            onClick={onClickUpdate}
          />
          <SmallButton
            text={"삭제"}
            style={{
              marginLeft: "9px",
              borderColor: "#E45959",
              color: "#E45959",
            }}
            onClick={onClickDelete}
          />
        </ButtonContainer>
        <CustomTable
          //page
          startSearch={false}
          tableHeader={HeaderData}
          tableHeaderStyle={{}}
          tableBodyTextRightColumn={[]}
          tableBodyTextLeftColumn={[1, 2]}
          tableHeaderRightColumn={[]}
          tableHeaderLeftColumn={[1, 2]}
          tableBody={searchPost.length !== 0 ? searchPost : posts}
          columnColor={null}
          CheckBoxStyle={{}}
          columnFunctions={{}}
          colorIncludeColumns={[]}
          selectedList={selectedList} //index or id를 통해서 위치알아올수 있도록함.
          setSelectedList={setSelectedList}
          isFullScreen={true}
          hasCheckBox={true}
          isShownPagenation={true}
          isFullTable={false}
          MAXPAGESIZE={10} //페이지네이션 보여지는 post 수
        />
      </TableLayout>
    </>
  );
};
let HeaderData = ["번호", "제목", "등록일"];
let TableBodyData = [];

export default FaqList;
const ButtonContainer = styled.div`
  margin: 35px 0 24px;
  text-align: right;
`;
