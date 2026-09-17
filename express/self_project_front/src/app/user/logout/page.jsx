"use client"
import {useContext, useState} from "react";
import axios from "axios";
import {useRouter} from "next/navigation";
import {AuthContext} from "@/app/context/AuthContext";

export default function Logout() {
    const router = useRouter();
    const {auth, setAuth} = useContext(AuthContext)
    if (auth.Authorization == null) {
        alert("로그인을 하지 않았습니다.");
    }
    setAuth({});
    alert("로그아웃 되었습니다.");
    router.push('/');
}