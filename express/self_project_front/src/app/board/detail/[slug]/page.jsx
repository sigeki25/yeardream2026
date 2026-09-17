"use client"

import {useContext, useEffect, useState} from "react";
import axios from "axios";
import Link from "next/link";
import {AuthContext} from "@/app/context/AuthContext";

export default function Detail({params}) {

    const [detail, setDetail] = useState({});
    const {auth, setAuth} = useContext(AuthContext)
    const config = {
        headers: {
            'Authorization': auth.Authorization,
            'Content-Type': 'application/json'
        }
    };

    useEffect(() => {
        params.then(({slug}) => {
            console.log(slug);
            getDetail(slug);
        });
    }, []);

    const getDetail = async _id => {
        const {data} = await axios.get(process.env.NEXT_PUBLIC_DB_SERVER_URL + "/board/detail/" + _id, config);
        setDetail(data.data);
        console.log(data.data);
    }
    const del = e => {

    }
    return(<div>
        <h3>{detail._id} 상세보기</h3>
        <hr/>
        <table className={"form"}>
            <tbody>
            <tr>
                <th>제목</th>
                <td>{detail.title}</td>
            </tr>
            <tr>
                <th>조회수</th>
                <td>{detail.views}</td>
            </tr>
            <tr>
                <th>작성자</th>
                <td>{detail.user}</td>
            </tr>
            <tr>
                <th>내용</th>
                <td>{detail.body}</td>
            </tr>
            <tr>
                <th>로그인 유저만 보이기</th>
                <td>{detail.view_login_only ? "예" : "아니오"}</td>
            </tr>
            <tr>
                <th>작성한 날짜</th>
                <td>{detail.createdAt}</td>
            </tr>
            <tr>
                <th>수정한 날짜</th>
                <td>{detail.updatedAt}</td>
            </tr>
            <tr>
                <th colSpan={2}>
                    <button onClick={del}>삭제</button>
                    <Link href="/board/list/1">돌아가기</Link>
                </th>
            </tr>
            </tbody>
        </table>
    </div>);
}