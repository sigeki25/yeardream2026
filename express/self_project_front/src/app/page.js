import Link from "next/link";

export default function Home() {
  return (
    <div>
      <Link href="./user/login">로그인</Link>
      <Link href="./user/signin">회원가입</Link>
    </div>
  );
}
