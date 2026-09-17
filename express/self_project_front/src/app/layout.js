"use client"
import {useLayoutEffect, useState} from "react";
import Link from "next/link";
import {AuthContext} from "@/app/context/AuthContext";

export default function App({children}) {
    const guest = <div>
        <Link href={"/user/login"}>로그인</Link>
        <Link href={"/user/signin"}>회원가입</Link>
    </div>;
    const [loginView, setLoginView] = useState(guest)
    const [auth, setAuth] = useState({})
    //sessionStorage.setItem('Authorization', "");
    console.log("auth: ",auth);

    useLayoutEffect(() => {
        const token = auth.Authorization;
        console.log("token : ", token);
        setLoginView(token == null ? guest :
            <div>
                {auth.name}님
                <Link href={"/user/logout"}>로그아웃</Link>
            </div>);
    }, [auth]);
    return (
        <html>
        <head>
            <meta charSet="UTF-8"/>
            <title>메인 페이지</title>
        </head>
        <body>
        <AuthContext.Provider value={{auth, setAuth}}>
            {loginView}
            <hr/>
            {children}
        </AuthContext.Provider>
        </body>
        </html>
    );
}