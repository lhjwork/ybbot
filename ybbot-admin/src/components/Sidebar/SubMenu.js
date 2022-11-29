import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { SidebarLink, SidebarLabel, Container } from "./styles";

const SubMenu = ({ item }) => {
  let navigate = useNavigate();

  const showSubnav = (e) => {
    e.preventDefault();
    navigate(item.path);
  };
  const [subnav, setSubnav] = useState(false);
  return (
    <Container>
      <SidebarLink onClick={showSubnav}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
          }}
        >
          {item.icon}
        </div>
        <div>
          <SidebarLabel>{item.title}</SidebarLabel>
        </div>

        {/* <ArrowSize
          style={{
            display: "flex",
            alignItems: "center",
          }}
        >
          {item.subNav && subnav
            ? item.iconOpened
            : item.subNav
            ? item.iconClosed
            : null}
        </ArrowSize> */}
      </SidebarLink>

      {/* {selectNav === item?.title &&
        item.subNav.map((item, index) => (
          <DropdownLink
            to={item.path}
            key={index}
            locations={location.pathname === item.path ? "true" : "false"}
          >
            {item.icon}
            <InSidebarLabel>{item.title}</InSidebarLabel>
          </DropdownLink>
        ))} */}
    </Container>
  );
};

export default SubMenu;
