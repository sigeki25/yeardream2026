"use client"

import {useContext, useEffect, useState} from "react";
import axios from "axios";
import Link from "next/link";
import {AuthContext} from "@/app/context/AuthContext";

export default function Board({params}) {

    const [list, setList] = useState([]);
    const {auth, setAuth} = useContext(AuthContext);
    const config = {
        headers: {
            'Authorization': auth.Authorization,
            'Content-Type': 'application/json'
        }
    };

    useEffect(() => {
        params.then(({slug}) => {
            slug = slug == null ? "1" : slug[0];
            console.log(slug);
            getList(slug);
        });
    }, []);

    const getList = async page => {
        const {data} = await axios.get(process.env.NEXT_PUBLIC_DB_SERVER_URL + "/board/list/" + page, config);
        setList(data.data);
        console.log(data.data);
    }

    const html = list.length === 0 ?
        <tr>
            <th colSpan={6}>작성된 글이 없습니다.</th>
        </tr> :
        list.map(item => {
            return (<tr key={item._id}>
                <td><Link href={`/board/detail/${item._id}`}>{item.title}</Link></td>
                <td>{item.user}</td>
                <td>{item.views}</td>
                <td>{item.createdAt}</td>
            </tr>)
        });


    return (<div>
        <table className={"list"}>
            <thead>
            <tr>
                <th>제목</th>
                <th>작성자</th>
                <th>조회수</th>
                <th>작성일</th>
            </tr>
            </thead>
            <tbody>
            {html}
            </tbody>
        </table>
    </div>);
}