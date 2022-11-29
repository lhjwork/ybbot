import React, { useEffect, useState } from 'react';
import {
    CheckBox,
    CheckBoxImage,
    TD,
    TDHeader,
    TR,
    TableContainer,
} from './styles';
import { TEXT_COLOR } from '../../untils/textColor';
import Pagination from 'react-js-pagination';
import './table.css';
import NullBodyTable from './NullBodyTable';
const CustomTable = (props) => {
    const {
        tableBody,
        tableHeader,
        tableHeaderStyle,
        tableStyle,
        style,
        isFullScreen,
        hasCheckBox,
        columnColor,
        colorIncludeColumns,
        selectedList,
        setSelectedList,
        isFullTable,
        isShownPagenation,
        MAXPAGESIZE,
        CheckBoxStyle,
        ContainerStyle,
        startSearch,
        tableBodyTextRightColumn,
        tableBodyTextLeftColumn,
        tableHeaderRightColumn,
        tableHeaderLeftColumn,
        columnFunctions,
    } = props;

    //pageNation
    let PageCount = MAXPAGESIZE ? MAXPAGESIZE : 10;
    const [page, setPage] = useState(1); // 현재 페이지
    const currentShowPost = tableBody?.slice(
        (page - 1) * PageCount,
        page * PageCount
    );

    useEffect(() => {
        setPage(1);
    }, [startSearch]);
    const handlePageChange = (page) => {
        setPage(page);
        if (hasCheckBox == true) {
            setSelectedList([]);
        }
    };

    const onClickPost = (e, data) => {
        e.preventDefault();
        if (selectedList.includes(data)) {
            setSelectedList(selectedList.filter((list) => list !== data));
        } else {
            setSelectedList([...selectedList, data]);
        }
    };
    const render = (data, index) => {
        if (
            columnColor?.filter((column) => column.column === index).length !==
            0
        ) {
            return columnColor?.filter((column) => column.column === index)[0]
                .style;
        }
        //특정 단어 마다 색상이 다를 경우에 사용 하는 if문
        else if (colorIncludeColumns?.includes(index)) {
            return TEXT_COLOR[data];
        }
    };

    const showTable = (data, index) => {
        if (isShownPagenation) {
            return currentShowPost.map((body, index) =>
                renderBody({ body, index, isNull: false })
            );
        } else {
            return tableBody?.map((body, index) =>
                renderBody({ body, index, isNull: false })
            );
        }
    };

    // 하이라이트 기능
    // let accountArr = Array(25).fill(0,0,25);
    const renderBody = ({ body, index, isNull }) => {
        if (!isNull) {
            return (
                <TR
                    style={{ cursor: hasCheckBox ? 'pointer' : 'default' }}
                    isSelected={
                        selectedList &&
                        setSelectedList &&
                        selectedList?.includes(body)
                    }
                    key={index}
                    onClick={(e) => {
                        selectedList && setSelectedList && onClickPost(e, body);
                    }}
                >
                    {hasCheckBox && selectedList && setSelectedList && (
                        <CheckBox style={{ ...CheckBoxStyle }}>
                            <CheckBoxImage
                                src={require(selectedList?.includes(body)
                                    ? '../../assets/Table/CheckBoxTrue.png'
                                    : '../../assets/Table/CheckBoxFalse.png')}
                                alt='checkbox'
                            />
                        </CheckBox>
                    )}
                    {/*<p>1</p>*/}
                    {body
                        ?.slice(1, tableHeader.length + 1)
                        ?.map((data, index) => (
                            <TD
                                onClick={(e) => {
                                    try {
                                        e.preventDefault();
                                        columnFunctions[index](e, body);
                                    } catch (e) {}
                                }}
                                hover={render(data, index)}
                                textAlign={
                                    tableBodyTextRightColumn?.includes(index)
                                        ? 'right'
                                        : tableBodyTextLeftColumn?.includes(
                                              index
                                          )
                                        ? 'left'
                                        : 'center'
                                }
                                style={{
                                    ...render(data, index),
                                    ...tableStyle,
                                }}
                                key={index}
                                isFullScreen={isFullScreen}
                            >
                                {data}
                            </TD>
                        ))}
                </TR>
            );
        } else {
            return (
                <tr key={index}>
                    {hasCheckBox && selectedList && setSelectedList && (
                        <CheckBox style={{ ...CheckBoxStyle }} />
                    )}
                    {tableHeader?.map((data, index) => (
                        <TD
                            isFullScreen={isFullScreen}
                            key={index}
                            style={{ ...tableStyle }}
                        />
                    ))}
                </tr>
            );
        }
    };
    const allClick = (e) => {
        e.preventDefault();
        let count = 0;
        let forCount = 0;
        let Array = [];
        let resetArray = [];
        for (let i = (page - 1) * PageCount; i < page * PageCount; i++) {
            forCount++;
            if (i > tableBody.length - 1) {
                forCount--;
            } else if (!selectedList?.includes(tableBody[i])) {
                Array.push(tableBody[i]);
            } else {
                count++;
            }
        }

        if (forCount === count) {
            resetArray = selectedList;
            for (let i = (page - 1) * PageCount; i < page * PageCount; i++) {
                if (i > tableBody.length - 1) {
                }
                resetArray = resetArray.filter((list) => list !== tableBody[i]);
            }

            setSelectedList(resetArray);
            return;
        }

        setSelectedList(selectedList.concat(Array));
    };
    return (
        <div style={{ width: '100%' }}>
            <TableContainer
                style={{
                    ...ContainerStyle,
                }}
            >
                <table
                    style={{
                        ...style,
                        width: isFullScreen ? '100%' : 'auto',
                        borderCollapse: 'collapse',
                    }}
                >
                    <thead>
                        <tr>
                            {hasCheckBox && selectedList && setSelectedList && (
                                <CheckBox style={{ background: '#f9f8f9' }}>
                                    <CheckBoxImage
                                        onClick={(e) => {
                                            allClick(e);
                                        }}
                                        style={{ cursor: 'cursor' }}
                                        src={require(selectedList.length ==
                                            currentShowPost.length
                                            ? '../../assets/Table/CheckBoxTrue.png'
                                            : '../../assets/Table/CheckBoxFalse.png')}
                                        alt='checkBox'
                                    />
                                </CheckBox>
                            )}
                            {tableHeader.map((body, index) => (
                                <TDHeader
                                    textAlign={
                                        tableHeaderRightColumn?.includes(index)
                                            ? 'right'
                                            : tableHeaderLeftColumn?.includes(
                                                  index
                                              )
                                            ? 'left'
                                            : 'center'
                                    }
                                    key={index}
                                    isFullScreen={isFullScreen}
                                    style={{ ...tableHeaderStyle }}
                                >
                                    {body}
                                </TDHeader>
                            ))}
                        </tr>
                    </thead>
                    {/*<tbody style={{ ...tableStyle }}>*/}
                    <tbody>
                        {tableBody?.length === 0 ? (
                            <tr>
                                <td
                                    colSpan='100%'
                                    style={{
                                        marginTop: 10,
                                    }}
                                >
                                    {<NullBodyTable />}
                                </td>
                            </tr>
                        ) : (
                            showTable()
                        )}
                        {tableBody.length !== 0 &&
                            isFullTable &&
                            tableBody.length < page * PageCount &&
                            Array(page * PageCount - tableBody.length)
                                .fill('null')
                                .map((res, index) =>
                                    renderBody({
                                        res,
                                        index,
                                        isNull: true,
                                    })
                                )}
                    </tbody>
                </table>
            </TableContainer>

            {isShownPagenation && (
                <Pagination
                    activePage={page}
                    itemsCountPerPage={PageCount}
                    totalItemsCount={tableBody?.length}
                    pageRangeDisplayed={5}
                    prevPageText={'‹'}
                    nextPageText={'›'}
                    onChange={handlePageChange}
                />
            )}
        </div>
    );
};

export default CustomTable;
