// test() : 특정한 테스트 단위
// except() : 테스트 실행
// describe() : test() 의 group, describe 는 describe 를 담을 수 있다.

import {divide, minus, multiply, plus} from "@/app/calcModule";

describe("시착연산 테스트", () => {
    test("더하기 모듈 테스트", () => {
        expect(plus(10, 30)).toBe(40)
    })
    test("빼기 모듈 테스트", () => {
        expect(minus(30, 10)).toBe(20)
    })
    test("곱하기 모듈 테스트", () => {
        expect(multiply(10, 30)).toBe(300)
    })
    test("나누기 모듈 테스트", () => {
        expect(divide(30, 10)).toBe(3)
    })
});
/*
toBe() : 숫자, 문자, 불리언 타입의 값이 일치
toEqual() : 겍체나 배열의 일치
toContain() : 배열이나 문자열 내에 특정 값 포함 여부
toMatch() : 문자열이 지정된 정규표현식 패턴에 일치하는지
toThrow() : 특정 에러가 발생하는지 여부
*/