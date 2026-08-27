import {divide, minus, multiply, plus} from "@/app/calcModule";
import {render, screen} from "@testing-library/react";
import App from "@/app/page";
import {userEvent} from "@testing-library/user-event/dist/cjs/setup/index.js";

async function calculateTest(v_su1, v_su2, v_oper, v_result) {
    // 1. UI 가져옴
    const {container} = render(<App/>);
    // 2. 원하는 요소 확보
    const su1 = container.querySelector("input[name=\"su1\"]");
    const su2 = container.querySelector("input[name=\"su2\"]");
    const oper = container.querySelector("select[name=\"oper\"]");
    const btn = container.querySelector("button");
    const result = screen.getByTestId("result");
    // 3. 특정 이벤트 발생 시
    await userEvent.type(su1, v_su1);
    await userEvent.type(su2, v_su2);
    await userEvent.selectOptions(oper, v_oper);
    await userEvent.click(btn);
    // 4. 특정한 결과 확인
    return expect(result).toHaveTextContent("답 : " + v_result);
}

describe("사칙연산 UI 테스트", () => {

    test("더하기 테스트", async () => {
        await calculateTest("30", "10", "+", "40");
    });
    test("빼기 테스트", async () => {
        await calculateTest("30", "10", "-", "20");
    });
    test("곱하기 테스트", async () => {
        await calculateTest("30", "10", "*", "300");
    });
    test("나누기 테스트", async () => {
        await calculateTest("30", "10", "/", "3");
    });
});