/*
    1. JEST 설치
        npm install -D jest jest-environment-jsdom
    2. jest.config.js 설정
    3. package.json 에 test script 추가
    4. 모듈작성(테스터블 하게)
    53. 테스트코드 작성
    6. npm run test
*/
"use client"
import {useState} from "react";
import {divide, minus, multiply, plus} from "@/app/calcModule";

export default function App() {
    const [result, setResult] = useState({su1:0, su2:0, oper:"+", result:0})

    const setVal = e => {
        setResult({
            ...result,
            [e.target.name]: e.target.value
        });
        console.log(result)
    }

    const operFunc = {
        "+": plus,
        "-": minus,
        "*": multiply,
        "/": divide,
    }

    const calculate = e => {
        console.log(result.oper)
        setResult({
            ...result,
            result: operFunc[result.oper](parseInt(result.su1), parseInt(result.su2))
        });
    }

    return (
        <div>
            <input type="number" name="su1" value={result.su1} onChange={setVal}/>
            <select name="oper" onChange={setVal}>
                <option value="+">+</option>
                <option value="-">-</option>
                <option value="*">*</option>
                <option value="/">/</option>
            </select>
            <input type="number" name="su2" value={result.su2} onChange={setVal}/>
            <p><button onClick={calculate}>계산</button></p>
            <h3>답 : {result.result}</h3>
        </div>
    );
}