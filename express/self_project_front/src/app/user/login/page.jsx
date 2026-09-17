"use client"
import {useContext, useState} from "react";
import axios from "axios";
import {AuthContext} from "@/app/context/AuthContext";

export default function Login() {
    const [input, setInput] = useState({"id": "user_1", "password": "password"});
    const {auth, setAuth} = useContext(AuthContext);
    const inputData = e => {
        setInput({
            ...input,
            [e.target.id]: e.target.value
        });
    }
    console.log("auth: ",auth);
    const login = async e => {
        const {data} = await axios.post(process.env.NEXT_PUBLIC_DB_SERVER_URL + "/user/login", input);
        console.log(data);
        if (data.success) {
            setAuth({
                "Authorization": data.token,
                "name": data.data.name == null ? data.data.id : data.data.name
            });
            return;
            //return location.href = "/board/list";
        }
        alert(data.message);
    }
    return (
        <div>
            <h3>로그인</h3>
            <input type={"text"} id={"id"} value={input.id} onInput={inputData}/>
            <input type={"password"} id={"password"} value={input.password} onInput={inputData}/>
            <button id={"btnLogin"} onClick={login}>로그인</button>
        </div>
    );
}
