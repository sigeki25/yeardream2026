export function plus(a, b) {return a + b}
export function minus(a, b) {return a - b}
export function multiply(a, b) {return a * b}
export function divide(a, b) {
    if (b === 0)
        throw new Error("0으로 나눌 수 없습니다.")
    return a / b
}


