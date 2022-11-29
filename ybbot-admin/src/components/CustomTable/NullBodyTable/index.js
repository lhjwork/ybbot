import React from 'react';
import { Container, SubTitle } from './styles';
import { AiFillWarning } from 'react-icons/ai';

const NullBodyTable = () => {
    return (
        <>
            <Container>
                <AiFillWarning size={20} style={{ marginRight: 13 }} />
                <SubTitle>데이터를 찾지 못하였습니다.</SubTitle>
            </Container>
        </>
    );
};

export default NullBodyTable;
