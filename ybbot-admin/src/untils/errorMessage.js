export const errMessage = (err, Text = '서버와 통신에 실패하였습니다.') => {
    console.log('err', err);
    let msg = { Text };
    const { data } = err?.response;
    if (!data?.ok && data?.msg) {
        msg = data?.msg;
    }
    alert(msg);
};

export const errMsg = (err) => {
    try {
        console.log(err.response);
        let msg = '서버와 통신에 실패하였습니다.';
        const { data } = err?.response;
        if (err.response.status === 500) {
            alert(msg);
            return;
        }
        if (err.response.status === 404) {
            alert('404');
            return;
        }
        if (!data?.ok && data?.msg) {
            msg = data?.msg;
            console.log(msg);
            alert(msg);
            return;
        }
        if (err?.response?.data) {
            alert(Object.values(err?.response?.data).join('\n'));
            return;
        }
        alert(msg);
    } catch (e) {
        console.log(e);
        console.log(e.response);
    }
};
