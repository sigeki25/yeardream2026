# 대상 프로그램 다운로드 여부
# docker search [프로그렘명]
docker search mariadb
# NAME      DESCRIPTION
# MariaDB Server is a high performing open sou…

# 이미지 다운로드
# docker pull [프로그램명(이미지)]:[버전]
docker pull mariadb:11.8.3

# 이미지 리스트
docker images

# 이미지 삭제
# docker rm image [이미지명]
# docker rmi [이미지명]
docker rmi mariadb